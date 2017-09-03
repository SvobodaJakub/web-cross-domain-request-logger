#!/bin/bash

# exit on empty variables
set -u

# exit on non-zero status
set -e

chromium-browser --disable-captive-portal-bypass-proxy --disable-cloud-import --disable-component-cloud-policy --disable-component-extensions-with-background-pages --disable-component-update --disable-default-apps --disable-contextual-search --disable-device-discovery-notifications --disable-dinosaur-easter-egg --disable-domain-reliability --disable-drive-search-in-app-launcher --disable-extensions --disable-field-trial-config --disable-file-system --disable-gaia-services --disable-gpu --disable-machine-cert-request --disable-notifications --disable-ntp-popular-sites --disable-ntp-most-likely-favicons-from-server --disable-offer-upload-credit-cards --disable-office-editing-component-extension --disable-origin-trial-controlled-blink-features --disable-search-geolocation-disclosure --disable-signin-promo --disable-signin-scoped-device-id --disable-speech-api --disable-sync --mute-audio --no-experiments --no-default-browser-check --no-service-autorun --no-wifi --safebrowsing-disable-auto-update --safebrowsing-disable-download-protection --safebrowsing-disable-extension-blacklist --disable-preconnect --disable-translate --disable-plugins-discovery --disable-plugins --disable-background-mode --disable-3d-apis --dns-prefetch-disable --incognito about:blank &

chromium_pid=$!

sleep 5

kill "$chromium_pid"
sleep 1
kill -9 "$chromium_pid" || true

mkdir home_template
cp -R .cache .config .local .pki home_template/


