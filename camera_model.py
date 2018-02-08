import ast
import math
import re

import numpy as np
import psycopg2
from shapely import wkb
from shapely.affinity import rotate
from shapely.geometry import Polygon
from shapely.wkt import dumps

## get the camera rotation matrix
## start with the camera model

## input xy position of the screen and get the realworld coordinate in return
def realworldXY(ScreenX,ScreenY,transformM):

    ## need to include the shearing matrix into
    a = transformM[0]
    b = transformM[1]
    c = transformM[2]
    d = transformM[3]
    e = transformM[4]
    f = transformM[5]
    g = transformM[6]
    h = transformM[7]

    realX = (a*ScreenX+b*ScreenY+c)/(g*ScreenX+h*ScreenY+1)
    realY = (d*ScreenX+e*ScreenY+f)/(g*ScreenX+h*ScreenY+1)


    return (realX,realY)

## Store the transformation
def Store_transformM(transformM,cam_uid):
    db="osi_social_db"
    dbuser="postgres"
    dbpassword=""
    dbhost="192.168.8.12"
    dbport="5432"

    transCointainer = []
    ## update the transformation matrix to remove the white space and replace with a comma
    for number in transformM:
        transCointainer.append(number)


    convertmatrix = str(transCointainer)
    convertmatrixA = convertmatrix.lstrip("[")
    convertmatrixB = convertmatrixA.rstrip("]")

    ## Load data from postgres
    db = psycopg2.connect(database=db, user=dbuser, password=dbpassword, host=dbhost, port=dbport)
    ## check if the data exist
    cursor = db.cursor()

    UpdateStatement = """update osi_camera
                            set transformation_matrix = %s
                            where camera_uid = %s;"""
    act_sql = cursor.mogrify(UpdateStatement, (str(convertmatrixB), cam_uid))
    # print act_sql
    cursor.execute(act_sql)
    db.commit()


## get camera footprint
def getCameraFOOTPrint():
    db="osi_social_db"
    dbuser="postgres"
    dbpassword=""
    dbhost="192.168.8.12"
    dbport="5432"

    ## Load data from postgres
    db = psycopg2.connect(database=db, user=dbuser, password=dbpassword, host=dbhost, port=dbport)

    ## extract the floor plan to compare
    cursor = db.cursor()
    cursor.execute("""select * from "osi_camera";""") ## <== get the floor from the floor plan
    footprintA = cursor.fetchall()

    del cursor
    del db
    return (footprintA)




def transformationMatrix(footprint,TVgrid):
    ## drop the element to 4 instead of 5 received in the array.
    ## use the example from
    ##  http://www.corrmap.com/features/homography_transformation.php
    ##  this example works in python

    footprint2 = footprint[0:4]

    ## x4,y2 ------------ x3,y2
    ##   |    (x4+x3)/2    |
    ##    |              |
    ## x2,y1 ---------- x1,y1
    ##  Big x and y in the sample
    x4,y2 = footprint[0]
    x3,y2 = footprint[1]
    x1,y1 = footprint[2]
    x2,y1 = footprint[3]


    ## TVgrid POINTS
    ## small x and y in the example

    TX4,TX3,TX1,TX2 = TVgrid[0]
    TY4,TY3,TY1,TY2 = TVgrid[1]

    matrixA = np.array([[TX4,TY4,1,0,0,0,-TX4*x4,-TY4*x4],
                [TX3,TY3,1,0,0,0,-TX3*x3,-TY3*x3],
                [TX1,TY1,1,0,0,0,-TX1*x1,-TY1*x1],
                [TX2,TY2,1,0,0,0,-TX2*x2,-TY2*x2],
                [0,0,0,TX4,TY4,1,-TX4*y2,-TY4*y2],
                [0,0,0,TX3,TY3,1,-TX3*y2,-TY3*y2],
                [0,0,0,TX2,TY2,1,-TX2*y1,-TY2*y1],
                [0,0,0,TX1,TY1,1,-TX1*y1,-TY1*y1]])

    ## output matrix in real world coordinate system
    O_matrix = np.array([x4,x3,x1,x2,y2,y2,y1,y1])
    ## use python matrix solver to get the transformation matrix.
    TMatrix = np.linalg.solve(matrixA,O_matrix)


    return TMatrix



if __name__ == '__main__':
    ## Screen resolution related
    ## obtain the resolution from json
    # screen_resolution=[1920,1200]
    # midX = screen_resolution[0]/2
    # midY = screen_resolution[1]/2

    sX = 1194
    sY = 879

    objectPixelH = 310

    ## 4 points


    for cameras in getCameraFOOTPrint():

        cam_uid = cameras[2]
        cam_height = cameras[8]

        screen_resolution = cameras[24].split(",")
        ScreenX = int(screen_resolution[0])
        ScreenY = int(screen_resolution[1])


        TVgrid = [[0,ScreenX,ScreenX, 0],
		[0,0,ScreenY,ScreenY]]

        camerapoint = wkb.loads(cameras[0],True)
        camX = camerapoint.xy[0]
        camY = camerapoint.xy[1]

        ## Check if footprint exist
        if cameras[22] is not None:
            # footprint =  ast.literal_eval(cameras[20])
            ## get the footprint pre ops.
            footprint =  ast.literal_eval(cameras[22])
            

            ## transformation matrix
            transformM = transformationMatrix(footprint,TVgrid)
            # print transformM

            Store_transformM(transformM,cam_uid)

    