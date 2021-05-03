import pandas as pd
import random


# stage3 correction
peak_occupancy=6
peak_duration_increase=0.2
peak_nozzles_increase=0.3

# Return release periods and active nozzles for stage1
def get_current_release_periods_active_nozzles(current_tem):
    if current_tem<20:
        return (0,0)
    elif current_tem>=20 and current_tem<25:
        return (20,20)
    elif current_tem>=25 and current_tem<30:
        return (40,60)
    elif current_tem>=30 and current_tem<35:
        return (50,100)
    else:
        return (60,100)

# Return release periods and active nozzles for stage2 correction
def get_recalculate_release_periods_active_nozzles(current_tem,trend):
#   "increase/equal"
    if trend >=0:
        if current_tem<20:
            return (20,20)
        elif current_tem>=20 and current_tem<25:
            return (40,60)
        elif current_tem>=25 and current_tem<30:
            return (50,100)
        elif current_tem>=30 and current_tem<35:
            return (60,100)
        else:
            return (60,100)
    else:
        if current_tem<20:
            return (0,0)
        elif current_tem>=20 and current_tem<25:
            return (0,0)
        elif current_tem>=25 and current_tem<30:
            return (20,20)
        elif current_tem>=30 and current_tem<35:
            return (40,60)
        else:
            return (50,100)


# Get the max occupancy count for the next 60 minutes
def get_next_hour_max(df):
    all_occupancy=df["OccupancyCount"].values
    next_hour_occupancy_list=[]
    length=len(df)
    for index, row in df.iterrows():
        if index <= length-6:
            next_hour_occupancy_list.append(all_occupancy[index:index+6].max())
        else:
            next_hour_occupancy_list.append(0)
    return next_hour_occupancy_list

# logic to get the Release Periods and Active Nozzles for Stage3
def get_occupancy_peak_release_nozzle(base_release_period,base_nozzles,next_hour_occupancy):
#    peak_occupancy is 6
    if next_hour_occupancy>peak_occupancy:
        release_period=base_release_period*(1+peak_duration_increase)
        nozzles_num=base_nozzles*(1+peak_nozzles_increase)
        if release_period>60:
            release_period=60
        if nozzles_num>100:
            nozzles_num=100
        return (release_period,nozzles_num)
    else:
        return (base_release_period,base_nozzles)

