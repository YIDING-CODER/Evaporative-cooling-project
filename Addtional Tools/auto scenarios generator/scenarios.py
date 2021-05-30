# Number of scenarios generated
NUM_SIMULATION=100

# Default T0 range [Low,High]
T0_LOW=10
T0_HIGH=15

import random
# @t0 initial temperature
def scenario_template(row,t0):
    T=row.Temperature
    P=row.OccupancyCount
    M=0
    t0=t0+5

    # start of the scenario logic
    if T <= t0 and P < 10:
        M = 0.4 * 10
    elif T <= t0 and P >= 10:
        M = 0.5 * 10
    elif t0 < T <= t0+5 and P < 10:
        M = 0.6 * 10
    elif t0 < T <= t0+5 and P >= 10:
        M = 0.7 * 10
    elif t0+5 < T <= t0+10 and P < 10:
        M = 0.6 * 10
    elif t0+5 < T <= t0+10 and P >= 10:
        M = 0.6 * 10
    elif T > t0+10:
        M = 0.6 * 10
    else:
        M=0
    # End of the scenario logic

    return M

# Do not need to update the code below------------------
def get_random_number(low,high):
    return round(random.uniform(low,high),2)

import pandas as pd

data_df=pd.read_excel("melbourne_temperature_calculated.xlsx")
data = {'scenarios': ["Scenario" + str(i+1) for i in range(NUM_SIMULATION)], 't0': [get_random_number(T0_LOW,T0_HIGH) for i in range(NUM_SIMULATION)]}

scenario_df=pd.DataFrame(data)

for index, row in scenario_df.iterrows():
    data_df[row["scenarios"]]=data_df.apply(lambda x: scenario_template(x,row["t0"]),axis=1)
data_df.to_excel("time_m.xlsx",index=None)
data_df.groupby([data_df['Time'].dt.date]).sum().reset_index().drop(columns=["Temperature","OccupancyCount"]).to_excel("sum_m.xlsx",index=None)
scenario_df.to_excel("senarios_t0.xlsx",index=None)
