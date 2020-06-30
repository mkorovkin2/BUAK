import dns.resolver
import base64
from alive_progress import alive_bar
import sys
import datetime
import os

filename = str(sys.argv[1])
out = "{0}_{2}{1}".format(*os.path.splitext("successes.txt") + (str(datetime.datetime.now().time()),))

def output():
    with open(out, 'w') as filehandle:
        filehandle.write("\n".join(successes))

nameservers_file = open("nameservers.txt", "r")
nameservers = nameservers_file.read().split("\n")
nameservers_file.close()

cache = dns.resolver.Resolver(configure=False)
cache.timeout = 2
cache.lifetime = 2
result = None

successes = []

print("Caching each record (this may take a few minutes): ")
count = 0
for nameserver in nameservers:
    count += 1
    if count % 25 == 0:
        output()
    cache.nameservers = [nameserver]
    if cache.cache != None:
        cache.cache.flush()
    try:
        subdomainCount = int(cache.resolve(filename + ".txt.txtrecords.dev", "TXT")[0].strings[0])
        with alive_bar(subdomainCount) as bar:
            for i in range(subdomainCount):
                result = cache.resolve(str(i) + "." + filename + ".txt.txtrecords.dev", "TXT")
                bar()
        print("success: " + nameserver)
        successes.append(nameserver)
    except Exception as e:
        print("failed: " + nameserver)
        result = None
