import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# subset to specific milan pm2.5 sensors
# 17122 - Milano via Senato (PM2.5)
# 20529 - Milano viale Marche (PM2.5)
# 10283 - Milano Pascal Città Studi (PM2.5)

# Function to average the PM2.5 values at each station of 24 hours for each day
def pm25_sensors_avg(data):
    # list of PM2.5 stations
    stations = [17122, 20529, 10283]
    # subset data to these Milan stations
    pm_data = data[data['IdSensore'].isin(stations)].copy()
    # Convert the datetime_column to datetime datatype
    pm_data['date'] = pd.to_datetime(pm_data['Data'], format='%d/%m/%Y %I:%M:%S %p', dayfirst=True)
    # Extract just the date part
    pm_data['date'] = pm_data['date'].dt.date.copy()
    # make new empty column for station names
    pm_data['Stazione'] = ''  # Create a new column with empty strings initially
    # Define the conditions and corresponding values
    conditions = [
        (pm_data['IdSensore'] == 17122),
        (pm_data['IdSensore'] == 20529),
        (pm_data['IdSensore'] == 10283)
    ]
    values = ['via Senato', 'viale Marche', 'Pascal Città Studi']  # Corresponding values for each condition
    # Apply the conditions and values using .loc
    for condition, value in zip(conditions, values):
        pm_data.loc[condition, 'Stazione'] = value
    # recode -9999.0 to NA
    pm_data['Valore'] = np.where(pm_data['Valore'] == -9999.0, np.nan, pm_data['Valore'])
    # Calculate average for 'Valore' by each unique value of 'date'
    mean_milan = pd.DataFrame(pm_data.groupby('date')['Valore'].mean())
    # Reset index to convert the Series to a DataFrame
    mean_milan = mean_milan.reset_index()
    # Rename columns if needed
    mean_milan.columns = ['date', 'Valore']
    return pm_data, mean_milan


def pm10_sensors_avg(data):
    # PM10 sensors
    stations_pm10 = [10320, 20429, 10273, 6956] # last one is via Verziere
    # subset data to these Milan stations
    pm10_data = data[data['IdSensore'].isin(stations_pm10)].copy()
    # Convert the datetime_column to datetime datatype
    pm10_data['date'] = pd.to_datetime(pm10_data['Data'], format='%d/%m/%Y %I:%M:%S %p', dayfirst=True)
    # Extract just the date part
    pm10_data['date'] = pm10_data['date'].dt.date.copy()
    # make new empty column for station names
    pm10_data['Stazione'] = ''  # Create a new column with empty strings initially
    # Define the conditions and corresponding values
    conditions = [
        (pm10_data['IdSensore'] == 10320),
        (pm10_data['IdSensore'] == 20429),
        (pm10_data['IdSensore'] == 10273),
        (pm10_data['IdSensore'] == 6956)
    ]
    values = ['via Senato', 'viale Marche', 'Pascal Città Studi', 'Verziere']  # Corresponding values for each condition
    # Apply the conditions and values using .loc
    for condition, value in zip(conditions, values):
        pm10_data.loc[condition, 'Stazione'] = value
    # recode -9999.0 to NA
    pm10_data['Valore'] = np.where(pm10_data['Valore'] == -9999.0, np.nan, pm10_data['Valore'])
    # Calculate average for 'Valore' by each unique value of 'date'
    mean_pm10_milan = pd.DataFrame(pm10_data.groupby('date')['Valore'].mean())
    # Reset index to convert the Series to a DataFrame
    mean_pm10_milan = mean_pm10_milan.reset_index()
    # Rename columns if needed
    mean_pm10_milan.columns = ['date', 'Valore']
    return pm10_data, mean_pm10_milan


