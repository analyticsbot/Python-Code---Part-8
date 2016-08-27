import configparser
import sys
import xml.etree.ElementTree as ET
import time
import smtplib
import re

def usage(code):
  sys.stderr.write("usage:\n")
  sys.stderr.write(" " + sys.argv[0] + "with-email.xml message-body.txt\n")
  sys.exit(code)


cfg = configparser.ConfigParser()
cfg.read('config.ini')

server = cfg.get('E-mail', 'server')
login = cfg.get('E-mail', 'login')
from_addr = cfg.get('E-mail', 'from')
password = cfg.get('E-mail', 'password')
timeout = int(cfg.get('Timeouts', 'send-mail'))


if len(sys.argv) < 3:
  usage(1)

src_xml = sys.argv[1]
msg_file = sys.argv[2]

server = smtplib.SMTP(server)
server.ehlo()
server.starttls()
server.login(login, password)

with open(msg_file) as f:
  msg_text = f.read()

tree = ET.parse(src_xml)
root = tree.getroot()

print("123")
  
for p in root:
  if 'email' in p.attrib:
    subject = p.attrib['title']
    text = re.sub('<<NAME>>', p.attrib['name'], msg_text)
    to_addr = p.attrib['email']
    msg = "\r\n".join([
      "From: " + from_addr,
      "To: " + to_addr,
      "Subject: " + subject,
      "",
      text
    ])
    server.sendmail(from_addr, to_addr, msg)
    time.sleep(timeout/1000.0)

server.quit()
