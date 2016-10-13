#python 3

"""

	ip_geolocator takes and ip address and can return latitude/longitude, city, country, zip
	#makes get rquest to http://freegeoip.net/json/{ip}

	use:
		import ip_geolocator

		ip = '76.184.50.213'
		l = ip_geolocator.Location(ip)
		lat = l.latitude

"""
import urllib
from urllib.request import urlopen  
import json

class Location( object ):

	def __init__(self, ip):
		url = "http://freegeoip.net/json/" + ip

		opener = urllib.request.URLopener() #default (proxies=None)
		opener.version = "Chrome/53.0.2785.116" #version Python-urllib/3.5 gets 999

		try:
			response = opener.open(url) #request, "get" by defualt 
			if response.getheader('Content-Type')=='application/json':
				#decoder
				data = response.read()
				json_string = data.decode("utf-8")
				location_dict = json.loads(json_string)

				#extract attributes
				self.ip =  location_dict['ip']
				self.latitude =  location_dict['latitude']
				self.longitude =  location_dict['longitude']
				self.zip_code =  location_dict['zip_code']
				self.city =  location_dict['city']
				self.region_code =  location_dict['region_code']
				self.country_code = location_dict['country_code']

				
		except Exception as e: 
			print("\trequest error: %s\n" % e)

	def to_json_string(self):
		json_dict = {}
		try:

			json_dict["latitude"] = self.latitude
			json_dict["longitude"] = self.longitude
			json_dict["zip_code"] = self.zip_code
			json_dict["city"] = self.city
			json_dict["region_code"] = self.region_code
			json_dict["country_code"] = self.country_code
		except Exception as e: 
			print("\nfile:ip_geolocator\nfunc:to_json_string\n\tno location: %s\n" % e)

		return json_dict