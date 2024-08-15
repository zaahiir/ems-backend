from django.core.management.base import BaseCommand
from apis.models import NavModel, AmcEntryModel
import requests
from datetime import datetime


class Command(BaseCommand):
    help = 'Fetch and create new NAV data for a specific date'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date for which to fetch NAV data in dd-MMM-yyyy format (e.g., 14-Aug-2024)',
        )

    def handle(self, *args, **options):
        date_str = options['date']
        if not date_str:
            self.stdout.write(self.style.ERROR('Please provide a date using --date option'))
            return

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
                    # This is a scheme type, not an AMC name
                    continue

                if not line[0].isdigit() and ';' not in line:
                    # This is likely an AMC name
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

                        NavModel.objects.create(
                            navAmcName=amc,
                            navFundName=scheme_name,
                            nav=net_asset_value,
                            navDate=parsed_date,
                        )
                    else:
                        self.stdout.write(self.style.WARNING(f"AMC not found: {current_amc_name}"))

            self.stdout.write(self.style.SUCCESS(f'Successfully created new NAV data for {date_str}'))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
