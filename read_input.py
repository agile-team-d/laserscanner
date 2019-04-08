# This code is for reading out the .csv files and putting them in to 1 3D Array.
# Also the defect data files, in terms of that one frame is split on multiple files, have to be repaired.

import csv
import os

no_frames = 700             # bigger than the actual number
no_points = 20000           # the actual number is not fixed per frame, but smaller than 20000 in any case
no_coordinates = 3          # x,y,z -> 3 coordinates per point
size_threshold = 1520000    # threshold for the detection of defect frames
path ='laser_scanner_data'  # path of the folder with the data

# use of the data type range because integer is not iterable
Data = [[[0 for k in range(no_coordinates)] for j in range(no_points)] for i in range(no_frames)]

# initialization values for the loop. All 'false' or 0.
frame_count, defect_size, defect_line_offset = 0, 0, 0
defect_1_flag, defect_2_flag = False, False

# loop for all files in the given directory. That directory should contain only the data.
for filename in os.listdir(path):

    if os.path.isfile(os.path.join(path, filename)):

        # measures the size of on file
        size = os.path.getsize(os.path.join(path, filename))
        defect_size= defect_size + size     # summation of the size of neighbored defect frames
        if defect_size < size_threshold:
            defect_1_flag = True
            #print(filename) #DEBUG
            #print(size) #DEBUG
        else:
            defect_1_flag = False

        full_path= path + '/' + filename
        with open(full_path) as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # first line is different (header)
                if line_count == 0:
                    line_count += 1
                else:
                    # filling the data array
                    Data[frame_count][line_count+defect_line_offset-1][0]={row[0]}
                    Data[frame_count][line_count+defect_line_offset-1][1]={row[1]}
                    Data[frame_count][line_count+defect_line_offset-1][2]={row[2]}

                    line_count += 1

        #print(Data[frame_count][3][1]) #DEBUG

        # setup for the next iteration. Depending of if defect correction is necessary.
        if defect_1_flag == True:
            defect_line_offset = defect_line_offset + line_count - 1
            #print(defect_line_offset) #DEBUG
        else:
            defect_line_offset = 0
            defect_size = 0
            frame_count += 1

#print('Finish to read in the data.')