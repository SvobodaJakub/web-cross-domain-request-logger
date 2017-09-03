
# it is set up to heavily lean towards .cz domains because I am from Czech Republic

# you need to find these files first:
# newly-registered-info-sample.csv
# top-1m.csv
# top-1million-sites.csv
# whois-db-download-info-sample.csv

ls newly-registered-info-sample.csv top-1m.csv top-1million-sites.csv whois-db-download-info-sample.csv || { echo "read the comments!" ; exit 1 ; }


cat whois-db-download-info-sample.csv | tail -n+2 | sed 's/^\([^,]*\),.*$/\1/g' | less > whois-db-download-info-sample.domains.txt
cat newly-registered-info-sample.csv | tail -n+2 | sed 's/^\([^,]*\),.*$/\1/g' | less > newly-registered-info-sample.domains.txt
cat top-1million-sites.csv | sed 's/[^,]*,\(.*\)/\1/g' > top-1million-sites.domains.txt
cat top-1m.csv | sed 's/[^,]*,\(.*\)/\1/g' > top-1m.domains.txt

cat top-1m.domains.txt | head -n 1000 > top-1m.domains.top1000.txt
cat top-1m.domains.txt | tail -n+1001 > top-1m.domains.below1000.txt

cat top-1million-sites.domains.txt | head -n 1000 > top-1million-sites.domains.top1000.txt
cat top-1million-sites.domains.txt | tail -n+1001 > top-1million-sites.domains.below1000.txt

cat top-1m.domains.below1000.txt top-1million-sites.domains.below1000.txt | sort | uniq | shuf --random-source=top-1m.csv > top-all-below1000.domains.txt

cat top-1m.domains.top1000.txt top-1million-sites.domains.top1000.txt | sort | uniq | shuf --random-source=top-1m.csv > top-all-top1000.domains.txt

cat top-all-below1000.domains.txt | grep -E '.+\.cz' > top-all-cz-below1000.domains.txt

cat top-all-below1000.domains.txt | grep -v -E '.+\.cz' > top-all-noncz-below1000.domains.txt

cat top-all-top1000.domains.txt | sed -n '1,700p' > batch000a.txt
cat top-all-top1000.domains.txt | sed -n '701,2000p' > batch000b.txt

cat top-all-cz-below1000.domains.txt | sed -n '1,1000p' > batch001.txt
cat top-all-cz-below1000.domains.txt | sed -n '1001,2000p' > batch002.txt
cat top-all-cz-below1000.domains.txt | sed -n '2001,3000p' > batch003.txt
cat top-all-cz-below1000.domains.txt | sed -n '3001,4000p' > batch004.txt
cat top-all-cz-below1000.domains.txt | sed -n '4001,5000p' > batch005.txt
cat top-all-cz-below1000.domains.txt | sed -n '5001,6000p' > batch006.txt
cat top-all-cz-below1000.domains.txt | sed -n '6001,7000p' > batch007.txt
cat top-all-cz-below1000.domains.txt | sed -n '7001,8000p' > batch008.txt
cat top-all-cz-below1000.domains.txt | sed -n '8001,9000p' > batch009.txt
cat top-all-cz-below1000.domains.txt | sed -n '9001,10000p' > batch010.txt


cat top-all-noncz-below1000.domains.txt | sed -n '1,1000p' >     batch011.txt
cat top-all-noncz-below1000.domains.txt | sed -n '1001,2000p' >  batch012.txt
cat top-all-noncz-below1000.domains.txt | sed -n '2001,3000p' >  batch013.txt
cat top-all-noncz-below1000.domains.txt | sed -n '3001,4000p' >  batch014.txt
cat top-all-noncz-below1000.domains.txt | sed -n '4001,5000p' >  batch015.txt
cat top-all-noncz-below1000.domains.txt | sed -n '5001,6000p' >  batch016.txt
cat top-all-noncz-below1000.domains.txt | sed -n '6001,7000p' >  batch017.txt
cat top-all-noncz-below1000.domains.txt | sed -n '7001,8000p' >  batch018.txt
cat top-all-noncz-below1000.domains.txt | sed -n '8001,9000p' >  batch019.txt
cat top-all-noncz-below1000.domains.txt | sed -n '9001,10000p' > batch020.txt

cat top-all-noncz-below1000.domains.txt | sed -n '10001,11000p' >  batch021.txt
cat top-all-noncz-below1000.domains.txt | sed -n '11001,12000p' >  batch022.txt
cat top-all-noncz-below1000.domains.txt | sed -n '12001,13000p' >  batch023.txt
cat top-all-noncz-below1000.domains.txt | sed -n '13001,14000p' >  batch024.txt
cat top-all-noncz-below1000.domains.txt | sed -n '14001,15000p' >  batch025.txt
cat top-all-noncz-below1000.domains.txt | sed -n '15001,16000p' >  batch026.txt
cat top-all-noncz-below1000.domains.txt | sed -n '16001,17000p' >  batch027.txt
cat top-all-noncz-below1000.domains.txt | sed -n '17001,18000p' >  batch028.txt
cat top-all-noncz-below1000.domains.txt | sed -n '18001,19000p' >  batch029.txt
cat top-all-noncz-below1000.domains.txt | sed -n '19001,20000p' >  batch030.txt

cat top-all-noncz-below1000.domains.txt | sed -n '20001,21000p' >  batch031.txt
cat top-all-noncz-below1000.domains.txt | sed -n '21001,22000p' >  batch032.txt
cat top-all-noncz-below1000.domains.txt | sed -n '22001,23000p' >  batch033.txt
cat top-all-noncz-below1000.domains.txt | sed -n '23001,24000p' >  batch034.txt
cat top-all-noncz-below1000.domains.txt | sed -n '24001,25000p' >  batch035.txt
cat top-all-noncz-below1000.domains.txt | sed -n '25001,26000p' >  batch036.txt
cat top-all-noncz-below1000.domains.txt | sed -n '26001,27000p' >  batch037.txt
cat top-all-noncz-below1000.domains.txt | sed -n '27001,28000p' >  batch038.txt
cat top-all-noncz-below1000.domains.txt | sed -n '28001,29000p' >  batch039.txt
cat top-all-noncz-below1000.domains.txt | sed -n '29001,30000p' >  batch040.txt

cat top-all-noncz-below1000.domains.txt | sed -n '30001,31000p' >  batch041.txt
cat top-all-noncz-below1000.domains.txt | sed -n '31001,32000p' >  batch042.txt
cat top-all-noncz-below1000.domains.txt | sed -n '32001,33000p' >  batch043.txt
cat top-all-noncz-below1000.domains.txt | sed -n '33001,34000p' >  batch044.txt
cat top-all-noncz-below1000.domains.txt | sed -n '34001,35000p' >  batch045.txt
cat top-all-noncz-below1000.domains.txt | sed -n '35001,36000p' >  batch046.txt
cat top-all-noncz-below1000.domains.txt | sed -n '36001,37000p' >  batch047.txt
cat top-all-noncz-below1000.domains.txt | sed -n '37001,38000p' >  batch048.txt
cat top-all-noncz-below1000.domains.txt | sed -n '38001,39000p' >  batch049.txt
cat top-all-noncz-below1000.domains.txt | sed -n '39001,40000p' >  batch050.txt



