import configparser
import sys
import xml.etree.ElementTree as ET
import time
import smtplib
import re

def usage(code):
  sys.stderr.write("usage:\n")
  sys.stderr.write(" " + sys.argv[0] + " <xml file with addresses> <subject> <file with message body>\n")
  sys.exit(code)

def get_tags(node):
  return [(t.attrib['key'], t.attrib['value']) for t in node]

def get_top_tag(node):
  return dict(get_tags(node)).get('top-tag')

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

with open(msg_file) as f:
  msg_text = f.read()

msg_text_orig = msg_text


required_name = msg_text.find('<<NAME>>') != -1
required_top_tag = msg_text.find('<<TOP-TAG>>') != -1


server = smtplib.SMTP(server)
server.ehlo()
server.starttls()
server.login(login, password)


tree = ET.parse(src_xml)
root = tree.getroot()

for p in root:
  msg_text = msg_text_orig

  if not ('email' in p.attrib):
    continue

  name = p.attrib.get('name')
  top_tag = get_top_tag(p)
 
  if required_name and name == None:
    print("No name. Skipped.")
    continue

  if required_top_tag and top_tag == None:
    print("No top-tag. Skipped.")
    continue

  subject = p.attrib['title']
  if required_name:
    msg_text = re.sub('<<NAME>>', name, msg_text)

  if required_top_tag:
    msg_text = re.sub('<<TOP-TAG>>', top_tag, msg_text)


  to_addr = p.attrib['email']
  msg = "\r\n".join([
    "From: " + from_addr,
    "To: " + to_addr,
    "Subject: " + subject,
    "",
    msg_text
  ])
  print(msg)
  server.sendmail(from_addr, to_addr, msg)
  time.sleep(timeout/1000.0)

server.quit()
