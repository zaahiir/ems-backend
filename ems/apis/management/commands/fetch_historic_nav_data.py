from django.core.management.base import BaseCommand
from apis.models import NavModel, AmcEntryModel
import requests
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Fetch and update historical NAV data'

    def handle(self, *args, **options):
        url = "https://latest-mutual-fund-nav.p.rapidapi.com/historic"
        headers = {
            "x-rapidapi-key": "53456b3ab5mshc8278abef35dcbcp1891e2jsne5db5cf7e514",
            "x-rapidapi-host": "latest-mutual-fund-nav.p.rapidapi.com"
        }

        # Fetch all AMCs once to reduce database queries
        amc_dict = {amc.amcName: amc for amc in AmcEntryModel.objects.all()}

        # Set the date range for historical data (e.g., last 30 days)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)

        current_date = start_date
        while current_date <= end_date:
            querystring = {
                "Scheme_Type": "Open",
                "Date": current_date.strftime('%d-%m-%Y')
            }

            response = requests.get(url, headers=headers, params=querystring)

            if response.status_code == 200:
                data = response.json()

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

                        # Create or update NavModel
                        NavModel.objects.update_or_create(
                            navAmcName=amc,
                            navFundName=scheme_name,
                            navDate=parsed_date,
                            defaults={
                                'nav': net_asset_value,
                            }
                        )
                    else:
                        self.stdout.write(self.style.WARNING(f"AMC not found: {mutual_fund_family}"))

                self.stdout.write(self.style.SUCCESS(f'Successfully updated NAV data for {current_date}'))
            else:
                self.stdout.write(self.style.ERROR(f'Error for {current_date}: {response.status_code}'))
                self.stdout.write(self.style.ERROR(response.text))

            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Finished updating historical NAV data'))
