import requests
import pandas as pd
from datetime import datetime

url = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"
querystring = {"Scheme_Type": "Open"}
headers = {
    "x-rapidapi-key": "53456b3ab5mshc8278abef35dcbcp1891e2jsne5db5cf7e514",
    "x-rapidapi-host": "latest-mutual-fund-nav.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json()

    # Extract only the required fields
    filtered_data = [{
        'Mutual_Fund_Family': item.get('Mutual_Fund_Family'),
        'Scheme_Name': item.get('Scheme_Name'),
        'Net_Asset_Value': item.get('Net_Asset_Value'),
        'Date': item.get('Date')
    } for item in data]

    # Convert the filtered data to a pandas DataFrame
    df = pd.DataFrame(filtered_data)

    # Generate a filename with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mutual_fund_nav_{timestamp}.xlsx"

    # Export the DataFrame to Excel
    df.to_excel(filename, index=False)

    print(f"Data exported to {filename}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)