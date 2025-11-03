"""
Quick script to download today's horse racing data using session token

If you already have a session token from a successful login,
you can use this script to download data directly.
"""

import requests
import pandas as pd
import datetime
import json
import os


def load_config():
    """Load configuration from config.json"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config['betfair']


def make_api_request(endpoint, app_key, session_token, params=None):
    """Make a request to Betfair API"""
    url = f"https://api.betfair.com/exchange/betting/rest/v1.0/{endpoint}/"

    headers = {
        'X-Application': app_key,
        'X-Authentication': session_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers, json=params if params else {})

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")


def main():
    # Load config
    config = load_config()

    # Use the app_key as session token (if it's actually a session token)
    session_token = config['app_key']
    app_key = config['app_key']  # We'll need the actual app key

    print("Testing API connection...")

    try:
        # Get today's horse racing events
        tomorrow = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

        horse_filter = {
            "filter": {
                "eventTypeIds": ["7"],  # Horse Racing
                "marketCountries": ["AU"],  # Australia
                "marketStartTime": {
                    "to": tomorrow
                }
            }
        }

        print("\nFetching today's horse racing events...")
        events = make_api_request('listEvents', app_key, session_token, horse_filter)

        if not events:
            print("No horse racing events found.")
            return

        print(f"✓ Found {len(events)} events")

        # Create events DataFrame
        events_data = []
        for event in events:
            events_data.append({
                'Event Name': event['event']['name'],
                'Event ID': event['event']['id'],
                'Venue': event['event'].get('venue', 'N/A'),
                'Country': event['event'].get('countryCode', 'N/A'),
                'Open Date': event['event'].get('openDate', 'N/A'),
                'Market Count': event.get('marketCount', 0)
            })

        events_df = pd.DataFrame(events_data)
        events_df = events_df.sort_values('Open Date')

        # Save events to CSV
        output_file = 'horse_racing_events.csv'
        events_df.to_csv(output_file, index=False)
        print(f"✓ Saved events to {output_file}")

        # Get market catalogues for first few events
        print("\nFetching market catalogues...")
        all_markets = []

        for idx, row in events_df.head(10).iterrows():
            event_id = row['Event ID']
            event_name = row['Event Name']

            market_filter = {
                "filter": {
                    "eventIds": [str(event_id)],
                    "marketTypeCodes": ["WIN"]
                },
                "maxResults": "100",
                "marketProjection": ["RUNNER_DESCRIPTION", "MARKET_START_TIME"]
            }

            try:
                catalogues = make_api_request('listMarketCatalogue', app_key, session_token, market_filter)

                for cat in catalogues:
                    all_markets.append({
                        'Event Name': event_name,
                        'Event ID': event_id,
                        'Market Name': cat.get('marketName', 'N/A'),
                        'Market ID': cat.get('marketId', 'N/A'),
                        'Total Matched': cat.get('totalMatched', 0),
                        'Start Time': cat.get('marketStartTime', 'N/A'),
                        'Runner Count': len(cat.get('runners', []))
                    })

                print(f"  ✓ {event_name}: {len(catalogues)} markets")

            except Exception as e:
                print(f"  ✗ Error fetching {event_name}: {e}")

        # Save markets to CSV
        if all_markets:
            markets_df = pd.DataFrame(all_markets)
            output_file = 'horse_racing_markets.csv'
            markets_df.to_csv(output_file, index=False)
            print(f"\n✓ Saved {len(all_markets)} markets to {output_file}")

            # Show summary
            print("\n" + "="*80)
            print("DOWNLOAD SUMMARY")
            print("="*80)
            print(f"Total Events: {len(events_df)}")
            print(f"Total Markets: {len(markets_df)}")
            print(f"Total Matched: ${markets_df['Total Matched'].sum():,.2f}")
            print("\nFiles created:")
            print("  - horse_racing_events.csv")
            print("  - horse_racing_markets.csv")
            print("="*80)
        else:
            print("\n✗ No markets found")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nThis might mean:")
        print("1. The session token has expired")
        print("2. You need to set up SSL certificates for automated login")
        print("3. The app_key in config.json needs to be the actual app key, not session token")


if __name__ == "__main__":
    main()
