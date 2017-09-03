# analyses 3rd party domains
# * only requests outside the originating second-level domain are considered 3rd-party
#   (example: b.com or x.y.b.com are 3rd party to the originating a.com; x.a.com is 1st party)
# * the originating domains are always considered to be second-level domain
#     * because of public suffixes that contain dots and any logic would make it less correct
#     * because the visited domains are sourced from a list of top n _domains_
# * performs detection of probable ad/tracking domains
#     * if a given 1st party domain makes requests to 3rd party domains that fall under more than 2 second-level 3rd party domains, then such a 1st party domain probably includes interesting trackers and all its 3rd party requests are taken as probable trackers
#     * 3rd party domains that include a suspicious keyword are taken as probable trackers
#     * some domains are whitelisted
import sys

hack_TLDs_with_dot = ["co.uk", "com.cn"]
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
            if not domain.endswith(domain_1st_party):
                visited_domain.add(domain)
                all_3rd_party_domains.add(domain)
                # ignoring the problem of public suffixes (co.uk etc.)
                domain_second_level = ".".join(domain.rsplit(".", 2)[-2:100000])
                visited_domain_second_level.add(domain_second_level)
                all_3rd_party_second_level_domains.add(domain_second_level)
        visited_3rd_party_domains[domain_1st_party] = visited_domain
        visited_3rd_party_second_level_domains[domain_1st_party] = visited_domain_second_level

# 3rd party domain, number of 1st party domains that requested this 3rd party domain
stats_3rd_party_domains = []
for domain_3rd_party_sought in all_3rd_party_domains:
    requested_times = 0
    for domain_1st_party, visited in visited_3rd_party_domains.items():
        for visited_domain in visited:
            if visited_domain == domain_3rd_party_sought:
                requested_times += 1
    stats_3rd_party_domains.append( (domain_3rd_party_sought, requested_times) )
stats_3rd_party_domains.sort(key=lambda x: x[1], reverse=True)

stats_3rd_party_second_level_domains = []
for domain_3rd_party_sought in all_3rd_party_second_level_domains:
    requested_times = 0
    for domain_1st_party, visited in visited_3rd_party_second_level_domains.items():
        for visited_domain in visited:
            if visited_domain == domain_3rd_party_sought:
                requested_times += 1
    stats_3rd_party_second_level_domains.append( (domain_3rd_party_sought, requested_times) )
stats_3rd_party_second_level_domains.sort(key=lambda x: x[1], reverse=True)


domains_1st_party_that_loaded_enough_3rd_party_domains = set()
for domain_1st_party, visited_domains in visited_3rd_party_second_level_domains.items():
    if len(visited_domains) > 2:
        domains_1st_party_that_loaded_enough_3rd_party_domains.add(domain_1st_party)

keywords_suspicious_3rd_party_domains = ["tag", "count", "user", "email", "opt", "chart", "stat", "ping", "click", "track", "ero", "data", "page", "reklam", "klik", "pocit", "check", "market", "lead", "reach", "affil", "platf", "yield", "engag", "media", "domain", "metric", "visit", ".ad", "ad.", "ads.", "adm.", "adn.", "adx.", "ad0.", "ad1.", "ad2.", "ad3.", "ad4.", "ad5.", "ad6.", "ad7.", "ad8.", "ad9.", ".ad", "advert", "anal", "pixel", "pxl", "impact", "see", "view"  ]
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

probably_tracking_3rd_party_second_level_domains = set()
for domain_1st_party in domains_1st_party_that_loaded_enough_3rd_party_domains:
    its_3rd_party_domains = set(visited_3rd_party_second_level_domains[domain_1st_party])
    probably_tracking_3rd_party_second_level_domains.update(its_3rd_party_domains)

