from django.core.management.base import BaseCommand
from apis.models import NavModel, AmcEntryModel
import requests
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch and create new NAV data'

    def handle(self, *args, **options):
        url = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"
        querystring = {"Scheme_Type": "Open"}
        headers = {
            "x-rapidapi-key": "53456b3ab5mshc8278abef35dcbcp1891e2jsne5db5cf7e514",
            "x-rapidapi-host": "latest-mutual-fund-nav.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()

            # Fetch all AMCs once to reduce database queries
            amc_dict = {amc.amcName: amc for amc in AmcEntryModel.objects.all()}

            for item in data:
                mutual_fund_family = item.get('Mutual_Fund_Family')
                scheme_name = item.get('Scheme_Name')
                net_asset_value = item.get('Net_Asset_Value')
                date = item.get('Date')

                # Check if the AMC exists
                amc = amc_dict.get(mutual_fund_family)
                if amc:
                    try:
                        # Parse the date using the correct format
                        parsed_date = datetime.strptime(date, '%d-%b-%Y').date() if date else None
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"Invalid date format: {date}"))
                        parsed_date = None

                    # Create new NavModel instance
                    NavModel.objects.create(
                        navAmcName=amc,
                        navFundName=scheme_name,
                        nav=net_asset_value,
                        navDate=parsed_date,
                    )
                else:
                    self.stdout.write(self.style.WARNING(f"AMC not found: {mutual_fund_family}"))

            self.stdout.write(self.style.SUCCESS('Successfully created new NAV data'))
        else:
            self.stdout.write(self.style.ERROR(f'Error: {response.status_code}'))
            self.stdout.write(self.style.ERROR(response.text))