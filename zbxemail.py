#!/usr/bin/env python3.6

import zbxemail_settings
import sys
import requests
import os
import base64
import smtplib
import sys
import base64
import datetime
import time

from pyzabbix import ZabbixAPI
from jinja2 import Template

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

server = zbxemail_settings.zbx_server
api_user = zbxemail_settings.zbx_api_user
api_pass = zbxemail_settings.zbx_api_pass

server_tmp_path = zbxemail_settings.zbx_tmp_path
server_alert_path = zbxemail_settings.zbx_alert_path
	
zapi = ZabbixAPI(server)
try:
	zapi.login(api_user, api_pass)
except:
	pass
	


def print_message(string):
	string = str(string) + "\n"
	filename = sys.argv[0].split("/")[-1]
	sys.stderr.write(filename + ": " + string)

def convert_time(a):
	return datetime.datetime.fromtimestamp(a).strftime('%Y-%m-%d %H:%M:%S')

	server = zbxemail_settings.zbx_server
	api_user = zbxemail_settings.zbx_api_user
	api_pass = zbxemail_settings.zbx_api_pass

	zapi = ZabbixAPI(server)
	try:
		zapi.login(api_user, api_pass)
	except:
		pass
	
	zdata = zbxdata()
	
	zbx_image = ZabbixImage(server=server, api_user=api_user, api_pass=api_pass)
	try:
		zbx_image.login()
	except:
		pass
	

class zbxdata(object):
	def __init__(self):
		super(zbxdata, self).__init__()
		self.event = ''
		self.items = []
		self.trigger = ''
		self.eventtime = ''
		self.history_types = []
		self.items_update = []
		self.items_name = []
		self.triggername = ''
		self.triggerstatus = ''
		self.itemuniq = []
		self.hostid = ''
		self.resolv_or_ack = 0
		
	def get_last_ten_minutes_data(self):
		sl=''
		for item in self.itemuniq:
			sl+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+item[1]+" :"
			sl+="<br>"
			if self.resolv_or_ack == 0:
				histrory_item = zapi.history.get(output='extend',
												history=item[2],
												itemids=item[0],
												time_from=str(int(self.eventtime)-10*60),
												time_till=self.eventtime, 
												sortfield='clock',
												sortorder='DESC',
												)
			if self.resolv_or_ack == 1:
				histrory_item = zapi.history.get(output='extend',
												history=item[2],
												itemids=item[0],
												time_from=str(int(time.time())-10*60),
												time_till=str(int(time.time())), 
												sortfield='clock',
												sortorder='DESC',
												)
			for tmp_history in histrory_item:
				sl+="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+"Time"+convert_time(int(tmp_history["clock"]))+"   Value: "+tmp_history["value"]+"<br>"
		return sl
	
	def get_last_ten_event(self):
		st=''
		events = zapi.event.get(output='extend',
						select_acknowledges='extend',
						selectTags='extend',
						objectids=self.trigger,
						sortfield=['clock', 'eventid'],
						sortorder='DESC',
						limit='10'
						)

		for event in events:
			if event["value"]=='1':
				st+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Status: PROBLEM Time: '+convert_time(int(event["clock"]))+'<br>'
			if event["value"]=='0':
				st+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Status: OK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Time: '+convert_time(int(event["clock"]))+'<br>'			
		return st			


class SendEmail(object):
	"""docstring for SendEmail"""
	def __init__(self):
		super(SendEmail, self).__init__()
		self.mail_from = 'zabbix@zabbix'
		self.mail_user = 'zabbix'
		self.mail_to = 'admin@admni'
		self.mail_server = 'localhost'
		self.mail_pass = ''
		self.mail_subject = 'Subject from Zabbix'
		self.mail_head = 'head'
		self.mail_graph = ''
		self.mail_footer = 'footer'
		self.mail_url = ''
		self.mail_url2 = ''

	def send(self):
		msg = MIMEMultipart("alternative")
		msg['Subject'] = self.mail_subject
		msg['From'] = self.mail_from
		msg['To'] = self.mail_to

		text = self.mail_head + self.mail_footer

		template_file = open(server_alert_path + '/email_template.j2')
		template_text = ''
		for lines in template_file:
			template_text = template_text + lines

		t = Template(template_text)
		
		fp = open(self.mail_graph, 'rb')
		img = MIMEImage(fp.read(), 'png')
		img.add_header('Content-Id', '<523856>') 
		img.add_header('Content-Disposition', 'attachment', filename=self.mail_graph)
	
		
		html = t.render(zabbix_name='',
								trigger_text=self.mail_head, graph='',
								trigger_url=self.mail_url, trigger_url2=self.mail_url2, trigger_details=self.mail_footer,
								company=self.company)

		part1 = MIMEText(text, 'plain', 'utf-8')
		part2 = MIMEText(html, 'html', 'utf-8')
		
		msg.attach(img)
		msg.attach(part1)
		msg.attach(part2)
		

		s = smtplib.SMTP()
		s.connect(self.mail_server)
		s.ehlo(self.mail_from)
		#s.login(self.mail_user, self.mail_pass)
		s.sendmail(self.mail_from, self.mail_to, msg.as_string())
		fp.close()
		os.remove(self.mail_graph)
		s.quit()

