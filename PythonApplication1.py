import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
import json
from matplotlib import patches 
import plotly as py
import plotly.graph_objs as go
from dateutil.parser import parse
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import time
import pytz

def format_date(z, pos=None):
    time_pr=matplotlib.dates.num2date(z)
    return datetime.strftime(time_pr,'%d %H:%M')


dt_start=parse("2018-08-11T12:00:00+0:00")
dt_end=parse("2018-08-13T6:00:00+0:00")
one_day=dt_end-dt_start
dt_start_axis=parse("2018-08-12T0:00:00")
dt_end_axis=parse("2018-08-13T0:00:00")
u = datetime.utcnow()
u = u.replace(tzinfo=pytz.utc)
while(dt_end<u):
    df=pd.read_json('http://217.23.157.236/karaf/ru.cos.cap.web.webapp/services/rest/find?timeStart={1}&timeEnd={0}'.format(int(time.mktime(dt_start.timetuple())*1000),int(time.mktime(dt_end.timetuple())*1000)), convert_dates=False)
    count=df["id"].count()
    print(count)
    t=[]
    temp=[]
    area=[]
    lat=[]
    lon=[]
    color=[(1,0,0),(0,1,0),(0,0,1)]
    lat_index=[]
    lon_index=[]
    area_index=[]
    i=0
    city_all=0
    for q in np.arange(count-1):
        time_str=df["infos"].iloc[q][0]["effective"]
        #index_of_bracket=time_str.rfind('[')
        time_datetime=parse(time_str)
        if (("ECOR_UNIT_Value" in df["infos"].iloc[q][0]["parametersMap"].keys())and (time_datetime>dt_start)):
            coord_array=df["infos"].iloc[q][0]["coordinates"]
            id=df["id"].iloc[q]
            df_details=pd.read_json('http://217.23.157.236/karaf/ru.cos.cap.web.webapp/services/rest/{0}/json'.format(str(id)), convert_dates=False)
            if ("areaDesc" in df_details["infos"].iloc[0]["coordinates"][0].keys()):
                area_in=df_details["infos"].iloc[0]["coordinates"][0]["areaDesc"]
                if (not len(lat_index)):
                    lat_index.append(coord_array[0][0])
                    lon_index.append(coord_array[0][1])
                    area_index.append(area_in)
                    t.append([])
                    temp.append([])
                    area.append([])
                    city_all+=1
                else:
                    flag=True
                    for index in np.arange(0,city_all,1):
                        if (area_in==area_index[index]): 
                            flag=False
                            break
                    if flag:
                        lat_index.append(coord_array[0][0])
                        lon_index.append(coord_array[0][1])
                        area_index.append(area_in)
                        t.append([])
                        temp.append([])
                        area.append([])
                        city_all+=1                
            if (len(coord_array)):
                lat.append(coord_array[0][0])
                lon.append(coord_array[0][1])
            else: 
                continue
            time_plot=matplotlib.dates.date2num(time_datetime)
            for city in range(city_all):
                if (area_in==area_index[city]):
                    t[city].append(time_plot)
                    temp[city].append(float(df["infos"].iloc[q][0]["parametersMap"]["ECOR_UNIT_Value"]))
                    area[city].append(area_in)
            i+=1
        if (("METEO_UNIT_Temperature" in df["infos"].iloc[q][0]["parametersMap"].keys())and (time_datetime>dt_start)):
            coord_array=df["infos"].iloc[q][0]["coordinates"]
            id=df["id"].iloc[q]
            df_details=pd.read_json('http://217.23.157.236/karaf/ru.cos.cap.web.webapp/services/rest/{0}/json'.format(str(id)), convert_dates=False)
            if ("areaDesc" in df_details["infos"][0]["coordinates"][0].keys()):
                area_in=df_details["infos"].iloc[0]["coordinates"][0]["areaDesc"]
                if (not len(lat_index)):
                    lat_index.append(coord_array[0][0])
                    lon_index.append(coord_array[0][1])
                    area_index.append(area_in)
                    t.append([])
                    temp.append([])
                    area.append([])
                    city_all+=1
                else:
                    flag=True
                    for index in np.arange(0,city_all,1):
                        if (area_in==area_index[index]): 
                            flag=False
                            break
                    if flag:
                        lat_index.append(coord_array[0][0])
                        lon_index.append(coord_array[0][1])
                        area_index.append(area_in)
                        t.append([])
                        temp.append([])
                        area.append([])
                        city_all+=1                
            if (len(coord_array)):
                lat.append(coord_array[0][0])
                lon.append(coord_array[0][1])
            else: 
                continue
            time_plot=matplotlib.dates.date2num(time_datetime)
            for city in range(city_all):
                if (area_in==area_index[city]):
                    t[city].append(time_plot)
                    temp[city].append(float(df["infos"].iloc[q][0]["parametersMap"]["METEO_UNIT_Temperature"]))
                    area[city].append(area_in)

    print(area_index)
    fig, ax = plt.subplots(figsize=(10,5))
    plt.title('Температура в Испании по городам', fontsize=14)
    ax.xaxis.set_major_locator(plt.LinearLocator(numticks=2))   
    print(dt_start_axis," ",dt_end_axis,matplotlib.dates.num2date(t[0][0]))
    ax.set_xlim(left=matplotlib.dates.date2num(dt_start_axis),right=matplotlib.dates.date2num(dt_end_axis))
    ax.set_ylim(bottom=-20,top=60)
    ax.yaxis.set_major_locator(plt.LinearLocator(numticks=9))
    myFmt=matplotlib.dates.DateFormatter("%d.%m.%y")
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_minor_locator(plt.LinearLocator(numticks=25))
    ax.yaxis.set_minor_locator(plt.LinearLocator(numticks=17))
    plt.xlabel("Дата и время")
    plt.ylabel("Температура")
    for i in np.arange(0,city_all,1):
        ax.plot(t[i],temp[i],label=area[i][0])
    lgd=plt.legend(loc=2,bbox_to_anchor=(1.1,0.5,0.3,1),ncol=2)
    fig.savefig('samplefigure',bbox_extra_artists=(lgd,), bbox_inches='tight')
    dt_start+=one_day
    dt_end+=one_day
    dt_start_axis+=one_day
    dt_end_axis+=one_day

