import ffmpy
import subprocess
import json
from bs4 import BeautifulSoup
import re

# RTSPlINK = "rtsp://root:pass@192.168.8.153/axis-media/media.amp"
# RTSPlINK ="rtsp://root:password@192.168.8.242/axis-media/media.amp"
RTSPlINK = "rtsp://admin:admin@172.16.20.12/cam/realmonitor?channel=1&subtype=0"
# RTSPlINK  = "rtsp://172.16.20.14/h264"


GETIMAGE = ffmpy.FFprobe(
    inputs={RTSPlINK:None},
    global_options=[
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format', '-show_streams']
).run(stdout=subprocess.PIPE)

extract = re.sub(r'([\\r\\n])',"",str(GETIMAGE))


meta = json.loads(GETIMAGE[0].decode('utf-8'))

for xxx in meta["streams"]:
    resolutionWidth = xxx["width"]
    resolutionHeight = xxx["height"]
    print str(resolutionWidth)+","+str(resolutionHeight)

# print str(meta["streams"]["width"])
