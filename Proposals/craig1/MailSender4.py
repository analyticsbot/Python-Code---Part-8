import configparser
import sys
import xml.etree.ElementTree as ET
import time
import smtplib
import re
from itertools import *


def usage(code):
  sys.stderr.write("usage:\n")
  sys.stderr.write(" " + sys.argv[0] + " <xml file with addresses> <subject> <file with message body>\n")
  sys.exit(code)

def get_tags(node):
  return [(t.attrib['key'], t.attrib['value']) for t in node]

def get_top_tag(node):
  return dict(get_tags(node)).get('top-tag')

class MailSettings:
  def __init__(self, cfg, section):
    self.server = cfg.get(section, 'server')
    self.login = cfg.get(section, 'login')
    self.from_addr = cfg.get(section, 'from')
    self.password = cfg.get(section, 'password')

def take(n, iterable):
  return list(islice(iterable, n))

def head(iterable):
  return take(1, iterable)[0]


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


section_names = map(lambda e: e[0], cfg.items())
dotted_mail_sections = filter(re.compile("^E-mail\.[0-9]+$").match, section_names)

dms_list = list(dotted_mail_sections)

if len(dms_list) > 0:
  suffixes = map(lambda e: int(e[7:]), dms_list)
  indexes = sorted(suffixes)
  print(indexes)
  accounts = map(lambda e: MailSettings(cfg, 'E-mail.%s' % e), indexes)
  
else:
  accounts = map(lambda e: MailSettings(cfg, 'E-mail'), [None])

accounts = cycle(accounts)




tree = ET.parse(src_xml)
root = tree.getroot()


def split_by_portions(l, sz):
  res = []
  for i in range(0, len(l), sz):
    res.append(l[i: i+sz])

  return res


for portion in split_by_portions(root, 30):
  next_account = head(accounts)

  print("Send via %s (login %s)" % (next_account.server, next_account.login))

  server = smtplib.SMTP(next_account.server)
  server.ehlo()
  server.starttls()
  server.login(next_account.login, next_account.password)

  for p in portion:
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
    #print(msg)
    server.sendmail(next_account.from_addr, to_addr, msg)
    time.sleep(timeout/1000.0)

  server.quit()

