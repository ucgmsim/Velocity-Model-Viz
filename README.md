# Velocity-Model-Viz

The scripts here form a suite of automated VM plotting tools as a companion to the NZVM.

## Prerequisites 

Prerequsites are: 
- 1) the compiled NZVM binary 
- 2) working installation of GMT (Generic Mapping tools). 
- 3) the python packages numpy and PyPDF2

## General Setup and Usage Instructions

- 1) Clone the Velocity model into this directory.

- 2) cd into Velocity-Model

- 3) execute ```make``` or ```make parallel```

- 4) Install python requirements in ```requirements.txt```  (e.g. ``` pip install -r requirements.txt```)

- 5) execute ```python investigateDomain.py``` or ``` python genDomain.py``` with an appropriate parameters file. Examples can be seen in the directory 'Example-Inputs'. (e.g. ``` python genDomain.py params_vel_korea.py ```)

See other sections for additional details. 

## Detailed Usage Instructions

There are two main tools avaliable 
- (1) a script to plot VM transects in a number of different ways
- (2) a script to plot a VM domain on a map given user specified parameters. 

Velocity transect plotting. There are two main types of transect plotting: 
- the first is where transect locations are automatically determined from a user specified domain (case AUTO); 
- the second is where the transect locations are given directly by the user (case USER). 

For each of the aforementioned cases there is the option to either generate slices directly (type _GENERATE) or to extract velocity transects  (type _EXTRACT) from VM binary files (which themselves are generated as part of this process for use in ground motion simulation). 

Each of the different methods for plotting velocity extracts are run the same way by setting parameters in a '.py' file then executing ```python genDomain.py [myParametersFile]``` where  [myParametersFile] is the python file containing user specified parameters. The required parameters for each type are detailed below. 

Mandatory parameters for all call types. All parameters (except for INVESTIGATION_TYPE are identical to their companions within the NZVM)

- INVESTIGATION_TYPE: set to one of four options: 
  - AUTO_EXTRACT
  - AUTO_GENERATE
  - USER_EXTRACT
  - USER_GENERATE
- MODEL_VERSION: select a model version from avaliable NZVM versions (see NZVM readme for a list)
- TOPO_TYPE: the type of topographic representation  (see NZVM readme for a list)
- OUTPUT_DIR: the directory to save output files to

For AUTO_EXTRACT the additional parameters are:
- ORIGIN_LON
- ORIGIN_LAT
- MODEL_ROT
- EXTENT_X
- EXTENT_Y
- EXTENT_LATLON_SPACING
- EXTENT_ZMIN
- EXTENT_ZMAX
- EXTENT_Z_SPACING

For USER_EXTRACT the additional parameters are (same as AUTO_EXTRACT with one additional parameter): 
- ORIGIN_LON
- ORIGIN_LAT
- MODEL_ROT
- EXTENT_X
- EXTENT_Y
- EXTENT_LATLON_SPACING
- EXTENT_ZMIN
- EXTENT_ZMAX
- EXTENT_Z_SPACING
- SLICE_PARAMETERS_TEXTFILES: a list of slice parameters textfiles to generate velocity transects at


For AUTO_GENERATE the additional parameters are:
- ORIGIN_LON
- ORIGIN_LAT
- MODEL_ROT
- EXTENT_X
- EXTENT_Y
- EXTENT_ZMIN
- EXTENT_ZMAX

For USER_GENERATE the additional parameters are:
- SLICE_PARAMETERS_TEXTFILES: a list of slice parameters textfiles to generate velocity transects at


Here is an example combo 
params_vel_example.py
```
INVESTIGATION_TYPE = "USER_GENERATE"
ORIGIN_LAT = "-43.35805601377026"
ORIGIN_LON = "171.7875594038442"
MODEL_ROT = "38.3183225905264"
MIN_VS = "0.5"
MODEL_VERSION = "2.06"
TOPO_TYPE = "SQUASHED_TAPERED"
OUTPUT_DIR = "/tmp/output"
EXTENT_X = "232.34383396290647"
EXTENT_Y = "355.0047402566312"
EXTENT_ZMAX = "46.0"
EXTENT_ZMIN = "0"
SLICE_PARAMETERS_TEXTFILES=["/tmp/slice_params.txt"]
```
slice_params.txt 
```
3
-43.5 -44.5 171 172 0 46 350 350
-43.25 -43.25 171 173.5 0 46 350 350
-43 -43.75 171 173.5 0 46 350 350
```
where each line stands for
```
number of slices
lat1 lat2 lon1 lon2 depth_top depth_bottom res_surface res_depth
...
```


To plot the VM domain on a map the function ```investigateDomain.py ``` is used which can be called from the command line using ```python investigateDomain.py [vmParametersTextfile]``` where [vmParametersTextfile] is a textfile containing the VM parameters of the format of  AUTO_EXTRACT or AUTO_GENERATE

