#PACKAGE: rd_file_tools
# Description: This package includes a collection of functions for handling files
# Author: Ricardo Domingues

import glob, calendar
from datetime import datetime
import os.path 
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import fnmatch
import os
    
#--------------------------------------------------- List Files in a Directory
def list_files(direc,pattern):
  files_list=[]  
  for file in sorted(os.listdir(direc)):
    if fnmatch.fnmatch(file, pattern):
        files_list.append(file)
        

  return files_list

#--------------------------------------------------- read ascii FILE columns 
def ascii_tab_read(ascii_file):
  fid = open(ascii_file, 'r')  
  T=[]
  for line in fid:
    line = line.strip()
    columns = line.split()
    T.append(columns)
  
  return T

#--------------------------------------------------- read ascii FILE columns 
def filename2date(filename):
  yyyy=float(filename[0:4])
  mm=float(filename[4:6])
  dd=float(filename[6:8])
  date_str=str(filename[4:6]+"/"+filename[6:8]+"/"+filename[0:4])
  
  
  return yyyy,mm,dd,date_str

#--------------------------------------------------- List with Date names
def list_files_bydate(direc,pattern):
  files_list      =[] 
  datetime_files  =[]
  timesec_files   =[]

  file_uses_use=glob.glob(direc+"/"+pattern)

  for file_use in file_uses_use:
    date_file_use=datetime.strptime(os.path.basename(file_use)[0:8], '%Y%m%d')
    datetime_files.append(date_file_use)
    timesec_files.append( calendar.timegm( date_file_use.timetuple() ) )
    files_list.append(file_use)

  return files_list, datetime_files, timesec_files
