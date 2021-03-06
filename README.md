# zbxemail
Zabbix email with graphs scripts on python<br>
Tested on Centos 7, zabbix 4.2, Outlook 2018 <br>
<br>
For install scripts you need python 3, requests, jinja2 and pyzabbix:<br>
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm <br>
sudo yum update <br>
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip <br>
pip3.6 install requests jinja2 pyzabbix <br>
<br>
<br>

<img src="https://image.ibb.co/hM7HWT/7.png"><br><br>

<img src="https://image.ibb.co/jkEaJ8/9.png"><br>



Zabbix Server: put zbxemail.py, zbxemail_settings.py and email_template.j2 into /usr/lib/zabbix/alertscripts (or you alertscripts folder for zabbix); create temp folder for image, for example /var/tmp/zbxemail, change permissions to rwxrwxrwx; <br> edit path in zbxemail_settings.py: zbx_tmp_path = '/var/tmp/zbxemail' zbx_alert_path = '/usr/lib/zabbix/alertscripts';<br>
change settings for email in zbxemail_settings.py <br>

Add media type:<br><br>
<img src="https://image.ibb.co/g1YSgT/1.png"><br><br>
Add media to user:<br><br>
<img src="https://image.ibb.co/mu0jT8/2.png"><br><br>
Add action:<br>
select New action<br>
in Action: Report problems to exmp.user<br>
<br>
<img src="https://image.ibb.co/jWR2Fo/3.png"><br><br>
                                          
in Operations:<br><br>

Problem: {TRIGGER.NAME}<br><br>

&lt;b&gt;Host:&lt;/b&gt; {HOST.NAME}<br>
&lt;b&gt;Problem name:&lt;/b&gt; {TRIGGER.NAME}<br>
&lt;b&gt;Problem started at&lt;/b&gt; {EVENT.TIME} &lt;b&gt;on&lt;/b&gt; {EVENT.DATE}<br>
&lt;b&gt;Severity:&lt;/b&gt; {TRIGGER.SEVERITY}<br>
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

<br><br>
<img src="https://image.ibb.co/diFJo8/4.png"><br><br>


in Recovery operations:<br><br>

Resolved: {TRIGGER.NAME}<br><br>

&lt;b&gt;Host:&lt;/b&gt; {HOST.NAME}<br>
&lt;b&gt;Problem name:&lt;/b&gt; {TRIGGER.NAME}<br>
&lt;b&gt;Problem has been resolved at&lt;/b&gt; {EVENT.RECOVERY.TIME} &lt;b&gt;on &lt;/b&gt;{EVENT.RECOVERY.DATE}<br>
&lt;b&gt;Severity:</b> {TRIGGER.SEVERITY}<br>
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

<br><br>
<img src="https://image.ibb.co/gNOSgT/5.png"><br><br>

in Acknowledgement operations:<br><br>

Acknowledged: {TRIGGER.NAME}<br><br>

&lt;b&gt;Host:&lt;/b&gt; {HOST.NAME}<br>
&lt;b&gt;Problem name:&lt;/b&gt; {TRIGGER.NAME}<br>
{USER.FULLNAME} &lt;b&gt;acknowledged problem at&lt;/b&gt; {ACK.DATE} {ACK.TIME} &lt;b&gt;with the following message:&lt;/b&gt; {ACK.MESSAGE}<br>
&lt;b&gt;Severity:&lt;/b&gt; {TRIGGER.SEVERITY}<br>
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

<br><br>
<img src="https://image.ibb.co/gP1f1T/6.png"><br>
