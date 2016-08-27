from selenium import webdriver

import selenium.common

from html.parser import HTMLParser
import configparser
import socket
import sys
import select
import json
import xml.etree.ElementTree as ET
import time
from xml.dom import minidom

fp = webdriver.FirefoxProfile('C:\\Users\\Luka Stevanov\\Application Data\\Mozilla\\Firefox\\Profiles\\qumo42ba.default')
browser = webdriver.Firefox(fp, proxy=None)
#browser = webdriver.Firefox()

def pretty(root):
  return '\n'.join([s for s in minidom.parseString(ET.tostring(root)).toprettyxml().split('\n') if len(s.strip()) > 0])


class Post:
  def __init__(self, url, title, price, small):
    self.title = title
    self.price = price
    self.small = small
    self.url = url
    self.tags = []

  def create_xml_node(self, parent):
    res = ET.SubElement(parent, 'post')
    res.set('title', self.title)
    res.set('url', self.url)
    if self.price != None:
      res.set('price', self.price)
    if self.small != None:
      res.set('small', self.small)

    for t in self.tags:
      tag_elem = ET.SubElement(res, 'tag')
      tag_elem.set('key', t[0])
      tag_elem.set('value', t[1])

  def append_tag(self, key, value):
    self.tags.append((key, value))
  

  def __str__(self):
    return self.title
 

  

class HTMLMark:    
  def is_open(self):
    return False

  def is_tag(self):
    return False

  def is_data(self):
    return False


class DataMark(HTMLMark):
  def __init__(self, data):
    self.data = data
    super(HTMLMark, self).__init__()

  def __str__(self):
    return "<DATA> <DATA " + self.data + ">" 

  def is_data(self):
    return True

  def get_data(self):
    return self.data


class TagMark(HTMLMark):
  def __init__(self, tag):
    self.tag = tag
    super(HTMLMark, self).__init__()

  def get_tag(self):
    return self.tag

  def is_tag(self):
    return True


class OpenTagMark(TagMark):
  def __init__(self, tag, attrs):
    self.attrs = dict(attrs)
    super(OpenTagMark, self).__init__(tag)

  def __str__(self):
    return "<OPEN> <TAG " + self.tag  + "> <ATTRS " + str(self.attrs) + ">" 

  def is_open(self):
    return True

  def get_attr(self, key):
    if key in self.attrs:
      return self.attrs[key]
    else:
      return None

class CloseTagMark(TagMark):
  def __init__(self, tag):
    super(CloseTagMark, self).__init__(tag)

  def __str__(self):
    return "<CLOSE> <TAG " + self.tag + ">" 


class MarksCollector(HTMLParser):
    def __init__(self):
      self.marks = []
      super(MarksCollector, self).__init__()

    def handle_starttag(self, tag, attrs):
      self.marks.append(OpenTagMark(tag, attrs))

    def handle_endtag(self, tag):
      self.marks.append(CloseTagMark(tag))

    def handle_data(self, data):
      self.marks.append(DataMark(data))

    @staticmethod
    def get_open_tags(text):
      collector = MarksCollector()
      collector.feed(text)
      return [e for e in collector.marks if e.is_open()]

    @staticmethod
    def get_ref_tags(text):
      collector = MarksCollector()
      collector.feed(text)
      return [e for e in collector.marks if e.is_open() and e.get_tag() == 'a']

    @staticmethod
    def get_all(text):
      collector = MarksCollector()
      collector.feed(text)
      return collector.marks



def usage(code):
  sys.stderr.write("usage:\n")
  sys.stderr.write(" " + sys.argv[0] + "<command> <options>\n")
  sys.stderr.write("where <command> is one of:\n\n")
  sys.stderr.write(" probe\n")
  sys.stderr.write(" url\n")
  sys.stderr.write(" load\n")
  sys.stderr.write(" content\n")
  sys.stderr.write(" get-addresses\n")
  sys.exit(code)

def is_alive(host, port):
  try:
    sock = socket.socket()
    sock.connect((host, port))
    sock.close()
    return True
  except socket.error:
    return False

def send_str(socket, s):
  socket.send(s.encode('UTF-8'))

def recv_str(socket):
  return recv_bytes(socket).decode('UTF-8')


def recv_bytes(socket):
  result = bytes([])
  while True:
    r =  recv_bytes_once(socket)
    if len(r) == 0:
      return result
    else:
      result = result + r      

def recv_bytes_once(socket):
  socket.setblocking(0)

  ready = select.select([socket], [], [], 3)
  if ready[0]:
    return socket.recv(8192)
  else:
    return []

def load_contents(url):
  sock = socket.socket()
  sock.connect(("localhost", port))
  send_str(sock, 'content.location="' + url + '"')
  sock.close()

def get_contents():
  sock = socket.socket()
  sock.connect(("localhost", port))
  send_str(sock, 'document.documentElement.innerHTML\n')
  json_response = recv_str(sock)
  sock.close()
  return json.loads(json_response)['result']

def elem_index(lst, func):
  for ind, elem in enumerate(lst):
    if func(elem):
      return ind  
  return -1


def is_open_tag(x, name, tag_class = None):
  return x.is_tag() and x.is_open() and x.get_tag() == name and (tag_class == None or x.get_attr('class') == tag_class)


cfg = configparser.ConfigParser()
cfg.read('config.ini')

port = int(cfg.get('Firefox', 'port'))
load_post_tout = int(cfg.get('Timeouts', 'load-post'))
load_reply_tout = int(cfg.get('Timeouts', 'load-reply'))

if len(sys.argv) < 2:
  usage(1)

if sys.argv[1] == 'probe':
  if is_alive("localhost", port):
    print("Alive")
  else:
    print("Absent")
elif sys.argv[1] == 'load':
  host = sys.argv[2]
  load_contents(host)
elif sys.argv[1] == 'url':
  sock = socket.socket()
  sock.connect(("localhost", port))
  send_str(sock, 'content.location\n')
  print(recv_str(sock))
  sock.close()
elif sys.argv[1] == 'content':
  response = get_contents()
  with (open("content.html", "wb")) as f:
    print(len(response))
    f.write(response.encode('UTF-8'))
    f.flush()
elif sys.argv[1] == 'get-addresses':

  src_xml = sys.argv[2]
  dest_xml = sys.argv[3]

  tree = ET.parse(src_xml)
  root = tree.getroot()

 
  for i, p in enumerate(root):
    url = p.attrib['url']

    browser.get(url)
    try:
      browser.find_element_by_class_name("reply_button").click()
    except selenium.common.exceptions.NoSuchElementException:
      print("No button")
      continue

    time.sleep(2)
    response = browser.page_source

    marks = MarksCollector.get_all(response)
    ind = elem_index(marks, lambda x: is_open_tag(x, 'a', 'mailapp'))
    if ind == -1:
      print("WARNING: no E-mail for " + url)
      continue

    mail_address = marks[ind+1].get_data()
    p.attrib['email'] = mail_address
    print(mail_address)     


  with open(dest_xml, "wb") as f:
    f.write(pretty(root).encode('utf-8'))

