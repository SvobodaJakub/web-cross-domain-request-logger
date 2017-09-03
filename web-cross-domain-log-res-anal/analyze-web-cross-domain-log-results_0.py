# analyses 3rd party domains in a dumb fashion
# * any string different than the visited domain is considered 3rd party, so even
#   img.example.com for visited www.example.com which makes the stats useless
# * 1.xx.example.com and 2.xx.example.com are considered different domains - no merging beyond
#   certain depth
import sys
all_domains = set()
all_3rd_party_domains = set()
visited_domains = {}
with open(sys.argv[1]) as fp:
    for line in fp:
        line = line.strip()
        if not line:
            continue
        domains = line.split(";")
        visited_domain = set()
        for domain in domains[1:]:
            domain = domain.strip()
            if not domain:
                continue
            if "." not in domain:
                continue
            if domain == domains[0]:
                # if the domain requested itself, I don't care
                continue
            visited_domain.add(domain)
            all_domains.add(domain)
            all_3rd_party_domains.add(domain)
        visited_domains[domains[0]] = visited_domain

# print("all_domains")
# print(repr(all_domains))
# print("")
#
# print("all_3rd_party_domains")
# print(repr(all_3rd_party_domains))
# print("")
#
# print("visited_domains")
# print(repr(visited_domains))
# print("")

# 3rd party domain, number of 1st party domains that requested this 3rd party domain
stats_3rd_party_domains = []

for domain_3rd_party_sought in all_3rd_party_domains:
    requested_times = 0
    for domain_1st_party, visited in visited_domains.items():
        for visited_domain in visited:
            if visited_domain == domain_3rd_party_sought:
                requested_times += 1
    stats_3rd_party_domains.append( (domain_3rd_party_sought, requested_times) )

stats_3rd_party_domains.sort(key=lambda x: x[1], reverse=True)

for i in range(max(100, len(stats_3rd_party_domains))):
    print("{} {}".format(stats_3rd_party_domains[i][1], stats_3rd_party_domains[i][0]))

