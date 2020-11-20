import os
import datetime
import shutil as sl
import numpy as np
import pandas as pd
import sys
import csv
import arcpy
from arcpy import env

sys.path.append(r'./py_modules')
from create_boundary import create_boundary
from generate_file_structure import generate_file_structure
from copyfiles import copyfiles
from parameters import parameters
from run_tuflow import run_tuflow
from stage_flow_inputs_mannings import stage_flow_inputs_mannings
from EHF_dist import distribution, flatten, get_max_dist, plot_distributions
from FloatToRaster import flt_to_tif

"""
from update_attri_table import update_attri_table
from run_tuflow import bc_data
from distutils.dir_util import copy_tree
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.colors as col
"""
# 0. Environment setting
os.chdir("F:/tuflow-wf_python3")
env.workspace = "F:/tuflow-wf_python3"

#############################################################################################
# 1 Input variables
# 1.1 Specify the case name
NAME = 'sfe_25'
#end_time = 6
end_time =  [10, 8, 6, 4, 4, 4, 3, 3, 2, 2, 2, 2, 2] #must be integers

# 1.2 Specify the proportions of bankfull depth to run
stages = np.array([0.05, 0.08, 0.1, 0.12, 0.15,0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1])
#stages = np.array([1])

# 1.3 Other parameters (Automatically assigned)
# Elevation, S0 are not recorded for SFE_322, SFE_95
params = pd.read_excel('./parameters_sfe.xlsx')
for ii in range(0,params.site.__len__()+1):
    if params.site[ii] == NAME:
        ind = ii
        break
n = params.n[ind]
S = params.Slope[ind]
Elevation = params.Elevation[ind] # downstream bottom elev.
bf_wse = params.bf_wse[ind]
cell_size = str(params.cell_size[ind])
grid_size = str(params.gridX[ind]) + ',' + str(params.gridY[ind])
#grid_size = grid_size_normalXY(NAME)

# 1.5 Parameters for plottingPlot
# Surveyed Terrain
intitle = NAME + " Terrain"

# 1.6 Distribution parameters:
# single letter strings of parameters to create
# distributions for. options (case sensitive) are BSS, d, h, n, V
param_i = ['d', 'V']
param_name = ['depth', 'velocity']  # parameter names of distributions to plot
vel_samp_zoom = 500     # value to zoom y-axis to on velocity distributions
vel_prop_zoom = 0.005   # value to zoom y-axis to on velocity density distributions

#############################################################################################
# 2 Code for setting up & running TUFLOW simulation
run_number = str(len(stages))   # how many discharge you want to run

# 2.1 Create a buffered boundary, negative to bring it in from the edge
meter = '-2'                    # buffer by x meters
create_boundary(NAME, meter)

# 2.2 Generate file structure
generate_file_structure(NAME, run_number)

# 2.3 Copy files
copyfiles(NAME, run_number)

# 2.4 Boundary conditions (Q for inlet, h for outlet)
stage_flow_inputs_mannings(NAME, stages, S, n, Elevation, bf_wse)
#stage_flow_inputs_mannings(NAME, stages, S, n, Elevation)

# 2.5 Setting up parameters for run
parameters(NAME, run_number, cell_size, grid_size, end_time)
# update_attri_table(NAME)   # just copy the files in which the attributes are updated
# skip update_attri_table if you are using the updated files

# 2.6 Run tuflow simulation
run_tuflow(NAME, run_number)  # the results are stored in /results/grid/*.flt (raster files)
# bc_data.csv need to be placed in the input folder

copyloc = flt_to_tif(NAME, run_number, end_time)  # convert .flt files to .tif files
(pypath, pyfile) = os.path.split(__file__)
if os.path.exists(copyloc):
    sl.copyfile(__file__, copyloc + "/" + pyfile)

#############################################################################################
# 3 Result Analysis
# 3.1 folder_name
# folder_name should be a string -directly- pointing to the folder that contains the depth_dist.xlsx and velocity_dist.xlsx files.
# Make sure it includes the / at the end. intitle is the base label to be added to the plot (and save
# file names in the communal location
folder_name = copyloc + "/results/hydraulic_performance/"

# 3.2 dist_collection_fold
# dist_collection_fold is communal location of all distributions (should keep this the same for all runs)
dist_collection_fold = copyloc + "/../Distributions/"

no_tif = len(stages)

max_bins = np.zeros_like(param_i, dtype='float')
for i in range(len(param_i)):
    max_bins[i] = get_max_dist(copyloc, param_i[i])
bin_sizes = max_bins / 100

plot_distributions(param_i, param_name, no_tif, folder_name, bin_sizes, max_bins, vel_samp_zoom, vel_prop_zoom, intitle,
                   dist_collection_fold)

print(datetime.datetime.now().strftime("%d-%B-%Y %I:%M %p"))
