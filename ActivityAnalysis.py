import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import seaborn as sns
import numpy as np
import os
import datetime
import math


def DailyAnalysis():
    date = ""
    while True:
        try:
            date = input("Enter date in format (YYYY-MM-DD) : ")
            date = datetime.datetime.strptime(date,'%Y-%m-%d')
            date = date.strftime('%Y-%m-%d')
            break
        except ValueError:
            os.system('cls')
            print("Incorrect Date Format!")
            print("Please date in required format (YYYY-MM-DD)!")   

    dateData = data[data["Date"]==date]
    
    if dateData.empty:
        print("No record found for this date!")
        DailyAnalysis()
    else:
        # print(dateData.head())
        totalScreenTime = 0
        totalTimeSeconds = []
        for totalTime in dateData["Total Time(h:m:s)"]:
            h,m,s = totalTime.split(':')
            totalTimeSeconds.append((int(h)*60+int(m))*60 + float(s))
            totalScreenTime += (int(h)*60+int(m))*60 + float(s)
        totalScreenTime = math.ceil(totalScreenTime)
        print("Total Screen Time : " + str(totalScreenTime) + " s")

        dateData["Time spent in seconds"] = pd.Series(totalTimeSeconds)

        with matplotlib.backends.backend_pdf.PdfPages("DailyAnalysis" + str(date) +".pdf") as pdf:
            temp = dateData.groupby(["Activity Name"])["Time spent in seconds"].sum()
            plt.figure(figsize=(20,6))
            sns.barplot(y=temp.index.values,x=temp.values)
            plt.title("Total time spent in different Activities")
            plt.ylabel("Activity Names")
            plt.xlabel("Time spent in seconds")
            pdf.savefig()
            plt.close()

            temp = dateData[dateData["isWebBrowser"]==1].groupby(["Website"])["Time spent in seconds"].sum()
            plt.figure(figsize=(20,6))
            sns.barplot(y=temp.index.values,x=temp.values)
            plt.title("Total time spent in different Websites")
            plt.ylabel("Website Names")
            plt.xlabel("Time spent in seconds")
            pdf.savefig()
            plt.close()
            

def WeeklyAnalysis():
    pass

def MonthlyAnalysis():
    pass

def YearlyAnalysis():
    pass


def getChoice():
    print("------------------MENU-------------------")
    print(":\t1. Daily Analysis\t\t:")
    print(":\t2. Weekly Analysis\t\t:")
    print(":\t3. Monthly Analysis\t\t:")
    print(":\t4. Yearly Analysis\t\t:")
    print(":\t5. Exit\t\t\t\t:")
    print("-----------------------------------------")
    return input("Select an option : ")


def startAnalysis():
    choice  = getChoice()
    while choice not in ['1','2','3','4','5']:
        os.system('cls')
        print("Please select the correct option!\n")
        choice = getChoice()
    
    if choice == '1':
        DailyAnalysis()
    elif choice == '2':
        WeeklyAnalysis()
    elif choice == '3':
        MonthlyAnalysis()
    elif choice == '4':
        YearlyAnalysis()
    else:
        print("Thank you!")
        return


if __name__ == "__main__":
    os.system('cls')
    if not os.path.exists('ActivityData.csv'):
        print("Required file (ActivityData.csv) not found!")
        print("Please make sure the file is in the same directory where this program is stored!")
    else:
        global data

        data = pd.read_csv('ActivityData.csv')
        
        # addTimeBlock()
        startAnalysis()