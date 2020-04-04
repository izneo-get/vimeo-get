import requests
import base64
import re
import math
import os
import sys
from urllib.parse import urljoin
from tabulate import tabulate

if len(sys.argv) < 2:
    print("Usage: ")
    print(sys.argv[0] + " <MASTER_JSON_URL>")
    exit()

master_json_url = sys.argv[-1]
output_folder = os.path.dirname(os.path.abspath(sys.argv[0])) + "/tmp"
if not os.path.exists(output_folder): os.mkdir(output_folder)

resp = requests.get(master_json_url)
content = resp.json()
base_url = urljoin(master_json_url, '.') + (content['base_url'] if 'base_url' in content else '')

all_elems = {}
header = ["mime_type", "codecs", "bitrate", "avg_bitrate", "duration", "framerate", "width", "height", "channels", "sample_rate"]
i = 1
stream_id = {}
for stream_type in ("video", "audio"):
    all_items = []
    local_elems = {}
    if stream_type in content:
        for elem in content[stream_type]:
            # print(f"[{i}] ID {elem['id']}")
            all_elems[str(i)] = elem
            local_elems[str(i)] = i
            item = [i]
            {item.append(elem[e] if e in elem else '') for e in header}
            all_items.append(item)
            i = i + 1
    print(tabulate(all_items, headers=['ID']+header))

    stream_id[stream_type] = ''
    while stream_id[stream_type] not in local_elems and stream_id[stream_type].lower() != 's':
        stream_id[stream_type] = input("Stream ID you want to grab ('S' to skip): ")

filename = {}
for stream_type in ("video", "audio"):
    if stream_type in stream_id and stream_id[stream_type] in all_elems:
        elem = all_elems[stream_id[stream_type]]
        filename[stream_type] = stream_id[stream_type] + '_' + elem['id'] + '_' + re.sub(r'[^\w\-_\. ]', '_', elem['mime_type']) + '.tmp'
        print(f"Writing to '{filename[stream_type]}'")
        my_file = open(output_folder + '/' + filename[stream_type], 'wb')

        init_segment = base64.b64decode(elem['init_segment'])
        my_file.write(init_segment)
        total = len(elem['segments']) - 1
        for i, segment in enumerate(elem['segments']):
            pct = math.floor(i * 100 / total)
            print(f"\r[{pct} %] {i} / {total}", end="")
            segment_url = base_url + elem['base_url'] + segment['url']
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


param_video = f"-i \"{output_folder}/{filename['video']}\"" if 'video' in filename else ''
param_audio = f"-i \"{output_folder}/{filename['audio']}\"" if 'audio' in filename else ''
file_ext = "mka" if 'video' not in filename else 'mkv'
if param_audio or param_video:
    print(f"ffmpeg {param_video} {param_audio} -c copy output.{file_ext}")