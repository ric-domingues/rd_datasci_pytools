import cartopy as cc
import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.io.img_tiles as cimgt
from cartopy.feature import NaturalEarthFeature
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import numpy as np
import cartopy.io.shapereader as shpreader
import matplotlib.path as mpltPath
import matplotlib.pyplot as plt

from scipy import signal
from scipy import interpolate

from functools import partial

import pyproj
from shapely import geometry
from shapely.geometry import Point
from shapely.ops import transform


# USAGE TO IMPORT
#import rd_file_tools as rd_files



# =============================================== Creates MAP and Includes Coastline
def map_subplots(nrows, ncols,currax):

  ax = plt.subplot(nrows,ncols,currax,projection=ccrs.PlateCarree())

  return ax


# =============================================== Creates MAP and Includes Coastline
def create_map(fig,axes_position,extent,lat_spc=5,lon_spc=5,land_res='50m',fcolor=[.3,.3,.3],ecolor='black',xlbl_plot=True,ylbl_plot=True,alp_grd=1,axs_wid=1,fsize=12,axes_use=False):

  if axes_use==False:
    ax = fig.add_axes(axes_position, projection=ccrs.PlateCarree())
  else:
    ax = axes_use

  ax.set_extent(extent, ccrs.PlateCarree())

  land_50m = NaturalEarthFeature('physical', 'land', land_res,
                                        edgecolor='face',
                                        facecolor='black')
  ax.add_feature(land_50m, edgecolor=ecolor,facecolor=fcolor,zorder=10)
  ax.add_feature(cfeature.BORDERS, edgecolor=ecolor,zorder=26,alpha=0.6)
  ax.outline_patch.set_linewidth(axs_wid)

  lat_ticks = np.arange(extent[2]-lat_spc*2, extent[3]+lat_spc*2, lat_spc)
  lon_ticks = np.arange(extent[0]-lon_spc*2, extent[1]+lon_spc*2, lon_spc)

  gl = ax.gridlines(draw_labels=True,linestyle="--", color='black',linewidth=.3,zorder=26,alpha=alp_grd)
  gl.xlabels_top = gl.ylabels_right = False
  gl.ylocator = mticker.FixedLocator(lat_ticks)
  gl.xlocator = mticker.FixedLocator(lon_ticks)

  gl.xformatter = LONGITUDE_FORMATTER
  gl.yformatter = LATITUDE_FORMATTER
  gl.xlabel_style = {'size': fsize}
  gl.ylabel_style = {'size': fsize}

  gl.xlabels_bottom = xlbl_plot
  gl.ylabels_left   = ylbl_plot

  return ax

# =============================================== ADD rivers to MAP
def add_river2map(ax,rcolor='darkblue',rwidth=1.5,ralpha=1,res_use='10m'):
  shp_path = cc.io.shapereader.natural_earth(
        resolution=res_use,
        category='physical',
        name='rivers_lake_centerlines')
  shp_contents = cc.io.shapereader.Reader(shp_path)
  river_generator = shp_contents.geometries()
  river_feature = cc.feature.ShapelyFeature(
        river_generator,
        cc.crs.PlateCarree(),
        edgecolor=rcolor,
        facecolor='none',
        linewidth=rwidth/3)
  ax.add_feature(river_feature,zorder=30,alpha=ralpha)
  ax.add_feature(cc.feature.RIVERS,edgecolor=rcolor,linewidth=rwidth,alpha=ralpha)

# =============================================== ADD rivers to MAP
def add_US_states(ax,rcolor='darkblue',rwidth=1.5,ecolor=[.9,.9,.9],ralpha=1):
  shapename = 'admin_1_states_provinces_lakes_shp'
  states_shp = shpreader.natural_earth(resolution='110m',category='cultural', name=shapename)

  for astate in shpreader.Reader(states_shp).records():
    ax.add_geometries([astate.geometry], ccrs.PlateCarree(),facecolor='none', edgecolor=ecolor,linewidth=rwidth,zorder=26,alpha=ralpha)  

#--------------------------------------------------- Function to find points inside polygon
def inpolygon(xv,yv,lon2,lat2):
  polygon = np.matrix([xv,yv]).T
  path = mpltPath.Path(polygon)
  x, y = lon2.flatten(), lat2.flatten()
  points = np.vstack((x,y)).T
  grid = path.contains_points(points)
  mask = grid.reshape(lon2.shape)

  return mask


def create_circle(lonC,latC,km_rad):
  """
  Function to creare a circle polygon given lonC,latC, radius in km

  Inputs:
      - lonC = longitude of the center of the circle 
      - latC = latitude of the center of the circle 
      - km_rad = radius of desired circle in km
  Outputs:
      - xV = longitudinal edges of circle 
      - yV = latitudinal edges of circle 
  """
  lon, lat = lonC, latC # lon lat for San Francisco
  radius = km_rad*1e3  # in m

  local_azimuthal_projection = "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(
      lat, lon
  )
  wgs84_to_aeqd = partial(
      pyproj.transform,
      pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
      pyproj.Proj(local_azimuthal_projection),
  )
  aeqd_to_wgs84 = partial(
      pyproj.transform,
      pyproj.Proj(local_azimuthal_projection),
      pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
  )

  center = Point(float(lon), float(lat))
  point_transformed = transform(wgs84_to_aeqd, center)
  buffer = point_transformed.buffer(radius)
  # Get the polygon with lat lon coordinates
  circle_poly = transform(aeqd_to_wgs84, buffer)
  xV, yV = circle_poly.exterior.coords.xy

  return xV, yV


#--------------------------------------------------- Function to fill 2D gaps in data
def inpaint_nans(im0):
    nans = np.isnan(im0)
    im = im0
    ipn_kernel = np.array([[1,1,1],[1,0,1],[1,1,1]]) # kernel for inpaint_nans
    while np.sum(nans)>0:
        im[nans] = 0
        vNeighbors = signal.convolve2d((nans==False),ipn_kernel,mode='same',boundary='symm')
        im2 = signal.convolve2d(im,ipn_kernel,mode='same',boundary='symm')
        im2[vNeighbors>0] = im2[vNeighbors>0]/vNeighbors[vNeighbors>0]
        im2[vNeighbors==0] = np.nan
        im2[(nans==False)] = im[(nans==False)]
        im = im2
        nans = np.isnan(im)
    return im2

#---------------------------------------------------
def find_nearest_point(x1d,y1d,xp,yp,dx):

  idx=np.where( (x1d>=xp-dx) & (x1d<=xp+dx) )
  idy=np.where( (y1d>=yp-dx) & (y1d<=yp+dx) )

  return idx,idy

#---------------------------------------------------
def find_nearest_point_2D(x2d,y2d,xp,yp,dx):

  imask=np.where( (x2d>=xp-dx) & (x2d<=xp+dx) & (y2d>=yp-dx) & (y2d<=yp+dx) )

  return imask

#---------------------------------------------------
def interp1(x,y,xnew):
  f = interpolate.interp1d(x, y)
  ynew = f(xnew)# use interpolation function returned by `interp1d`
  return ynew

#---------------------------------------------------
def interp2(x1d,y1d,z,xnew,ynew,paint_nans=True):

  mask = np.zeros(z.shape)
  mask[np.isnan(z)] = 1
  if paint_nans:
    fm = interpolate.interp2d(x1d, y1d, mask)
    mask_new = fm(xnew,ynew) 

  zp = (inpaint_nans(z) if paint_nans else z)
  fz = interpolate.interp2d(x1d, y1d, zp) 
  z_new = fz(xnew,ynew)

  if paint_nans:
    z_new[mask_new>0.95] = np.nan

  return z_new








