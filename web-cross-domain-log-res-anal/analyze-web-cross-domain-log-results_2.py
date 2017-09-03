# analyses 3rd party domains
# * only requests outside the originating second-level domain are considered 3rd-party
#   (example: b.com or x.y.b.com are 3rd party to the originating a.com; x.a.com is 1st party)
# * the originating domains are always considered to be second-level domain
#     * because of public suffixes that contain dots and any logic would make it less correct
#     * because the visited domains are sourced from a list of top n _domains_
import sys
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
        for domain in domains[1:]:
            domain = domain.strip()
            if not domain:
                continue
            if "." not in domain:
                continue
            if domain == domains[0]:
                # if the domain requested itself, I don't care
                continue
            all_domains.add(domain)
            if not domain.endswith(domains[0]):
                visited_domain.add(domain)
                all_3rd_party_domains.add(domain)
                # ignoring the problem of public suffixes (co.uk etc.)
                domain_second_level = ".".join(domain.rsplit(".", 2)[-2:100000])
                visited_domain_second_level.add(domain_second_level)
                all_3rd_party_second_level_domains.add(domain_second_level)
        visited_3rd_party_domains[domains[0]] = visited_domain
        visited_3rd_party_second_level_domains[domains[0]] = visited_domain_second_level

# print("all_domains")
# print(repr(all_domains))
# print("")
#
# print("all_3rd_party_domains")
# print(repr(all_3rd_party_domains))
# print("")
#
# print("visited_3rd_party_domains")
# print(repr(visited_3rd_party_domains))
# print("")

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


print("3rd party domains without subdomain merging")
print("-------------------------------------------\n")
for i in range(min(200, len(stats_3rd_party_domains)-1)):
    print("{} {}".format(stats_3rd_party_domains[i][1], stats_3rd_party_domains[i][0]))
print("\n")

print("3rd party second-level domains")
print("------------------------------\n")
for i in range(min(1000, len(stats_3rd_party_second_level_domains)-1)):
    print("{} {}".format(stats_3rd_party_second_level_domains[i][1], stats_3rd_party_second_level_domains[i][0]))
    ending = stats_3rd_party_second_level_domains[i][0]
    # print all the individual 3rd party subdomains under this second-level domain
    for fulldomain in all_3rd_party_domains:
        if fulldomain.endswith("." + ending) or fulldomain == ending:
            print("        {}".format(fulldomain))
    # print 1st party domains from which these 3rd party domains were requested
    for domain_1st_party, domains_3rd_party in visited_3rd_party_second_level_domains.items():
        if ending in domains_3rd_party: 
            print("  *    {}".format(domain_1st_party))
print("")


