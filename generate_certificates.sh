#!/bin/bash

# Script to generate SSL certificates for Betfair API
# This will create a private key and certificate signing request (CSR)

echo "=================================================="
echo "Betfair SSL Certificate Generator"
echo "=================================================="
echo ""

# Create certs directory if it doesn't exist
mkdir -p certs
cd certs

echo "Step 1: Generating private key..."
openssl genrsa -out client-2048.key 2048

if [ $? -eq 0 ]; then
    echo "✓ Private key generated: certs/client-2048.key"
else
    echo "✗ Failed to generate private key"
    exit 1
fi

echo ""
echo "Step 2: Generating Certificate Signing Request (CSR)..."
echo ""
echo "You will be asked to enter some information."
echo "You can leave most fields blank, but here are some suggestions:"
echo "  - Country Name: AU"
echo "  - State: Your state"
echo "  - City: Your city"
echo "  - Organization: Your name or company"
echo "  - Common Name: Your Betfair username (pancakeshouse)"
echo ""

openssl req -new -key client-2048.key -out client-2048.csr

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ CSR generated: certs/client-2048.csr"
else
    echo "✗ Failed to generate CSR"
    exit 1
fi

echo ""
echo "=================================================="
echo "Certificate files created successfully!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. View your CSR file:"
echo "   cat certs/client-2048.csr"
echo ""
echo "2. Copy the ENTIRE contents (including BEGIN and END lines)"
echo ""
echo "3. Go to Betfair Developer Portal:"
echo "   https://myaccount.betfair.com/account/certificategeneration"
echo ""
echo "4. Paste the CSR and generate the certificate"
echo ""
echo "5. Download the certificate file and save it as:"
echo "   certs/client-2048.crt"
echo ""
echo "6. Update config.json to point to the certs folder:"
echo '   "certs_path": "certs"'
echo ""
echo "=================================================="
