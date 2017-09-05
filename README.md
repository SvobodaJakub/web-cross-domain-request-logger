Scripts in this repo

* assemble batches of domains to go through from sources of top N domains
* create firejail sandboxes
* automatically open the batched domains in chromium in the sandboxes
* for each visited 1st-party domain record the requested 3rd party domains
* analyze the data and assemble a blacklist of probable tracking domains


Disclaimers:

* Experimental.
* Use at your own risk.
* Identification of a domain by these tools doesn't imply or correlate with the domain's real conduct or policies. Take the results with a grain of salt.
* Presence or absence of a domain in the generated list or in the whitelist doesn't imply or correlate with the domain's real conduct or policies and is merely a result of experimentation with the tooling.


This tooling doesn't care about site's actual function, just about the technological possibility of its tracking of users across the web. It assumes guilt until whitelisted, and so you should use it very carefully, if ever.
