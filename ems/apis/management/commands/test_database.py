from django.core.management.base import BaseCommand
from django.db import transaction
from apis.models import NavModel, AmcEntryModel
import requests
from datetime import datetime, timedelta
import pytz
import logging
from django.db.models import Count
from collections import defaultdict

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch and create new NAV data for a specific date, yesterday, or a date range'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date for which to fetch NAV data in dd-MMM-yyyy format (e.g., 14-Aug-2024). If not provided, uses yesterday\'s date.',
            required=False,
        )
        parser.add_argument(
            '--start_date',
            type=str,
            help='Start date for fetching NAV data in dd-MMM-yyyy format (e.g., 14-Aug-2024)',
            required=False,
        )
        parser.add_argument(
            '--end_date',
            type=str,
            help='End date for fetching NAV data in dd-MMM-yyyy format (e.g., 20-Aug-2024)',
            required=False,
        )

    def handle(self, *args, **options):
        logger.info(f"Starting fetch_nav_data command at {datetime.now()}")
        try:
            date = options.get('date')
            start_date = options.get('start_date')
            end_date = options.get('end_date')

            self.records_per_day = defaultdict(int)
            self.records_per_month = defaultdict(int)
            self.total_records_fetched = 0

            if start_date and end_date:
                self.fetch_date_range(start_date, end_date)
            elif date:
                self.fetch_single_date(date)
            else:
                self.fetch_yesterday()

            self.print_summary()

        except Exception as e:
            error_msg = f'Unexpected error: {str(e)}'
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg, exc_info=True)

    def fetch_date_range(self, start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, '%d-%b-%Y')
        end_date = datetime.strptime(end_date_str, '%d-%b-%Y')

        current_date = start_date
        while current_date <= end_date:
            records = self.fetch_data_for_date(current_date)
            if records is None:
                self.stdout.write(
                    self.style.WARNING(f"Failed to fetch data for {current_date.date()}. Stopping execution."))
                break
            current_date += timedelta(days=1)

    def fetch_single_date(self, date_str):
        date = datetime.strptime(date_str, '%d-%b-%Y')
        self.fetch_data_for_date(date)

    def fetch_yesterday(self):
        kolkata_tz = pytz.timezone('Asia/Kolkata')
        yesterday = datetime.now(kolkata_tz) - timedelta(days=1)
        self.fetch_data_for_date(yesterday)

    def fetch_data_for_date(self, date):
        date_str = date.strftime('%d-%b-%Y')
        url = f"https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={date_str}"
        logger.info(f"Fetching data for date: {date_str}")

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data_lines = response.text.splitlines()
            nav_count = self.process_nav_data(data_lines, date)

            self.update_statistics(date, nav_count)
            self.stdout.write(self.style.SUCCESS(f"\nRecords fetched for {date_str}: {nav_count}"))
            return nav_count

        except Exception as e:
            error_msg = f'Error fetching/processing data for {date_str}: {str(e)}'
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg, exc_info=True)
            return None

    def process_nav_data(self, data_lines, date):
        nav_count = 0
        nav_data = []
        current_amc_name = None
        amc_cache = {}

        for line in data_lines:
            if not line.strip() or line.startswith("Open Ended Schemes") or line.startswith("Close Ended Schemes"):
                continue

            if ';' not in line:
                current_amc_name = line.strip()
                continue

            if current_amc_name and ';' in line:
                fields = line.split(';')
                if len(fields) < 8:
                    continue

                scheme_name, net_asset_value, nav_date = fields[1], fields[4], fields[7]

                if current_amc_name not in amc_cache:
                    amc_cache[current_amc_name] = self.get_or_create_amc(current_amc_name)

                try:
                    parsed_date = datetime.strptime(nav_date, '%d-%b-%Y').date() if nav_date else None
                except ValueError:
                    parsed_date = None

                nav_data.append({
                    'navAmcName': amc_cache[current_amc_name],
                    'navFundName': scheme_name,
                    'navDate': parsed_date,
                    'nav': net_asset_value
                })

                nav_count += 1

                if len(nav_data) >= 10000:
                    self.bulk_update_or_create(nav_data)
                    nav_data = []

        if nav_data:
            self.bulk_update_or_create(nav_data)

        return nav_count

    @transaction.atomic
    def bulk_update_or_create(self, nav_data):
        existing_navs = NavModel.objects.filter(
            navAmcName__in=[data['navAmcName'] for data in nav_data],
            navFundName__in=[data['navFundName'] for data in nav_data],
            navDate__in=[data['navDate'] for data in nav_data]
        ).values('id', 'navAmcName', 'navFundName', 'navDate')

        existing_navs_dict = {
            (nav['navAmcName'], nav['navFundName'], nav['navDate']): nav['id']
            for nav in existing_navs
        }

        navs_to_update = []
        navs_to_create = []

        for nav in nav_data:
            key = (nav['navAmcName'].id, nav['navFundName'], nav['navDate'])
            if key in existing_navs_dict:
                nav['id'] = existing_navs_dict[key]
                navs_to_update.append(NavModel(**nav))
            else:
                navs_to_create.append(NavModel(**nav))

        NavModel.objects.bulk_create(navs_to_create)
        NavModel.objects.bulk_update(navs_to_update, ['nav'])

    def get_or_create_amc(self, amc_name):
        amc, _ = AmcEntryModel.objects.get_or_create(amcName=amc_name)
        return amc

    def update_statistics(self, date, nav_count):
        self.records_per_day[date.date()] += nav_count
        self.records_per_month[(date.year, date.month)] += nav_count
        self.total_records_fetched += nav_count

    def print_summary(self):
        self.stdout.write(self.style.SUCCESS("\nSummary:"))
        self.stdout.write("Records fetched per day:")
        for date, count in self.records_per_day.items():
            self.stdout.write(f"  {date}: {count}")

        self.stdout.write("\nRecords fetched per month:")
        for (year, month), count in self.records_per_month.items():
            self.stdout.write(f"  {year}-{month:02d}: {count}")

        self.stdout.write(f"\nTotal records fetched: {self.total_records_fetched}")

        total_records_in_db = NavModel.objects.count()
        self.stdout.write(f"\nTotal records in the database: {total_records_in_db}")
