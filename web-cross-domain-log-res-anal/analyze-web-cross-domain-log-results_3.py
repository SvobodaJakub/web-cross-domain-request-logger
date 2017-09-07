# analyses 3rd party domains
# * only requests outside the originating second-level domain are considered 3rd-party
#   (example: b.com or x.y.b.com are 3rd party to the originating a.com; x.a.com is 1st party)
# * the originating domains are always considered to be second-level domain
#     * because of public suffixes that contain dots and any logic would make it less correct
#     * because the visited domains are sourced from a list of top n _domains_
# * performs detection of probable ad/tracking domains
#     * if a given 1st party domain makes requests to 3rd party domains that fall under more than `n` second-level 1st party domains, then such a 1st party domain probably includes interesting trackers and all its 3rd party requests are taken as probable trackers
#     * 3rd party domains that include a suspicious keyword are taken as probable trackers
#     * some domains are whitelisted
import sys

# from how many 1st party domains a 3rd party domain must be included in order to be considered a tracker
MIN_INCLUDED_SUSPICIOUS = 20

# from how many 1st party domains a 3rd party domain must be included in order to be reported to the user (final filter on the suspicious domains just before printing the results)
MIN_INCLUDED_REPORT = 6

# it should hold that MIN_INCLUDED_REPORT < MIN_INCLUDED_SUSPICIOUS plus some more
assert MIN_INCLUDED_REPORT + 6 < MIN_INCLUDED_SUSPICIOUS

hack_TLDs_with_dot = ["co.uk", "com.cn", "com.au", "com.br", "azureedge.net", "azurewebsites.net", "co.nz", "org.br", "com.vn", "tmall.com", "com.pl", "org.uk", "wz.cz", "co.jp", ]
hack_TLDs_with_dot_mangled = [x.replace(".", "§§§") for x in hack_TLDs_with_dot]
def hack_TLDs_mangle_TLD(domain):
    # turn example.co.uk into example.co§§§uk
    for tld_with_dot in hack_TLDs_with_dot:
        if domain.endswith("." + tld_with_dot):
            return domain.replace("." + tld_with_dot, "." + tld_with_dot.replace(".", "§§§"))
    # noop
    return domain
def hack_TLDs_unmangle_TLD(domain):
    # turn example.co§§§uk into example.co.uk
    for tld_with_dot in hack_TLDs_with_dot_mangled:
        if domain.endswith("." + tld_with_dot):
            return domain.replace("." + tld_with_dot, "." + tld_with_dot.replace("§§§", "."))
    # noop
    return domain

all_domains = set()
all_3rd_party_domains = set()
visited_3rd_party_domains = {}
all_3rd_party_second_level_domains = set()
visited_3rd_party_second_level_domains = {}
all_3rd_party_second_level_domains_mapping_to_subdomains = {}
visited_3rd_party_second_level_domains_mapping_to_1st_party = {}
with open(sys.argv[1]) as fp:
    for line in fp:
        line = line.strip()
        if not line:
            continue
        domains = line.split(";")
        visited_domain = set()
        visited_domain_second_level = set()
        domain_1st_party = domains[0]
        domain_1st_party = hack_TLDs_mangle_TLD(domain_1st_party)
        domain_1st_party_second_level = ".".join(domain_1st_party.rsplit(".", 2)[-2:100000])
        for domain in domains[1:]:
            domain = domain.strip()
            domain = hack_TLDs_mangle_TLD(domain)
            if not domain:
                continue
            if "." not in domain:
                continue
            if domain == domain_1st_party:
                # if the domain requested itself, I don't care
                continue
            if domain.endswith("." + domain_1st_party):
                # if the domain requested itself, I don't care
                continue
            all_domains.add(domain)
            if not domain.endswith("." + domain_1st_party) and not domain == domain_1st_party:
                visited_domain.add(domain)
                all_3rd_party_domains.add(domain)
                # ignoring the problem of public suffixes (co.uk etc.)
                domain_second_level = ".".join(domain.rsplit(".", 2)[-2:100000])
                visited_domain_second_level.add(domain_second_level)
                all_3rd_party_second_level_domains.add(domain_second_level)

                if domain_second_level not in all_3rd_party_second_level_domains_mapping_to_subdomains:
                    all_3rd_party_second_level_domains_mapping_to_subdomains[domain_second_level] = set()
                all_3rd_party_second_level_domains_mapping_to_subdomains[domain_second_level].add(domain)

                if domain_second_level not in visited_3rd_party_second_level_domains_mapping_to_1st_party:
                    visited_3rd_party_second_level_domains_mapping_to_1st_party[domain_second_level] = set()
                visited_3rd_party_second_level_domains_mapping_to_1st_party[domain_second_level].add(domain_1st_party_second_level)
                
        visited_3rd_party_domains[domain_1st_party] = visited_domain
        visited_3rd_party_second_level_domains[domain_1st_party] = visited_domain_second_level


