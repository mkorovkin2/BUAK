import dns.resolver
import base64
from alive_progress import alive_bar
import sys
import datetime
import os
import random
import hashlib

class Download():
    def __init__(self, n=10):
        self.n = n
        self.nameservers_file = open("dns_backend/nameservers.txt", "r")
        self.nameservers_all = self.nameservers_file.read().split("\n")
        self.serv = dns.resolver.Resolver(configure=False)
        #denmark: 89.233.43.71

    def append_id(self, filename):
      return "{0}_{2}{1}".format(*os.path.splitext(filename) + (str(datetime.datetime.now().time()),))

    def downloadFromPath(path):
        if os.path.isdir(path): #if path is a folder
            if not os.path.exists(path):
                os.makedirs(path)
            for f in os.listdir(path):
                self.download(os.path.join(path, f))
            return
        else:
            filename = path
        downloadFromFile(filename)

    def downloadFromFile(self, filename):
        print("Downloading " + filename + ": ")
        hash = int(hashlib.sha256(filename.encode("utf-8")).hexdigest(), 16) % 10**8
        nameservers = [self.nameservers_all[(hash + (i * self.n)) % len(self.nameservers_all)] for i in range(self.n)]

        self.serv = dns.resolver.Resolver(configure=False)
        self.serv.timeout = 2
        self.serv.lifetime = 2
        result = None

        for nameserver in nameservers:
            results = []
            self.serv.nameservers = [nameserver]
            if self.serv.cache != None:
                self.serv.cache.flush()
            print("Attempting to get file from: " + nameserver)
            try:
                subdomainCount = int(self.serv.resolve(filename + ".txt.txtrecords.dev", "TXT")[0].strings[0])
                with alive_bar(subdomainCount) as bar:
                    for i in range(subdomainCount):
                        result = self.serv.resolve(str(i) + "." + filename + ".txt.txtrecords.dev", "TXT")
                        results.extend([None] * len(result))
                        for data in result:
                            results[int(data.strings[0].decode("utf-8"))] = data.strings[1]
                        bar()
                    print("Success.")
                    break
            except Exception as e:
                print("Failure: " + str(e))

        print("Recompiling file from records: ")
        with alive_bar(len(results)) as bar:
            out = b""
            for b in results:
                out += base64.b64decode(b)
                bar()

        print("Done.")
        if len(out) == 0:
            return None
        self.nameservers_file.close()
        with open(filename, 'wb') as f:
            f.write(out)
        f_out = open(filename, 'rb')
        return f_out

    def download_all(self, path):
        return self.downloadFromFile(path)
