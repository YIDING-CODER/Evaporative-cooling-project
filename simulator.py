import pandas as pd
import numpy as np
from adjustText import adjust_text
import os

# Read the configuration file
import configparser
config = configparser.ConfigParser()
config.read('configure.ini')

AUTO_GENERATE_OCCUPANTS=config["SETTING"].getboolean("AUTO_GENERATE_OCCUPANTS")
ADJUST_TEXT=config["SETTING"].getboolean("ADJUST_TEXT")
MAIN_TITLE=config["CHART"]["MAIN_TITLE"]
ROOM_TITLE=config["CHART"]["ROOM_TITLE"]
CHART2_TITLE=config["CHART"]["CHART2_TITLE"]
CHART3_TITLE=config["CHART"]["CHART3_TITLE"]
MAX_OCCUPANCY=int(config["PARAMETERS"]["MAX_OCCUPANCY"])
EXPORT=config["CHARTEXPORT"].getboolean("EXPORT")
START_FRAME=int(config["CHARTEXPORT"]["START_FRAME"])
END_FRAME=int(config["CHARTEXPORT"]["END_FRAME"])
LEFT=float(config["CHARTSETTING"]["LEFT"])
BOTTOM=float(config["CHARTSETTING"]["BOTTOM"])
RIGHT=float(config["CHARTSETTING"]["RIGHT"])
TOP=float(config["CHARTSETTING"]["TOP"])
HSPACE=float(config["CHARTSETTING"]["HSPACE"])
# Create folder if not existed
if not os.path.exists('data/images'):
    os.makedirs('data/images')

# some default setting of the charts
circle_r=3
circle_c=4
circle_x=circle_y=circle_c
# Size of the dot
occupancy_size=80
# number of time intervals to display in chart
num_date=10

import matrix_generator
import helper_function
tempatature_df_final=matrix_generator.get_matrix(AUTO_GENERATE_OCCUPANTS,MAX_OCCUPANCY)
tempatature_df_final["Positions"]=tempatature_df_final["OccupancyCount"].apply(lambda x:helper_function.generate_position(x,circle_x,circle_y,circle_r))

import matplotlib.pyplot as plt
plt.rcParams['toolbar'] = 'toolmanager'
import matplotlib.patches as patches
from animation_player import Player,GroupHideTool


# Create figure and axes
fig, ax = plt.subplots(figsize=(12,15))
fig.suptitle(MAIN_TITLE, fontsize=12)

current_time=fig.text(0.82, 0.946,"Current Time") # a text element to represent the current time

# Section 1: Room Chart
room = plt.subplot(221)
room.set_title(ROOM_TITLE, fontsize=12)
room.set_xlim([0, circle_c*2])
room.set_ylim([0, circle_c*2])
room.set_aspect(1)
# Add cicle area
circle = patches.Circle((circle_x,circle_y),circle_r,color='#F5F5F5',zorder=0)
room.add_patch(circle)


# Add addtional text for the PreviousTemperature and CurrentTemperature
temperature_change_label=room.text(circle_x-1, -1, 'Temperature')


# Use dots to represent occupants for next five intervals
scat=room.scatter([], [], color='r',s=occupancy_size,label="Current")
next_occupancy=room.scatter([], [], color='orange',s=occupancy_size,label="Next1")
next2_occupancy=room.scatter([], [], color='yellow',s=occupancy_size,label="Next2")
next3_occupancy=room.scatter([], [], color='grey',s=occupancy_size,label="Next3")
next4_occupancy=room.scatter([], [], color='blue',s=occupancy_size,label="Next4")
room.legend([scat,next_occupancy,next2_occupancy,next3_occupancy,next4_occupancy],
            [scat.get_label(),next_occupancy.get_label(),next2_occupancy.get_label(),
             next3_occupancy.get_label(),next4_occupancy.get_label()],bbox_to_anchor=(-0.1, 1))

# Add nozzles  to home chart

