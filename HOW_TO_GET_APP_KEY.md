# How to Get Your Betfair App Key - Step by Step Guide

## Quick Summary

You need an **Application Key** (App Key) to use the Betfair API. There are two types:
- **Delayed App Key** - Free, for testing (provides delayed data)
- **Live App Key** - Requires £299 fee, for live data

For getting started, you'll use the **Delayed App Key** which is free and active immediately.

---

## Method 1: Using the Accounts API Demo Tool (Recommended)

### Step 1: Go to the Accounts API Demo Tool
Visit: **https://docs.developer.betfair.com/visualisers/api-ng-account-operations/**

### Step 2: Login to Betfair (in another tab)
- Open a new browser tab
- Go to: **https://www.betfair.com.au** (or .com)
- Login with your Betfair credentials (pancakeshouse)
- Keep this tab open

### Step 3: Select Operation
Back in the API Demo Tool:
- Find the dropdown menu at the top left
- Select: **"getDeveloperAppKeys"** (to view existing keys)
  - OR select **"createDeveloperAppKeys"** (to create new keys if you don't have any)

### Step 4: Get Session Token
- Click in the **"Session Token (ssoid)"** field
- The tool should automatically populate it from your logged-in session
- If not, refresh the demo tool page while you're logged into Betfair

### Step 5: Execute
- If using **getDeveloperAppKeys**: Just click **"Execute"**
  - This will show you any existing App Keys

- If using **createDeveloperAppKeys**:
  - Enter an **Application Name** (e.g., "MyBettingApp" or "HorseRacing")
  - This name must be unique
  - Click **"Execute"**

### Step 6: Copy Your App Key
In the response, you'll see:
```json
{
  "appName": "YourAppName",
  "appId": 12345,
  "appVersions": [
    {
      "version": "1.0",
      "applicationKey": "YOUR_APP_KEY_HERE",
      "delayData": true,
      "subscriptionRequired": false,
      "ownerManaged": false,
      "active": true
    }
  ]
}
```

**Copy the `applicationKey` value** - this is your App Key!

---

## Method 2: Direct Account Page

### Option A: Australia
1. Go to: **https://myaccount.betfair.com.au/accountdetails/apikeyaccess**
2. Login with your credentials
3. Look for "Developer Apps" or "Application Keys" section
4. Your App Keys should be listed there

### Option B: International
1. Go to: **https://myaccount.betfair.com/accountdetails/apikeyaccess**
2. Follow the same steps as above

### Option C: My Account Security Page
1. Go to: **https://myaccount.betfair.com.au/accountdetails/mysecurity?showAPI=1**
2. Scroll down to find "API Access" or "Developer Access" section
3. Your App Keys should be visible there

---

## Method 3: Betfair Developer Portal

1. Go to: **https://developer.betfair.com/**
2. Click **"Login"** (top right)
3. Login with your Betfair credentials
4. Navigate to **"My Account"** or **"App Keys"**
5. View or create your Application Keys

---

## What Your App Key Looks Like

✅ **Correct App Key format**:
- Usually alphanumeric
- Example: `aBcDeFgHiJkLmNoPqRsT`
- Example: `ab1cd2ef3gh4ij5kl6mn`

❌ **NOT an App Key** (this is a session token):
- `8aGvkxDNhUnVEypjjK8KFNH1riIsnHq7fRZvKV8q/kQ=` ← Has `/` and `=`

---

## Important Notes

### About Delayed vs Live App Keys

**Delayed App Key** (Free):
- Active immediately upon creation
- Provides delayed price data (~60 seconds behind)
- Perfect for testing and development
- **Use this to get started!**

**Live App Key** (£299 fee):
- Inactive by default
- Requires activation application
- £299 fee debited from your Betfair account
- Provides real-time live data
- Only activate when you need live data

### Troubleshooting

**"I don't see any App Keys"**
- You need to create them using Method 1 (createDeveloperAppKeys)

**"The demo tool doesn't auto-fill session token"**
- Make sure you're logged into Betfair in another tab
- Refresh the demo tool page
- Clear browser cache and try again

**"I get an error when creating App Keys"**
- App names must be unique across all Betfair users
- Try a different, more unique name
- You can only have one set of App Keys per account

**"My Live App Key is inactive"**
- This is normal - Live App Keys are inactive by default
- Use the Delayed App Key for now (it's active immediately)
- Only apply for Live access if you need real-time data

---

## Quick Start for This Project

For downloading horse racing data and getting started:

1. **Use the Delayed App Key** (free, active immediately)
2. It provides data that's ~60 seconds delayed
3. This is perfect for:
   - Testing the API
   - Downloading historical data
   - Building and testing your scripts
   - Learning how the API works

You can always upgrade to a Live App Key later if needed!

---

## Once You Have Your App Key

Paste it here in the chat, and I will:
1. ✅ Update your config.json with the correct App Key
2. ✅ Test the API connection
3. ✅ Download today's horse racing data
4. ✅ Save it to CSV files for you!

---

## Helpful Links

- **Accounts API Demo Tool**: https://docs.developer.betfair.com/visualisers/api-ng-account-operations/
- **Developer Support**: https://support.developer.betfair.com/
- **API Documentation**: https://docs.developer.betfair.com/
- **Developer Forum**: https://forum.developer.betfair.com/
