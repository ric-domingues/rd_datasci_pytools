# PACKAGE: rd_mapping_tools
# Description: This package includes a series of tools for quickly aiding in producing spatial maps for variables of interest
#              It automatically imports some of the required dependencies that are required 
# Author: Ricardo Domingues
#

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

# =============================================== Creates MAP and Includes Coastline
def create_map(fig,axes_position,extent,lat_spc=5,lon_spc=5,land_res='50m',fcolor=[.3,.3,.3],ecolor='black'):

  ax = fig.add_axes(axes_position, projection=ccrs.PlateCarree())
  ax.set_extent(extent, ccrs.PlateCarree())

  land_50m = NaturalEarthFeature('physical', 'land', land_res,
                                        edgecolor='face',
                                        facecolor='black')
  ax.add_feature(land_50m, edgecolor=ecolor,facecolor=fcolor,zorder=25)
  ax.add_feature(cfeature.BORDERS, edgecolor=[.9,.9,.9],zorder=26)

  lat_ticks = np.arange(extent[2]-lat_spc, extent[3]+lat_spc, lat_spc)
  lon_ticks = np.arange(extent[0]-lon_spc, extent[1]+lon_spc, lon_spc)

  gl = ax.gridlines(draw_labels=True,linestyle="--", color='black',linewidth=.3,zorder=26)
  gl.xlabels_top = gl.ylabels_right = False
  gl.ylocator = mticker.FixedLocator(lat_ticks)
  gl.xlocator = mticker.FixedLocator(lon_ticks)
  gl.xformatter = LONGITUDE_FORMATTER
  gl.yformatter = LATITUDE_FORMATTER
  gl.xlabel_style = {'size': 12}
  gl.ylabel_style = {'size': 12}

  return ax

# =============================================== ADD rivers to MAP
def add_river2map(ax,rcolor='darkblue',rwidth=1.5,ralpha=1):
  shp_path = cc.io.shapereader.natural_earth(
        resolution='10m',
        category='physical',
        name='rivers_lake_centerlines')
  shp_contents = cc.io.shapereader.Reader(shp_path)
  river_generator = shp_contents.geometries()
  river_feature = cc.feature.ShapelyFeature(
        river_generator,
        cc.crs.PlateCarree(),
        edgecolor=rcolor,
        facecolor='none',
        linewidth=rwidth)
  ax.add_feature(river_feature,zorder=30,alpha=ralpha)


# =============================================== ADD US states to the MAP
def add_US_states(ax,rcolor='darkblue',rwidth=1.5,ecolor=[.9,.9,.9],ralpha=1):
  shapename = 'admin_1_states_provinces_lakes_shp'
  states_shp = shpreader.natural_earth(resolution='110m',category='cultural', name=shapename)

  for astate in shpreader.Reader(states_shp).records():
    ax.add_geometries([astate.geometry], ccrs.PlateCarree(),facecolor='none', edgecolor=[.9,.9,.9],linewidth=.5,zorder=26,alpha=ralpha)  

#--------------------------------------------------- Function to find points inside geographic (or other 2D coordinate frame) polygon
def inpolygon(xv,yv,lon2,lat2):
  polygon = np.matrix([xv,yv]).T
  path = mpltPath.Path(polygon)
  x, y = lon2.flatten(), lat2.flatten()
  points = np.vstack((x,y)).T 
  grid = path.contains_points(points)
  mask = grid.reshape(lon2.shape)
  
  return mask



