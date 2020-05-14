 #PACKAGE: rd_ocean_tools
# Description: This package includes a collection of functions pretaining to the realm of Physical Oceanography & Meteorology
# Author: Ricardo Domingues
#
import glob, calendar
from datetime import datetime
import os.path 
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import fnmatch
import os
#========================================================= FUNCTION to list file_uses from AVISO RT and DT

#--------------------------------------------------- Function to List AVISO RT and DT files
def altimetry_file_list(altimetry_rt,altimetry_dt):
  
  file_uses_rt=glob.glob(altimetry_rt+"/*[!latest].nc")
  file_uses_use=glob.glob(altimetry_dt+"/*.nc")
  
  datetime_altimetry=[]
  timesecs_altimetry=[]
  altim_fyle_type   =[]
  
  for file_use in file_uses_use:
    date_file_use=datetime.strptime(os.path.basename(file_use)[24:32], '%Y%m%d')
    datetime_altimetry.append(date_file_use)
    timesecs_altimetry.append( calendar.timegm( date_file_use.timetuple() ) )
    altim_fyle_type.append('DT')
  
  date_dt_last = datetime_altimetry[-1]
  for file_use in file_uses_rt:  
    date_file_use=datetime.strptime(os.path.basename(file_use)[25:33], '%Y%m%d')   
    if(date_file_use > date_dt_last):
      file_uses_use.append(file_use)
      datetime_altimetry.append(date_file_use)
      timesecs_altimetry.append( calendar.timegm( date_file_use.timetuple() ) )
      altim_fyle_type.append('RT')
        #print(file_use)
  return file_uses_use, datetime_altimetry, timesecs_altimetry, altim_fyle_type

#--------------------------------------------------- Function to List AVISO RT and DT files
def altimetry_file_list_all(altimetry_rt,altimetry_dt):
  
  file_uses_rt=glob.glob(altimetry_rt+"/*[!latest].nc")
  file_uses_use=glob.glob(altimetry_dt+"/*.nc")
  
  datetime_altimetry=[]
  timesecs_altimetry=[]
  altim_fyle_type   =[]
  
  for file_use in file_uses_use:
    date_file_use=datetime.strptime(os.path.basename(file_use)[24:32], '%Y%m%d')
    datetime_altimetry.append(date_file_use)
    timesecs_altimetry.append( calendar.timegm( date_file_use.timetuple() ) )
    altim_fyle_type.append('DT')
  
  for file_use in file_uses_rt:  
    
    file_uses_use.append(file_use)
    datetime_altimetry.append(date_file_use)
    timesecs_altimetry.append( calendar.timegm( date_file_use.timetuple() ) )
    altim_fyle_type.append('RT')
        #print(file_use)
  return file_uses_use, datetime_altimetry, timesecs_altimetry, altim_fyle_type  

#--------------------------------------------------- Generic Function to read AVISO files to subset
def read_altimetry_sha(file_use,LON_LIM,LAT_LIM):
  print('     - reading AVISO: '+file_use)
  nc_fid = nc.Dataset(file_use,'r')
  
  lon_sha = nc_fid.variables['longitude'][:] 
  lon_sha[lon_sha>180] = lon_sha[lon_sha>180] - 360    
  srt_lon = np.argsort(lon_sha)
  lon_sha = lon_sha[srt_lon] 
  lat_sha = nc_fid.variables['latitude'][:] 
  lon_sha2, lat_sha2 = np.meshgrid(lon_sha, lat_sha)
  sha = nc_fid.variables['sla'][:][0]
  sha = sha[:,srt_lon]

  sha_out = sha
  lon_out = lon_sha2
  lat_out = lat_sha2
  
  ind_lon = (lon_sha>=LON_LIM[0]) & (lon_sha<=LON_LIM[1])
  sha_out = sha_out[:,ind_lon]
  lon_out = lon_out[:,ind_lon]
  lat_out = lat_out[:,ind_lon]
  lon_sha = lon_sha[ind_lon]
  
  ind_lat = (lat_sha>=LAT_LIM[0]) & (lat_sha<=LAT_LIM[1])
  sha_out = sha_out[ind_lat,:]
  lon_out = lon_out[ind_lat,:]
  lat_out = lat_out[ind_lat,:]
  lat_sha = lat_sha[ind_lat]
    
  #plt.contourf(lon_out,lat_out,sha_out),
  #plt.show()
  #exit()
  
  return sha_out, lon_sha, lat_sha, lon_out, lat_out

