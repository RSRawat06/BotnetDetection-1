from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()

urls = ["https://iplists.firehol.org/files/feodo.ipset", ]

url = "https://iplists.firehol.org/files/firehol_level1.netset"
response = http.request('GET', url)
soup = BeautifulSoup(response.data)

print(soup)
