import xml.etree.ElementTree as ET
import sys
import shutil
import os
from xml.dom import minidom

def pretty(root):
  return '\n'.join([s for s in minidom.parseString(ET.tostring(root)).toprettyxml().split('\n') if len(s.strip()) > 0])

def tofile(name, s):
  with open(name, 'w') as f:
    f.write(s)


dest_xml = sys.argv[1]
src_xmls = sys.argv[2:]

src_trees = [ET.parse(s) for s in src_xmls]


new_root = ET.Element(src_trees[0].getroot().tag)
roots = [list(t.getroot()) for t in src_trees ]



nodes = sum(roots, [])
print(len(nodes))

for p in nodes:
  new_root.append(p)

tofile(dest_xml, pretty(new_root))
