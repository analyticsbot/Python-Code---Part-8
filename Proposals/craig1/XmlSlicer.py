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


slice_size = int(sys.argv[1])
src_xml = sys.argv[2]
dest_dir = sys.argv[3]

tree = ET.parse(src_xml)
root = tree.getroot()

ind_ranges = list(range(0, len(root), slice_size))
ind_ranges2 = ind_ranges[1:] + [len(root)]

print(ind_ranges)
print(ind_ranges2)
  
if os.path.exists(dest_dir):
  shutil.rmtree(dest_dir)

os.mkdir(dest_dir)
src_basename = os.path.basename(src_xml)

for (i, (i1, i2)) in enumerate(zip(ind_ranges, ind_ranges2)):
  new_root = ET.Element(root.tag)
  dest_file = os.path.join(dest_dir, str(i+1) + '-' + src_basename)
  print(dest_file)
  for p in root[i1:i2]:
    new_root.append(p)
  tofile(dest_file, pretty(new_root))
  