def calculate_sensor_avg(data, pm_stations):
    # subset to data in all Lombardia
    pm_data = data[data['IdSensore'].isin(pm_stations)].copy()
    # Convert the datetime_column to datetime datatype
    pm_data['date'] = pd.to_datetime(pm_data['Data'], format='%d/%m/%Y %I:%M:%S %p', dayfirst=True)
    # Extract just the date part
    pm_data['date'] = pm_data['date'].dt.date.copy()
    # recode -9999.0 to NA
    pm_data['Valore'] = np.where(pm_data['Valore'] == -9999.0, np.nan, pm_data['Valore'])
    # Calculate average for 'Valore' by each unique value of 'date'
    mean_pm_data = pd.DataFrame(pm_data.groupby('date')['Valore'].mean())
    # Reset index to convert the Series to a DataFrame
    mean_pm_data = mean_pm_data.reset_index()
    # Rename columns if needed
    mean_pm_data.columns = ['date', 'Valore']
    return mean_pm_data



def plot_air_quality_25_milan(data, city, start_date, end_date, save=False, annotation=True):
    UE_limit = 25
    WHO_limit = 15

    UE_limit_annual = 10
    WHO_limit_annual = 5

    # Sorting DataFrame by date within each station group
    data.sort_values('date', inplace=True)

    # Filter data to all times
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    days_above_EU = filtered_data[filtered_data['Valore'] > UE_limit].nunique()['Valore']
    days_above_alarm = filtered_data[filtered_data['Valore'] > 50].nunique()['Valore']
    days_above_OMS = filtered_data[filtered_data['Valore'] > WHO_limit].nunique()['Valore']

    if annotation:
        # Count number of days where in 2023
        start_2023 = pd.to_datetime('01/01/2023').date()
        end_2023 = pd.to_datetime('12/31/2023').date()

        data_2023 = data[(data['date'] >= start_2023) & (data['date'] <= end_2023)]
        days_above_EU_2023 = data_2023[data_2023['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2023 = data_2023[data_2023['Valore'] > 50].nunique()['Valore']
        days_above_OMS_2023 = data_2023[data_2023['Valore'] > WHO_limit].nunique()['Valore']

        avg_2023 = data_2023['Valore'].mean()

        # Count number of days where in 2024
        start_2024 = pd.to_datetime('01/01/2024').date()
        end_2024 = pd.to_datetime('12/31/2024').date()

        data_2024 = data[(data['date'] >= start_2024) & (data['date'] <= end_2024)]
        days_above_EU_2024 = data_2024[data_2024['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2024 = data_2024[data_2024['Valore'] > 50].nunique()['Valore']
        days_above_OMS_2024 = data_2024[data_2024['Valore'] > WHO_limit].nunique()['Valore']

        avg_2024 = data_2024['Valore'].mean()

        # Count number of days where in 2025
        start_2025 = pd.to_datetime('01/01/2025').date()
        end_2025 = pd.to_datetime('01/31/2025').date()

        data_2025 = data[(data['date'] >= start_2025) & (data['date'] <= end_2025)]
        days_above_EU_2025 = data_2025[data_2025['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2025 = data_2025[data_2025['Valore'] > 50].nunique()['Valore']
        days_above_OMS_2025 = data_2025[data_2025['Valore'] > WHO_limit].nunique()['Valore']

    # Calculate average value for each station
    average = filtered_data['Valore'].mean()

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(
        filtered_data['date'], 
        filtered_data['Valore'],
        label=f'ARPA (media di 3 stazioni)',
        linewidth=3
    )

    # horizontal dashed line for EU and WHO limits
    plt.axhline(y=WHO_limit, color='black', linestyle='--')
    plt.axhline(y=UE_limit, color='gray', linestyle='--')
    plt.axhline(y=50, color='red', linestyle='--')

    plt.annotate(
        'Limite UE', 
        xy=(filtered_data['date'].iloc[110], UE_limit), 
        xytext=(filtered_data['date'].iloc[110], UE_limit+10),
        arrowprops=dict(facecolor='black', arrowstyle='-')
    )

    plt.annotate(
        'Limite OMS', 
        xy=(filtered_data['date'].iloc[150], WHO_limit), 
        xytext=(filtered_data['date'].iloc[150], WHO_limit+15),
        arrowprops=dict(facecolor='black', arrowstyle='-')
    )

    plt.text(filtered_data['date'].iloc[90], 52, "Soglia proposta per l'allarme")

    if annotation:
        plt.text(filtered_data['date'].iloc[0], 80, f"Giorni sopra il limite OMS nel 2023: {days_above_OMS_2023}")
        plt.text(filtered_data['date'].iloc[0], 85, f"Giorni sopra il limite UE nel 2023: {days_above_EU_2023}")
        plt.text(filtered_data['date'].iloc[0], 90, f"Giorni sopra la soglia d'allarme nel 2023: {days_above_alarm_2023}")

        plt.text(filtered_data['date'].iloc[0], 100, f"Giorni sopra il limite OMS nel 2024: {days_above_OMS_2024}")
        plt.text(filtered_data['date'].iloc[0], 105, f"Giorni sopra il limite UE nel 2024: {days_above_EU_2024}")
        plt.text(filtered_data['date'].iloc[0], 110, f"Giorni sopra la soglia d'allarme nel 2024: {days_above_alarm_2024}")

        plt.text(filtered_data['date'].iloc[0], 120, f"Giorni sopra il limite OMS nel 2025: {days_above_OMS_2025}")
        plt.text(filtered_data['date'].iloc[0], 125, f"Giorni sopra il limite UE nel 2025: {days_above_EU_2025}")
        plt.text(filtered_data['date'].iloc[0], 130, f"Giorni sopra la soglia d'allarme nel 2025: {days_above_alarm_2025}")

        plt.text(filtered_data['date'].iloc[450], 105, f"Media di PM2.5 nel 2023: {avg_2023:.2f} \n(limite UE: {UE_limit_annual}, limite OMS: {WHO_limit_annual})")
        plt.text(filtered_data['date'].iloc[450], 125, f"Media di PM2.5 nel 2024: {avg_2024:.2f} \n(limite UE: {UE_limit_annual}, limite OMS: {WHO_limit_annual})")

    plt.yticks(range(0, int(filtered_data['Valore'].max()) + 5, 5))
    plt.xticks(filtered_data['date'], rotation=45, ha='right', fontsize=8)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(1, 13, 1)))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

    legend = plt.legend(frameon=False, loc='upper left')
    for line in legend.get_lines():
        line.set_linewidth(4)

    plt.style.use('seaborn-white')
    plt.tick_params(axis='x', direction='out', length=4, width=1, colors='black')

    plt.xlabel('')
    plt.ylabel('Concentrazione PM2.5 (µg/m³)')
    plt.title(f'Inquinamento PM2.5 a {city} ({start_date} - {end_date})', pad=10)

    if save==False:
        plt.show()



def plot_air_quality_pm10_milan(data, city, start_date, end_date, save=False, annotation=True):
    UE_limit = 45
    WHO_limit = 45
    alarm_limit = 90

    UE_limit_annual = 20
    WHO_limit_annual = 15

    # Sorting DataFrame by date within each station group
    data.sort_values('date', inplace=True)

    # Filter data to all times
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    days_above_EU = filtered_data[filtered_data['Valore'] > UE_limit].nunique()['Valore']
    days_above_alarm = filtered_data[filtered_data['Valore'] > alarm_limit].nunique()['Valore']
    days_above_OMS = filtered_data[filtered_data['Valore'] > WHO_limit].nunique()['Valore']

    if annotation:
        # Count number of days where in 2023
        start_2023 = pd.to_datetime('01/01/2023').date()
        end_2023 = pd.to_datetime('12/31/2023').date()

        data_2023 = data[(data['date'] >= start_2023) & (data['date'] <= end_2023)]
        days_above_EU_2023 = data_2023[data_2023['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2023 = data_2023[data_2023['Valore'] > alarm_limit].nunique()['Valore']
        days_above_OMS_2023 = data_2023[data_2023['Valore'] > WHO_limit].nunique()['Valore']

        avg_2023 = data_2023['Valore'].mean()

        # Count number of days where in 2024
        start_2024 = pd.to_datetime('01/01/2024').date()
        end_2024 = pd.to_datetime('12/31/2024').date()

        data_2024 = data[(data['date'] >= start_2024) & (data['date'] <= end_2024)]
        days_above_EU_2024 = data_2024[data_2024['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2024 = data_2024[data_2024['Valore'] > alarm_limit].nunique()['Valore']
        days_above_OMS_2024 = data_2024[data_2024['Valore'] > WHO_limit].nunique()['Valore']

        avg_2024 = data_2024['Valore'].mean()

        # Count number of days where in 2025
        start_2025 = pd.to_datetime('01/01/2025').date()
        end_2025 = pd.to_datetime('01/31/2025').date()

        data_2025 = data[(data['date'] >= start_2025) & (data['date'] <= end_2025)]
        days_above_EU_2025 = data_2025[data_2025['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2025 = data_2025[data_2025['Valore'] > 50].nunique()['Valore']
        days_above_OMS_2025 = data_2025[data_2025['Valore'] > WHO_limit].nunique()['Valore']

    # Calculate average value for each station
    average = filtered_data['Valore'].mean()

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(
        filtered_data['date'], 
        filtered_data['Valore'],
        label=f'ARPA (media di 4 stazioni)',
        linewidth=3
    )

    # horizontal dashed line for EU and WHO limits
    plt.axhline(y=WHO_limit, color='black', linestyle='--')
    plt.axhline(y=UE_limit, color='gray', linestyle='--')
    plt.axhline(y=alarm_limit, color='red', linestyle='--')

    plt.annotate(
        'Limite UE / OMS', 
        xy=(filtered_data['date'].iloc[110], UE_limit), 
        xytext=(filtered_data['date'].iloc[90], UE_limit+10),
        arrowprops=dict(facecolor='black', arrowstyle='-')
    )

    # plt.annotate(
    #     'Limite OMS', 
    #     xy=(filtered_data['date'].iloc[150], WHO_limit), 
    #     xytext=(filtered_data['date'].iloc[150], WHO_limit+15),
    #     arrowprops=dict(facecolor='black', arrowstyle='-')
    # )

    plt.text(filtered_data['date'].iloc[90], 92, "Soglia proposta per l'allarme")

    if annotation:
        plt.text(filtered_data['date'].iloc[0], 120, f"Giorni sopra il limite OMS nel 2023: {days_above_OMS_2023}")
        plt.text(filtered_data['date'].iloc[0], 125, f"Giorni sopra il limite UE nel 2023: {days_above_EU_2023}")
        plt.text(filtered_data['date'].iloc[0], 130, f"Giorni sopra la soglia d'allarme nel 2023: {days_above_alarm_2023}")

        plt.text(filtered_data['date'].iloc[0], 140, f"Giorni sopra il limite OMS nel 2024: {days_above_OMS_2024}")
        plt.text(filtered_data['date'].iloc[0], 145, f"Giorni sopra il limite UE nel 2024: {days_above_EU_2024}")
        plt.text(filtered_data['date'].iloc[0], 150, f"Giorni sopra la soglia d'allarme nel 2024: {days_above_alarm_2024}")

        plt.text(filtered_data['date'].iloc[0], 160, f"Giorni sopra il limite OMS nel 2025: {days_above_OMS_2025}")
        plt.text(filtered_data['date'].iloc[0], 165, f"Giorni sopra il limite UE nel 2025: {days_above_EU_2025}")
        plt.text(filtered_data['date'].iloc[0], 170, f"Giorni sopra la soglia d'allarme nel 2025: {days_above_alarm_2025}")

        plt.text(filtered_data['date'].iloc[450], 145, f"Media di PM2.5 nel 2023: {avg_2023:.2f} \n(limite UE: {UE_limit_annual}, limite OMS: {WHO_limit_annual})")
        plt.text(filtered_data['date'].iloc[450], 165, f"Media di PM2.5 nel 2024: {avg_2024:.2f} \n(limite UE: {UE_limit_annual}, limite OMS: {WHO_limit_annual})")


    plt.yticks(range(0, int(filtered_data['Valore'].max()) + 5, 5))
    plt.xticks(filtered_data['date'], rotation=45, ha='right', fontsize=8)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(1, 13, 1)))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

    legend = plt.legend(frameon=False, loc='upper left')
    for line in legend.get_lines():
        line.set_linewidth(4)

    plt.style.use('seaborn-white')
    plt.tick_params(axis='x', direction='out', length=4, width=1, colors='black')

    plt.xlabel('')
    plt.ylabel('Concentrazione PM10 (µg/m³)')
    plt.title(f'Inquinamento PM10 a {city} ({start_date} - {end_date})', pad=10)

    if save==False:
        plt.show()


def plot_air_quality_25_lombardia(data, city, start_date, end_date, save=False, annotation=True):
    UE_limit = 25
    WHO_limit = 15

    UE_limit_annual = 10
    WHO_limit_annual = 5

    # Sorting DataFrame by date within each station group
    data.sort_values('date', inplace=True)

    # Filter data to all times
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    days_above_EU = filtered_data[filtered_data['Valore'] > UE_limit].nunique()['Valore']
    days_above_alarm = filtered_data[filtered_data['Valore'] > 50].nunique()['Valore']
    days_above_OMS = filtered_data[filtered_data['Valore'] > WHO_limit].nunique()['Valore']

    if annotation:
        # Count number of days where in 2023
        start_2023 = pd.to_datetime('01/01/2023').date()
        end_2023 = pd.to_datetime('12/31/2023').date()

        data_2023 = data[(data['date'] >= start_2023) & (data['date'] <= end_2023)]
        days_above_EU_2023 = data_2023[data_2023['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2023 = data_2023[data_2023['Valore'] > 50].nunique()['Valore']
        days_above_OMS_2023 = data_2023[data_2023['Valore'] > WHO_limit].nunique()['Valore']

        avg_2023 = data_2023['Valore'].mean()

        # Count number of days where in 2024
        start_2024 = pd.to_datetime('01/01/2024').date()
        end_2024 = pd.to_datetime('12/31/2024').date()

        data_2024 = data[(data['date'] >= start_2024) & (data['date'] <= end_2024)]
        days_above_EU_2024 = data_2024[data_2024['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2024 = data_2024[data_2024['Valore'] > 50].nunique()['Valore']
        days_above_OMS_2024 = data_2024[data_2024['Valore'] > WHO_limit].nunique()['Valore']

        avg_2024 = data_2024['Valore'].mean()

        # Count number of days where in 2025
        start_2025 = pd.to_datetime('01/01/2025').date()
        end_2025 = pd.to_datetime('01/31/2025').date()

        data_2025 = data[(data['date'] >= start_2025) & (data['date'] <= end_2025)]
        days_above_EU_2025 = data_2025[data_2025['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2025 = data_2025[data_2025['Valore'] > 50].nunique()['Valore']
        days_above_OMS_2025 = data_2025[data_2025['Valore'] > WHO_limit].nunique()['Valore']

    # Calculate average value for each station
    average = filtered_data['Valore'].mean()

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(
        filtered_data['date'], 
        filtered_data['Valore'],
        label=f'ARPA (media di 41 stazioni)',
        linewidth=3
    )

    # horizontal dashed line for EU and WHO limits
    plt.axhline(y=WHO_limit, color='black', linestyle='--')
    plt.axhline(y=UE_limit, color='gray', linestyle='--')
    plt.axhline(y=50, color='red', linestyle='--')

    plt.annotate(
        'Limite UE', 
        xy=(filtered_data['date'].iloc[110], UE_limit), 
        xytext=(filtered_data['date'].iloc[110], UE_limit+10),
        arrowprops=dict(facecolor='black', arrowstyle='-')
    )

    plt.annotate(
        'Limite OMS', 
        xy=(filtered_data['date'].iloc[150], WHO_limit), 
        xytext=(filtered_data['date'].iloc[150], WHO_limit+15),
        arrowprops=dict(facecolor='black', arrowstyle='-')
    )

    plt.text(filtered_data['date'].iloc[90], 52, "Soglia proposta per l'allarme")

    if annotation:
        plt.text(filtered_data['date'].iloc[0], 92, f"Giorni sopra il limite OMS nel 2023: {days_above_OMS_2023}")
        plt.text(filtered_data['date'].iloc[0], 94, f"Giorni sopra il limite UE nel 2023: {days_above_EU_2023}")
        plt.text(filtered_data['date'].iloc[0], 96, f"Giorni sopra la soglia d'allarme nel 2023: {days_above_alarm_2023}")

        plt.text(filtered_data['date'].iloc[0], 100, f"Giorni sopra il limite OMS nel 2024: {days_above_OMS_2024}")
        plt.text(filtered_data['date'].iloc[0], 102, f"Giorni sopra il limite UE nel 2024: {days_above_EU_2024}")
        plt.text(filtered_data['date'].iloc[0], 104, f"Giorni sopra la soglia d'allarme nel 2024: {days_above_alarm_2024}")

        plt.text(filtered_data['date'].iloc[0], 108, f"Giorni sopra il limite OMS nel 2025: {days_above_OMS_2025}")
        plt.text(filtered_data['date'].iloc[0], 110, f"Giorni sopra il limite UE nel 2025: {days_above_EU_2025}")
        plt.text(filtered_data['date'].iloc[0], 112, f"Giorni sopra la soglia d'allarme nel 2025: {days_above_alarm_2025}")

        plt.text(filtered_data['date'].iloc[450], 98, f"Media di PM2.5 nel 2023: {avg_2023:.2f} \n(limite UE: {UE_limit_annual}, limite OMS: {WHO_limit_annual})")
        plt.text(filtered_data['date'].iloc[450], 106, f"Media di PM2.5 nel 2024: {avg_2024:.2f} \n(limite UE: {UE_limit_annual}, limite OMS: {WHO_limit_annual})")


    plt.yticks(range(0, int(filtered_data['Valore'].max()) + 5, 5))
    plt.xticks(filtered_data['date'], rotation=45, ha='right', fontsize=8)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(1, 13, 1)))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

    legend = plt.legend(frameon=False, loc='upper left')
    for line in legend.get_lines():
        line.set_linewidth(4)

    plt.style.use('seaborn-white')
    plt.tick_params(axis='x', direction='out', length=4, width=1, colors='black')

    plt.xlabel('')
    plt.ylabel('Concentrazione PM2.5 (µg/m³)')
    plt.title(f'Inquinamento PM2.5 in {city} ({start_date} - {end_date})', pad=10)

    if save==False:
        plt.show()


def plot_air_quality_pm10_lombardia(data, city, start_date, end_date, save=False, annotation=True):
    UE_limit = 45
    WHO_limit = 45
    alarm_limit = 90

    UE_limit_annual = 20
    WHO_limit_annual = 15

    # Sorting DataFrame by date within each station group
    data.sort_values('date', inplace=True)

    # Filter data to all times
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    days_above_EU = filtered_data[filtered_data['Valore'] > UE_limit].nunique()['Valore']
    days_above_alarm = filtered_data[filtered_data['Valore'] > alarm_limit].nunique()['Valore']
    days_above_OMS = filtered_data[filtered_data['Valore'] > WHO_limit].nunique()['Valore']

    if annotation:
        # Count number of days where in 2023
        start_2023 = pd.to_datetime('01/01/2023').date()
        end_2023 = pd.to_datetime('12/31/2023').date()

        data_2023 = data[(data['date'] >= start_2023) & (data['date'] <= end_2023)]
        days_above_EU_2023 = data_2023[data_2023['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2023 = data_2023[data_2023['Valore'] > alarm_limit].nunique()['Valore']
        days_above_OMS_2023 = data_2023[data_2023['Valore'] > WHO_limit].nunique()['Valore']

        avg_2023 = data_2023['Valore'].mean()

        # Count number of days where in 2024
        start_2024 = pd.to_datetime('01/01/2024').date()
        end_2024 = pd.to_datetime('12/31/2024').date()

        data_2024 = data[(data['date'] >= start_2024) & (data['date'] <= end_2024)]
        days_above_EU_2024 = data_2024[data_2024['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2024 = data_2024[data_2024['Valore'] > alarm_limit].nunique()['Valore']
        days_above_OMS_2024 = data_2024[data_2024['Valore'] > WHO_limit].nunique()['Valore']

        avg_2024 = data_2024['Valore'].mean()

        # Count number of days where in 2025
        start_2025 = pd.to_datetime('01/01/2025').date()
        end_2025 = pd.to_datetime('01/31/2025').date()

        data_2025 = data[(data['date'] >= start_2025) & (data['date'] <= end_2025)]
        days_above_EU_2025 = data_2025[data_2025['Valore'] > UE_limit].nunique()['Valore']
        days_above_alarm_2025 = data_2025[data_2025['Valore'] > 50].nunique()['Valore']
        days_above_OMS_2025 = data_2025[data_2025['Valore'] > WHO_limit].nunique()['Valore']

    # Calculate average value for each station
    average = filtered_data['Valore'].mean()

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(
        filtered_data['date'], 
        filtered_data['Valore'],
        label=f'ARPA (media di 91 stazioni)',
        linewidth=3
    )

    # horizontal dashed line for EU and WHO limits
    plt.axhline(y=WHO_limit, color='black', linestyle='--')
    plt.axhline(y=UE_limit, color='gray', linestyle='--')
    plt.axhline(y=alarm_limit, color='red', linestyle='--')

    plt.annotate(
        'Limite UE / OMS', 
        xy=(filtered_data['date'].iloc[110], UE_limit), 
        xytext=(filtered_data['date'].iloc[90], UE_limit+10),
        arrowprops=dict(facecolor='black', arrowstyle='-')
    )

    # plt.annotate(
    #     'Limite OMS', 
    #     xy=(filtered_data['date'].iloc[150], WHO_limit), 
    #     xytext=(filtered_data['date'].iloc[150], WHO_limit+15),
    #     arrowprops=dict(facecolor='black', arrowstyle='-')
    # )

    plt.text(filtered_data['date'].iloc[90], 86, "Soglia proposta per l'allarme")

    if annotation:
        plt.text(filtered_data['date'].iloc[0], 104, f"Giorni sopra il limite OMS nel 2023: {days_above_OMS_2023}")
        plt.text(filtered_data['date'].iloc[0], 107, f"Giorni sopra il limite UE nel 2023: {days_above_EU_2023}")
        plt.text(filtered_data['date'].iloc[0], 110, f"Giorni sopra la soglia d'allarme nel 2023: {days_above_alarm_2023}")

        plt.text(filtered_data['date'].iloc[0], 115, f"Giorni sopra il limite OMS nel 2024: {days_above_OMS_2024}")
        plt.text(filtered_data['date'].iloc[0], 118, f"Giorni sopra il limite UE nel 2024: {days_above_EU_2024}")
        plt.text(filtered_data['date'].iloc[0], 121, f"Giorni sopra la soglia d'allarme nel 2024: {days_above_alarm_2024}")

        plt.text(filtered_data['date'].iloc[0], 126, f"Giorni sopra il limite OMS nel 2025: {days_above_OMS_2025}")
        plt.text(filtered_data['date'].iloc[0], 129, f"Giorni sopra il limite UE nel 2025: {days_above_EU_2025}")
        plt.text(filtered_data['date'].iloc[0], 132, f"Giorni sopra la soglia d'allarme nel 2025: {days_above_alarm_2025}")

        plt.text(filtered_data['date'].iloc[450], 108, f"Media di PM2.5 nel 2023: {avg_2023:.2f} \n(limite UE: {UE_limit_annual}, limite OMS: {WHO_limit_annual})")
        plt.text(filtered_data['date'].iloc[450], 116, f"Media di PM2.5 nel 2024: {avg_2024:.2f} \n(limite UE: {UE_limit_annual}, limite OMS: {WHO_limit_annual})")

    plt.yticks(range(0, int(filtered_data['Valore'].max()) + 5, 5))
    plt.xticks(filtered_data['date'], rotation=45, ha='right', fontsize=8)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(1, 13, 1)))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

    legend = plt.legend(frameon=False, loc='upper left')
    for line in legend.get_lines():
        line.set_linewidth(4)

    plt.style.use('seaborn-white')
    plt.tick_params(axis='x', direction='out', length=4, width=1, colors='black')

    plt.xlabel('')
    plt.ylabel('Concentrazione PM10 (µg/m³)')
    plt.title(f'Inquinamento PM10 in {city} ({start_date} - {end_date})', pad=10)

    if save==False:
        plt.show()