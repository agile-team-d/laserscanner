import csv

# read out the csv and put it into an array
start_frame = 120
no_frames = 100
no_points = 20000 # the actual number is not fixed per frame
no_coordinates = 3


# range because integer is not iterable
Data = [[[0 for k in range(no_coordinates)] for j in range(no_points)] for i in range(no_frames)]

frame_count = 0

for i in range(no_frames):
    temp_name= 'laser_scanner_data/laser_scanner_data (Frame 0' + str(start_frame + frame_count) + ').csv'

    with open(temp_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}') #DEBUG
                line_count += 1
            else:
                #if line_count < 100:
                #   print(f'\t x: {row[0]} \t y: {row[1]} \t z: {row[2]}.')

                Data[frame_count][line_count-1][0]={row[0]}
                Data[frame_count][line_count-1][1]={row[1]}
                Data[frame_count][line_count-1][2]={row[2]}

                # if line_count < 100:
                #     xTemp=Data[frame_count][line_count-1][0]
                #     yTemp=Data[frame_count][line_count-1][1]
                #     zTemp = Data[frame_count][line_count - 1][2]
                #     sTemp = '\t x: ' + str(xTemp) +' \t y: '+ str(yTemp)+' \t z: '+ str(Data[frame_count][line_count-1][2])
                #     print(sTemp)

                line_count += 1

    #print(frame_count)
    #print(Data[frame_count][3][1])
    #print(f'Processed {line_count} lines.')

    frame_count += 1