# 3rd party domain, number of 1st party domains that requested this 3rd party domain
stats_3rd_party_domains = []
stats_3rd_party_domains_dict_nums = {}
for domain_1st_party, visited in visited_3rd_party_domains.items():
    for visited_domain in visited:
        if visited_domain in stats_3rd_party_domains_dict_nums:
            stats_3rd_party_domains_dict_nums[visited_domain] += 1
        else:
            stats_3rd_party_domains_dict_nums[visited_domain] = 1
for domain_3rd_party_sought in all_3rd_party_domains:
    if domain_3rd_party_sought in stats_3rd_party_domains_dict_nums:
        stats_3rd_party_domains.append( (domain_3rd_party_sought, stats_3rd_party_domains_dict_nums[domain_3rd_party_sought]) )
stats_3rd_party_domains.sort(key=lambda x: x[1], reverse=True)


stats_3rd_party_second_level_domains = []
stats_3rd_party_second_level_domains_dict_nums = {}
for domain_1st_party, visited in visited_3rd_party_second_level_domains.items():
    for visited_domain in visited:
        if visited_domain in stats_3rd_party_second_level_domains_dict_nums:
            stats_3rd_party_second_level_domains_dict_nums[visited_domain] += 1
        else:
            stats_3rd_party_second_level_domains_dict_nums[visited_domain] = 1
for domain_3rd_party_sought in all_3rd_party_second_level_domains:
    if domain_3rd_party_sought in stats_3rd_party_second_level_domains_dict_nums:
        stats_3rd_party_second_level_domains.append( (domain_3rd_party_sought, stats_3rd_party_second_level_domains_dict_nums[domain_3rd_party_sought]) )
stats_3rd_party_second_level_domains.sort(key=lambda x: x[1], reverse=True)



domains_1st_party_that_loaded_enough_3rd_party_domains = set()
for domain_1st_party, visited_domains in visited_3rd_party_second_level_domains.items():
    if len(visited_domains) > MIN_INCLUDED_SUSPICIOUS:
        domains_1st_party_that_loaded_enough_3rd_party_domains.add(domain_1st_party)

keywords_suspicious_3rd_party_domains = ["tag", "count", "user", "email", "opt", "chart", "stats", "statis", "stat.", "ping", "click", "track", "ero", "data", "page", "reklam", "klik", "pocit", "check", "market", "lead", "reach", "affil", "platf", "yield", "engag", "media", "domain", "metric", "visit", ".ad", "ad.", "ads.", "adm.", "adn.", "adx.", "ad0.", "ad1.", "ad2.", "ad3.", "ad4.", "ad5.", "ad6.", "ad7.", "ad8.", "ad9.", ".ad", "advert", "push", "pixel", "pixl", "pxl", "anal", "impact", "see", "view" ]
keywords_beginning_suspicious_3rd_party_domains = ["ads", "adx", "adn", "advert"]
suspicious_3rd_party_domains = set()
for domain in all_3rd_party_domains:
    for keyword in keywords_suspicious_3rd_party_domains:
        if keyword in domain:
            suspicious_3rd_party_domains.add(domain)
    for keyword in keywords_beginning_suspicious_3rd_party_domains:
        if domain.startswith(keyword):
            suspicious_3rd_party_domains.add(domain)
