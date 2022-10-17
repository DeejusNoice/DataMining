from datetime import datetime
from datetime import timedelta

import numpy as np
import pandas as pd


def Percent_Hyper(dataframe):
    count = 0
    for data in dataframe['Sensor Glucose (mg/dL)'].items():
        if data[1] > 180:
            count += 1
    return count / 288


def Percent_Hyper_Critical(dataframe):
    count = 0
    for data in dataframe['Sensor Glucose (mg/dL)'].items():
        if data[1] > 250:
            count += 1
    return count / 288


def Percent_Normal(dataframe):
    count = 0
    for data in dataframe['Sensor Glucose (mg/dL)'].items():
        if 180 >= data[1] >= 70:
            count += 1
    return count / 288


def Percent_Secondary(dataframe):
    count = 0
    for data in dataframe['Sensor Glucose (mg/dL)'].items():
        if 150 >= data[1] >= 70:
            count += 1
    return count / 288


def Percent_Hypo1(dataframe):
    count = 0
    for data in dataframe['Sensor Glucose (mg/dL)'].items():
        if 70 > data[1]:
            count += 1
    return count / 288


def Percent_Hypo2(dataframe):
    count = 0
    for data in dataframe['Sensor Glucose (mg/dL)'].items():
        if 54 > data[1]:
            count += 1
    return count / 288


def Night_Part(dataframe):
    overnightCutoff = datetime.strptime("06:00:00", "%H:%M:%S")
    splitIndex = 0
    for data in dataframe['Time'].items():
        if datetime.strptime(data[1], "%H:%M:%S") < overnightCutoff:
            splitIndex = data[0]
            break
    nightData = dataframe.query(f'index > {splitIndex - 1}')
    return nightData


def Day_Part(dataframe):
    overnightCutoff = datetime.strptime("06:00:00", "%H:%M:%S")
    splitIndex = 0
    for data in dataframe['Time'].items():
        if datetime.strptime(data[1], "%H:%M:%S") < overnightCutoff:
            splitIndex = data[0]
            break
    DayData = dataframe.query(f'index < {splitIndex}')
    return DayData


def Night_Hyper(dataframe):
    nightData = Night_Part(dataframe)
    return Percent_Hyper(nightData)


def Night_Hyper_Critical(dataframe):
    nightData = Night_Part(dataframe)
    return Percent_Hyper_Critical(nightData)


def Night_Normal(dataframe):
    nightData = Night_Part(dataframe)
    return Percent_Normal(nightData)


def Night_Secondary(dataframe):
    nightData = Night_Part(dataframe)
    return Percent_Secondary(nightData)


def Night_Hypo1(dataframe):
    nightData = Night_Part(dataframe)
    return Percent_Hypo1(nightData)


def Night_Hypo2(dataframe):
    nightData = Night_Part(dataframe)
    return Percent_Hypo2(nightData)


def Day_Hyper(dataframe):
    dayData = Day_Part(dataframe)
    return Percent_Hyper(dayData)


def Day_Hyper_Critical(dataframe):
    dayData = Day_Part(dataframe)
    return Percent_Hyper_Critical(dayData)


def Day_Normal(dataframe):
    dayData = Day_Part(dataframe)
    return Percent_Normal(dayData)


def Day_Secondary(dataframe):
    dayData = Day_Part(dataframe)
    return Percent_Secondary(dayData)


def Day_Hypo1(dataframe):
    dayData = Day_Part(dataframe)
    return Percent_Hypo1(dayData)


def Day_Hypo2(dataframe):
    dayData = Day_Part(dataframe)
    return Percent_Hypo2(dayData)


def Auto_Split_Time(dataframe):
    autoIndex = 0
    for data in dataframe['Alarm'].items():
        if data[1] == 'AUTO MODE ACTIVE PLGM OFF':
            autoIndex = data[0] + 1
    timeValue = dataframe.loc[autoIndex, 'Time']
    dateValue = dataframe.loc[autoIndex, 'Date']
    return dateValue, timeValue

def Split_CGM_Data(insulinData, cgmData):
    date, time = Auto_Split_Time(insulinData)
    splitDay = cgmData.loc[cgmData['Date'] == date]
    splitIndex = 0
    for data in splitDay['Time'].items():
        if datetime.strptime(data[1], "%H:%M:%S") < datetime.strptime(time, "%H:%M:%S"):
            splitIndex = data[0]
            break
    cgmManual = cgmData[splitIndex:]
    cgmAuto = cgmData[:splitIndex]
    return cgmManual, cgmAuto

def Subtract_Day(date):
    # Convert date to subtractable date object
    year = int(date.split("/")[2])
    month = int(date.split("/")[0])
    day = int(date.split("/")[1])
    date1 = datetime(year, month, day)
    oneDay = timedelta(days=1)
    newDate = date1 - oneDay

    # Convert new date back to string
    daystring = newDate.strftime("%d")
    if daystring[0] == '0':
        daystring = daystring[1]
    monthstring = newDate.strftime("%m")
    if monthstring[0] == '0':
        monthstring = monthstring[1]
    yearstring = newDate.strftime("%Y")
    newdayString = monthstring + "/" + daystring + "/" + yearstring
    return newdayString

