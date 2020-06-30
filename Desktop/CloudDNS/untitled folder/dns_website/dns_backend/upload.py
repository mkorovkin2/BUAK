from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import base64
import sys
import dns.resolver
from alive_progress import alive_bar
import time
import json
import hashlib
import os
from threading import Thread

class Upload:
    def __init__(self, ttl=2147483647, n=10):
        #this is google api stuff
        self.ttl = ttl
        self.n = n
        credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build("dns", "v1", credentials=credentials)
        self.project = "dnstxt"
        self.managed_zone = "txt"
        self.nameservers_file = open("dns_backend/nameservers.txt", "r")
        self.nameservers_all = self.nameservers_file.read().split("\n")

    #adds the provided record to the list
    def add_record(self, texts, text, count):
        texts.append(str(count) + " " + text)

    #sends the change request to the name server and stores it in the json dict
    def sendChange(self, change_body_add, json_dump, save = True):
        request = self.service.changes().create(project=self.project, managedZone=self.managed_zone, body=change_body_add)
        response = request.execute()
        if save:
            json_dump["additions"].append(change_body_add["additions"])

    def uploadFromPath(self, path):
        if os.path.isdir(path): #if path is a folder
            for f in os.listdir(path):
                self.upload(os.path.join(path, f))
            return
        else:
            filename = path
        # value for key, value in variable}#set the self.ttl to command line arg, otherwise 10min
        in_file = open(filename, "rb")
        return uploadFromFile(in_file, in_file.name)

    def uploadFromFile(self, in_file, filename):
        data = in_file.read()
        in_file.close()
        chunk_size = 180 # chunk size (chars per TXT record)
        #split the data from the file into chunks and encode them in base64
        chunks = [base64.b64encode(data[i:i+chunk_size]).decode("utf-8") for i in range(0, len(data), chunk_size)]

        #used to save the record data for later removal
        json_dump = {
          "additions": []
        }

        count = 0
        subdomainCount = 0
        print("Uploading " + filename + ": ")

        change_body_add = {
          "additions": []
        }

        with alive_bar(len(chunks)) as bar:
            while count < len(chunks):
                texts = []
                while count < len(chunks):
                    #need to create a new record set every 40 records or so since they can't be more than 100,000 bytes
                    if (count + 1) % 40 == 0:
                        bar()
                        self.add_record(texts, chunks[count], count)
                        count += 1
                        break
                    bar()
                    self.add_record(texts, chunks[count], count)
                    count += 1

                #create a new record set
                change_body_add["additions"].append({
                  "type": "TXT",
                  "rrdatas": texts,
                  "name": str(subdomainCount) + "." + filename + ".txt.txtrecords.dev.",
                  "self.ttl": self.ttl
                })
                #need to send the changes every 400 records or the request exceeds the quota
                if count % 400 == 0:
                    sendChange(change_body_add, json_dump)
                    change_body_add = {
                      "additions": []
                    }
                subdomainCount += 1

        #add the count record
        change_body_add["additions"].append({
          "type": "TXT",
          "rrdatas": str(subdomainCount),
          "name": filename + ".txt.txtrecords.dev.",
          "self.ttl": self.ttl
        })
        self.sendChange(change_body_add, json_dump)
        with open(filename.replace("/", "_") + ".json", "w") as outfile:
            json.dump(json_dump["additions"], outfile)
        return len(chunks)

    def cacheFromPath(self, path):
        if os.path.isdir(path): #if path is a folder
            for f in os.listdir(path):
                self.cache(os.path.join(path, f))
            return
        else:
            filename = path
        cacheFromFile(filename)

    def cacheFromFile(self, filename):
        hash = int(hashlib.sha256(filename.encode("utf-8")).hexdigest(), 16) % 10**8
        nameservers = [self.nameservers_all[(hash + (i * self.n)) % len(self.nameservers_all)] for i in range(self.n)]

        serv = dns.resolver.Resolver(configure=False)
        serv.timeout = 2
        serv.lifetime = 2
        result = None

        for nameserver in nameservers:
            serv.nameservers = [nameserver]
            if serv.cache != None:
                serv.cache.flush()
            try:
                print(nameserver + ":")
                subdomainCount = int(serv.resolve(filename + ".txt.txtrecords.dev", "TXT")[0].strings[0])
                with alive_bar(subdomainCount) as bar:
                    for i in range(subdomainCount):
                        result = serv.resolve(str(i) + "." + filename + ".txt.txtrecords.dev", "TXT")
                        bar()
                print("success.")
            except Exception as e:
                print("failure: " + str(e))
                result = None

        print("Removing records from authoritative server... ")
        with open(filename.replace("/", "_") + ".json") as json_file:
            data = json.load(json_file)
            change_body_remove = {"deletions": [data]}
            request = self.service.changes().create(project=self.project, managedZone=self.managed_zone, body=change_body_remove)
            response = request.execute()
        os.remove(filename.replace("/", "_") + ".json")
        print("Done.")

    def saveFromFile(self, file, filename):
        txt_count = self.uploadFromFile(file, filename)
        thread = Thread(target = self.waitThenCacheFromFile, args = (filename,))
        thread.start()
        self.nameservers_file.close()
        return txt_count

    def saveFromPath(self, path):
        self.uploadFromPath(path)
        print("Caching records (this may take a few minutes): ")
        time.sleep(60)
        self.cacheFromPath(path)
        self.nameservers_file.close()

    def waitThenCacheFromFile(self, filename):
        print("Caching records (this may take a few minutes): ")
        time.sleep(60)
        self.cacheFromFile(filename)
