#	Python utils to remote control BrovoTech h265/h265 HDMI Encoder
# 	Work in progress...
#   	rob@m0dts.co.uk 
# 	14/10/2020
# 
# 	requirements: apt-get install python-pil python-xmltodict python-requests
# 
# 

import requests
import time
from PIL import Image,ImageDraw,ImageFont
import xmltodict


class encoder:
	def __init__(self,_encoderIP,_streamname,_streamkey):
		self.encoderIP = _encoderIP
		self.xml_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
		self.fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
		self.streamname = _streamname
		self.streamkey = _streamkey
		self.logopath='/home/pi/'


	##################
	#
	#	UDP OUTPUT RESTART - can be handy at power up if pluto does not start transmitting
	#

	def restartUDP(self):
		try:
			xml= requests.post('http://'+self.encoderIP+'/action/get?subject=multicast', auth=('admin', '12345'),timeout=2).text
		except:
			return "Error with request"
		xmldict= xmltodict.parse(xml)
		xmldict['response']['multicast']['mcast'][0]['active']="0"
		xml_data = xmltodict.unparse(xmldict)
		try:
			requests.post('http://'+self.encoderIP+'/action/set?subject=multicast', data=xml_data, headers=self.xml_headers, auth=('admin', '12345'),timeout=2).text
		except:
			return "Error with request"
		time.sleep(2)
		xmldict['response']['multicast']['mcast'][0]['active']="1"
		xml_data = xmltodict.unparse(xmldict)
		try:
			requests.post('http://'+self.encoderIP+'/action/set?subject=multicast', data=xml_data, headers=self.xml_headers, auth=('admin', '12345'),timeout=2).text
		except:
			return "Error with request"
	#
	#
	#	
	##########	


	##################
	#
	#	RTMP STREAMING
	#
	def streaming(self,state):
		
		try:
			xml= requests.post('http://'+self.encoderIP+'/action/get?subject=rtmp', auth=('admin', '12345'),timeout=2).text
		except:
			return "Error with request"
		#print xml
		xmldict= xmltodict.parse(xml)

		if state=="OFF":
			xmldict['response']['rtmp']['push'][0]['active']="0"
			xmldict['response']['rtmp']['push'][1]['active']="0"
			xmldict['response']['rtmp']['push'][2]['active']="0"
			xml_data = xmltodict.unparse(xmldict)
			try:
				requests.post('http://'+self.encoderIP+'/action/set?subject=rtmp', data=xml_data, headers=self.xml_headers, auth=('admin', '12345'),timeout=2).text
			except:
				print "Error Setting Streaming..."

		if state=="SD":
			xmldict['response']['rtmp']['push'][0]['active']="0"
			xmldict['response']['rtmp']['push'][1]['active']="1"
			xmldict['response']['rtmp']['push'][2]['active']="0"
			xml_data = xmltodict.unparse(xmldict)
			try:
				requests.post('http://'+self.encoderIP+'/action/set?subject=rtmp', data=xml_data, headers=self.xml_headers, auth=('admin', '12345'),timeout=2).text
			except:
				print "Error Setting Streaming..."

		if state=="HD":
			xmldict['response']['rtmp']['push'][0]['active']="1"
			xmldict['response']['rtmp']['push'][1]['active']="0"
			xmldict['response']['rtmp']['push'][2]['active']="0"
			xml_data = xmltodict.unparse(xmldict)
			try:
				requests.post('http://'+self.encoderIP+'/action/set?subject=rtmp', data=xml_data, headers=self.xml_headers, auth=('admin', '12345'),timeout=2).text
			except:
				print "Error Setting Streaming..."


	def set_streaming_source(self):
		try:
			xml= requests.post('http://'+self.encoderIP+'/action/get?subject=videoenc&stream=1', auth=('admin', '12345'),timeout=2).text
		except:
			return "Error with request"
		#print xml
		xmldict= xmltodict.parse(xml)
		xmldict['response']['videoenc']['codec']="0"	#h264
		xmldict['response']['videoenc']['resolution']="1280x720"
		xmldict['response']['videoenc']['frmerate']="15"
		xmldict['response']['videoenc']['keygop']="30"
		xmldict['response']['videoenc']['rc']="0"	#vbr
		xmldict['response']['videoenc']['bitrate']="400"
		#xmldict['response']['videoenc']['smartenc']="0"	#what is this?
		xml_data = xmltodict.unparse(xmldict)
		try:
			requests.post('http://'+self.encoderIP+'/action/set?subject=videoenc&stream=1', data=xml_data, headers=self.xml_headers, auth=('admin', '12345'),timeout=2).text
		except:
			print "Error Setting Streaming..."
	#
	#
	#	
	##########





	#####################
	#
	#	Image OSD functions
	#	An image is better quality than the text over built in but does not support transparency
	#
	def create_osd_image(self,string,fontsize):
		startsize=fontsize
		font = ImageFont.truetype(self.fontfile, startsize)
		(width, height), (offset_x, offset_y)=font.font.getsize(string)
		#print width,height,offset_y
		text = string
		image = Image.new('RGB', (width+8,height+8), (50,50,50) )
		draw = ImageDraw.Draw(image)

		xpos=(width/2)
		ypos=(height/2)
		draw.text((4,4-offset_y),text, fill="white",font=font)
		try:
			image.save(self.logopath+"image.jpg",format="JPEG", quality=95)
		except:
			return "Error saving file"

	def upload_osd_image(self,channel,image):
		with open(self.logopath+image, "rb") as image_file:
			files = {'file': (image, image_file.read(), 'image/jpg')}
			try:
				requests.post('http://'+self.encoderIP+'/action/upload?file=osdpic'+str(channel),files=files,auth=('admin', '12345'),timeout=2)
			except:
				return "Error with request"

	def enable_osd_image(self,channel,locx,locy,opacity):
		try:
			xml= requests.post('http://'+self.encoderIP+'/action/get?subject=osd&stream='+str(channel), auth=('admin', '12345'),timeout=2).text
		except:
			return "Error with request"
		#print xml
		xmldict= xmltodict.parse(xml)
		xmldict['response']['osd']['picture']['active']="1"
		xmldict['response']['osd']['picture']['xpos']=str(locx)
		xmldict['response']['osd']['picture']['ypos']=str(locy)
		xmldict['response']['osd']['picture']['transparent']=str(opacity)
		xml_data = xmltodict.unparse(xmldict)
		try:
			requests.post('http://'+self.encoderIP+'/action/set?subject=osd&stream='+str(channel), data=xml_data, headers=self.xml_headers, auth=('admin', '12345'),timeout=2).text
		except:
			return "Error with request"


	def disable_osd_image(self,channel):
		try:
			xml= requests.post('http://'+self.encoderIP+'/action/get?subject=osd&stream='+str(channel), auth=('admin', '12345'),timeout=2).text
		except:
			return "Error with request"
		#print xml
		xmldict= xmltodict.parse(xml)
		xmldict['response']['osd']['picture']['active']="0"
		xml_data = xmltodict.unparse(xmldict)
		try:
			requests.post('http://'+self.encoderIP+'/action/set?subject=osd&stream='+str(channel), data=xml_data, headers=self.xml_headers, auth=('admin', '12345'),timeout=2).text
		except:
			return "Error with request"
	#
	#
	#
	#######################
