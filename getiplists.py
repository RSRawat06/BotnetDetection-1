from bs4 import BeautifulSoup
from netaddr import IPNetwork
import urllib3

http = urllib3.PoolManager()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urls = ["https://iplists.firehol.org/files/feodo.ipset"]

url = "https://iplists.firehol.org/files/firehol_level1.netset"
response = http.request('GET', url)
soup = BeautifulSoup(response.data, features="html.parser").prettify()

soup = soup.split("\n")

with open("iplist.txt", "w+") as outFile:
	for line in soup:
		if len(line) == 0 or line[0] == "#":
		 	continue
		outFile.write("{0}\n".format(line))
