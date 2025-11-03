"""
Quick script to download today's horse racing data

Run this after successfully authenticating to the API.
This will save market data to CSV files.
"""

import betfairlightweight
from betfairlightweight import filters
import pandas as pd
import json
import datetime
import os


def load_config():
    """Load configuration from config.json"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config['betfair']


def main():
    # Load config and connect
    config = load_config()

    # Create API client - use certs if available, otherwise use interactive login
    if config['certs_path']:
        trading = betfairlightweight.APIClient(
            username=config['username'],
            password=config['password'],
            app_key=config['app_key'],
            certs=config['certs_path']
        )
    else:
        # Interactive login without certificates
        trading = betfairlightweight.APIClient(
            username=config['username'],
            password=config['password'],
            app_key=config['app_key']
        )

    trading.login()
    print("✓ Connected to Betfair API")

    # Get today's horse racing events
    print("\nFetching today's horse racing events...")
    tomorrow = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%TZ")

    horse_filter = betfairlightweight.filters.market_filter(
        event_type_ids=['7'],  # Horse Racing
        market_countries=['AU'],  # Australia
        market_start_time={'to': tomorrow}
    )

    events = trading.betting.list_events(filter=horse_filter)

    if not events:
        print("No horse racing events found.")
        return

    print(f"✓ Found {len(events)} events")

    # Create events DataFrame
    events_df = pd.DataFrame({
        'Event Name': [e.event.name for e in events],
        'Event ID': [e.event.id for e in events],
        'Venue': [e.event.venue for e in events],
        'Country': [e.event.country_code for e in events],
        'Open Date': [e.event.open_date for e in events],
        'Market Count': [e.market_count for e in events]
    }).sort_values('Open Date')

    # Save events to CSV
    events_df.to_csv('horse_racing_events.csv', index=False)
    print(f"✓ Saved events to horse_racing_events.csv")

    # Get market catalogues for all events
    print("\nFetching market catalogues...")
    all_markets = []

    for idx, row in events_df.head(10).iterrows():  # Limit to first 10 events
        event_id = row['Event ID']
        event_name = row['Event Name']

        market_filter = betfairlightweight.filters.market_filter(
            event_ids=[str(event_id)],
            market_type_codes=['WIN']  # Just WIN markets
        )

        try:
            catalogues = trading.betting.list_market_catalogue(
                filter=market_filter,
                max_results='100',
                market_projection=['RUNNER_DESCRIPTION', 'MARKET_START_TIME']
            )

            for cat in catalogues:
                all_markets.append({
                    'Event Name': event_name,
                    'Event ID': event_id,
                    'Market Name': cat.market_name,
                    'Market ID': cat.market_id,
                    'Total Matched': cat.total_matched,
                    'Start Time': cat.market_start_time,
                    'Runner Count': len(cat.runners) if hasattr(cat, 'runners') else 0
                })

            print(f"  ✓ {event_name}: {len(catalogues)} markets")

        except Exception as e:
            print(f"  ✗ Error fetching {event_name}: {e}")

    # Save markets to CSV
    if all_markets:
        markets_df = pd.DataFrame(all_markets)
        markets_df.to_csv('horse_racing_markets.csv', index=False)
        print(f"\n✓ Saved {len(all_markets)} markets to horse_racing_markets.csv")

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


if __name__ == "__main__":
    main()
