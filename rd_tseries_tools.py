# PACKAGE: rd_tseries_tools
# Description: This package includes a few commonly used tools when carrying out time-series analysis
#              It automatically imports some of the required dependencies that are required 
# Author: Ricardo Domingues
#
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpltPath
import datetime as dt
import math
#========================================================= FUNCTION to list file_uses from AVISO RT and DT

#--------------------------------------------------- function to exract date information from file name
def filename2date(filename):
  yyyy=float(filename[0:4])
  mm=float(filename[4:6])
  dd=float(filename[6:8])
  date_str=str(filename[4:6]+"/"+filename[6:8]+"/"+filename[0:4])
  
  
  return yyyy,mm,dd,date_str

#--------------------------------------------------- function to calculate annual period average
def calc_annaul_period_mean(start_jday,end_jday,time,var):
  yyyy_aux = np.arange(np.floor(np.min(time)), np.floor(np.max(time)), 1)  
  var_ann = np.empty(yyyy_aux.shape); var_ann[:]=np.nan
  
  c=-1
  for y in yyyy_aux:
    c+=1
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

#--------------------------------------------------- function to calculate a simple linear trend line
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


#--------------------------------------------------- transforms continuous time reference in seconds to datetime objects
def timenum2datetime(timenum,refdate):
  

  time_datetimeobj = []
  for i in range(0,len(timenum)):
    d = dt.datetime(refdate[0],refdate[1],refdate[2],refdate[3],refdate[4]) + dt.timedelta(seconds=timenum[i])
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
 