class ZabbixImage(object):
	"""For get graph image"""
	def __init__(self, server, api_user, api_pass):
		super(ZabbixImage, self).__init__()
		#self.arg = arg
		self.server = server
		self.api_user = api_user
		self.api_pass =api_pass
		self.verify = True
		self.cookie = None
		self.res_img = None
		self.res_url = None
		self.res_url_evnt = None

	def login(self):

		if not self.verify:
			requests.package.urllib3.disable_warnings()

		data_api = {"name": self.api_user, "password": self.api_pass, "enter": "Sign in"}
		req_cookie = requests.post(self.server + "/", data=data_api, verify=self.verify)
		cookie = req_cookie.cookies

		if len(req_cookie.history) > 1 and req_cookie.history[0].status_code == 302:
			print_message("Probably the server in your config file has not full URL")

		if not cookie:
			print_message("authorization failed")
			cookie = None

		self.cookie = cookie

	def graph_get(self, itemid, period, triggername, width, height, problem, hostid, event, trigger):
		
	
		if problem == 0:
			colors = {
				0: "00CC00",
				1: "f7c0c0",
				2: "0000CC",
				3: "CCCC00",
				4: "00CCCC",
				5: "CC00CC",
			}
		if problem == 1:
			colors = {
				0: "fca6a6",
				1: "004700",
				2: "0000CC",
				3: "CCCC00",
				4: "00CCCC",
				5: "CC00CC",
			}
		drawtype = 2
		title = triggername

		zbx_img_url_itemids = []
		ftmpname = []
		for i in range(0, len(itemid)):
			itemid_url = "&items[{0}][itemid]={1}&items[{0}][sortorder]={0}&" \
						 "items[{0}][drawtype]={3}&items[{0}][color]={2}".format(i, itemid[i][0], colors[i], drawtype)
			zbx_img_url_itemids.append(itemid_url)
			ftmpname.append(itemid[i][0])
		
		file_img = server_tmp_path + "/{0}.png".format("".join(ftmpname))
		
		zbx_img_url = self.server + "/chart3.php?period={0}&name={1}" \
									"&width={2}&height={3}&graphtype=0&legend=1".format(period, title, width, height)
		
		zbx_url_url = self.server + "/latest.php?fullscreen=0&filter_set=1&show_without_data=1&hostids[]="
		zbx_url_url_event = self.server + "/tr_events.php?triggerid={0}&eventid={1}".format(trigger, event)
		
		zbx_img_url += "".join(zbx_img_url_itemids)
		zbx_url_url += hostid

		res = requests.get(zbx_img_url, cookies=self.cookie)
		res_code = res.status_code
		if res_code == 404:
			print_message("can`t get image from '{0}'".format(zbx_img_url))
			return False


		res_img = res.content
		self.res_url = zbx_url_url
		self.res_url_evnt = zbx_url_url_event
		with open(file_img, 'wb') as fp:
			fp.write(res_img)
		self.res_img = file_img
		fp.close()


