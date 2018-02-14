import ffmpy
import subprocess
import json
from bs4 import BeautifulSoup
import re
import psycopg2


def connectiondb():
    db="osi_social_db"
    dbuser="postgres"
    dbpassword=""
    dbhost="192.168.8.12"
    dbport="5432"
    ## Load data from postgres
    db = psycopg2.connect(database=db, user=dbuser, password=dbpassword, host=dbhost, port=dbport)
    ## extract the floor plan to compare
    cursor = db.cursor()
    return cursor



def updatedb(resolution,camera_UID):
    db="osi_social_db"
    dbuser="postgres"
    dbpassword=""
    dbhost="192.168.8.12"
    dbport="5432"
    ## Load data from postgres
    db = psycopg2.connect(database=db, user=dbuser, password=dbpassword, host=dbhost, port=dbport)
    ## extract the floor plan to compare
    cursor = db.cursor()

    UpdateStatement = """update osi_camera set camera_res = '%s' where camera_uid = '%s'"""
    cursor.execute(UpdateStatement % (resolution,camera_UID))
    db.commit()
    print "update: "+ str(camera_UID)

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


    cursor = connectiondb()
    cursor.execute("""select * from osi_camera;""") ## <== get the whole content of fixed lens camera
    CameraList = cursor.fetchall()

    for camera in CameraList:
        stream_url = camera[7]
        camera_UID =camera[2]
        ResResult = CameraResolution(stream_url)
        updatedb(ResResult,camera_UID)
        # print("update cameraid: "+camera_UID)



