#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      thomas
#
# Created:     09/02/2018
# Copyright:   (c) thomas 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import os,io
from collections import Counter

import itertools
from operator import itemgetter
from itertools import groupby
from collections import OrderedDict



def PartA(readdetail):
    cam_container = []

    for jsondetail in readdetail:
##        print"==> "+ str(jsondetail)
        detectionList = jsondetail['detection']
        camera_id = jsondetail['camera_id']
        timeStamp = jsondetail['time']
        resolution_width = jsondetail['resolution_width']
        resolution_height = jsondetail['resolution_height']
        frame_No = jsondetail['frame']


        framesCombo = []
        detectionList.sort(key=itemgetter('type'))
        for typeGet, items in groupby(detectionList, key=itemgetter('type')):
##            print typeGet

            reformA=[]
            for i in items:
                CoordI = i['coordinate']
                TWidth = i['width']
                IHeight = i['height']
                groupA = {"coordinate":str(CoordI),
                        "height":IHeight,
                        "width":TWidth}
                reformA.append(groupA)

            ## group2
            groupingB = {"frame":frame_No,"type": typeGet,"detections": reformA}


            framesCombo.append(groupingB)


        out = {"frames":framesCombo,"time":timeStamp,"resolution_width":resolution_width,"resolution_height":resolution_height,"camera_id":camera_id}
        cam_container.append(out)


##            json.dump(unicode(out), outfile)
##            outfile.write(u"\n")

    body = {"time":timeStamp,"cameras":cam_container}

    sortkey =(
            "time",
            "cameras",
            'frames',
            'time',
            'resolution_width',
            'resolution_height',
            'camera_id',
        )

    sortResult = json.dumps(OrderedDict(body),sortkey)
##    fd = open(r"D:\github\data\hjklasd.json","w")
    with open(r"D:\github\data\hjklasd.json", 'w') as outfile:
        json.dump(sortResult, outfile)
##        print sortResult










if __name__ == '__main__':
    ## rEAD JSON
    inputjsonlink = r"D:\github\data\Camera-Bullet-6\all_detections\all_osi_camera.dahua-bullet-6_1517877479.json"
    readdetail = json.load(open(inputjsonlink))

    PartA(readdetail)






