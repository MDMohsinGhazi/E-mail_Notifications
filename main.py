from netmiko import ConnectHandler
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import difflib

# Credentials
ip = "10.0.137.143"
usr = "admin"
pswd = "pnet"


#connection to device using netmiko
device ={
    "device_type": "cisco_ios",
    "ip": ip,
    "username": usr,
    "password": pswd
}

connect = ConnectHandler(**device)
output = connect.send_command("sho run")

#files handling

old_conf_file =("conf_files/"+(datetime.date.today() - datetime.timedelta(days=1)).isoformat())

with open("conf_files/" + datetime.date.today().isoformat(), "w") as new_conf_file:
    new_conf_file.write(output)
# diffrence

with open(old_conf_file, "r") as old_file , open("conf_files/" + datetime.date.today().isoformat(), "r") as new_file:
    diffrence = difflib.HtmlDiff().make_file(fromlines= old_file.readlines(), tolines= new_file.readlines(), fromdesc= "yesterday", todesc="today")

#mail_part
from_addr = "youremail@gmail.com"
to_addr = "youremail@gmail.com"
msg = MIMEMultipart()
msg["from"] = from_addr
msg["to"] = to_addr
msg["sub"] = "Daily configuration Report"
msg.attach(MIMEText(diffrence, 'html'))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
    s.login(from_addr, "password")
    s.sendmail(from_addr,to_addr, msg.as_string())
