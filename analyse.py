import dpkt
from scapy.all import *
import pygeoip
import pandas as pd
import socket

gi = pygeoip.GeoIP('GeoLiteCity.dat')
x = pd.DataFrame(columns=['City','Region','Country','lat','lon'])

def printRecord(tgt):
	global x
	rec = gi.record_by_name(tgt)
	city = rec['city']
	region = rec['region_name']
	country = rec['country_name']
	lon = rec['longitude']
	lat = rec['latitude']
	x = x.append({'City': str(city),
				'Region': str(region),
				'Country': str(country),
				'lat': str(lat),
				'lon': str(lon)
				}, ignore_index=True)

	x.to_csv("test.csv",index=False)

def printPcap(pkts):
	for each in pkts:
		try:
			ip_addr = each.getlayer('IP').dst
			print ip_addr, socket.gethostbyaddr("tgt")
			printRecord(ip_addr)
		except Exception, e:
			print e
			pass

if __name__ == '__main__':
	#f = open('test.pcap')
	while True:
		pkts = sniff(filter='tcp',count=100)
		printPcap(pkts)