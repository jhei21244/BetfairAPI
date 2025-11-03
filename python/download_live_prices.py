"""
Download live prices for current markets

This script fetches real-time prices for active markets and saves them to CSV.
Useful for analysis, tracking odds movements, or building betting strategies.
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


def get_runner_prices(runner_books):
    """Process runner books and return DataFrame with prices"""
    data = []

    for runner in runner_books:
        # Get best back price (what you can back at)
        best_back_price = None
        best_back_size = None
        if runner.ex.available_to_back:
            best_back_price = runner.ex.available_to_back[0].price
            best_back_size = runner.ex.available_to_back[0].size

        # Get best lay price (what you can lay at)
        best_lay_price = None
        best_lay_size = None
        if runner.ex.available_to_lay:
            best_lay_price = runner.ex.available_to_lay[0].price
            best_lay_size = runner.ex.available_to_lay[0].size

        data.append({
            'Selection ID': runner.selection_id,
            'Status': runner.status,
            'Last Price Traded': runner.last_price_traded,
            'Total Matched': runner.total_matched,
            'Back Price': best_back_price,
            'Back Size': best_back_size,
            'Lay Price': best_lay_price,
            'Lay Size': best_lay_size,
        })

    return pd.DataFrame(data)


def main():
    # Connect to API
    config = load_config()
    trading = betfairlightweight.APIClient(
        username=config['username'],
        password=config['password'],
        app_key=config['app_key'],
        certs=config['certs_path']
    )

    trading.login()
    print("✓ Connected to Betfair API\n")

    # Get markets starting in the next 6 hours
    now = datetime.datetime.utcnow()
    six_hours_ahead = now + datetime.timedelta(hours=6)

    print("Searching for active markets...")

    # Filter for horse racing markets starting soon
    market_filter = betfairlightweight.filters.market_filter(
        event_type_ids=['7'],  # Horse Racing
        market_countries=['AU'],
        market_type_codes=['WIN'],
        market_start_time={
            'from': now.strftime("%Y-%m-%dT%TZ"),
            'to': six_hours_ahead.strftime("%Y-%m-%dT%TZ")
        }
    )

    # Get market catalogues
    catalogues = trading.betting.list_market_catalogue(
        filter=market_filter,
        max_results='50',
        market_projection=['RUNNER_DESCRIPTION', 'EVENT', 'MARKET_START_TIME']
    )

    if not catalogues:
        print("No active markets found in the next 6 hours.")
        return

    print(f"✓ Found {len(catalogues)} active markets\n")

    # Get prices for each market
    all_prices = []

    for cat in catalogues[:10]:  # Limit to first 10 markets
        market_id = cat.market_id
        market_name = cat.market_name
        event_name = cat.event.name if hasattr(cat, 'event') else 'Unknown'

        try:
            # Request market book with prices
            price_filter = betfairlightweight.filters.price_projection(
                price_data=['EX_BEST_OFFERS', 'EX_TRADED']
            )

            market_books = trading.betting.list_market_book(
                market_ids=[market_id],
                price_projection=price_filter
            )

            if market_books and market_books[0].runners:
                market_book = market_books[0]

                # Get runner names from catalogue
                runner_names = {r.selection_id: r.runner_name for r in cat.runners}

                # Get prices
                prices_df = get_runner_prices(market_book.runners)

                # Add market info
                prices_df['Market ID'] = market_id
                prices_df['Market Name'] = market_name
                prices_df['Event Name'] = event_name
                prices_df['Market Start Time'] = cat.market_start_time
                prices_df['Download Time'] = datetime.datetime.utcnow()

                # Add runner names
                prices_df['Runner Name'] = prices_df['Selection ID'].map(runner_names)

                all_prices.append(prices_df)

                print(f"✓ {event_name} - {market_name}")
                print(f"  Total Matched: ${prices_df['Total Matched'].sum():,.2f}")

        except Exception as e:
            print(f"✗ Error fetching {market_name}: {e}")

    # Combine and save all prices
    if all_prices:
        final_df = pd.concat(all_prices, ignore_index=True)

        # Reorder columns for better readability
        cols = ['Event Name', 'Market Name', 'Market Start Time', 'Runner Name',
                'Selection ID', 'Status', 'Back Price', 'Back Size',
                'Lay Price', 'Lay Size', 'Last Price Traded', 'Total Matched',
                'Download Time', 'Market ID']
        final_df = final_df[cols]

        # Save to CSV
        filename = f"live_prices_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        final_df.to_csv(filename, index=False)

        print("\n" + "="*80)
        print("DOWNLOAD COMPLETE")
        print("="*80)
        print(f"Total Markets: {len(all_prices)}")
        print(f"Total Runners: {len(final_df)}")
        print(f"Total Volume: ${final_df['Total Matched'].sum():,.2f}")
        print(f"\nSaved to: {filename}")
        print("="*80)

        # Show sample of data
        print("\nSample data:")
        print(final_df[['Event Name', 'Runner Name', 'Back Price', 'Lay Price',
                        'Total Matched']].head(10).to_string(index=False))
    else:
        print("\n✗ No price data available")


if __name__ == "__main__":
    main()
