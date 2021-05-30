# Milica, Please add all the scenario by creating new functions
#  *Please name the function as "scenario"+"number"
#  *Please make sure the scenario number is continuous, 1,2,3,4,5..n
#  *All the scenarios will be added to the final calculation automatically.

def scenario1(row):
    T=row.Temperature
    P=row.OccupancyCount
    M=0

    # start of the scenario logic
    if T <= 20 and P < 10:
        M = 0.4 * 10
    elif T <= 20 and P >= 10:
        M = 0.5 * 10
    elif 20 < T <= 25 and P < 10:
        M = 0.6 * 10
    elif 20 < T <= 25 and P >= 10:
        M = 0.7 * 10
    elif 25 < T <= 30 and P < 10:
        M = 0.6 * 10
    elif 25 < T <= 30 and P >= 10:
        M = 0.6 * 10
    elif T > 30:
        M = 0.6 * 10
    else:
        M=0
    # End of the scenario logic

    return M

def scenario2(row):
    T=row.Temperature
    P=row.OccupancyCount
    M=0

    # start of the scenario logic
    if 15 < T <= 20:
        M = 0.3 * 10
    elif 20<T <= 25:
        M = 0.6 * 10
    elif 25 < T <= 30:
        M = 0.8 * 10
    elif T > 30:
        M = 1 * 10
    else:
        M=0
    # End of the scenario logic
    return M

def scenario3(row):
    T=row.Temperature
    P=row.OccupancyCount
    M=0

    # start of the scenario logic
    if 15 < T <= 20:
        M = 0.25 * 10
    elif 20<T <= 25:
        M = 0.50 * 10
    elif 25 < T <= 30:
        M = 0.75 * 10
    elif T > 30:
        M = 1 * 10
    else:
        M=0
    # End of the scenario logic

    return M

def scenario4(row):
    T=row.Temperature
    P=row.OccupancyCount
    M=0

    # start of the scenario logic
    if 15 < T <= 20:
        M = 0.15 * 10
    elif 20<T <= 25:
        M = 0.3 * 10
    elif 25 < T <= 30:
        M = 0.6 * 10
    elif T > 30:
        M = 1 * 10
    else:
        M=0
    # End of the scenario logic
    return M

# Do not need to update the code below------------------
import pandas as pd

data_df=pd.read_excel("melbourne_temperature_calculated.xlsx")

scenario_num=1
scenario="scenario"+str(scenario_num)
while scenario in globals():
    scenario_func = globals()[scenario]
    data_df[scenario]=data_df.apply(lambda row: scenario_func(row),axis=1)
    scenario_num=scenario_num+1
    scenario="scenario"+str(scenario_num)
data_df.to_excel("time_m.xlsx",index=None)
data_df.groupby([data_df['Time'].dt.date]).sum().reset_index().drop(columns=["Temperature","OccupancyCount"]).to_excel("sum_m.xlsx",index=None)
