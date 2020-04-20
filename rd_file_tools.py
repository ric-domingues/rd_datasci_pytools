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