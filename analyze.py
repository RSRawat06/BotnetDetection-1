import time
import json
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
from netaddr import IPNetwork
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

    def feedData(self):
        es = Elasticsearch([{'host': 'bulika.eecs.utk.edu', 'port': 9200}])
        for i in es.indices.get("argus-live-*"):
            res = es.search(index=i, scroll = '2m', size = 1)
            sid = res['_scroll_id']
            scroll_size = res['hits']['total']
            
            count = 0
            print("Data for %s" % (i))
            while (scroll_size > 0):
            	count += 1
            	res = es.scroll(scroll_id = sid, scroll = '2m')
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
                        self.findIP('d', dst, src)
                    elif src.find(":") == -1:
                        self.findIP('s', src, dst)
                    
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
							if direction == 'd':
                                print("%s connecting with malicious IP %s" % (ip, connectionip))
                                #print()
                            else:
                                print("malicious IP %s connecting with %s" % (ip, connectionip))                    
                                #print()
                            #print("{0} detected as a malicious IP".format(ip)
            if firstip[0] > ip[0]:
            	break
            
def main():
    I = IPFinder()
    I.feedData()

if __name__ == '__main__':
    main()
	
