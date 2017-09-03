#!/bin/bash

# exit on empty variables
set -u

# exit on non-zero status
set -e

page_list="page-list.txt"

page_list_num_of_lines=$( cat "$page_list" | wc -l ; )

if [[ $page_list_num_of_lines == "0" ]] ; then
    echo "$page_list is empty"
    exit 1
fi

top_line=$( head -n1 "$page_list" ; )

tail -n+2 "$page_list" > "$page_list.tmp"
mv "$page_list.tmp" "$page_list" 

bash log-page.sh "$top_line" || true
exit 0
