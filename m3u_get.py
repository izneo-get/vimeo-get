# -*- coding: utf-8 -*-
__version__ = "0.01"

import requests
import base64
import re
import math
import os
import sys
from urllib.parse import urljoin
from urllib.parse import urlparse
from datetime import datetime

if __name__ == "__main__":
    file_out_name = ''
    is_command_line = False
    if len(sys.argv) == 1:
        # Interactive mode.
        m3u_url = input("M3U URL : ")
        if m3u_url[0] == '"' and m3u_url[-1] == '"':
            m3u_url = m3u_url[1:-1]
        file_out_name = input("File out (optional) : ")
    else:
        # Command line mode.
        is_command_line = True
        m3u_url = sys.argv[1]
        if len(sys.argv) > 2:
            file_out_name = sys.argv[2]



    output_folder = os.path.dirname(os.path.abspath(sys.argv[0])) + "/tmp"
    if not os.path.exists(output_folder): os.mkdir(output_folder)


    resp = requests.get(m3u_url)
    urls = resp.text.split('\n')
    urls_clean = []
    {urls_clean.append(l) for l in urls if len(l) and l[0] != '#'}
    base_url = urljoin(m3u_url, '.')
    ext = urls_clean[0].split('?')[0].split('.')[-1]
    stream_id = '.'.join(os.path.basename(urlparse(m3u_url).path).split('.')[0:-1])
    filename = file_out_name if len(file_out_name) else datetime.today().strftime('%Y%m%d_%H%M%S') + '_' + str(stream_id) + '.' + ext
    if not filename.endswith('.' + ext):
        filename = filename + '.' + ext
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
    command_line = f"ffmpeg -i \"{output_folder}/{filename}\" -map 0 -c copy \"{output_folder}/{new_filename}\""
    print(command_line)

    if is_command_line == False:
        answer = ""
        while answer not in ["O", "Y", "N"]:
            answer = input("Execute this command line ([Y]es / [N]o) ? ").upper()
        if answer.upper() in ["Y", "O"]:
            os.system(command_line)
    
    if is_command_line == False:
        os.system("pause")