def Calc_Percentages(dataframe):
    dayData = dataframe
    percentData = np.array([[Night_Hyper(dayData), Night_Hyper_Critical(dayData), Night_Normal(dayData),
                             Night_Secondary(dayData), Night_Hypo1(dayData), Night_Hypo2(dayData),
                             Day_Hyper(dayData), Day_Hyper_Critical(dayData), Day_Normal(dayData),
                             Day_Secondary(dayData), Day_Hypo1(dayData), Day_Hypo2(dayData),
                             Percent_Hyper(dayData), Percent_Hyper_Critical(dayData), Percent_Normal(dayData),
                             Percent_Secondary(dayData), Percent_Hypo1(dayData), Percent_Hypo2(dayData)]])
    cols = ['Overnight Hyperglycemia', 'Overnight Hyperglycemia Critical', 'Overnight Normal',
            'Overnight Secondary', 'Overnight Hypoglycemia 1', 'Overnight Hypoglycemia 2',
            'Daytime Hyperglycemia', 'Daytime Hyperglycemia Critical', 'Daytime Normal',
            'Daytime Secondary', 'Daytime Hypoglycemia 1', 'Daytime Hypoglycemia 2',
            'Whole Day Hyperglycemia', 'Whole Day Hyperglycemia Critical', 'Whole Day Normal',
            'Whole Day Secondary', 'Whole Day Hypoglycemia 1', 'Whole Day Hypoglycemia 2']
    percentDataframe = pd.DataFrame(percentData, columns=cols)
    return percentDataframe

def Calc_All(dataframe):
    # Loop through each date and calculate percentages
    # Start with first date in dataframe
    startDate = dataframe.iat[0, 0]
    dayData = dataframe.loc[dataframe['Date'] == startDate]

    # calculate percentages and store them
    percentDataframe = Calc_Percentages(dayData)

    # Check if new date has sensor information
    newdate = Subtract_Day(startDate)
    while newdate in dataframe['Date'].values:
        dayData = dataframe.loc[dataframe['Date'] == newdate]
        if dayData['Sensor Glucose (mg/dL)'].count() / 288 < 0.8:
            newdate = Subtract_Day(newdate)
            continue
        else:
            percentData = Calc_Percentages(dayData)
            percentDataframe = percentDataframe.append(percentData)
            newdate = Subtract_Day(newdate)
    return percentDataframe

def Calc_Means(dataframe):
    meanData = np.array([[dataframe['Overnight Hyperglycemia'].mean()*100, dataframe['Overnight Hyperglycemia Critical'].mean()*100,
                          dataframe['Overnight Normal'].mean()*100, dataframe['Overnight Secondary'].mean()*100,
                          dataframe['Overnight Hypoglycemia 1'].mean()*100, dataframe['Overnight Hypoglycemia 2'].mean()*100,
                          dataframe['Daytime Hyperglycemia'].mean()*100, dataframe['Daytime Hyperglycemia Critical'].mean()*100,
                          dataframe['Daytime Normal'].mean()*100, dataframe['Daytime Secondary'].mean()*100,
                          dataframe['Daytime Hypoglycemia 1'].mean()*100, dataframe['Daytime Hypoglycemia 2'].mean()*100,
                          dataframe['Whole Day Hyperglycemia'].mean()*100, dataframe['Whole Day Hyperglycemia Critical'].mean()*100,
                          dataframe['Whole Day Normal'].mean()*100, dataframe['Whole Day Secondary'].mean()*100,
                          dataframe['Whole Day Hypoglycemia 1'].mean()*100, dataframe['Whole Day Hypoglycemia 2'].mean()*100]])
    cols = ['Overnight Hyperglycemia', 'Overnight Hyperglycemia Critical', 'Overnight Normal',
            'Overnight Secondary', 'Overnight Hypoglycemia 1', 'Overnight Hypoglycemia 2',
            'Daytime Hyperglycemia', 'Daytime Hyperglycemia Critical', 'Daytime Normal',
            'Daytime Secondary', 'Daytime Hypoglycemia 1', 'Daytime Hypoglycemia 2',
            'Whole Day Hyperglycemia', 'Whole Day Hyperglycemia Critical', 'Whole Day Normal',
            'Whole Day Secondary', 'Whole Day Hypoglycemia 1', 'Whole Day Hypoglycemia 2']
    meanDataframe = pd.DataFrame(meanData, columns=cols)
    return meanDataframe


cgmData = pd.read_csv('CGMData.csv', usecols=['Date', 'Time', 'Sensor Glucose (mg/dL)'])
insulinData = pd.read_csv('InsulinData.csv', usecols=['Alarm', 'Time', 'Date'])

cgmManual, cgmAuto = Split_CGM_Data(insulinData, cgmData)
manualData = Calc_All(cgmManual)
autoData = Calc_All(cgmAuto)

manualMeans = Calc_Means(manualData)
autoMeans = Calc_Means(autoData)

results = manualMeans.append(autoMeans)

results.to_csv("Results.csv", header=False)