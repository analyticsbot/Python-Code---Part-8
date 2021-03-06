import urllib.request as urllib2
import urllib.parse as urlparse
import sys
from html.parser import HTMLParser
import os.path
import shutil
import configparser
import random
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
import urllib.error



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

def download(url):
  sys.stderr.write("downloading " + url + "\n")
  try:
    return urllib2.urlopen(url).read().decode(encoding='UTF-8')
  except urllib.error.HTTPError as err:
    sys.stderr.write("got " + err + "\n")
    sys.stderr.write("code: " + str(err.code) + "\n")
    sys.stderr.write("reason: " + str(err.reason) + "\n")
    sys.stderr.write("headers: " + str(err.headers) + "\n")



def read_file(name):
  with open(name) as f:
    return f.read()

def dump_list(name, lst):
  with open(name, 'w') as f:
    for e in lst:
      f.write(e)
      f.write("\n")

def create_dir(d):
  if not os.path.exists(d):
    os.makedirs(d)

def store_entry(root_dir, fname, contents):
  target = os.path.join(root_dir, fname)
  create_dir(os.path.dirname(target))
  with open(target, 'wb') as f:
    f.write(contents.encode(encoding='UTF-8'))

def usage(code):
  sys.stderr.write("usage:\n")
  sys.stderr.write(" " + sys.argv[0] + " <options>\n")
  sys.stderr.write("where <options> is list of:\n")
  sys.stderr.write(" -url <http/https URL>\n")
  sys.stderr.write(" -file <file name>\n")
  sys.exit(code)

def get_opt_value(base_ind):
  val_ind = base_ind + 1
  if val_ind >= len(sys.argv):
    usage(2)
  return sys.argv[val_ind]

def refs_to_entries(contents):
  return [e.get_attr('href') for e in MarksCollector.get_ref_tags(contents) if e.get_attr('class')=='hdrlnk']

def record_keywords(contents):
  [print(e) for e in MarksCollector.get_open_tags(contents)]

def random_sleep(base_ms):
  ms = base_ms + random.randrange(base_ms/2)
  time.sleep(ms/1000.0)

if len(sys.argv) < 2:
  usage(1)

option = sys.argv[1]
url = None
filename = None

if option=='-url':
  url = get_opt_value(1)
elif option == '-file':
  filename = get_opt_value(1)

cfg = configparser.ConfigParser()
cfg.read('config.ini')

record_timeout = int(cfg.get('Timeouts', 'record-contents'))

contents = None
entries_dir = "entries"

if os.path.exists(entries_dir):
  shutil.rmtree(entries_dir)


def marks_inside_ptitle(marks):
  h2_inds = [i for i,x in enumerate(marks) if x.is_tag() and x.is_open() and x.get_tag() == 'h2' and x.get_attr('class') == 'postingtitle']
  if len(h2_inds) == 0:
    print("WARNING: no title")
    return []
  if len(h2_inds) > 1:
    print("WARNING: too much title title")

  found = False
  for ind in range(h2_inds[0] + 1, len(marks)): 
    x = marks[ind]
    if x.is_tag() and not x.is_open() and x.get_tag() == 'h2':
      found = True
      break

  if not found:
    print("WARNING: <h2> title is not closed")
    return []

  return marks[h2_inds[0]+1:ind-1]

def marks_inside_attrgroup(marks):
  from_ind = elem_index(marks, lambda x: is_open_tag(x, 'p', 'attrgroup'))
  if from_ind < 0:
    return []

  tail = marks[from_ind:]
  to_ind = elem_index(tail, lambda x: x.is_tag() and not x.is_open() and x.get_tag() == 'p')

  return tail[:to_ind+1]

  #found = False
  #for ind in range(h2_inds[0] + 1, len(marks)): 
  #  x = marks[ind]
  #  if x.is_tag() and not x.is_open() and x.get_tag() == 'h2':
  #    found = True
  #    break

  #if not found:
  #  print("WARNING: <h2> title is not closed")
  #  return []

  #return marks[h2_inds[0]+1:ind-1]



def drop_empty_data(marks):
  return [x for x in marks if not (x.is_data() and x.get_data().strip()=='')] 

def elem_index(lst, func):
  for ind, elem in enumerate(lst):
    if func(elem):
      return ind  
  return -1

def elem_indexes(lst, func):
  return [ind for ind, elem in enumerate(lst) if func(elem)]


def is_open_tag(x, name, tag_class = None):
  return x.is_tag() and x.is_open() and x.get_tag() == name and (tag_class == None or x.get_attr('class') == tag_class)


def get_small_data(marks):
  ind = elem_index(marks, lambda x: is_open_tag(x, 'small'))
  if ind >= 0:
    return marks[ind+1].get_data()
  else:
    return None

def get_price_data(marks):
  ind = elem_index(marks, lambda x: is_open_tag(x, 'span', 'price') and x.get_attr('class') == 'price')
  if ind >= 0:
    return marks[ind+1].get_data()
  else:
    return None

def get_title_data(marks):
  ind = elem_index(marks, lambda x: is_open_tag(x, 'span', 'postingtitletext'))
  if ind >= 0:
    return marks[ind+1].get_data()
  else:
    return None

def merge_title(head, price, small):
  if head == None:
    return None

  result = head
  if price != None:
    result = result + price
  if small != None:
    result = result + small
  return result


log = open("___log.out", "w")

if url != None:
  parsed_url = urlparse.urlparse(url)
  refs = refs_to_entries(download(url))
  if parsed_url.query == '':
    grow = len(refs)
    pos = 0
    while grow > 0:
      pos = pos + grow
      print("Another retrieval from position " + str(pos))
      url_next = urlparse.urlunparse(parsed_url) + "?s=" + str(pos)
      refs_next = refs_to_entries(download(url_next))
      refs = refs + refs_next
      grow = len(refs_next)
  dump_list('hrefs.log', refs)

  posts = []
  root = ET.Element('root')

  for r in refs:
    random_sleep(record_timeout)
    sys.stdout.write('+')
    sys.stdout.flush()
    record_url = parsed_url.scheme + "://" + parsed_url.netloc + r  
    entry_contents = download(record_url)
    if entry_contents != None:
      store_entry(entries_dir, urlparse.urlparse(record_url).path[1:], entry_contents)
      marks = MarksCollector.get_all(entry_contents)
    else:
      continue
    h2_marks = marks_inside_ptitle(marks)
    h2_marks = drop_empty_data(h2_marks)

    log.write("-------\n")
    log.write(record_url + "\n")
    small = get_small_data(h2_marks)
    price = get_price_data(h2_marks)
    title = merge_title(get_title_data(h2_marks), price, small)

    if title == None:
      log.write("None title !!!!")
      continue

    if small != None:
      log.write("small: " + small + "\n")
    if price != None:
      log.write("price: " + price + "\n")
    log.write("title: " + title + "\n")

    ag_marks = marks_inside_attrgroup(marks)
    span_inds = elem_indexes(ag_marks, lambda x: is_open_tag(x, 'span'))
    log.write(str(span_inds) + "\n")

    p = Post(record_url, title, price, small)

    for i in span_inds:
      log.write(ag_marks[i+1].get_data() + " --> " + ag_marks[i+3].get_data() + "\n")
      p.append_tag(ag_marks[i+1].get_data().strip(), ag_marks[i+3].get_data().strip())

    posts.append(p)

  for p in posts:
    p.create_xml_node(root)

  with open("out.xml", "w") as f:
    f.write(minidom.parseString(ET.tostring(root)).toprettyxml())

elif filename != None:
  refs = refs_to_entries(read_file(filename))
  dump_list('hrefs.log', refs)