#--------------------------------------------------- Generic Function to read AVISO files to subset
def read_altimetry_sha_all(file_use,LON_LIM,LAT_LIM,resort_lon=True):
  print('     - reading AVISO: '+file_use)
  nc_fid = nc.Dataset(file_use,'r')

  lon_sha = nc_fid.variables['longitude'][:]
  lat_sha = nc_fid.variables['latitude'][:]  
  sha = nc_fid.variables['sla'][:][0]
  adt = nc_fid.variables['adt'][:][0]
  vgos = nc_fid.variables['vgos'][:][0]    
  ugos = nc_fid.variables['ugos'][:][0]


  if resort_lon:
    lon_sha[lon_sha>180] = lon_sha[lon_sha>180] - 360
    srt_lon = np.argsort(lon_sha)
    lon_sha = lon_sha[srt_lon]
    sha = sha[:,srt_lon]
    adt = adt[:,srt_lon]
    vgos = vgos[:,srt_lon]
    ugos = vgos[:,srt_lon]    

  lon_sha2, lat_sha2 = np.meshgrid(lon_sha, lat_sha)
  fillValue = getattr(nc_fid.variables['sla'], '_FillValue')
  sha[sha<=fillValue+1] = np.nan
  adt[adt<=fillValue+1] = np.nan
  vgos[vgos<=fillValue+1] = np.nan
  ugos[ugos<=fillValue+1] = np.nan

  sha_out = sha
  adt_out = adt
  vgos_out= vgos
  ugos_out= ugos

  lon_out = lon_sha2
  lat_out = lat_sha2

  ind_lon = (lon_sha>=LON_LIM[0]) & (lon_sha<=LON_LIM[1])
  sha_out = sha_out[:,ind_lon]
  adt_out = adt_out[:,ind_lon]
  vgos_out= vgos_out[:,ind_lon]
  ugos_out= ugos_out[:,ind_lon]

  lon_out = lon_out[:,ind_lon]
  lat_out = lat_out[:,ind_lon]
  lon_sha = lon_sha[ind_lon]

  ind_lat = (lat_sha>=LAT_LIM[0]) & (lat_sha<=LAT_LIM[1])
  sha_out = sha_out[ind_lat,:]
  adt_out = adt_out[ind_lat,:]
  vgos_out= vgos_out[ind_lat,:]
  ugos_out= ugos_out[ind_lat,:]

  lon_out = lon_out[ind_lat,:]
  lat_out = lat_out[ind_lat,:]
  lat_sha = lat_sha[ind_lat]

  #plt.contourf(lon_out,lat_out,sha_out),
  #plt.show()
  #exit()
  return sha_out, adt_out, vgos_out, ugos_out, lon_out, lat_out, lon_sha, lat_sha