# find all 1st party domains that loaded any of the suspicious 3rd party domains and add them to the list of 1st party domains that loaded enough 3rd party domains
for domain_1st_party, visited_domains in visited_3rd_party_domains.items():
    for visited_domain in visited_domains:
        if visited_domain in suspicious_3rd_party_domains:
            domains_1st_party_that_loaded_enough_3rd_party_domains.add(domain_1st_party)
# generate second level suspicious domains from the suspicious domains
suspicious_3rd_party_second_level_domains = set()
for domain_suspicious in suspicious_3rd_party_domains:
    domain_suspicious_second_level = ".".join(domain_suspicious.rsplit(".", 2)[-2:100000])
    suspicious_3rd_party_second_level_domains.add(domain_suspicious_second_level)

probably_tracking_3rd_party_second_level_domains = set()
for domain_1st_party in domains_1st_party_that_loaded_enough_3rd_party_domains:
    its_3rd_party_domains = set(visited_3rd_party_second_level_domains[domain_1st_party])
    probably_tracking_3rd_party_second_level_domains.update(its_3rd_party_domains)

# some of these have to be dealt manually on a subdomain basis (such as google.com, gstatic.com), some of them are false positives (such as github.io)
# it depends on personal taste where is your line between false and true positive
whitelist_second_level_domains = set(["google.com", "comodo.com", "akamai.net", "o2.cz", "mapy.cz", "stripe.network", "getpocket.com", "microsoft.com",
"s-microsoft.com", "akamaized.net", "typekit.com", "reddit.com", "stripe.com", "akamaihd.com", "googlecode.com", "windows.net", "imgur.com", "fontawesome.com", "appspot.com", "wp.com", "wordpress.com", "vimeo.com", "seznam.cz", "blogspot.cz", "blogspot.com", "github.io", "aspnetcdn.com", "vimeocdn.com", "blogger.com", "w.org", "jsdelivr.com", "jsdelivr.net", "t.co", "bing.com", "googleusercontent.com", "typekit.net", "twimg.com", "youtube.com", "ytimg.com", "jquery.com", "amazonaws.com", "cloudfront.net", "heureka.cz", "cloudflare.com", "bootstrapcdn.com", "twitter.com", "google.cz", "gstatic.com", "googleapis.com", "goo.gl", "szn.cz", "jquerytools.com", "adobetm.net", "adobetm.com", "steampowered.com", "steamstatic.com", "akamaihd.net", "pcworld.cz", "cz.", "com.", "virustotal.com", "nytimes.com", "muni.cz", "alza.cz", "penize.cz", "mathjax.org", 
"free.fr", "wikimedia.org", "googlepages.com", "ggpht.com", "cad.cz", "rozhlas.cz", "github.com", "jquerytools.com", "polyfill.io", "ifirmy.cz", "webnode.cz", "webnode.com", "sdk.azureedge.net", "dropboxusercontent.com", "dropbox.com", "githubusercontent.com",
"googlevideo.com", "youtube.cz", "googlevideo.cz", "youtube-nocookie.com", "giphy.com", "googledrive.com", 

])

# some domains are for ocsp https cert checking and similar stuff and we don't want to detect them as tracking domains (well, probably :D )
whitelist_subdomains_keywords = set(["ocsp"])
subdomains_matching_whitelist = set()
for domain in all_3rd_party_domains:
    for keyword in whitelist_subdomains_keywords:
        if keyword in domain:
            subdomains_matching_whitelist.add(domain)
# convert identified whitelisted subdomains into whitelisted second-level domains
for domain in probably_tracking_3rd_party_second_level_domains:
    for subdomain in subdomains_matching_whitelist:
        if subdomain.endswith("." + domain) or subdomain == domain:
            whitelist_second_level_domains.add(domain)

# apply whitelist
probably_tracking_3rd_party_second_level_domains -= whitelist_second_level_domains
    
