# -*- coding: utf-8 -*-
__version__ = "0.01"

import requests
import base64
import re
import math
import os
import sys
from urllib.parse import urljoin
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: ")
    print(sys.argv[0] + " <MASTER_M3U_URL> [FILE_OUT]")
    exit()

file_out_name = ''
if len(sys.argv) > 2:
    file_out_name = sys.argv[2]


master_m3u_url = sys.argv[1]
output_folder = os.path.dirname(os.path.abspath(sys.argv[0])) + "/tmp"
if not os.path.exists(output_folder): os.mkdir(output_folder)

resp = requests.get(master_m3u_url)
content = resp.text.split('\n')

all_elems = {}
index = 1
for i, line in enumerate(content):
    if len(line) and line[0] != '#':
        header_items = content[i - 1].split(':')[-1]
        print(f"{index} : {header_items}")
        all_elems[str(index)] = line
        index = index + 1


stream_id = ''
while stream_id not in all_elems and stream_id.lower() != 's':
    stream_id = input("Stream ID you want to grab ('S' to skip): ")

if stream_id not in all_elems:
    exit()

resp = requests.get(all_elems[stream_id])
urls = resp.text.split('\n')
urls_clean = []
{urls_clean.append(l) for l in urls if len(l) and l[0] != '#'}
base_url = urljoin(all_elems[stream_id], '.')
ext = urls_clean[0].split('?')[0].split('.')[-1]

filename = file_out_name if len(file_out_name) else datetime.today().strftime('%Y%m%d_%H%M%S') + '_' + str(stream_id) + '.' + ext
print(f"Writing to '{filename}'")
my_file = open(output_folder + '/' + filename, 'wb')

total = len(urls_clean) - 1
for i, segment_url in enumerate(urls_clean):
    pct = math.floor(i * 100 / total)
    print(f"\r[{pct} %] {i} / {total}", end="")
    if not segment_url.lower().startswith('http://') and not segment_url.lower().startswith('https://'):
        segment_url = base_url + '/' + segment_url
    resp = requests.get(segment_url, stream=True)
    if resp.status_code != 200:
        print('not 200!')
        print(resp)
        print(segment_url)
        break
    for chunk in resp:
        my_file.write(chunk)
        my_file.flush()

my_file.close()
print()
print("Done!")
print()
print("You can clean your file with:")
new_filename = '.'.join(filename.split('.')[0:-1]) + '.mkv'
print(f"ffmpeg -i \"{output_folder}/{filename}\" -map 0 -c copy \"{output_folder}/{new_filename}\"")

