import time
import json
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
from netaddr import IPNetwork
import pandas as pd
import json
import sys

class IPFinder:
    def __init__(self):
        iplist = open("iplist.txt").read().strip().split("\n")

        self.firstIP, self.lastIP = [], []
        for line in iplist:
            slashLoc = line.find("/")
            if slashLoc != -1:
                self.firstIP.append(line[:slashLoc])
            else:
                self.firstIP.append(line)
                self.lastIP.append(str(IPNetwork(line)[-1]))
        
        self.botnetCount = 1
        self.normalCount = 1
        self.reachCount = 1000
        self.netList = []

    def feedData(self):
        es = Elasticsearch([{'host': 'bulika.eecs.utk.edu', 'port': 9200}])
        with open('out.csv', 'w+') as outFile:
            for i in es.indices.get("argus-live-*"):
                if self.botnetCount > 1000 and self.normalCount > 1000:
                    print("Found {0} botnets and {1} normals".format(self.botnetCount, self.normalCount))
                    self.createCSV()
                    sys.exit(1)
                
                res = es.search(index=i, scroll = '2m', size = 1)
                sid = res['_scroll_id']
                scroll_size = res['hits']['total']
                
                count = 0
                print("Data for %s" % (i))
                while (scroll_size > 0):
                    count += 1
                    res = es.scroll(scroll_id = sid, scroll = '2m')

                    if self.botnetCount > 1000 and self.normalCount > 1000:
                        print("Found {0} botnets and {1} normals".format(self.botnetCount, self.normalCount))
                        self.createCSV()
                        sys.exit(1)
                    elif res['hits']['hits'][0]['_source']['doc']['dst']['security'] != ['B']\
                        and res['hits']['hits'][0]['_source']['doc']['src']['security'] != ['B']\
                        and self.normalCount <= 1000:
                        print(" Found normal #{0}".format(self.normalCount))
                        self.normalCount += 1
                        res['security'] = 0
                        self.netList.append(res)

                    sid = res['_scroll_id']
                    scroll_size = len(res['hits']['hits'])
                    #print(json.dumps(res, indent = 4))
                    #print(json.dumps(res['hits']['hits'][0], indent = 4))
                    #print("IP is %d" % (res['hits']['hits'][0]['_source']['doc']))
                    s = res['hits']['hits'][0]['_source']['doc']
                    dst = s['dst']['ip']
                    src = s['src']['ip']
            
                    try:
                        # print("Destination IP is %s " % (dst));
                        # print("Source IP is %s " % (src));
                        # TODO: Handle IPv6
                        if dst.find(":") == -1:
                            findDst = self.findIP('d', dst, src)
                        if src.find(":") == -1:
                            findSrc = self.findIP('s', src, dst)
                        if findDst and findSrc and self.botnetCount <= 1000:
                            print("\tFound botnet #{0}".format(self.botnetCount))
                            self.botnetCount += 1
                            res['security'] = 1
                            self.netList.append(res)
                        
                    except IndexError:
                        break
            
                print("Data for %s" % (i))
                print("%d connections read" % (count))
        
    # TODO: Distinguish between source/destination IPs (print differently)
    def findIP(self, direction, ip, connectionip):
        ip = [int(x) for x in ip.split(".")]
        
        for tmp in zip(self.firstIP, self.lastIP):
            firstip = [int(x) for x in tmp[0].split(".")]
            lastip = [int(x) for x in tmp[1].split(".")]
            
            if ip[0] >= firstip[0] and ip[0] <= lastip[0]:
                if ip[1] >= firstip[1] and ip[1] <= lastip[1]:
                    if ip[2] >= firstip[2] and ip[2] <= lastip[2]:
                        if ip[3] >= firstip[3] and ip[3] <= lastip[3]:
                            # if direction == 'd':
                            #     print("%s connecting with malicious IP %s" % (ip, connectionip))
                            # else:
                            #     print("malicious IP %s connecting with %s" % (ip, connectionip))   
                            return True

                            
            if firstip[0] > ip[0]:
            	break
        
        return False

    def createCSV(self):
        print("Writing to CSV")
        with open('out.csv', 'w+') as outFile:
            outFile.write(
                "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23},{24},{24},{25}\n"\
                .format(
                    'appbytes',
                    'bytes',
                    'count',
                    'dstbytes',
                    'dstload',
                    'dstport',
                    'dstrate',
                    'duration',
                    'hops',
                    'intpkt',
                    'jitter',
                    'loss',
                    'maxsize',
                    'meansize',
                    'minsize',
                    'packets',
                    'pcr',
                    'ploss',
                    'protocol',
                    'rate',
                    'rtt',
                    'srcbytes',
                    'srcload',
                    'srcport',
                    'srcrate',
                    'security'
                )
            )
            print("Size =", len(self.netList))
            for r in self.netList:
                doc = r['hits']['hits'][0]['_source']['doc']
                outFile.write(
                    "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23},{24},{24},{25}\n"\
                    .format(
                        doc['appbytes'],
                        doc['bytes'],
                        doc['count'],
                        doc['dst']['bytes'],
                        doc['dst']['load'],
                        doc['dst']['port'],
                        doc['dst']['rate'],
                        doc['duration'],
                        doc['hops'],
                        doc['intpkt'],
                        doc['jitter'],
                        doc['loss'],
                        doc['maxsize'],
                        doc['meansize'],
                        doc['minsize'],
                        doc['packets'],
                        doc['pcr'],
                        doc['ploss'],
                        doc['protocol'],
                        doc['rate'],
                        doc['rtt'],
                        doc['src']['bytes'],
                        doc['src']['load'],
                        doc['src']['port'],
                        doc['src']['rate'],
                        r['security']
                    )
                )

        return 0
            
def main():
    I = IPFinder()
    I.feedData()

if __name__ == '__main__':
    main()
	
