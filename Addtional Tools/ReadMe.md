# Evaporative Cooling Simulation Additional Tool

Calculate the M value under different scenario.
Enable editable simulation where we can change temperature range, assigned active nozzles percentage and people number limit.

## Features

- Add additional scenario by adding python functions
- Auto calculate the M value under different scenarios.
- Export simulation result as excel document

## File Structures

```
├── scenarios.py
├── melbourne_temperature_calculated.xlsx
├── time_m.xlsx
├── sum_m.xlsx
└── ReadMe.md
```

| File | Description |
| ------ | ------ |
| ```scenarios.py``` | The simulator program. |
| ```melbourne_temperature_calculated.xlsx``` | The input data which includes the Time, temperature and Occupancy Count.|
| ```time_m.xlsx``` | The output file of running the simulation. This file include the calculated M value for each 10 minutes interval and scenarios. |
| ```sum_m.xlsx``` | The output file of running the simulation. This file include the calculated Sum(M) value per day for each scenarios. |
| ```ReadMe.md``` | Documentation file |



## Run the Simulation
Under the current folder type the following code in the terminal
```sh
python scenarios.py
```
You will get a ```time_m.xlsx``` and ```sum_m.xlsx``` after runing the simulator.

## How to add additional scenario
1. The scenario is defined by the python function, so a new python function need to be created for a new scenario.
2. Don't be panic, adding a new scenario is quite easy. Please open the scenarios.py in any text editor, and you can find there are 4 scenarios has been created already.
3. To add a new scenario, you just need to create a new function(you can copy the existing function) and give it a name as "scenario" + number. Please make sure the scenario number is continuous. There is no maximum number of scenario, so you can add scenarios as many as you can.
4. Then you can edit the scenario logic between the #start of the scenario logic and #end of the scenario logic.
```sh
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
```
5. Please save the scenarios.py after adding new scenarios.