# stage1 nozzles
nozzles_set1=[] #use an array to store nozzles
nozzles_positions_set1=helper_function.get_nozzles_position(circle_x,circle_y,circle_r) # get the positions for 9 nozzles
for num in range(9):
    # get position for each nozzles
    x,y,rotate=nozzles_positions_set1[num]
    # each nozzle is represented by a text element
    nozzles_set1.append(room.text(x,y,"-",gid="nozzles1",color="b",rotation=rotate,fontsize=12,horizontalalignment='center', verticalalignment='center'))

# stage2 nozzles
nozzles_set2=[]
nozzles_positions_set2=helper_function.get_nozzles_position(circle_x,circle_y,circle_r,margin=0.5)
for num in range(9):
    x,y,rotate=nozzles_positions_set2[num]
    nozzles_set2.append(room.text(x,y,"-",gid="nozzles2",color="g",rotation=rotate,fontsize=12,horizontalalignment='center', verticalalignment='center'))

# stage3 nozzles
nozzles_set3=[]
nozzles_positions_set3=helper_function.get_nozzles_position(circle_x,circle_y,circle_r,margin=0.8)
for num in range(9):
    x,y,rotate=nozzles_positions_set3[num]
    nozzles_set3.append(room.text(x,y,"-",gid="nozzles3",color="y",rotation=rotate,fontsize=12,horizontalalignment='center', verticalalignment='center'))

#Section2 Temperature and Occupancy number chart
temperature_chart=plt.subplot(222)
occupancy_chart=temperature_chart.twinx() # create chart which share the x axis

temperature_chart.set_ylim(0,30)
temperature_chart.set_ylabel("Temperature °C")
occupancy_chart.set_ylim(0,MAX_OCCUPANCY+2)
occupancy_chart.set_ylabel("Occupancy Count")
temperature_chart.set_title(CHART2_TITLE, fontsize=12)

# plot two lines and the actual points will be updated in the animation
tem_line, = temperature_chart.plot([],[],'b-', label="Temperature")
occ_line, = occupancy_chart.plot([],[],'g-', label="occupancy")
temperature_chart.legend([tem_line,occ_line], [tem_line.get_label(),occ_line.get_label()],bbox_to_anchor=(1.1, 1),loc='upper left')

# Used for adjust the postion of the value label to prevent the value overlap, and it slow down the processing time.
tem_value=[]
occ_value=[]


# Section 3 Release Period and Active Nozzles chart
release_chart=plt.subplot(212)
nozzle_chart=release_chart.twinx() # create chart which share the x axis

release_chart.set_ylim(0,70)
release_chart.set_ylabel("Release Periods [min]")
nozzle_chart.set_ylim(0,110)
nozzle_chart.set_ylabel("Active nozzles [%]")
release_chart.set_title(CHART3_TITLE, fontsize=12,pad=60)

# Set lines for the charts
release_line, = release_chart.plot([],[],'b--', label="Release Periods(Current T)")
tem_release_line, = release_chart.plot([],[],'g--', label="Release Periods(Increasing or Decreasing T)")
occ_release_line, = release_chart.plot([],[],'y--', label="Release Periods(Ahead of Occupancy Peak)")
nozzle_line, = nozzle_chart.plot([],[],'b:*', label="Active Nozzles (Current T)")
tem_nozzle_line, = nozzle_chart.plot([],[],'g:*', label="Active Nozzles (Increasing or Decreasing T)")
occ_nozzle_line, = nozzle_chart.plot([],[],'y:*', label="Active Nozzles(Ahead of Occupancy Peak)")

# Add legend to the chart
release_lines=[release_line,tem_release_line,occ_release_line,nozzle_line,tem_nozzle_line,occ_nozzle_line]
release_chart.legend(release_lines, [item.get_label() for item in release_lines],bbox_to_anchor=(0.5, 1.20), loc="upper center",ncol=2,fontsize=8)



