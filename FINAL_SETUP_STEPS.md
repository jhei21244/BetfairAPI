# Final Setup Steps - Get Your API Working!

You're almost there! Here's what you need to do to complete the setup.

## Current Status
✅ Certificate files generated (`client-2048.key` and `client-2048.crt`)
✅ Config file created with your credentials
✅ Python dependencies installed
⏳ Need to upload certificate to Betfair
⏳ Need to verify your App Key

## Step 1: Upload Certificate to Betfair

### Go to Your Account Security Settings

**For Australia:**
https://myaccount.betfair.com.au/accountdetails/mysecurity?showAPI=1

**For International:**
https://myaccount.betfair.com/accountdetails/mysecurity?showAPI=1

### Upload Process

1. **Login** with your Betfair credentials (pancakeshouse)
2. Scroll to **"Automated Betting Program Access"** or **"API Access"** section
3. Click **"Edit"** or **"Upload Certificate"**
4. **Upload the file**: `certs/client-2048.crt`
5. Click **"Save"** or **"Submit"**

### Downloading the Certificate

If you need to download the certificate file from this environment:

The certificate file is located at:
```
/home/user/BetfairAPI/certs/client-2048.crt
```

You can view it with:
```bash
cat /home/user/BetfairAPI/certs/client-2048.crt
```

## Step 2: Verify Your App Key

The value you provided (`8aGvkxDNhUnVEypjjK8KFNH1riIsnHq7fRZvKV8q/kQ=`) looks like it might be a session token rather than an App Key.

### What is an App Key?

An **App Key** (also called Application Key) is a unique identifier for your application. It typically looks like:
- A shorter string (not as long as a session token)
- Usually alphanumeric without special characters like `/` or `=`
- Example format: `aBcDeFgHiJkLmNoPqRsT`

### How to Get Your App Key

1. **Go to**: https://myaccount.betfair.com.au/account/apidemo (or `.com` for international)
2. **Or try**: https://myaccount.betfair.com.au/accountdetails/apikeyaccess
3. **Login** to your Betfair account
4. Look for **"App Keys"** or **"Application Keys"** section
5. You might need to:
   - Create a new app key if you don't have one
   - Or copy your existing app key
6. **Copy the App Key** - it will be different from the session token

### Update Your Config

Once you have the correct App Key, update `/home/user/BetfairAPI/config.json`:

```json
{
  "betfair": {
    "username": "pancakeshouse",
    "password": ".mrUmJ*ar#8sBw_",
    "app_key": "YOUR_ACTUAL_APP_KEY_HERE",
    "certs_path": "/home/user/BetfairAPI/certs"
  }
}
```

## Step 3: Test the Connection

After uploading the certificate AND getting the correct app key, run:

```bash
cd /home/user/BetfairAPI/python
python quick_download.py
```

This will:
- ✅ Connect to Betfair API
- ✅ Download today's horse racing events
- ✅ Save data to CSV files

## Troubleshooting

### Error: 403 Forbidden
- **Cause**: Certificate not uploaded or App Key is incorrect
- **Solution**: Complete Step 1 and Step 2 above

### Error: Certificate not found
- **Cause**: Certificate files not in the right location
- **Solution**: Verify files exist in `/home/user/BetfairAPI/certs/`

### Error: Invalid credentials
- **Cause**: Username or password is incorrect
- **Solution**: Verify credentials in config.json

## Alternative: Use Betfair Developer Portal

If you're having trouble finding the certificate upload or app key pages:

1. Go to: https://developer.betfair.com/
2. Click **"Log in"** (top right)
3. Login with your Betfair credentials
4. Navigate to **"My Account"** or **"API Keys"**
5. You should find both certificate management and app key generation there

## Need Help?

The certificate file content (to upload) is:
```
-----BEGIN CERTIFICATE-----
MIIDpTCCAo2gAwIBAgIUY2CWvFknzFs5TYLUibwt+496CH0wDQYJKoZIhvcNAQEL
BQAwYjELMAkGA1UEBhMCQVUxETAPBgNVBAgMCFZpY3RvcmlhMRIwEAYDVQQHDAlN
ZWxib3VybmUxFDASBgNVBAoMC0JldGZhaXJVc2VyMRYwFAYDVQQDDA1wYW5jYWtl
c2hvdXNlMB4XDTI1MTEwNzA1MDgwOFoXDTI2MTEwNzA1MDgwOFowYjELMAkGA1UE
BhMCQVUxETAPBgNVBAgMCFZpY3RvcmlhMRIwEAYDVQQHDAlNZWxib3VybmUxFDAS
BgNVBAoMC0JldGZhaXJVc2VyMRYwFAYDVQQDDA1wYW5jYWtlc2hvdXNlMIIBIjAN
BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz1yGz6vccb6jQupExEd0NCNTBRfO
VSBIZwCX+Tk7qvlLmwuZ7LOy3SPOB15vZVMdI1n72CrlJArlIgwNc7GGCh1HvFJ8
d9wo2GBeY9yonwzu5zmDS7G0nWKHL6/5ISQP3wYJ39eu9OQIHSAleH6y4p1WlAGg
p0AQX4E1NqMTDHdJLEU6vl7piJ4VHCZF5u85XG12qVB+MntzDqp76aLYxahiBBh8
bDuHIcq+fV3iwOmGOtXEuK/I5xMZE8RLSaznZ9d63mvGLJnsiZ+SGivwNr0hxta0
2GHmAzHuMenOOLx9PcA3JA0AmVTQEUsHJDCqD9LHv4b158TmvGizrzkwGQIDAQAB
o1MwUTAdBgNVHQ4EFgQUARMv2XB3FWvLuAxhf4MdYPmc4kAwHwYDVR0jBBgwFoAU
ARMv2XB3FWvLuAxhf4MdYPmc4kAwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0B
AQsFAAOCAQEAdwhPgvfpVV73fNM/Wg5ZN/+PbX6cSfNr+Dx+rHP2yQMBFAnODlea
ORmxLIg6Ci/DrDASFLcLjHEOJ1m8XQ4/A2c8jRIVXCQ9582mu2gl8XukFzxHCdiT
7x+LXLYFOsUrCHy76KC31Xqn3riAbJ0hjqmVvq8HfcR7du6OBuAXdzRUWDMrpU9K
5o5Jn4CrNyu/tYX6lOO00Mypf5xYOBMK3LOTgCrtc/r/S2hrIGvfptEO8AMi8Fx8
da3D15W+oyN8VWJUc9ZaFsUS1GkXeE2b1TrMiMLy/4l51ZAUops6F9ds+3aS3hkK
6KPd3rd3BesHuKkU5E2p/oQYyEQv9NL+cg==
-----END CERTIFICATE-----
```

Once you've completed these steps, you'll be able to download Betfair data!
