# Betfair API Setup Guide

This guide will help you set up the Betfair API to download betting data.

## Prerequisites

1. A Betfair account
2. Python 3.7+ installed on your system
3. pip (Python package manager)

## Step-by-Step Setup

### 1. Install Python Dependencies

Run the following command in the repository root:

```bash
pip install -r requirements.txt
```

This will install:
- `betfairlightweight` - The Python library for Betfair API
- `pandas` - For data manipulation
- `numpy` - For numerical operations
- `jupyter` - For running the tutorial notebooks

### 2. Get Your Betfair API App Key

You'll need to register for a Betfair Developer Program app key:

1. Visit the [Betfair Developer Program](https://www.betfair.com.au/hub/tools/betting-tools/developer-program/)
2. Login with your Betfair account
3. Follow the instructions at [How to setup your Betfair API key](https://www.betfair.com.au/hub/tools/betting-tools/how-to-setup-your-betfair-api-key/)
4. Note down your App Key - you'll need this later

### 3. Generate SSL Certificates

For non-interactive (automated) login, Betfair requires SSL certificates:

#### Option A: Windows (using XCA)
Follow the detailed instructions here:
https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Certificate+Generation+With+XCA

#### Option B: Mac/Linux (using OpenSSL)
Follow the instructions here:
https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login

**Quick Steps:**
1. Generate a private key
2. Generate a certificate signing request (CSR)
3. Upload the CSR to Betfair
4. Download the certificate from Betfair
5. Store both the certificate and key in a `certs/` folder in this repository

### 4. Configure Your Credentials

1. Copy the config template:
   ```bash
   cp config_template.json config.json
   ```

2. Edit `config.json` with your actual credentials:
   ```json
   {
     "betfair": {
       "username": "your_betfair_username",
       "password": "your_betfair_password",
       "app_key": "your_app_key_here",
       "certs_path": "./certs"
     }
   }
   ```

3. Make sure your certificates are in the `certs/` folder

**Important:** The `config.json` file is already added to `.gitignore` so it won't be committed to version control.

### 5. Test Your Setup

Run the example script to test your connection:

```bash
python python/download_data_example.py
```

If successful, you should see market data downloaded from Betfair!

## Quick Start Examples

### Python Example

See the comprehensive tutorial in:
- `python/API Tutorial.ipynb` - Jupyter notebook with full examples
- `python/download_data_example.py` - Simple script to download data

### R Example

If you prefer R, check out:
- `R/README.md` - R setup instructions
- `R/get_world_cup_odds_tutorial.R` - Example script

## Useful Resources

- [Betfair API Documentation](https://docs.developer.betfair.com/)
- [Sports API Visualiser](https://docs.developer.betfair.com/visualisers/api-ng-sports-operations/)
- [Account API Visualiser](https://docs.developer.betfair.com/visualisers/api-ng-account-operations/)
- [betfairlightweight GitHub](https://github.com/liampauling/betfair)
- [abettor R package](https://github.com/phillc73/abettor)

## Common Issues

### Authentication Errors
- Double-check your username, password, and app key
- Ensure certificates are properly generated and uploaded to Betfair
- Verify the `certs_path` points to the correct folder

### Import Errors
- Make sure you've installed all requirements: `pip install -r requirements.txt`
- Check your Python version is 3.7 or higher: `python --version`

### No Data Returned
- Ensure you have funds in your Betfair account (some API calls require this)
- Check that the markets you're querying are currently available
- Verify your account is approved for API access

## Next Steps

Once you're set up, explore the tutorials:
1. `python/API Tutorial.ipynb` - Learn to fetch market data, place bets, and more
2. `python/Stream API Tutorial.ipynb` - Real-time streaming data
3. `R/get_world_cup_odds_tutorial.R` - Downloading odds data in R

Happy coding!