# Section4 Animation
# update the graph based on the calculated data in the matrix
def plot_simulation(frame):

    # Section1 Room Chart elements updated

    # update the position of occupants
    scat.set_offsets(tempatature_df_final.iloc[frame]["Positions"])
    next_occupancy.set_offsets(tempatature_df_final.iloc[frame+1]["Positions"])
    next2_occupancy.set_offsets(tempatature_df_final.iloc[frame+2]["Positions"])
    next3_occupancy.set_offsets(tempatature_df_final.iloc[frame+3]["Positions"])
    next4_occupancy.set_offsets(tempatature_df_final.iloc[frame+4]["Positions"])

    # Update Stage1 Nozzles
    nozzles_status=helper_function.get_nozzles_status(tempatature_df_final.iloc[frame]["Active Nozzles (Current T)[%]"])
    helper_function.update_nozzles_status(nozzles_set1,nozzles_status)

    # Update Stage2 Nozzles
    nozzles_status_set2=helper_function.get_nozzles_status(tempatature_df_final.iloc[frame]["Active Nozzles(Increasing or Decreasing T)[%]"])
    helper_function.update_nozzles_status(nozzles_set2,nozzles_status_set2)

    # Update Stage3 Nozzles
    nozzles_status_set3=helper_function.get_nozzles_status(tempatature_df_final.iloc[frame]["Active Nozzles(Ahead of Occupancy Peak)[%]"])
    helper_function.update_nozzles_status(nozzles_set3,nozzles_status_set3)

#   Update the previous temperature label for Chart 1
    previous_tem="  "
    if tempatature_df_final.iloc[frame]["PreviousTemperature"] !=0:
        previous_tem=str(tempatature_df_final.iloc[frame]["PreviousTemperature"])
    temperature_change_label.set_text( previous_tem+ " > "+str(tempatature_df_final.iloc[frame]["Temperature"])+" [°C]")

    # update the temparature and Occupancy Count chart
    temperature=list(tempatature_df_final.iloc[frame:frame+num_date]["Temperature"].values)
    occupancy_num=list(tempatature_df_final.iloc[frame:frame+num_date]["OccupancyCount"].values)
    tem_line.set_data(range(frame, frame+num_date),temperature)
    occ_line.set_data(range(frame, frame+num_date),occupancy_num)

    # update the x axis range
    tem_line.axes.set_xlim(frame,frame+num_date-1)
    occ_line.axes.set_xlim(frame,frame+num_date-1)

