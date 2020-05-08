 #PACKAGE: rd_plotting_tools
# Description: This package includes a few simple functions for aiding in plots
# Author: Ricardo Domingues
#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpltPath
import os
import matplotlib.image as mpimg

#========================================================= 
#--------------------------------------------------- Function to plot positive and negative bars in blue and red, respectively
def pos_neg_bars(ax,Xvar,Yvar,bwidth=0.1,bbttom=0,alp_level=1,ewid=0.3):
  ax.bar(Xvar[Yvar>bbttom],Yvar[Yvar>bbttom]-bbttom,width=bwidth,bottom=bbttom,align='center',color='#B36D6D',edgecolor=[1,0,1,0.5],linewidth=ewid,alpha=alp_level)
  ax.bar(Xvar[Yvar<bbttom],Yvar[Yvar<bbttom]-bbttom,width=bwidth,bottom=bbttom,align='center',color='#5597B3',edgecolor=[0,1,1,0.5],linewidth=ewid,alpha=alp_level)
  ax.plot([np.nanmin(Xvar),np.nanmax(Xvar)],[bbttom,bbttom],'k-',linewidth=0.5)


#--------------------------------------------------- Function to define general axis properties
def plot_properties(ax,fsize=12,xticks=[],yticks=[],xlabel='x-label',ylabel='y-label',alp_grd=1):

  ax.set_xticks(xticks)
  ax.set_yticks(yticks)
  ax.tick_params(axis='both', which='major', labelsize=fsize)
  ax.grid(axis='both',linestyle=':',lw=1,c=[.3,.3,.3],alpha=alp_grd)
  ax.set_ylabel(ylabel,fontsize=fsize,fontweight='bold')
  ax.set_xlabel(xlabel,fontsize=fsize,fontweight='bold')

#---------------------------------------------------
def imagesc(var):
  fig = plt.figure(figsize=(4.5, 5))
  ax1 = fig.add_axes([0.1, 0.1, .85, .85])
  ax1.pcolor(var)
  plt.show()

#---------------------------------------------------
def gen_plot1(var):
  fig = plt.figure(figsize=(4.5, 5))
  ax1 = fig.add_axes([0.1, 0.1, .85, .85])
  ax1.plot(var)
  plt.show()

def gen_plot2(x,y):

  fig = plt.figure(figsize=(4.5, 5))
  ax1 = fig.add_axes([0.1, 0.1, .85, .85])
  ax1.plot(x,y)
  plt.show()
  return ax1

