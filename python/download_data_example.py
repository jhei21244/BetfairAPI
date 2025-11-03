"""
Simple example script to download Betfair market data

This script demonstrates how to:
1. Connect to Betfair API
2. List available sports/event types
3. Find upcoming horse racing events
4. Download market data for those events

Before running, ensure you have:
- Installed requirements: pip install -r requirements.txt
- Created config.json with your credentials
- Generated SSL certificates
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

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "config.json not found. Please copy config_template.json to config.json "
            "and fill in your credentials."
        )

    with open(config_path, 'r') as f:
        config = json.load(f)

    return config['betfair']


def connect_to_api(config):
    """Create and login to Betfair API client"""
    print("Connecting to Betfair API...")

    trading = betfairlightweight.APIClient(
        username=config['username'],
        password=config['password'],
        app_key=config['app_key'],
        certs=config['certs_path']
    )

    # Login
    trading.login()
    print("Successfully logged in!")

    return trading


def list_event_types(trading):
    """List all available event types (sports)"""
    print("\nFetching available event types...")

    event_types = trading.betting.list_event_types()

    df = pd.DataFrame({
        'Sport': [event_type.event_type.name for event_type in event_types],
        'ID': [event_type.event_type.id for event_type in event_types],
        'Market Count': [event_type.market_count for event_type in event_types]
    }).sort_values('Market Count', ascending=False)

    print("\nAvailable Sports:")
    print(df.to_string(index=False))

    return df


def get_horse_racing_events(trading, days_ahead=1):
    """Get upcoming horse racing events"""
    print(f"\nFetching horse racing events for the next {days_ahead} day(s)...")

    # Horse Racing event type ID is 7
    horse_racing_filter = betfairlightweight.filters.market_filter(
        event_type_ids=['7'],
        market_start_time={
            'to': (datetime.datetime.utcnow() + datetime.timedelta(days=days_ahead)).strftime("%Y-%m-%dT%TZ")
        }
    )

    events = trading.betting.list_events(filter=horse_racing_filter)

    if not events:
        print("No horse racing events found in the specified time period.")
        return None

    df = pd.DataFrame({
        'Event Name': [event.event.name for event in events],
        'Event ID': [event.event.id for event in events],
        'Venue': [event.event.venue for event in events],
        'Country': [event.event.country_code for event in events],
        'Open Date': [event.event.open_date for event in events],
        'Market Count': [event.market_count for event in events]
    }).sort_values('Open Date')

    print(f"\nFound {len(df)} horse racing events:")
    print(df.to_string(index=False))

    return df


def get_market_data(trading, event_id, max_results=20):
    """Get market catalogue for a specific event"""
    print(f"\nFetching market data for event ID: {event_id}...")

    market_filter = betfairlightweight.filters.market_filter(
        event_ids=[str(event_id)]
    )

    market_catalogues = trading.betting.list_market_catalogue(
        filter=market_filter,
        max_results=str(max_results),
        sort='FIRST_TO_START'
    )

    if not market_catalogues:
        print("No markets found for this event.")
        return None

    df = pd.DataFrame({
        'Market Name': [market.market_name for market in market_catalogues],
        'Market ID': [market.market_id for market in market_catalogues],
        'Total Matched': [market.total_matched for market in market_catalogues],
        'Market Start Time': [market.market_start_time for market in market_catalogues]
    })

    print(f"\nMarket data for event {event_id}:")
    print(df.to_string(index=False))

    return df


def get_market_prices(trading, market_id):
    """Get current prices for a specific market"""
    print(f"\nFetching current prices for market: {market_id}...")

    # Create price filter to get best available prices
    price_filter = betfairlightweight.filters.price_projection(
        price_data=['EX_BEST_OFFERS', 'EX_TRADED']
    )

    market_books = trading.betting.list_market_book(
        market_ids=[market_id],
        price_projection=price_filter
    )

    if not market_books or not market_books[0].runners:
        print("No price data available for this market.")
        return None

    market_book = market_books[0]

    runners_data = []
    for runner in market_book.runners:
        runners_data.append({
            'Selection ID': runner.selection_id,
            'Status': runner.status,
            'Last Price Traded': runner.last_price_traded,
            'Total Matched': runner.total_matched,
            'Best Back Price': runner.ex.available_to_back[0].price if runner.ex.available_to_back else None,
            'Best Back Size': runner.ex.available_to_back[0].size if runner.ex.available_to_back else None,
            'Best Lay Price': runner.ex.available_to_lay[0].price if runner.ex.available_to_lay else None,
            'Best Lay Size': runner.ex.available_to_lay[0].size if runner.ex.available_to_lay else None,
        })

    df = pd.DataFrame(runners_data)

    print(f"\nCurrent prices:")
    print(df.to_string(index=False))

    return df


def main():
    """Main function to demonstrate API usage"""
    try:
        # Load configuration
        config = load_config()

        # Connect to API
        trading = connect_to_api(config)

        # List all event types
        event_types_df = list_event_types(trading)

        # Get horse racing events
        events_df = get_horse_racing_events(trading, days_ahead=1)

        if events_df is not None and len(events_df) > 0:
            # Get market data for the first event
            first_event_id = events_df.iloc[0]['Event ID']
            markets_df = get_market_data(trading, first_event_id)

            if markets_df is not None and len(markets_df) > 0:
                # Get prices for the first market
                first_market_id = markets_df.iloc[0]['Market ID']
                prices_df = get_market_prices(trading, first_market_id)

        print("\n" + "="*80)
        print("Data download complete!")
        print("="*80)
        print("\nNext steps:")
        print("1. Explore the Jupyter notebooks in python/API Tutorial.ipynb")
        print("2. Modify this script to download the specific data you need")
        print("3. Save data to CSV using: df.to_csv('output.csv', index=False)")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nSetup steps:")
        print("1. Copy config_template.json to config.json")
        print("2. Fill in your Betfair credentials in config.json")
        print("3. Generate SSL certificates and place them in the certs/ folder")
        print("4. See SETUP.md for detailed instructions")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("\nPlease check:")
        print("- Your credentials are correct in config.json")
        print("- Your SSL certificates are properly set up")
        print("- You have an active internet connection")
        print("- Your Betfair account has API access enabled")


if __name__ == "__main__":
    main()
