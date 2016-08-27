import os.path
import argparse
import configparser
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
import time
import urlparse
import urllib2
import smtplib
import re
from itertools import *
from FlattenHTML import *
from selenium import webdriver
import selenium.common


class Post:
    def __init__(self, url, title, name, price, small):
        self.title = title
        self.name = name.rstrip()
        if self.name[-1] == '-':
            self.name = self.name[:-1].rstrip()

        self.price = price
        self.small = small
        self.url = url
        self.tags = []

    def create_xml_node(self, parent):
        res = ET.SubElement(parent, 'post')
        res.set('title', self.title)
        res.set('name', self.name)
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


def parse_args():
    parser = argparse.ArgumentParser(description='Extracts info and sends E-mails')
    parser.add_argument("urls_file")
    parser.add_argument("output_xml")
    parser.add_argument("msg_file")
    return parser.parse_args()

def get_lines(name):
    with open(name, 'r') as f:
        return [s.strip() for s in f.readlines()]

def download(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    response = urllib2.urlopen(req)
    return response.read().decode(encoding='utf-8', errors = 'ignore')

def pretty(root):
    return '\n'.join([s for s in minidom.parseString(ET.tostring(root)).toprettyxml().split('\n') if len(s.strip()) > 0])

def write_file(name, contents):
    with open(name, 'wb') as f:
        f.write(contents.encode(encoding = 'utf-8'))
    
def refs_to_entries(contents):
    return [e.get_attr('href') for e in MarksCollector.get_ref_tags(contents) if e.get_attr('class')=='hdrlnk']

def with_path(url, path):
    parsed_url = urlparse.urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.netloc + path

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

def drop_empty_data(marks):
    return [x for x in marks if not (x.is_data() and x.get_data().strip()=='')] 

def find(lst, predicate):
    return [i for i, x in enumerate(lst) if predicate(x)]

def find_first(lst, predicate):
    return elem_index(lst, predicate)

def elem_index(lst, func):
    for ind, elem in enumerate(lst):
        if func(elem):
            return ind  
    return -1

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

def attrgroup_begins(marks):
    return find(marks, lambda x: is_open_tag(x, 'p', 'attrgroup'))

def attrgroup_ends(marks, begins):
    return [b + find_first(marks[b:], lambda x: x.is_tag() and not x.is_open() and x.get_tag() == 'p') for b in begins]

def attrgroups_bounds(marks):
    bs = attrgroup_begins(marks)
    return list(zip(bs, attrgroup_ends(marks, bs)))

def span_begins(marks):
    return find(marks, lambda x: x.is_tag() and x.is_open() and x.get_tag() == 'span')

def span_ends(marks, begins):
    return [b + find_first(marks[b:], lambda x: x.is_tag() and not x.is_open() and x.get_tag() == 'span') for b in begins]

def span_bounds(marks):
    bs = span_begins(marks)
    return list(zip(bs, span_ends(marks, bs)))

def parse_attrgroup(marks, inds):
    group = marks[inds[0]: inds[1]] 
    span_groups = [group[b[0]:b[1]] for b in span_bounds(group)]
    filtered = [sg for sg in span_groups if sg[0].get_attr('class') != 'otherpostings']  
    result = []
    for sg in filtered:
        if len(sg) == 5 and sg[1].is_data() and sg[3].is_data():
            result.append((sg[1].get_data().strip(), sg[3].get_data().strip()))
        elif len(sg) == 4 and sg[2].is_data():
            result.append(("top-tag", sg[2].get_data().strip()))
        else:
            print("WARNING: unexpected pattern in HTML layout found: ")
            for e in sg:
                print(e) 
    return result

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

def split_by_portions(l, sz):
    res = []
    for i in range(0, len(l), sz):
        res.append(l[i: i+sz])

    return res


ARGS = parse_args()

CONFIG = configparser.ConfigParser()
if len(CONFIG.read('config.ini')) == 0:
    print('No config.ini file')
    sys.exit(1)

try:
    PROFILE = CONFIG.get('Firefox', 'profile')
except configparser.NoSectionError as e:
    print('No section [Firefox] in config file')
    sys.exit(1)
except configparser.NoOptionError as e:
    PROFILE = None

if PROFILE != None and not os.path.isdir(PROFILE):
    print('Profile is not directory')
    sys.exit(1)


try:
    REPLY_TIMEOUT = int(CONFIG.get('Timeouts', 'load-reply')) / 1000.0
except configparser.NoSectionError as e:
    print('No section [Timeouts] in config file')
    sys.exit(1)
except configparser.NoOptionError as e:
    print('No property load-reply in section [Timeouts]')
    sys.exit(1)

try:
    SEND_TIMEOUT = int(CONFIG.get('Timeouts', 'send-mail')) / 1000.0
except configparser.NoSectionError as e:
    print('No section [Timeouts] in config file')
    sys.exit(1)
except configparser.NoOptionError as e:
    print('No property load-reply in section [Timeouts]')
    sys.exit(1)

try:
    PER_ACCOUNT = int(CONFIG.get('Limits', 'mail-sends-per-account'))
except configparser.NoSectionError as e:
    print('No section [Limits] in config file')
    sys.exit(1)
except configparser.NoOptionError as e:
    print('No property mail-sends-per-account in section [Limits]')
    sys.exit(1)



print(get_lines(ARGS.urls_file))

posts = []
root = ET.Element('root')

for url in get_lines(ARGS.urls_file):
    print("Downloading %s" % url)

    post_paths = refs_to_entries(download(url))

    for ppath in post_paths:
        purl = with_path(url, ppath)

        print("Processing %s" % purl)

        marks = MarksCollector.get_all(download(purl))

        h2_marks = marks_inside_ptitle(marks)

        h2_marks = drop_empty_data(h2_marks)

        small = get_small_data(h2_marks)
        price = get_price_data(h2_marks)
        name = get_title_data(h2_marks)
        title = merge_title(name, price, small)

        #print(small, price, name, title, sep = '|||' )

        if title == None:
            print("Skipping (no title)")
            continue

        post = Post(purl, title, name, price, small)

        for ab in attrgroups_bounds(marks):
            for attr in parse_attrgroup(marks, ab):
                post.append_tag(attr[0], attr[1])

        posts.append(post)

for p in posts:
    p.create_xml_node(root)

write_file(ARGS.output_xml, pretty(root))

print()
print("Starting E-mail extraction")
print("Profile: %s" % PROFILE)
if PROFILE == None:
    browser = webdriver.Firefox()
else:
    fp = webdriver.FirefoxProfile(PROFILE)
    browser = webdriver.Firefox(fp, proxy=None)

for i, p in enumerate(root):
    url = p.attrib['url']

    browser.get(url)

    try:
        browser.find_element_by_class_name("reply_button").click()
    except selenium.common.exceptions.NoSuchElementException:
        print("No reply button. Skipping")
        continue

    time.sleep(REPLY_TIMEOUT)
    response = browser.page_source

    marks = MarksCollector.get_all(response)
    ind = elem_index(marks, lambda x: is_open_tag(x, 'a', 'mailapp'))
    if ind == -1:
      print("WARNING: no E-mail for " + url)
      continue

    mail_address = marks[ind+1].get_data()
    p.attrib['email'] = mail_address
    print(mail_address)     

write_file(ARGS.output_xml, pretty(root))

with open(ARGS.msg_file) as f:
    msg_text = f.read()

msg_text_orig = msg_text

required_name = msg_text.find('<<NAME>>') != -1
required_top_tag = msg_text.find('<<TOP-TAG>>') != -1

section_names = map(lambda e: e[0], CONFIG.items())
dotted_mail_sections = filter(re.compile(r"^E-mail\.[0-9]+$").match, section_names)

dms_list = list(dotted_mail_sections)

if len(dms_list) > 0:
    suffixes = map(lambda e: int(e[7:]), dms_list)
    indexes = sorted(suffixes)
    print(indexes)
    accounts = map(lambda e: MailSettings(CONFIG, 'E-mail.%s' % e), indexes)
 
else:
    accounts = map(lambda e: MailSettings(CONFIG, 'E-mail'), [None])

accounts = cycle(accounts)


for portion in split_by_portions(root, PER_ACCOUNT):
    login_ok = False
    while not login_ok:
        next_account = head(accounts)
        print("Send via %s (login %s)" % (next_account.server, next_account.login))

        server = smtplib.SMTP(next_account.server)
        server.ehlo()
        server.starttls()
        try:
            server.login(next_account.login, next_account.password)
            login_ok = True
        except smtplib.SMTPDataError:
            print("Unable to login. Try next...")

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
            "From: " + next_account.from_addr,
            "To: " + p.attrib['email'],
            "Subject: " + subject,
            "",
            msg_text
        ])

        print("sending to %s" % to_addr)
        send_counter = 0
        while True:
            try:
                server.sendmail(next_account.from_addr, to_addr, msg)
                print("OK")
                break
            except UnicodeEncodeError:
                print("Contins non-ASCII chars. Skipped")
                break
            except smtplib.SMTPDataError:
                print("Send rejected ")
                if send_counter < 5:
                    time.sleep(SEND_TIMEOUT)
                    print("Try again...")
                    send_counter = send_counter + 1
                else:
                    print("Skipped")
                    break


        time.sleep(SEND_TIMEOUT)

    server.quit()