def get_matrix(AUTO_GENERATE_OCCUPANTS,MAX_OCCUPANCY=10):
    if AUTO_GENERATE_OCCUPANTS:
        tempatature_df=pd.read_csv("data/melbourne_temperature.csv")
        tempatature_df["Time"]=pd.to_datetime(tempatature_df["Time"], format='%Y%m%dT%H%M')
        tempatature_df["Temperature"]=tempatature_df["Temperature"].astype(int)
        tempatature_df_final=tempatature_df[(tempatature_df["Time"].dt.hour>=9) & (tempatature_df["Time"].dt.hour <=17)].reset_index(drop=True)
        tempatature_df_final["PreviousTemperature"]=tempatature_df_final['Temperature'].shift(1)
        tempatature_df_final["PreviousTemperature"]=tempatature_df_final.apply(lambda x: 0 if x["Time"].hour==9 else x["PreviousTemperature"], axis=1)
        tempatature_df_final["PreviousTemperature"]=tempatature_df_final["PreviousTemperature"].astype(int)
        tempatature_df_final=tempatature_df_final[(tempatature_df_final["Time"].dt.hour>=10) & (tempatature_df_final["Time"].dt.hour <=17)].reset_index(drop=True)
        time_interval=10
        intervals=list(range(int(60/time_interval)))
        tempatature_df_final["intervals"]=[intervals]*len(tempatature_df_final)
        tempatature_df_explode=tempatature_df_final.explode("intervals")
        tempatature_df_explode["time_explode"]=tempatature_df_explode.apply(lambda x:x.Time+pd.Timedelta(minutes=time_interval*x.intervals),axis=1)
        tempatature_df_final=tempatature_df_explode[["time_explode","Temperature","PreviousTemperature"]].rename(columns={"time_explode":"Time"})
        tempatature_df_final["OccupancyCount"]=tempatature_df_final.apply(lambda x:random.randint(1,MAX_OCCUPANCY),axis=1)
        tempatature_df_final=tempatature_df_final.reset_index(drop=True)

    else:
        tempatature_df=pd.read_csv("data/melbourne_temperature_occupancy.csv")
        tempatature_df["Time"]=pd.to_datetime(tempatature_df["Time"], format='%Y%m%dT%H%M')
        tempatature_df["Temperature"]=tempatature_df["Temperature"].astype(int)
        tempatature_df_final=tempatature_df[(tempatature_df["Time"].dt.hour>=9) & (tempatature_df["Time"].dt.hour <=17)].reset_index(drop=True)
        tempatature_df_final["PreviousTemperature"]=tempatature_df_final['Temperature'].shift(1)
        tempatature_df_final["PreviousTemperature"]=tempatature_df_final.apply(lambda x: 0 if x["Time"].hour==9 else x["PreviousTemperature"], axis=1)
        tempatature_df_final["PreviousTemperature"]=tempatature_df_final["PreviousTemperature"].astype(int)
        tempatature_df_final=tempatature_df_final[(tempatature_df_final["Time"].dt.hour>=10) & (tempatature_df_final["Time"].dt.hour <=17)].reset_index(drop=True)
        tempatature_df_final=tempatature_df_final[["Time","Temperature","OccupancyCount","PreviousTemperature"]]
        tempatature_df_final["OccupancyCount"]=tempatature_df_final["OccupancyCount"].astype(int)
        tempatature_df_final=tempatature_df_final.reset_index(drop=True)

    tempatature_df_final["trend"]=tempatature_df_final["Temperature"]-tempatature_df_final["PreviousTemperature"]

    # The following code will generate the Release Periods and Active Nozzles for stage1
    # The release periods and active Nozzles will only be calculated when the current Release Period is 0,
    # otherwise it will inherit the value from previous 10 minutes.
    previous_release_value,previous_nozzole_value=0,0
    current_release_value,current_nozzole_value=0,0
    value_pair_list=[]
    for index, row in tempatature_df_final.iterrows():
        if (previous_release_value<=10) or (row["Time"].hour==10 and row["Time"].minute==0) :
            current_release_value,current_nozzole_value=get_current_release_periods_active_nozzles(row["Temperature"])
            value_pair_list.append((current_release_value,current_nozzole_value))
            previous_release_value,previous_nozzole_value=current_release_value,current_nozzole_value
        else:
            current_release_value=previous_release_value-10
            current_nozzole_value=previous_nozzole_value
            value_pair_list.append((current_release_value,current_nozzole_value))
            previous_release_value,previous_nozzole_value=current_release_value,current_nozzole_value

    tempatature_df_final[["Release Periods (Current T)[min]","Active Nozzles (Current T)[%]"]]=pd.DataFrame(value_pair_list,index=tempatature_df_final.index)


    # The following code will generate the Release Periods and Active Nozzles for Stage2
    # The release periods and active Nozzles will only be calculated when the current Release Period is 0,
    # otherwise it will inherit the value from previous 10 minutes.
    previous_release_value,previous_nozzole_value=0,0
    current_release_value,current_nozzole_value=0,0
    value_pair_list=[]
    for index, row in tempatature_df_final.iterrows():
        if (previous_release_value<=10) or (row["Time"].hour==10 and row["Time"].minute==0):
            current_release_value,current_nozzole_value=get_recalculate_release_periods_active_nozzles(row["Temperature"],row["trend"])
            value_pair_list.append((current_release_value,current_nozzole_value))
            previous_release_value,previous_nozzole_value=current_release_value,current_nozzole_value
        else:
            current_release_value=previous_release_value-10
            current_nozzole_value=previous_nozzole_value
            value_pair_list.append((current_release_value,current_nozzole_value))
            previous_release_value,previous_nozzole_value=current_release_value,current_nozzole_value

    tempatature_df_final[["Release Periods (Increasing or Decreasing T)[min]","Active Nozzles(Increasing or Decreasing T)[%]"]]=pd.DataFrame(value_pair_list,index=tempatature_df_final.index)


    tempatature_df_final["Next Hour Occupancy"]=get_next_hour_max(tempatature_df_final)

    # Remove the time interval after 17:00 after calculating the Next Hour Occupancy
    tempatature_df_final=tempatature_df_final[tempatature_df_final["Time"].dt.hour!=17]



    # The following code will generate the Release Periods and Active Nozzles for Stage3
    # The release periods and active Nozzles will only be calculated when the current Release Period is 0,
    # otherwise it will inherit the value from previous 10 minutes.
    previous_release_value,previous_nozzole_value=0,0
    current_release_value,current_nozzole_value=0,0
    value_pair_list=[]
    for index, row in tempatature_df_final.iterrows():
        if (previous_release_value<=10) or (row["Time"].hour==10 and row["Time"].minute==0):
            current_release_value,current_nozzole_value=get_occupancy_peak_release_nozzle(row["Release Periods (Increasing or Decreasing T)[min]"],row["Active Nozzles(Increasing or Decreasing T)[%]"],row["Next Hour Occupancy"])
            value_pair_list.append((current_release_value,current_nozzole_value))
            previous_release_value,previous_nozzole_value=current_release_value,current_nozzole_value
        else:
            current_release_value=previous_release_value-10
            current_nozzole_value=previous_nozzole_value
            value_pair_list.append((current_release_value,current_nozzole_value))
            previous_release_value,previous_nozzole_value=current_release_value,current_nozzole_value

    tempatature_df_final[["Release Periods(Ahead of Occupancy Peak)[min]","Active Nozzles(Ahead of Occupancy Peak)[%]"]]=pd.DataFrame(value_pair_list,index=tempatature_df_final.index)

    # Export the calculated Matrix
    tempatature_df_final[["Time","Temperature","OccupancyCount",
                          "Release Periods (Current T)[min]","Active Nozzles (Current T)[%]",
                          "Release Periods (Increasing or Decreasing T)[min]","Active Nozzles(Increasing or Decreasing T)[%]",
                          "Release Periods(Ahead of Occupancy Peak)[min]","Active Nozzles(Ahead of Occupancy Peak)[%]",
                          "PreviousTemperature","trend","Next Hour Occupancy"
                         ]].to_excel("data/melbourne_temperature_calculated.xlsx",index=None)
    return tempatature_df_final
