#!/bin/bash

# exit on empty variables
set -u

# exit on non-zero status
set -e



( cd web-cross-domain-req-logger-01 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-02 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-03 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-04 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-05 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-06 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-07 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-08 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-09 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-10 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-11 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-12 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-13 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-14 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &
sleep 5
( cd web-cross-domain-req-logger-15 && ionice -c 3 nice -n 19 bash enter-start-restart-sandbox-logger.sh & ) &

echo waiting almost forever
sleep 3000d
