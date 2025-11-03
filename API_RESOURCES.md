# Betfair API Resources and Setup Guide

This document consolidates helpful resources for working with the Betfair API.

## Official Documentation

### API Documentation
- [Developer Program](https://www.betfair.com.au/hub/tools/betting-tools/developer-program/)
- [API Documentation](https://docs.developer.betfair.com/)
- [Sports API Visualiser](https://docs.developer.betfair.com/visualisers/api-ng-sports-operations/)
- [Account API Visualiser](https://docs.developer.betfair.com/visualisers/api-ng-account-operations/)

### Authentication & Setup
- [How to Setup Your API Key](https://www.betfair.com.au/hub/tools/betting-tools/how-to-setup-your-betfair-api-key/)
- [Certificate Generation (Windows/XCA)](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Certificate+Generation+With+XCA)
- [Certificate Generation (Mac/Linux)](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login)
- [Certificate Management Portal](https://myaccount.betfair.com/account/certificategeneration)

### Community Resources
- [Betfair Data Scientists Hub](https://betfair-datascientists.github.io/)
- [API Resources Page](https://betfair-datascientists.github.io/api/apiResources/)
- [Automation Hub](https://betfair-datascientists.github.io/api/)

## Python Libraries

### betfairlightweight
- **GitHub**: https://github.com/liampauling/betfair
- **Documentation**: https://betfairlightweight.readthedocs.io/
- **Examples**: https://github.com/liampauling/betfair/tree/master/examples
- **Installation**: `pip install betfairlightweight`

### Alternative: flumine
- **GitHub**: https://github.com/betcode-org/flumine
- **Documentation**: https://flumine.readthedocs.io/
- **Use case**: Trading framework built on betfairlightweight

## R Libraries

### abettor
- **GitHub**: https://github.com/phillc73/abettor
- **Installation**: `devtools::install_github("phillc73/abettor")`

## Authentication Methods

### 1. Interactive Login (Simple, requires certificates)
```python
import betfairlightweight

trading = betfairlightweight.APIClient(
    username="your_username",
    password="your_password",
    app_key="your_app_key",
    certs="/path/to/certs"
)
trading.login()
```

### 2. Interactive Login (No certificates - DEPRECATED)
**Note**: This method is being phased out by Betfair and requires certificates for most operations.

### 3. Session Token (Advanced)
If you have a valid session token from another application:
```python
import requests

headers = {
    'X-Application': 'your_app_key',
    'X-Authentication': 'your_session_token',
    'Content-Type': 'application/json'
}

response = requests.post(
    'https://api.betfair.com/exchange/betting/rest/v1.0/listEventTypes/',
    headers=headers,
    json={"filter": {}}
)
```

## Certificate Setup Guide

### Step 1: Generate Private Key and CSR
```bash
# Generate private key
openssl genrsa -out client-2048.key 2048

# Generate CSR
openssl req -new -key client-2048.key -out client-2048.csr
```

### Step 2: Upload CSR to Betfair
1. Go to: https://myaccount.betfair.com/account/certificategeneration
2. Paste your CSR content
3. Click "Generate Certificate"
4. Download the certificate

### Step 3: Save Certificate
Save the downloaded certificate as `client-2048.crt` in the same folder as your key.

### Step 4: Configure Your Application
```python
trading = betfairlightweight.APIClient(
    username="your_username",
    password="your_password",
    app_key="your_app_key",
    certs="/path/to/certs"  # Folder containing .key and .crt files
)
```

## Common Operations

### List Event Types (Sports)
```python
event_types = trading.betting.list_event_types()
for event_type in event_types:
    print(f"{event_type.event_type.name}: {event_type.event_type.id}")
```

### Get Horse Racing Events
```python
from betfairlightweight import filters
import datetime

# Filter for horse racing in next 24 hours
horse_filter = filters.market_filter(
    event_type_ids=['7'],  # Horse Racing
    market_start_time={
        'to': (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%TZ")
    }
)

events = trading.betting.list_events(filter=horse_filter)
```

### Get Market Prices
```python
# Get market catalogue
market_filter = filters.market_filter(
    event_ids=['event_id'],
    market_type_codes=['WIN']
)

catalogues = trading.betting.list_market_catalogue(
    filter=market_filter,
    max_results='100'
)

# Get live prices
price_filter = filters.price_projection(
    price_data=['EX_BEST_OFFERS']
)

market_books = trading.betting.list_market_book(
    market_ids=['market_id'],
    price_projection=price_filter
)
```

## Event Type IDs (Common Sports)

| Sport | Event Type ID |
|-------|---------------|
| Soccer | 1 |
| Tennis | 2 |
| Golf | 3 |
| Cricket | 4 |
| Rugby Union | 5 |
| Boxing | 6 |
| Horse Racing | 7 |
| Motor Sport | 8 |
| Rugby League | 1477 |
| Darts | 3503 |
| Basketball | 7522 |
| Ice Hockey | 7524 |
| Snooker | 6422 |
| American Football | 6423 |
| Baseball | 7511 |
| Australian Rules | 61420 |
| Greyhound Racing | 4339 |
| Mixed Martial Arts | 26420387 |

## Market Type Codes (Common Markets)

| Market Type | Code |
|-------------|------|
| Match Odds | MATCH_ODDS |
| Over/Under 0.5 Goals | OVER_UNDER_05 |
| Over/Under 1.5 Goals | OVER_UNDER_15 |
| Over/Under 2.5 Goals | OVER_UNDER_25 |
| Both Teams To Score | BTTS |
| Correct Score | CORRECT_SCORE |
| Win | WIN |
| Place | PLACE |
| Each Way | EACH_WAY |
| To Be Placed | TO_BE_PLACED |
| Match Betting | MATCH_BET |
| Total Goals | TOTAL_GOALS |

## Troubleshooting

### "Certificate Error" or "Authentication Failed"
- Ensure your certificates are in the correct format (.crt and .key)
- Verify the certificates were generated from Betfair's portal
- Check that the username in the CSR matches your Betfair username
- Ensure your app key is valid and not expired

### "Access Denied" or 403 Errors
- Verify your app key is correct
- Check that your Betfair account has API access enabled
- Ensure you have funds in your account (some endpoints require this)
- Confirm your account is not suspended

### "No Data Returned"
- Check that markets are actually available for your query
- Verify date/time filters are correct (use UTC time)
- Ensure the event type ID is correct
- Some markets may require minimum account activity

### Rate Limiting
- Betfair has rate limits on API calls
- Free accounts: Lower rate limits
- Paid accounts: Higher rate limits
- Use efficient queries and cache data when possible

## Best Practices

1. **Cache Market Data**: Don't repeatedly query for the same data
2. **Use Filters Wisely**: Narrow your queries to reduce data transfer
3. **Handle Errors Gracefully**: Network issues and API errors can occur
4. **Keep Certificates Secure**: Never commit certificates to version control
5. **Monitor Rate Limits**: Track your API usage to avoid throttling
6. **Use UTC Times**: All Betfair timestamps are in UTC
7. **Test on Small Datasets**: Start with single events before scaling up

## Getting Help

- **Betfair Developer Forum**: https://forum.developer.betfair.com/
- **GitHub Issues**: Report issues in relevant library repositories
- **Stack Overflow**: Tag questions with 'betfair-api'
- **Betfair Support**: For account or access issues

## Example Projects

This repository contains several example projects:
- `python/API Tutorial.ipynb` - Comprehensive Python tutorial
- `python/Stream API Tutorial.ipynb` - Real-time streaming data
- `R/get_world_cup_odds_tutorial.R` - R example for odds data
- `R/AFL_odds_pulleR.R` - AFL betting data example

## Additional Resources

- [Betfair Exchange API Docs](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni)
- [Exchange Stream API](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)
- [Historical Data](https://historicdata.betfair.com/)
- [Betting Strategies](https://www.betfair.com.au/hub/tools/betting-tools/betting-strategies/)
