from django.core.management.base import BaseCommand
from apis.models import NavModel, AmcEntryModel
import requests
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Fetch and create new NAV data for a date range'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from_date',
            type=str,
            help='Start date to fetch NAV data in dd-MMM-yyyy format (e.g., 01-Jan-2024).',
            required=True
        )
        parser.add_argument(
            '--to_date',
            type=str,
            help='End date to fetch NAV data in dd-MMM-yyyy format (e.g., 08-Aug-2024).',
            required=True
        )

    def handle(self, *args, **options):
        from_date = options['from_date']
        to_date = options['to_date']

        url = f"https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={from_date}&todt={to_date}"
        try:
            response = requests.get(url)
            response.raise_for_status()

            data_lines = response.text.splitlines()
            current_amc_name = None
            amc_dict = {amc.amcName: amc for amc in AmcEntryModel.objects.all()}

            for line in data_lines:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("Open Ended Schemes") or line.startswith("Close Ended Schemes"):
                    continue

                if not line[0].isdigit() and ';' not in line:
                    current_amc_name = line
                    continue

                if current_amc_name and ';' in line:
                    fields = line.split(';')
                    if len(fields) < 8:
                        continue

                    scheme_name = fields[1]
                    net_asset_value = fields[4]
                    date = fields[7]

                    amc = amc_dict.get(current_amc_name)
                    if amc:
                        try:
                            parsed_date = datetime.strptime(date, '%d-%b-%Y').date() if date else None
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f"Invalid date format: {date}"))
                            parsed_date = None

                        NavModel.objects.update_or_create(
                            navAmcName=amc,
                            navFundName=scheme_name,
                            navDate=parsed_date,
                            defaults={'nav': net_asset_value}
                        )
                    else:
                        self.stdout.write(self.style.WARNING(f"AMC not found: {current_amc_name}"))

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created/updated NAV data from {from_date} to {to_date}'))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
