# This code is for reading out the .csv files and putting them in to 1 3D Array.
# Also the defect data files, in terms of that one frame is split on multiple files, have to be repaired.
import csv
import os
import math


####################### Task 1 and 2
#### read in files
#### resort the array by azimuth and laser id
#### [array sorted by azimuth and laser id, without defect points]

# Read files in folder 'laser_scanner_data' and sort data in each file by "laser_id" and "azimuth"
# Return an python list of all 2D Array of each file
def read_files():
    path = 'laser_scanner_data'  # folder path of data files
    size_threshold = 1520000  # for defect frame
    datas = []

    # loop for all files in the given directory. That directory should contain only the data.
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)) and os.path.getsize(
                os.path.join(path, filename)) < size_threshold:
            print("Opening file " + filename)

            # reading file
            full_path = path + '/' + filename
            csv_data = csv.reader(open(full_path), delimiter=',')
            next(csv_data, None)  # Skip the header line

            lines = []  # array of all raw
            # itering over raw in csv
            for raw in csv_data:
                lines.append([float(c) for c in raw])

            # sort data by "laser_id" and "azimuth" (respectively row[4] and row[5])
            lines = sorted(lines, key=lambda row: (row[4], row[5]))  # , reverse=True
            datas.append(lines)

    return datas


####################### Task 3
#### find background by comparing same points (depending on laser id, azimuth)
#### [array without the background]

# Check if 2 points are the same or not, regarding the pair (laser_id, azimuth).
# Return true (if they are the same) or false (otherwise).
def equals(pt1, pt2):
    if (pt1[0] == pt2[0] and pt2[1] == pt2[1] and pt1[2] == pt2[2]):
        return True
    else:
        return False


# return id1 < id2 (is line 1 lower in index than line 2 ?)
def is_inf(id1, id2):
    if id1[4] == id2[4]:
        return id1[5] < id2[5]
    return id1[4] < id2[4]


# return index of a point in an frame
# None if the point is not in the frame
# point is identtified by the tuple (laser_id, azimuth)
def getPoint(id, frame):
    l = 0
    r = len(frame) - 1
    while l <= r:
        m = (int)((l + r) / 2)
        if is_inf(frame[m], id):
            l = m + 1
        elif is_inf(id, frame[m]):
            r = m - 1
        else:
            return m
    return None


# Clean all background points identified by "Laser_id" and "azimuth"
# Background points have constant coordonates in each file.
# returns an array without this background point
def clean_background(datas):
    background_p = []
    # we compare each points of this frame with other frame
    # to detect background point
    refFrame = datas[0]
    # loop over each point in reference frame
    for point in refFrame:
        isBakgd = True
        # we check if this point is in all frame
        # and if his position change
        frames = iter(datas)
        next(frames)  # skip comparaison with reference frame
        for frame in frames:
            i = getPoint(point, frame)
            # if p is not in the frame or with different coordonates
            # it is not a background point
            if i == None or not equals(point, frame[i]):
                isBakgd = False
                break  # the point is not in this frame -> not a background point
        if isBakgd:
            background_p.append(point)
        # print(str(point[4])+","+str(point[5])) # debug

    # print("number of background point: "+str(len(background_p))) # debug

    # Delete background points found in datas
    for p in background_p:
        for frame in datas:
            del frame[getPoint(p, frame)]
    # datas are already cleaned but we return also a reference to this object
    return datas


####################### Task 4
#### find closures
#### [2D array with the points of each closure]

# Return the distance between 2 points.
# Each point has 3 coordinates (x, y, z).
def distance(pt1, pt2):
    coord_x = pt1[0] - pt2[0]
    coord_y = pt1[1] - pt2[1]
    coord_z = pt1[2] - pt2[2]
    sum_square = coord_x * coord_x + coord_y * coord_y + coord_z * coord_z

    return math.sqrt(sum_square)


## Determine if a point is in object
# point: corresponding to a line in a frame file
# obj: list of point in an object
# dist: distance in float number, determining the maximal
# distance to be part of an object
def isPointInObj(point, obj, dist):
    for p in obj:
        if distance(point, p) < dist:
            return True
    return False


# return objects found in a frame
# an objects is a list of points
# /!\ Fonction still in developement
def getClosure(frame):
    objs = []  # list of closures

    return objs


#######################
#### Main Program

def main():
    datas = read_files()

    print("nb of point in frame 0 :" + str(len(datas[0])))
    clean_background(datas)
    print("and after cleaning background :" + str(len(datas[0])))


if __name__ == "__main__":
    main()