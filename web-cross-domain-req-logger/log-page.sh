#!/bin/bash

# exit on empty variables
set -u

# exit on non-zero status
set -e

if [[ $# == 0 ]]; then
    echo provide the url as first argument
    exit 1
fi

ls home_template || exit 1  # if this doesn't exist, something is wrong
rsync -a --delete home_template/.cache/ ./.cache/ || true
rsync -a --delete home_template/.config/ ./.config/ || true
rsync -a --delete home_template/.local/ ./.local/ || true
rsync -a --delete home_template/.pki/ ./.pki/ || true

webpage="$1"
echo "$webpage"
chromium-browser --disable-captive-portal-bypass-proxy --disable-cloud-import --disable-component-cloud-policy --disable-component-extensions-with-background-pages --disable-component-update --disable-default-apps --disable-contextual-search --disable-device-discovery-notifications --disable-dinosaur-easter-egg --disable-domain-reliability --disable-drive-search-in-app-launcher --disable-extensions --disable-field-trial-config --disable-file-system --disable-gaia-services --disable-gpu --disable-machine-cert-request --disable-notifications --disable-ntp-popular-sites --disable-ntp-most-likely-favicons-from-server --disable-offer-upload-credit-cards --disable-office-editing-component-extension --disable-origin-trial-controlled-blink-features --disable-search-geolocation-disclosure --disable-signin-promo --disable-signin-scoped-device-id --disable-speech-api --disable-sync --mute-audio --no-experiments --no-default-browser-check --no-service-autorun --no-wifi --safebrowsing-disable-auto-update --safebrowsing-disable-download-protection --safebrowsing-disable-extension-blacklist --disable-preconnect --disable-translate --disable-plugins-discovery --disable-plugins --disable-background-mode --disable-3d-apis --dns-prefetch-disable --incognito --kiosk --log-net-log=netlog.json "$webpage" &

chromium_pid=$!

sleep 80

kill "$chromium_pid"
sleep 0.3
kill -9 "$chromium_pid" || true

resolutions=$( cat netlog.json | tr '{' '\n' | strings | grep -E '^"host":"' | sed 's/^"host":"\([^"]\+\)".*/\1/g' | grep -v -E ':[0-9]+$' | grep -v -E '^[^.]+$' | uniq | tr '\n' ';' ; )

echo "$1;$resolutions" >> log-resolutions.txt