# some of these have to be dealt manually on a subdomain basis (such as google.com), some of them are false positives (such as github.io)
# it depends on personal taste where is your line between false and true positive
whitelist_second_level_domains = set(["google.com", "comodo.com", "akamai.net", "o2.cz", "mapy.cz", "stripe.network", "getpocket.com", "microsoft.com",
"s-microsoft.com", "akamaized.net", "typekit.com", "reddit.com", "stripe.com", "akamaihd.com", "googlecode.com", "windows.net", "imgur.com", "fontawesome.com", "appspot.com", "wp.com", "wordpress.com", "vimeo.com", "seznam.cz", "blogspot.cz", "blogspot.com", "github.io", "aspnetcdn.com", "vimeocdn.com", "blogger.com", "w.org", "jsdelivr.com", "t.co", "bing.com", "googleusercontent.com", "typekit.net", "twimg.com", "youtube.com", "ytimg.com", "jquery.com", "amazonaws.com", "cloudfront.net", "heureka.cz", "cloudflare.com", "bootstrapcdn.com", "twitter.com", "google.cz", "gstatic.com", "googleapis.com", "mathjax.org", 
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
    
# also whitelist domains that were included less than 2 times (because then the data are too imprecise)
second_level_3rd_party_domains_that_were_included_2_or_more_times = set()
for domain_2nd_level, num_of_inclusions in stats_3rd_party_second_level_domains:
    if num_of_inclusions >= 2:
        second_level_3rd_party_domains_that_were_included_2_or_more_times.add(domain_2nd_level)

probably_tracking_3rd_party_second_level_domains.intersection_update(second_level_3rd_party_domains_that_were_included_2_or_more_times)


# for user's overview
print("3rd party domains without subdomain merging and without ad/tracking detection")
print("-----------------------------------------------------------------------------\n")
for i in range(min(200, len(stats_3rd_party_domains)-1)):
    print("{} {}".format(stats_3rd_party_domains[i][1], hack_TLDs_unmangle_TLD(stats_3rd_party_domains[i][0])))
print("\n")

# for user's overview of top-used 3rd party domains to aid decisions how to use the information for assembling a blocklist; not printing the 1st party domains so as not to be too long
print("3rd party second-level domains without ad/tracking detection")
print("------------------------------------------------------------\n")
for i in range(min(200, len(stats_3rd_party_second_level_domains)-1)):
    print("{} {}".format(stats_3rd_party_second_level_domains[i][1], hack_TLDs_unmangle_TLD(stats_3rd_party_second_level_domains[i][0])))
    ending = stats_3rd_party_second_level_domains[i][0]
    # print all the individual 3rd party subdomains under this second-level domain
    for fulldomain in all_3rd_party_domains:
        if fulldomain.endswith("." + ending) or fulldomain == ending:
            print("        {}".format(hack_TLDs_unmangle_TLD(fulldomain)))
    # # print 1st party domains from which these 3rd party domains were requested
    # for domain_1st_party, domains_3rd_party in visited_3rd_party_second_level_domains.items():
    #     if ending in domains_3rd_party: 
    #         print("  *    {}".format(domain_1st_party))
print("")

print("3rd party second-level domains that are probably ads/trackers")
print("-------------------------------------------------------------\n")
for i in range(min(1000, len(stats_3rd_party_second_level_domains)-1)):
    num_of_inclusions_in_1st_party_domains = stats_3rd_party_second_level_domains[i][1]
    second_level_3rd_party_subdomain = stats_3rd_party_second_level_domains[i][0]
    # we are printing only those detected as trackers
    if second_level_3rd_party_subdomain not in probably_tracking_3rd_party_second_level_domains:
        continue
    print("{} {}".format(num_of_inclusions_in_1st_party_domains, hack_TLDs_unmangle_TLD(second_level_3rd_party_subdomain)))
    # print all the individual 3rd party subdomains under this second-level domain
    for fulldomain in all_3rd_party_domains:
        if fulldomain.endswith("." + second_level_3rd_party_subdomain) or fulldomain == second_level_3rd_party_subdomain:
            print("        {}".format(hack_TLDs_unmangle_TLD(fulldomain)))
    # print 1st party domains from which these 3rd party domains were requested
    for domain_1st_party, domains_3rd_party in visited_3rd_party_second_level_domains.items():
        if second_level_3rd_party_subdomain in domains_3rd_party: 
            print("  *    {}".format(hack_TLDs_unmangle_TLD(domain_1st_party)))
print("")



print("3rd party second-level domains that are probably ads/trackers - only the domains")
print("--------------------------------------------------------------------------------\n")
for i in range(min(1000, len(stats_3rd_party_second_level_domains)-1)):
    num_of_inclusions_in_1st_party_domains = stats_3rd_party_second_level_domains[i][1]
    second_level_3rd_party_subdomain = stats_3rd_party_second_level_domains[i][0]
    # we are printing only those detected as trackers
    if second_level_3rd_party_subdomain not in probably_tracking_3rd_party_second_level_domains:
        continue
    print("{}".format(hack_TLDs_unmangle_TLD(second_level_3rd_party_subdomain)))
print("")