def main():
	
	zdata = zbxdata()
	
	zbx_image = ZabbixImage(server=server, api_user=api_user, api_pass=api_pass)
	try:
		zbx_image.login()
	except:
		pass
	
	subj = sys.argv[2]
	
	if subj.find('Resolved') == 0 or subj.find('Acknowledged') == 0:
		zdata.resolv_or_ack = 1
	
	body = sys.argv[3].split('\n')

	for line in sys.argv[3].split('\n'):

		if line.find('item1') == 0:
			item1 = line.split(';')[1]
			item1_name = line.split(';')[2]
			if item1.find('*UNKNOWN*') == -1:
				tmp_items = zapi.item.get(output='extend', itemids=item1)
				zdata.items.append(item1)
				zdata.items_name.append(item1_name)
				for tmp_item in tmp_items:
					zdata.history_types.append(tmp_item["value_type"])
					zdata.items_update.append(tmp_item["delay"])
					zdata.hostid = tmp_item["hostid"]
		if line.find('item2') == 0:
			item2 = line.split(';')[1]
			item2_name = line.split(';')[2]
			if item2.find('*UNKNOWN*') == -1:
				tmp_items = zapi.item.get(output='extend', itemids=item2)
				zdata.items.append(item2)
				zdata.items_name.append(item2_name)
				for tmp_item in tmp_items:
					zdata.history_types.append(tmp_item["value_type"])
					zdata.items_update.append(tmp_item["delay"])
		if line.find('item3') == 0:
			item3 = line.split(';')[1]
			item3_name = line.split(';')[2]
			if item3.find('*UNKNOWN*') == -1:
				tmp_items = zapi.item.get(output='extend', itemids=item3)
				zdata.items.append(item3)
				zdata.items_name.append(item3_name)
				for tmp_item in tmp_items:
					zdata.history_types.append(tmp_item["value_type"])
					zdata.items_update.append(tmp_item["delay"])
		if line.find('item4') == 0:
			item4 = line.split(';')[1]
			item4_name = line.split(';')[2]
			if item4.find('*UNKNOWN*') == -1:
				tmp_items = zapi.item.get(output='extend', itemids=item4)
				zdata.items.append(item4)
				zdata.items_name.append(item4_name)
				for tmp_item in tmp_items:
					zdata.history_types.append(tmp_item["value_type"])
					zdata.items_update.append(tmp_item["delay"])
		if line.find('item5') == 0:
			item5 = line.split(';')[1]
			item5_name = line.split(';')[2]
			if item5.find('*UNKNOWN*') == -1:
				tmp_items = zapi.item.get(output='extend', itemids=item5)
				zdata.items.append(item5)
				zdata.items_name.append(item5_name)
				for tmp_item in tmp_items:
					zdata.history_types.append(tmp_item["value_type"])
					zdata.items_update.append(tmp_item["delay"])
		if line.find('item6') == 0:
			item6 = line.split(';')[1]
			item6_name = line.split(';')[2]
			if item6.find('*UNKNOWN*') == -1:
				tmp_items = zapi.item.get(output='extend', itemids=item6)
				zdata.items.append(item6)
				zdata.items_name.append(item6_name)
				for tmp_item in tmp_items:
					zdata.history_types.append(tmp_item["value_type"])
					zdata.items_update.append(tmp_item["delay"])
		if line.find('eventid') == 0:
			zdata.event = line.split(';')[1]
			tmp_events = zapi.event.get(output='extend', eventids=zdata.event)
			for tmp_event in tmp_events:
				zdata.eventtime = tmp_event["clock"]
		if line.find('triggerid') == 0:
			zdata.trigger = line.split(';')[1]	
		if line.find('triggername') == 0:
			zdata.triggername = line.split(';')[1]
		if line.find('status') == 0:
			zdata.triggerstatus = line.split(';')[1]

			


	i=0
	j=0
	for item in zdata.items:
		tmp = []
		j=i+1
		while j<=len(zdata.items)-1:
			if item == zdata.items[j]:
				break
			j+=1
		if 	j==len(zdata.items):
			tmp.append(item)
			tmp.append(zdata.items_name[i])
			tmp.append(zdata.history_types[i])
			tmp.append(zdata.items_update[i])
			zdata.itemuniq.append(tmp)
		i+=1
		
	
	
			
	email = SendEmail()
	image_height = zbxemail_settings.zbx_graph_height
	image_width = zbxemail_settings.zbx_graph_width
	image_period = zbxemail_settings.zbx_graph_period
	
	if zdata.triggerstatus == 'OK':
		email.mail_head = '<p>'+body[0]+'<br>\n'+body[1]+'<br>\n'+body[3]+'</p><p style=\'background-color: #00CC00\'>'+body[2]+'</p>'
		problem=0
		
	if zdata.triggerstatus == 'PROBLEM':
		email.mail_head = '<p>'+body[0]+'<br>\n'+body[1]+'<br>\n'+body[3]+'</p><p style=\'background-color: #fca6a6\'>'+body[2]+'</p>'
		problem=1
		
	zbx_image.graph_get(zdata.itemuniq, image_period, zdata.triggername, image_width, image_height, problem, zdata.hostid, zdata.event, zdata.trigger)




	email.mail_from = zbxemail_settings.email_from
	email.mail_user = zbxemail_settings.email_username
	email.mail_pass = zbxemail_settings.email_password
	email.mail_to = sys.argv[1]
	email.mail_subject = sys.argv[2]
	email.mail_server = zbxemail_settings.email_smtp

	email.company = zbxemail_settings.company
	
	cid='<img src="cid:523856">'

	if zdata.history_types[0] == '0' or zdata.history_types[0] == '3':
		email.mail_head+='<p>'+cid+'</p>'
	s1='<p><br><b>' + 'Latest data (ten minutes interval):' + '</b>'
	s1+='<br>' + zdata.get_last_ten_minutes_data() + '</p>'
	s2='<p><br><b>' + 'Last events (max ten):' + '</b>'
	s2+='<br>' + zdata.get_last_ten_event() + '</p>'
	email.mail_footer = s1+s2
	email.mail_graph = zbx_image.res_img
	email.mail_url = zbx_image.res_url
	email.mail_url2 = zbx_image.res_url_evnt
	email.send()




if __name__ == "__main__":
	main()
