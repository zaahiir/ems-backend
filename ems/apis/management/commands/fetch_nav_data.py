from django.core.management.base import BaseCommand
from apis.models import NavModel, AmcEntryModel
import requests
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Fetch and create new NAV data for a specific date or yesterday'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date for which to fetch NAV data in dd-MMM-yyyy format (e.g., 14-Aug-2024). If not provided, uses yesterday\'s date.',
        )

    def handle(self, *args, **options):
        date_str = options['date']
        if not date_str:
            yesterday = datetime.now() - timedelta(days=1)
            date_str = yesterday.strftime('%d-%b-%Y')

        url = f"https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={date_str}"
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

            self.stdout.write(self.style.SUCCESS(f'Successfully created/updated NAV data for {date_str}'))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
