from django.core.management.base import BaseCommand
from apis.models import NavModel, AmcEntryModel
import requests
from datetime import datetime, timedelta
import pytz
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch and create new NAV data for a specific date or yesterday'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date for which to fetch NAV data in dd-MMM-yyyy format (e.g., 14-Aug-2024). If not provided, uses yesterday\'s date.',
        )

    def handle(self, *args, **options):
        logger.info(f"Starting fetch_nav_data command at {datetime.now()}")
        try:
            date_str = options['date']
            if not date_str:
                kolkata_tz = pytz.timezone('Asia/Kolkata')
                yesterday = datetime.now(kolkata_tz) - timedelta(days=1)
                date_str = yesterday.strftime('%d-%b-%Y')

            url = f"https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={date_str}"
            logger.info(f"Fetching data from URL: {url}")

            response = requests.get(url)
            response.raise_for_status()

            logger.info(f"Data fetched successfully. Status code: {response.status_code}")
            logger.debug(f"Response content (first 500 chars): {response.text[:500]}")

            data_lines = response.text.splitlines()
            logger.info(f"Total lines in response: {len(data_lines)}")

            current_amc_name = None
            amc_dict = {amc.amcName: amc for amc in AmcEntryModel.objects.all()}
            logger.info(f"Total AMCs in database: {len(amc_dict)}")

            nav_count = 0
            for line in data_lines:
                try:
                    line = line.strip()
                    if not line:
                        continue

                    if line.startswith("Open Ended Schemes") or line.startswith("Close Ended Schemes"):
                        continue

                    if not line[0].isdigit() and ';' not in line:
                        current_amc_name = line
                        logger.debug(f"Current AMC: {current_amc_name}")
                        continue

                    if current_amc_name and ';' in line:
                        fields = line.split(';')
                        if len(fields) < 8:
                            logger.warning(f"Skipping line due to insufficient fields: {line}")
                            continue

                        scheme_name = fields[1]
                        net_asset_value = fields[4]
                        date = fields[7]

                        amc = amc_dict.get(current_amc_name)
                        if amc:
                            try:
                                parsed_date = datetime.strptime(date, '%d-%b-%Y').date() if date else None
                            except ValueError:
                                logger.warning(f"Invalid date format: {date}")
                                parsed_date = None

                            nav, created = NavModel.objects.update_or_create(
                                navAmcName=amc,
                                navFundName=scheme_name,
                                navDate=parsed_date,
                                defaults={'nav': net_asset_value}
                            )
                            nav_count += 1
                            if nav_count % 1000 == 0:
                                logger.info(f"Processed {nav_count} NAV entries")
                        else:
                            logger.warning(f"AMC not found: {current_amc_name}")
                except Exception as e:
                    logger.error(f"Error processing line: {line}. Error: {str(e)}")

            logger.info(f"Total NAV entries processed: {nav_count}")
            self.stdout.write(self.style.SUCCESS(f'Successfully created/updated NAV data for {date_str}'))
            logger.info(f'Successfully created/updated NAV data for {date_str}')

        except requests.exceptions.RequestException as e:
            error_msg = f'Error fetching data: {str(e)}'
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg, exc_info=True)
        except Exception as e:
            error_msg = f'Unexpected error: {str(e)}'
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg, exc_info=True)

        return f"Command execution completed. Processed {nav_count} NAV entries."