#     Update the label of x axis from number to actual date
    date_time=list(tempatature_df_final.iloc[frame:frame+num_date]["Time"].dt.strftime("%m/%d %H:%M").values)
    current_time.set_text(date_time[0]) #update current time

    # replace the integer on x axis to date
    temperature_chart.set_xticks(range(frame, frame+num_date))
    temperature_chart.set_xticklabels(date_time,rotation = 90)



    # The matplotlib built-in annotation function doesn't check the text overlap
    # we are using an external library adjustText to rearrange the text when they
    # are overlaped.
    # We create lists to store the text object and then update it for each frame.
    if ADJUST_TEXT:

        if len(tem_value)==0:
            for i in range(num_date):
                tem_value.append(temperature_chart.text(frame+i,temperature[i],temperature[i]))
                occ_value.append(occupancy_chart.text(frame+i,occupancy_num[i],occupancy_num[i]))
        else:
            for i in range(num_date):
                tem_value[i].set_text(temperature[i])
                tem_value[i].set_position((frame+i,temperature[i]))
                occ_value[i].set_text(occupancy_num[i])
                occ_value[i].set_position((frame+i,occupancy_num[i]))
        adjust_text(tem_value+occ_value,ax=ax)
    else:
        # The following code are applied if we are not using the adjustText library
        for i in range(num_date):
            temperature_chart.annotate(temperature[i],xy=(frame+i,temperature[i]))
            occupancy_chart.annotate(occupancy_num[i],xy=(frame+i,occupancy_num[i]))


    # Section 3 update release period and active nozzles chart
    # get the data for each lines
    release=list(tempatature_df_final.iloc[frame:frame+num_date]["Release Periods (Current T)[min]"].values)
    tem_release=list(tempatature_df_final.iloc[frame:frame+num_date]["Release Periods (Increasing or Decreasing T)[min]"].values)
    occ_release=list(tempatature_df_final.iloc[frame:frame+num_date]["Release Periods(Ahead of Occupancy Peak)[min]"].values)
    nozzle=list(tempatature_df_final.iloc[frame:frame+num_date]["Active Nozzles (Current T)[%]"].values)
    tem_nozzle=list(tempatature_df_final.iloc[frame:frame+num_date]["Active Nozzles(Increasing or Decreasing T)[%]"].values)
    occ_nozzle=list(tempatature_df_final.iloc[frame:frame+num_date]["Active Nozzles(Ahead of Occupancy Peak)[%]"].values)
    # Set Release value
    release_line.set_data(range(frame, frame+num_date),release)
    tem_release_line.set_data(range(frame, frame+num_date),tem_release)
    occ_release_line.set_data(range(frame, frame+num_date),occ_release)
    # Set Active Nozzles Value
    nozzle_line.set_data(range(frame, frame+num_date),nozzle)
    tem_nozzle_line.set_data(range(frame, frame+num_date),tem_nozzle)
    occ_nozzle_line.set_data(range(frame, frame+num_date),occ_nozzle)

    # Update x axis for Release
    release_line.axes.set_xlim(frame,frame+num_date-1)
    tem_release_line.axes.set_xlim(frame,frame+num_date-1)
    occ_release_line.axes.set_xlim(frame,frame+num_date-1)
    # Update x axis for Active Nozzles
    nozzle_line.axes.set_xlim(frame,frame+num_date-1)
    tem_nozzle_line.axes.set_xlim(frame,frame+num_date-1)
    occ_nozzle_line.axes.set_xlim(frame,frame+num_date-1)

    # replace the integer on x axis to date
    release_chart.set_xticks(range(frame, frame+num_date))
    release_chart.set_xticklabels(date_time,rotation = 90)

    # Increase the y axis maximum value if chart value is above some threshold
    # temperature >28 or occupancy count>12
    current_max_tem=max(temperature)
    current_max_occ=max(occupancy_num)
    if current_max_tem>28:
        temperature_chart.set_ylim(0,current_max_tem+3)

    else:
        if temperature_chart.get_ylim()[1] != 30:
            temperature_chart.set_ylim(0,30)

    if current_max_occ>12:
        occupancy_chart.set_ylim(0,current_max_occ+3)
    else:
        if occupancy_chart.get_ylim()[1] != 12:
            occupancy_chart.set_ylim(0,12)


# Alter the margin and padding of charts
# The graph may display differently on different screens
# The value set left=0.085, bottom=0.2, right=0.82,top=0.915,hspace=0.68 is pefect for exporting the image using savefig
plt.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT,top=TOP,hspace=HSPACE)


# Create animation controller
ani = Player(fig, plot_simulation, maxi=len(tempatature_df_final)-num_date,interval=1000,repeat=False)

# Export image logic
if EXPORT:
    for index, row in tempatature_df_final.iterrows():
        if index>=START_FRAME and index <=END_FRAME and index<(len(tempatature_df_final)-num_date):
            ani.update(index)
            time=row["Time"].strftime('%Y%m%dT%H%M')
            fig.savefig('data/images/'+time+'.png', bbox_inches = "tight")
            print("Export "+str(index-START_FRAME+1)+"/"+str(END_FRAME-START_FRAME+1))

# Add the custom tools that we created for active/deactive the stage2/3 nozzles
fig.canvas.manager.toolmanager.add_tool('Show S2', GroupHideTool, gid='nozzles2')
fig.canvas.manager.toolmanager.add_tool('Show S3', GroupHideTool, gid='nozzles3')

plt.show()
