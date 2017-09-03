#!/bin/bash

# exit on empty variables
set -u

# exit on non-zero status
set -e

script_basename=$(basename "$0")

while true ; do
    bash take-one-page-from-top-of-list-and-log.sh || { echo "$script_basename is done" ; exit 0 ; }
done

