# zbxemail
Fork https://github.com/andreineustroev/zabbix-email-extra and https://github.com/ableev/Zabbix-in-Telegram<br>
Zabbix email with graphs scripts on python<br>
Tested on Centos 7.4, zabbix 3.4.8, Outlook 2018 <br>
<br>
For install scripts you need python 3, requests, jinja2 and pyzabbix:<br>
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm <br>
sudo yum update <br>
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip <br>
pip3.6 install requests jinja2 pyzabbix <br>
<br>
<br>

<img src="<img src="https://image.ibb.co/eJENFo/8.png"><br>

<img src="<img src="https://image.ibb.co/bOAjT8/9.png"><br>


Add media type:<br>
<img src="<img src="https://image.ibb.co/g1YSgT/1.png"><br>
Add media to user:<br>
<img src="<img src="https://image.ibb.co/mu0jT8/2.png><br>
Add action:<br>
select New action<br>
Report problems to ....<br>

<img src="<img src="https://image.ibb.co/jWR2Fo/3.png"><br>
                                          
Operations:<br><br>

Problem: {TRIGGER.NAME}<br><br>

<b>Host:</b> {HOST.NAME}<br>
<b>Problem name:</b> {TRIGGER.NAME}<br>
<b>Problem started at</b> {EVENT.TIME} <b>on</b> {EVENT.DATE}<br>
<b>Severity:</b> {TRIGGER.SEVERITY}<br>
item1:;{ITEM.ID1};{ITEM.NAME1}<br>
item2:;{ITEM.ID2};{ITEM.NAME2}<br>
item3:;{ITEM.ID3};{ITEM.NAME3}<br>
item4:;{ITEM.ID4};{ITEM.NAME4}<br>
item5:;{ITEM.ID5};{ITEM.NAME5}<br>
item6:;{ITEM.ID6};{ITEM.NAME6}<br>
eventid:;{EVENT.ID}<br>
triggerid:;{TRIGGER.ID}<br>
triggername:;{TRIGGER.NAME}<br>
status:;{TRIGGER.STATUS}<br><br>

<img src="<img src="https://image.ibb.co/diFJo8/4.png"><br>


Recovery operations:<br><br>

Resolved: {TRIGGER.NAME}<br><br>

<b>Host:</b> {HOST.NAME}<br>
<b>Problem name:</b> {TRIGGER.NAME}<br>
<b>Problem has been resolved at</b> {EVENT.RECOVERY.TIME} <b>on </b>{EVENT.RECOVERY.DATE}<br>
<b>Severity:</b> {TRIGGER.SEVERITY}<br>
item1:;{ITEM.ID1};{ITEM.NAME1}<br>
item2:;{ITEM.ID2};{ITEM.NAME2}<br>
item3:;{ITEM.ID3};{ITEM.NAME3}<br>
item4:;{ITEM.ID4};{ITEM.NAME4}<br>
item5:;{ITEM.ID5};{ITEM.NAME5}<br>
item6:;{ITEM.ID6};{ITEM.NAME6}<br>
eventid:;{EVENT.ID}<br>
triggerid:;{TRIGGER.ID}<br>
triggername:;{TRIGGER.NAME}<br>
status:;{TRIGGER.STATUS}<br><br>

<img src="<img src="https://image.ibb.co/gNOSgT/5.png"><br>

Acknowledgement operations:<br><br>

Acknowledged: {TRIGGER.NAME}<br><br>

<b>Host:</b> {HOST.NAME}<br>
<b>Problem name:</b> {TRIGGER.NAME}<br>
{USER.FULLNAME} <b>acknowledged problem at</b> {ACK.DATE} {ACK.TIME} <b>with the following message:</b> {ACK.MESSAGE}<br>
<b>Severity:</b> {TRIGGER.SEVERITY}<br>
item1:;{ITEM.ID1};{ITEM.NAME1}<br>
item2:;{ITEM.ID2};{ITEM.NAME2}<br>
item3:;{ITEM.ID3};{ITEM.NAME3}<br>
item4:;{ITEM.ID4};{ITEM.NAME4}<br>
item5:;{ITEM.ID5};{ITEM.NAME5}<br>
item6:;{ITEM.ID6};{ITEM.NAME6}<br>
eventid:;{EVENT.ID}<br>
triggerid:;{TRIGGER.ID}<br>
triggername:;{TRIGGER.NAME}<br>
status:;{TRIGGER.STATUS}<br>

<img src="<img src="https://image.ibb.co/gP1f1T/6.png"><br>
