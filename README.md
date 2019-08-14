# Auto-Vel-Mod-Generation

The scripts here form a suite of automated VM plotting tools as a companion to the NZVM.

Prerequisites the compiled NZVM binaries and a working installation of GMT (Generic Mapping tools).

There are two main tools avaliable (1) a script to plot VM transects in a number of differnt ways and (2) a script to plot a VM domain on a map given user specified parameters. 

Velocity transect plotting. There are two main types of transect plotting: the first is where transect locations are automatically determined from a user specified domain (case AUTO); and the second is where the transect locations are given directly by the user (case USER). For each of the aforementioned cases there is the option to either generate slices directly (type GENERATE) or to extract velocity transects  (type GENERATE) from VM binary files (which themselves are generated as part of this process for use in ground motion simulation). 

Each of the different methods for plotting velocity extracts are run the same way by setting parameters in a '.py' file then executing './genDomain.py [myParametersFile]' where  [myParametersFile] is the python file containing user specified parameters. The required parameters for each type are detailed below. 

Mandatory parameters for all call types. All parameters (except for INVESTIGATION_TYPE are identical to their companions within the NZVM)

INVESTIGATION_TYPE: set to one of four options: AUTO_EXTRACT, AUTO_GENERATE, USER_EXTRACT, USER_GENERATE

MODEL_VERSION: select a model version from avaliable NZVM versions (see NZVM readme for a list)

TOPO_TYPE: the type of topographic representation  (see NZVM readme for a list)

OUTPUT_DIR: the directory to save output files to

For AUTO_EXTRACT the additional parameters are:
ORIGIN_LON
ORIGIN_LAT
MODEL_ROT
EXTENT_X
EXTENT_Y
EXTENT_LATLON_SPACING
EXTENT_ZMIN
EXTENT_ZMAX
EXTENT_Z_SPACING

For USER_EXTRACT the additional parameters are (same as AUTO_EXTRACT with one additional parameter): 
ORIGIN_LON
ORIGIN_LAT
MODEL_ROT
EXTENT_X
EXTENT_Y
EXTENT_LATLON_SPACING
EXTENT_ZMIN
EXTENT_ZMAX
EXTENT_Z_SPACING
SLICE_PARAMETERS_TEXTFILES: a list of slice parameters textfiles to generate velocity transects at


For AUTO_GENERATE the additional parameters are:
ORIGIN_LON
ORIGIN_LAT
MODEL_ROT
EXTENT_X
EXTENT_Y
EXTENT_ZMIN
EXTENT_ZMAX


For USER_GENERATE the additional parameters are:
SLICE_PARAMETERS_TEXTFILES: a list of slice parameters textfiles to generate velocity transects at





        
To plot the VM domain on a map the function 'investigateDomain.py' is used which can be called from the command line using "./investigateDomain.py [vmParametersTextfile]" where [vmParametersTextfile] is a textfile containing the VM parameters of the format of  AUTO_EXTRACT or AUTO_GENERATE

Mandatory parameters here are (1) 



 (1) To plot domain on map use the python script

1) Clone the Velocity model into this directory.

2) cd into Velocity-Model

3) execute 'make' or 'make parallel'

4) run generate_parameters.py using Mw, lat, lon and depth (this generates params_vel.py which can then be edited if desired)

5) run investigateDomain.py This plots the domain on a NZ map for interrogation purposes. Plot is housed in Domain subdir.

6) change / manually update the parameters in params_vel.py if desired (repeat steps 5 and 6 as necessary)

7) run genDomain.py resulting VM will be stored in Rapid_Model with slice plots and domain location

Run config_vm to generate params_vel.py (then edit this accordingly)

Run genDomain

(run clean if necessary)
