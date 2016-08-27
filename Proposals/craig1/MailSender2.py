import configparser
import sys
import xml.etree.ElementTree as ET
import time
import smtplib

def usage(code):
  sys.stderr.write("usage:\n")
  sys.stderr.write(" " + sys.argv[0] + " <xml file with addresses> <subject> <file with message body>\n")
  sys.exit(code)


cfg = configparser.ConfigParser()
cfg.read('config.ini')

server = cfg.get('E-mail', 'server')
login = cfg.get('E-mail', 'login')
from_addr = cfg.get('E-mail', 'from')
password = cfg.get('E-mail', 'password')
timeout = int(cfg.get('Timeouts', 'send-mail'))


if len(sys.argv) < 4:
  usage(1)

src_xml = sys.argv[1]
subject = sys.argv[2]
msg_file = sys.argv[3]

server = smtplib.SMTP(server)
server.ehlo()
server.starttls()
server.login(login, password)

with open(msg_file) as f:
  msg_text = f.read()

tree = ET.parse(src_xml)
root = tree.getroot()
  
for p in root:
  if 'email' in p.attrib:
    to_addr = p.attrib['email']
    msg = "\r\n".join([
      "From: " + from_addr,
      "To: " + to_addr,
      "Subject: " + subject,
      "",
      msg_text
    ])
    server.sendmail(from_addr, to_addr, msg)
    time.sleep(timeout/1000.0)

server.quit()
