Logs DNS name resolution requests in an automatable fashion.

1. bash create-sandbox-logger.sh 
    * creates a safe sandbox and xephyr X11 display in which the tools can run

2. bash enter-start-restart-sandbox-logger.sh
    * processes page-list.txt and if the sandbox crashes, running again will continue from where it crashed (except for the page that crashed it)

3. bash enter-sandbox-logger.sh
    * gets you bash inside the sandbox - for debugging

Rest of scripts are to be run in sandbox only and are normally launched automatically.

Results are in firejail-home-logger/log-resolutions.txt
