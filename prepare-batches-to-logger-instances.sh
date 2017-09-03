#!/bin/bash

# exit on empty variables
set -u

# exit on non-zero status
set -e

if [[ $# == 0 ]]; then
    echo provide the web-cross-domain-req-logger folder name as first argument
    echo 'provide the folder name with batch*txt files as second argument'
    exit 1
fi

cp -R "$1" web-cross-domain-req-logger-01
cp -R "$1" web-cross-domain-req-logger-02
cp -R "$1" web-cross-domain-req-logger-03
cp -R "$1" web-cross-domain-req-logger-04
cp -R "$1" web-cross-domain-req-logger-05
cp -R "$1" web-cross-domain-req-logger-06
cp -R "$1" web-cross-domain-req-logger-07
cp -R "$1" web-cross-domain-req-logger-08
cp -R "$1" web-cross-domain-req-logger-09
cp -R "$1" web-cross-domain-req-logger-10
cp -R "$1" web-cross-domain-req-logger-11
cp -R "$1" web-cross-domain-req-logger-12
cp -R "$1" web-cross-domain-req-logger-13
cp -R "$1" web-cross-domain-req-logger-14
cp -R "$1" web-cross-domain-req-logger-15

cp "$2/batch000a.txt" web-cross-domain-req-logger-01/page-list.txt
cp "$2/batch000b.txt" web-cross-domain-req-logger-02/page-list.txt
cp "$2/batch001.txt" web-cross-domain-req-logger-03/page-list.txt
cp "$2/batch002.txt" web-cross-domain-req-logger-04/page-list.txt
cp "$2/batch003.txt" web-cross-domain-req-logger-05/page-list.txt
cp "$2/batch004.txt" web-cross-domain-req-logger-06/page-list.txt
cp "$2/batch005.txt" web-cross-domain-req-logger-07/page-list.txt
cp "$2/batch006.txt" web-cross-domain-req-logger-08/page-list.txt
cp "$2/batch007.txt" web-cross-domain-req-logger-09/page-list.txt
cp "$2/batch008.txt" web-cross-domain-req-logger-10/page-list.txt
cp "$2/batch009.txt" web-cross-domain-req-logger-11/page-list.txt
cp "$2/batch010.txt" web-cross-domain-req-logger-12/page-list.txt
cp "$2/batch011.txt" web-cross-domain-req-logger-13/page-list.txt
cp "$2/batch012.txt" web-cross-domain-req-logger-14/page-list.txt
cp "$2/batch013.txt" web-cross-domain-req-logger-15/page-list.txt
cat "$2/batch014.txt" >> web-cross-domain-req-logger-01/page-list.txt
cat "$2/batch015.txt" >> web-cross-domain-req-logger-02/page-list.txt
cat "$2/batch016.txt" >> web-cross-domain-req-logger-03/page-list.txt
cat "$2/batch017.txt" >> web-cross-domain-req-logger-04/page-list.txt
cat "$2/batch018.txt" >> web-cross-domain-req-logger-05/page-list.txt
cat "$2/batch019.txt" >> web-cross-domain-req-logger-06/page-list.txt
cat "$2/batch020.txt" >> web-cross-domain-req-logger-07/page-list.txt
cat "$2/batch021.txt" >> web-cross-domain-req-logger-08/page-list.txt
cat "$2/batch022.txt" >> web-cross-domain-req-logger-09/page-list.txt
cat "$2/batch023.txt" >> web-cross-domain-req-logger-10/page-list.txt
cat "$2/batch024.txt" >> web-cross-domain-req-logger-11/page-list.txt
cat "$2/batch025.txt" >> web-cross-domain-req-logger-12/page-list.txt
cat "$2/batch026.txt" >> web-cross-domain-req-logger-13/page-list.txt
cat "$2/batch027.txt" >> web-cross-domain-req-logger-14/page-list.txt
cat "$2/batch028.txt" >> web-cross-domain-req-logger-15/page-list.txt
cat "$2/batch029.txt" >> web-cross-domain-req-logger-01/page-list.txt
cat "$2/batch030.txt" >> web-cross-domain-req-logger-02/page-list.txt
cat "$2/batch031.txt" >> web-cross-domain-req-logger-03/page-list.txt
cat "$2/batch032.txt" >> web-cross-domain-req-logger-04/page-list.txt
cat "$2/batch033.txt" >> web-cross-domain-req-logger-05/page-list.txt
cat "$2/batch034.txt" >> web-cross-domain-req-logger-06/page-list.txt
cat "$2/batch035.txt" >> web-cross-domain-req-logger-07/page-list.txt
cat "$2/batch036.txt" >> web-cross-domain-req-logger-08/page-list.txt
cat "$2/batch037.txt" >> web-cross-domain-req-logger-09/page-list.txt
cat "$2/batch038.txt" >> web-cross-domain-req-logger-10/page-list.txt
cat "$2/batch039.txt" >> web-cross-domain-req-logger-11/page-list.txt
cat "$2/batch040.txt" >> web-cross-domain-req-logger-12/page-list.txt
cat "$2/batch041.txt" >> web-cross-domain-req-logger-13/page-list.txt
cat "$2/batch042.txt" >> web-cross-domain-req-logger-14/page-list.txt
cat "$2/batch043.txt" >> web-cross-domain-req-logger-15/page-list.txt
cat "$2/batch044.txt" >> web-cross-domain-req-logger-01/page-list.txt
cat "$2/batch045.txt" >> web-cross-domain-req-logger-02/page-list.txt
cat "$2/batch046.txt" >> web-cross-domain-req-logger-03/page-list.txt
cat "$2/batch047.txt" >> web-cross-domain-req-logger-04/page-list.txt
cat "$2/batch048.txt" >> web-cross-domain-req-logger-05/page-list.txt
cat "$2/batch049.txt" >> web-cross-domain-req-logger-06/page-list.txt
cat "$2/batch050.txt" >> web-cross-domain-req-logger-07/page-list.txt


( cd web-cross-domain-req-logger-01 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-02 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-03 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-04 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-05 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-06 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-07 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-08 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-09 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-10 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-11 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-12 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-13 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-14 && bash create-sandbox-logger.sh ; )
( cd web-cross-domain-req-logger-15 && bash create-sandbox-logger.sh ; )

