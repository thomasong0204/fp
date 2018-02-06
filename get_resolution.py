import ffmpy
import subprocess
import json
from bs4 import BeautifulSoup
import re

# RTSPlINK = "rtsp://root:pass@192.168.8.153/axis-media/media.amp"
# RTSPlINK ="rtsp://root:password@192.168.8.242/axis-media/media.amp"
RTSPlINK = "rtsp://admin:admin@172.16.20.12/cam/realmonitor?channel=1&subtype=0"
# RTSPlINK  = "rtsp://172.16.20.14/h264"


def CameraResolution(stream_url):
    try:
        GETIMAGE = ffmpy.FFprobe(
            inputs={stream_url:None},
            global_options=[
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format', '-show_streams']
        ).run(stdout=subprocess.PIPE)

        # extract = re.sub(r'([\\r\\n])',"",str(GETIMAGE))

        meta = json.loads(GETIMAGE[0].decode('utf-8'))
        resExtract = str()

        for xxx in meta["streams"]:
            resolutionWidth = xxx["width"]
            resolutionHeight = xxx["height"]
            resExtract = str(resolutionWidth)+","+str(resolutionHeight)

    except Exception:
        resExtract = str("0,0")


    
    return resExtract



if __name__ == '__main__':

    db="osi_social_db"
    dbuser="postgres"
    dbpassword=""
    dbhost="192.168.8.12"
    dbport="5432"

    ## Load data from postgres
    db = psycopg2.connect(database=db, user=dbuser, password=dbpassword, host=dbhost, port=dbport)

    ## extract the floor plan to compare
    cursor = db.cursor()
    cursor.execute("""select * from "osi_camera";""") ## <== get the whole content of fixed lens camera
    CameraList = cursor.fetchall()
    for camera in CameraList:
        stream_url = camera[7]

    CameraResolution