# =============================================== PLOT TC tracks (Wind in Knots, Saffir-Sympson Scale)
def plot_TCs_track(ax,TC_lon,TC_lat,TC_wind,szfac=1):

  ax.plot(TC_lon,TC_lat,'-',linewidth=2*szfac,color='lightgray',zorder=35)
  lbl_td, = ax.plot(TC_lon[(TC_wind>=0) & (TC_wind<34) ],TC_lat[(TC_wind>0) & (TC_wind<=33)],'x',markeredgewidth=2*szfac, markersize=5*szfac,color='r',markeredgecolor='r',zorder=35)
  lbl_ts, = ax.plot(TC_lon[(TC_wind>=34) & (TC_wind<64) ],TC_lat[(TC_wind>=34) & (TC_wind<64)],'o',markeredgewidth=2.5*szfac, markersize=5*szfac,markeredgecolor='b',markerfacecolor='none',zorder=35)
  lbl_cat1, = ax.plot(TC_lon[(TC_wind>=64) & (TC_wind<83) ],TC_lat[(TC_wind>64) & (TC_wind<=83)],'o',markeredgewidth=1.5*szfac, markersize=6.5*szfac,color=[.1,.9,.9],markeredgecolor='k',zorder=35)
  lbl_cat2, = ax.plot(TC_lon[(TC_wind>=83) & (TC_wind<96) ],TC_lat[(TC_wind>83) & (TC_wind<=96)],'o',markeredgewidth=1.5*szfac, markersize=6.5*szfac,color=[.4,.9,.4],markeredgecolor='k',zorder=35)
  lbl_cat3, = ax.plot(TC_lon[(TC_wind>=96) & (TC_wind<113) ],TC_lat[(TC_wind>96) & (TC_wind<=113)],'o',markeredgewidth=1.5*szfac, markersize=7*szfac,color=[.9,.9,.3],markeredgecolor='k',zorder=35)
  lbl_cat4, = ax.plot(TC_lon[(TC_wind>=113) & (TC_wind<137) ],TC_lat[(TC_wind>113) & (TC_wind<=137)],'o',markeredgewidth=1.5*szfac, markersize=7*szfac,color=[.9,.5,.1],markeredgecolor='k',zorder=35)
  lbl_cat5, = ax.plot(TC_lon[(TC_wind>=137)],TC_lat[(TC_wind>137)],'o',markeredgewidth=1.5*szfac, markersize=7*szfac,color=[.9,.4,.4],markeredgecolor='k',zorder=35)

  lbl_cats = (lbl_td, lbl_ts, lbl_cat1, lbl_cat2, lbl_cat3, lbl_cat4, lbl_cat5)
  lbl_strs = ('TD', 'TS', 'Cat-1', 'Cat-2', 'Cat-3', 'Cat-4', 'Cat-5')

  # usage: ax.legend(lbl_cats, lbl_strs,handletextpad=0.01,borderpad=1,loc='lower left')  
  return lbl_cats, lbl_strs

#--------------------------------------------------- function to simple moving average
def box_average_profile(var,z,dz,maxdepth):
 
  zref=np.arange(0,maxdepth+dz,dz)
  box_var = np.empty((len(zref),1)); box_var[:]=np.nan

  for k in range(0,len(zref)):

    box_var[k] = np.nanmean( var[ (z>=zref[k]-dz/2) & (z<=zref[k]+dz/2) ] )

  mask = np.isnan(box_var)

  box_varnonans = inpaint_nans(box_var)
  box_var[mask] = np.nan
  box_varnonans[zref>np.nanmax(z)+dz]=np.nan
  return zref, box_var, box_varnonans

# =============================================== PLOT TC tracks (Wind in Knots, Saffir-Sympson Scale)
def plot_TCs_track_lines(ax,TC_lon,TC_lat,TC_wind,szfac=1,lincol='lightgray',alp_lin=1):

  for i in range(0,len(TC_lon)-1):
    lon_aux=TC_lon[i:i+2]
    lat_aux=TC_lat[i:i+2]

    if(TC_wind[i]>=0) & (TC_wind[i]<50):
      lbl_td, = ax.plot(lon_aux,lat_aux,'--',linewidth=0.5*szfac,color='k',zorder=35,alpha=alp_lin)

    elif(TC_wind[i]>=34) & (TC_wind[i]<64):
      lbl_ts, = ax.plot(lon_aux,lat_aux,'-',linewidth=2*szfac,color=[0,0,.8],zorder=35,alpha=alp_lin)

    elif(TC_wind[i]>=64) & (TC_wind[i]<83):
      lbl_cat1, = ax.plot(lon_aux,lat_aux,'-',linewidth=2*szfac,color=[.1,.9,.9],zorder=35,alpha=alp_lin)

    elif(TC_wind[i]>=83) & (TC_wind[i]<96):
      lbl_cat2, = ax.plot(lon_aux,lat_aux,'-',linewidth=2*szfac,color=[.4,.9,.4],zorder=35,alpha=alp_lin)

    elif(TC_wind[i]>=96) & (TC_wind[i]<113):
      lbl_cat3, = ax.plot(lon_aux,lat_aux,'-',linewidth=2*szfac,color=[.9,.9,.3],zorder=35,alpha=alp_lin)

    elif(TC_wind[i]>=113) & (TC_wind[i]<137):
      lbl_cat4, = ax.plot(lon_aux,lat_aux,'-',linewidth=2*szfac,color='#FF8000',zorder=35,alpha=alp_lin)

    elif(TC_wind[i]>=137):
      lbl_cat5, = ax.plot(lon_aux,lat_aux,'-',linewidth=2*szfac,color='red',zorder=35,alpha=alp_lin)


