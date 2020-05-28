# PACKAGE: rd_tseries_tools
# Description: This package includes a few commonly used tools when carrying out time-series analysis
#              It automatically imports some of the required dependencies that are required
# Author: Ricardo Domingues

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpltPath
import datetime as dt
import math
from datetime import date, timedelta, datetime
#========================================================= FUNCTION to list file_uses from AVISO RT and DT

#--------------------------------------------------- function to calculate annual period average
def calc_annaul_period_mean(start_jday,end_jday,time,var):
  yyyy_aux = np.arange(np.floor(np.min(time)), np.floor(np.max(time)), 1)  
  var_ann = np.empty(yyyy_aux.shape); var_ann[:]=np.nan
  
  c=-1
  for y in yyyy_aux:
    c=c+1
    start_dt = y + start_jday/365
    end_dt   = y + end_jday/365    
    ind_time = ( time>=start_dt) & (time<=end_dt)
    var_ann[c] = np.nanmean(var[ind_time])    
  
  return yyyy_aux, var_ann


#--------------------------------------------------- function to simple moving average
def rmean(var,wdith):
 
  xsmo = np.empty(var.shape); xsmo[:]=np.nan
  wid = int(np.round((wdith-1)/2));
  
  len_var = len(xsmo)
  for i in range(0,len_var-1):
    if(i < wid+1):
      xsmo[i] = np.nanmean(var[0:i+wid])

    elif(i > (len_var-1)-wid):
      xsmo[i] = np.nanmean(var[i-wid:len_var-1])

    else:
      xsmo[i] = np.nanmean(var[i-wid:i+wid])

    # print(i,xsmo[i])
    mask=np.isnan(var)
    # xsmo[mask] = np.nan



  return xsmo

#--------------------------------------------------- function to simple moving average
def get_trend(xtime,yval):

  X_val=xtime

  print('getting trend>>')
  mask=np.logical_not(np.isnan(xtime))
  xtime=xtime[mask]
  yval=yval[mask]

  mask=np.logical_not(np.isnan(yval))
  xtime=xtime[mask]
  yval=yval[mask]
  P = np.polyfit(xtime, yval, 1)
  Pval = np.poly1d(np.polyfit(xtime, yval, 1))
  v_trend=P[0]
  Y_val=Pval(X_val)

  return v_trend,X_val,Y_val


#--------------------------------------------------- function to simple moving average
def timenum2datetime(timenum,refdate):
  

  time_datetimeobj = []
  for i in range(0,len(timenum)):
    d = dt.datetime(refdate[0],refdate[1],refdate[2],refdate[3],refdate[4]) + dt.timedelta(seconds=timenum[i])
    time_datetimeobj.append(d)   
    
  return time_datetimeobj

#--------------------------------------------------- function to simple moving average
def timenum2datetime_ndays(timenum,refdate):


  time_datetimeobj = []
  for i in range(0,len(timenum)):
    d = dt.datetime(refdate[0],refdate[1],refdate[2],refdate[3],refdate[4]) + dt.timedelta(days=timenum[i])
    time_datetimeobj.append(d)

  return time_datetimeobj

#--------------------------------------------------- ceil datetime object to next day 
def ceil_dt(date_use):
    daysecs=86400
    nsecs = date_use.hour*3600 + date_use.minute*60 + date_use.second    
    delta = daysecs - nsecs
    return date_use + dt.timedelta(seconds=delta)

#--------------------------------------------------- floor datetime object to next day 
def floor_dt(date_use):
    daysecs=86400
    nsecs = date_use.hour*3600 + date_use.minute*60 + date_use.second    
    delta = - nsecs
    return date_use + dt.timedelta(seconds=delta)
 
#--------------------------------------------------- floor datetime object to next day 
def floor_dt(date_use):
    daysecs=86400
    nsecs = date_use.hour*3600 + date_use.minute*60 + date_use.second    
    delta = - nsecs
    return date_use + dt.timedelta(seconds=delta)


def datevec(t_ordinal):
  t_vec = []
  t_datetime = []

  for i in range(0,len(t_ordinal)):    
    t_date  = str(date.fromordinal(int(t_ordinal[i])-366))
    td    = str(timedelta(days=t_ordinal[i]%1))
    yr    = t_date[0:4]
    mon   = t_date[5:7]
    day   = t_date[8:10]
    if td[0:2].isdigit() == False:
      hrs   = td[0:1]
      mins  = td[2:4]
      secs  = td[5:]
    else:
      hrs   = td[0:2]
      mins  = td[3:5]
      secs  = td[6:]

    t_aux = np.array([yr, mon, day, hrs, mins, secs])
    t_vec.append([yr, mon, day, hrs, mins, secs])
    s=int(np.floor(float(secs)))
    d=dt.datetime(int(yr), int(mon), int(day), int(hrs), int(mins), s)
    t_datetime.append(d)

  return t_vec, t_datetime
  

# This function is inverse to datevec. That is, takes
# a date vector of yr, month, day, etc. and converts it
# into a serial date. Note that there will be some
# disagreement between Matlab and Python routines. Upon
# testing, the Python routine matches Matlab's 'datenum'
# function up to four decimal places.
#
# NOTE:
  # This function assumes the time vector to have the same
  # orientation as what is given in datevec, i.e. 
  # ['year', 'month', 'day', 'hrs' 'sec', 'ms'].
def datenum(t_vec):

  t_num = []

  for i in range(0,len(t_vec)):

    year  = np.int(t_vec[i][0])
    mon   = np.int(t_vec[i][1])
    day   = np.int(t_vec[i][2])
    hrs   = np.int(t_vec[i][3])
    mins  = np.int(t_vec[i][4])
    secs  = np.int(np.round(np.float(t_vec[i][5])))
    if secs == 60:
       secs = 0
       mins = mins + 1
       datestr = dt.datetime(year, mon, day, hrs, mins, secs)
       frac_datestr= (hrs + (mins + secs / 60) / 60)/24
       serial_date = date.toordinal(datestr) + 366 + frac_datestr
    else:
       datestr = dt.datetime(year, mon, day, hrs, mins, secs)
       frac_datestr= (hrs + (mins + secs / 60) / 60)/24
       serial_date = date.toordinal(datestr) + 366 + frac_datestr
    
    t_num.append(serial_date)
    # Subtract 366 since MATLAB has a preset date of 1-1-0000
    # and PYTHON has a preset date of 1-1-0001
  t_num = np.array(t_num)
  return t_num #- 366