# also whitelist non-suspicious domains that were included less than MIN_INCLUDED_SUSPICIOUS times (because else the data are too imprecise)
# also whitelist suspicious domains that were included less than MIN_INCLUDED_REPORT times (because else the data are too imprecise)
second_level_3rd_party_domains_that_were_included_n_or_more_times = set()
for domain_2nd_level, num_of_inclusions in stats_3rd_party_second_level_domains:
    if (
        (num_of_inclusions >= MIN_INCLUDED_SUSPICIOUS)
        or
        (num_of_inclusions >= MIN_INCLUDED_REPORT and domain_2nd_level in suspicious_3rd_party_second_level_domains)
    ):
        second_level_3rd_party_domains_that_were_included_n_or_more_times.add(domain_2nd_level)
probably_tracking_3rd_party_second_level_domains.intersection_update(second_level_3rd_party_domains_that_were_included_n_or_more_times)



# for user's overview
print("3rd party domains without subdomain merging and without ad/tracking detection")
print("-----------------------------------------------------------------------------\n")
for i in range(min(50000, len(stats_3rd_party_domains)-1)):
    print("{} {}".format(stats_3rd_party_domains[i][1], hack_TLDs_unmangle_TLD(stats_3rd_party_domains[i][0])))
print("\n")

# for user's overview of top-used 3rd party domains to aid decisions how to use the information for assembling a blocklist; not printing the 1st party domains so as not to be too long
print("3rd party second-level domains without ad/tracking detection")
print("------------------------------------------------------------\n")
for i in range(min(50000, len(stats_3rd_party_second_level_domains)-1)):
    print("{} {}".format(stats_3rd_party_second_level_domains[i][1], hack_TLDs_unmangle_TLD(stats_3rd_party_second_level_domains[i][0])))
    ending = stats_3rd_party_second_level_domains[i][0]
    # print all the individual 3rd party subdomains under this second-level domain
    if ending in all_3rd_party_second_level_domains:
        fulldomains = all_3rd_party_second_level_domains_mapping_to_subdomains[ending]
        for fulldomain in fulldomains:
            print("        {}".format(hack_TLDs_unmangle_TLD(fulldomain)))
    # # print 1st party domains from which these 3rd party domains were requested
    # for domain_1st_party, domains_3rd_party in visited_3rd_party_second_level_domains.items():
    #     if ending in domains_3rd_party: 
    #         print("  *    {}".format(domain_1st_party))
print("")

print("3rd party second-level domains that are probably ads/trackers")
print("-------------------------------------------------------------\n")
for i in range(min(50000, len(stats_3rd_party_second_level_domains)-1)):
    num_of_inclusions_in_1st_party_domains = stats_3rd_party_second_level_domains[i][1]
    second_level_3rd_party_domain = stats_3rd_party_second_level_domains[i][0]
    # we are printing only those detected as trackers
    if second_level_3rd_party_domain not in probably_tracking_3rd_party_second_level_domains:
        continue
    print("{} {}".format(num_of_inclusions_in_1st_party_domains, hack_TLDs_unmangle_TLD(second_level_3rd_party_domain)))
    # print all the individual 3rd party subdomains under this second-level domain
    if second_level_3rd_party_domain in all_3rd_party_second_level_domains:
        fulldomains = all_3rd_party_second_level_domains_mapping_to_subdomains[ending]
        for fulldomain in fulldomains:
            print("        {}".format(hack_TLDs_unmangle_TLD(fulldomain)))
    # print 1st party domains from which these 3rd party domains were requested
    for domain_1st_party_second_level in visited_3rd_party_second_level_domains_mapping_to_1st_party[second_level_3rd_party_domain]:
        print("  *    {}".format(hack_TLDs_unmangle_TLD(domain_1st_party_second_level)))
print("")



print("3rd party second-level domains that are probably ads/trackers - only the domains")
print("--------------------------------------------------------------------------------\n")
for i in range(min(50000, len(stats_3rd_party_second_level_domains)-1)):
    num_of_inclusions_in_1st_party_domains = stats_3rd_party_second_level_domains[i][1]
    second_level_3rd_party_domain = stats_3rd_party_second_level_domains[i][0]
    # we are printing only those detected as trackers
    if second_level_3rd_party_domain not in probably_tracking_3rd_party_second_level_domains:
        continue
    print("{}".format(hack_TLDs_unmangle_TLD(second_level_3rd_party_domain)))
print("")
