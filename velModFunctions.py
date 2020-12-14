# python functions for automatic generation of velocity models
import sys
import numpy as np
import re
import os 
from inspect import getsourcefile


#==================================================================================================
#
#           readDomainExtents
#
#==================================================================================================
def readDomainExtents(paramsFileName):

    # generate the domain extents based on the magnitude and epicentre
    class Domain:
        MODEL_VERSION=0
        MIN_VS=0
        TOPO_TYPE=0
        EXTENT_Z_SPACING=0
        EXTENT_LATLON_SPACING=0
        OUTPUT_DIR=0
        EXTENT_ZMIN=0
        ORIGIN_ROT=0
        SLICE_PARAMETERS_TEXTFILES=''
        INVESTIGATION_TYPE = ''

        ORIGIN_LAT=0
        ORIGIN_LON=0
        EXTENT_X=0
        EXTENT_Y=0
        EXTENT_ZMAX=0
    
    # parameters that all call types have 
    loadCommand = "from {0} import INVESTIGATION_TYPE, MODEL_VERSION,TOPO_TYPE,MIN_VS,OUTPUT_DIR".format(paramsFileName)
    print(loadCommand)
    exec(loadCommand,globals()) # load in parameters from file 
    
    Domain.INVESTIGATION_TYPE = INVESTIGATION_TYPE
    Domain.MODEL_VERSION = MODEL_VERSION
    Domain.TOPO_TYPE = TOPO_TYPE
    Domain.OUTPUT_DIR = OUTPUT_DIR
    Domain.MIN_VS = float(MIN_VS)
    
    if (INVESTIGATION_TYPE == "AUTO_EXTRACT"):
        
        loadCommand = "from {0} import EXTENT_Z_SPACING,EXTENT_LATLON_SPACING,EXTENT_ZMIN,EXTENT_ZMAX,MODEL_ROT,ORIGIN_LAT,ORIGIN_LON,EXTENT_X,EXTENT_Y".format(paramsFileName)

        exec(loadCommand,globals()) # load in parameters from file 
        
        Domain.EXTENT_Z_SPACING= float(EXTENT_Z_SPACING)
        Domain.EXTENT_LATLON_SPACING = float(EXTENT_LATLON_SPACING)
        Domain.EXTENT_ZMIN = float(EXTENT_ZMIN)
        Domain.EXTENT_ZMAX = float(EXTENT_ZMAX)
        Domain.ORIGIN_ROT = float(MODEL_ROT)
        Domain.ORIGIN_LAT = float(ORIGIN_LAT)
        Domain.ORIGIN_LON = float(ORIGIN_LON)
        Domain.EXTENT_X = float(EXTENT_X)
        Domain.EXTENT_Y = float(EXTENT_Y)
    
    elif (INVESTIGATION_TYPE == "AUTO_GENERATE"):
        
        loadCommand = "from {0} import EXTENT_ZMIN,EXTENT_ZMAX,MODEL_ROT,ORIGIN_LAT,ORIGIN_LON,EXTENT_X,EXTENT_Y".format(paramsFileName)

        exec(loadCommand,globals()) # load in parameters from file 
        
        Domain.EXTENT_ZMIN = float(EXTENT_ZMIN)
        Domain.EXTENT_ZMAX = float(EXTENT_ZMAX)
        Domain.ORIGIN_ROT = float(MODEL_ROT)
        Domain.ORIGIN_LAT = float(ORIGIN_LAT)
        Domain.ORIGIN_LON = float(ORIGIN_LON)
        Domain.EXTENT_X = float(EXTENT_X)
        Domain.EXTENT_Y = float(EXTENT_Y)

        
    elif (INVESTIGATION_TYPE == "USER_EXTRACT"):
        
        loadCommand = "from {0} import SLICE_PARAMETERS_TEXTFILES,EXTENT_Z_SPACING,EXTENT_LATLON_SPACING,EXTENT_ZMIN,EXTENT_ZMAX,MODEL_ROT,ORIGIN_LAT,ORIGIN_LON,EXTENT_X,EXTENT_Y".format(paramsFileName)

        exec(loadCommand,globals()) # load in parameters from file 
        
        Domain.EXTENT_Z_SPACING= float(EXTENT_Z_SPACING)
        Domain.EXTENT_LATLON_SPACING = float(EXTENT_LATLON_SPACING)
        Domain.EXTENT_ZMIN = float(EXTENT_ZMIN)
        Domain.EXTENT_ZMAX = float(EXTENT_ZMAX)
        Domain.ORIGIN_ROT = float(MODEL_ROT)
        Domain.ORIGIN_LAT = float(ORIGIN_LAT)
        Domain.ORIGIN_LON = float(ORIGIN_LON)
        Domain.EXTENT_X = float(EXTENT_X)
        Domain.EXTENT_Y = float(EXTENT_Y)
        Domain.SLICE_PARAMETERS_TEXTFILES = SLICE_PARAMETERS_TEXTFILES 
    
    elif (INVESTIGATION_TYPE == "USER_GENERATE"):
        
        loadCommand = "from {0} import SLICE_PARAMETERS_TEXTFILES".format(paramsFileName)

        exec(loadCommand,globals()) # load in parameters from file 
        Domain.SLICE_PARAMETERS_TEXTFILES = SLICE_PARAMETERS_TEXTFILES 

        
    print('Completed reading of input parameters.')
    return Domain

#==================================================================================================
#
#           writeGenerateSlicesAutoShellScript
#
#==================================================================================================
def writeGenerateSlicesAutoShellScript(Domain):


    fileName = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
    # write domain parameters to a textfile
    fid =  open(fileName,'w')
    fid.write('CALL_TYPE=GENERATE_VELOCITY_SLICES\n')
    fid.write('MODEL_VERSION={0}\n'.format(Domain.MODEL_VERSION))
    fid.write('OUTPUT_DIR={0}\n'.format('temp'))
    fid.write('MIN_VS={0}\n'.format(Domain.MIN_VS))
    fid.write('TOPO_TYPE={0}\n'.format(Domain.TOPO_TYPE))
    fid.write('GENERATED_SLICE_PARAMETERS_TEXTFILE={0}\n'.format(os.path.join(Domain.OUTPUT_DIR,'SliceParametersAuto.txt')))
    fid.close()

    print('Completed writing generate slices auto shell script.')
    
#==================================================================================================
#
#           writeGenerateSlicesAutoShellScriptSpecificSlices
#
#==================================================================================================
def writeGenerateSlicesAutoShellScriptSpecificSlices(Domain,sliceParamsFile):


    fileName = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
    # write domain parameters to a textfile
    fid =  open(fileName,'w')
    fid.write('CALL_TYPE=GENERATE_VELOCITY_SLICES\n')
    fid.write('MODEL_VERSION={0}\n'.format(Domain.MODEL_VERSION))
    fid.write('OUTPUT_DIR={0}\n'.format('temp'))
    fid.write('MIN_VS={0}\n'.format(Domain.MIN_VS))
    fid.write('TOPO_TYPE={0}\n'.format(Domain.TOPO_TYPE))
    fid.write('GENERATED_SLICE_PARAMETERS_TEXTFILE={0}\n'.format(sliceParamsFile))
    fid.close()

    print('Completed writing generate slices auto shell script.')
    

#==================================================================================================
#
#           writeGenerateExtractSlicesAutoShellScript
#
#==================================================================================================
def writeGenerateExtractSlicesAutoShellScript(Domain):


    fileName = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
    # write domain parameters to a textfile
    fid =  open(fileName,'w')
    fid.write('CALL_TYPE=GENERATE_VELOCITY_MOD\n')
    fid.write('MODEL_VERSION={0}\n'.format(Domain.MODEL_VERSION))
    fid.write('OUTPUT_DIR={0}\n'.format('temp'))
    fid.write('ORIGIN_LAT={0}\n'.format(Domain.ORIGIN_LAT))
    fid.write('ORIGIN_LON={0}\n'.format(Domain.ORIGIN_LON))
    fid.write('ORIGIN_ROT={0}\n'.format(Domain.ORIGIN_ROT))
    fid.write('EXTENT_X={0}\n'.format(Domain.EXTENT_X))
    fid.write('EXTENT_Y={0}\n'.format(Domain.EXTENT_Y))
    fid.write('EXTENT_ZMAX={0}\n'.format(Domain.EXTENT_ZMAX))
    fid.write('EXTENT_ZMIN={0}\n'.format(Domain.EXTENT_ZMIN))
    fid.write('EXTENT_Z_SPACING={0}\n'.format(Domain.EXTENT_Z_SPACING))
    fid.write('EXTENT_LATLON_SPACING={0}\n'.format(Domain.EXTENT_LATLON_SPACING))
    fid.write('MIN_VS={0}\n'.format(Domain.MIN_VS))
    fid.write('TOPO_TYPE={0}\n'.format(Domain.TOPO_TYPE))
    fid.close()


    print('Completed writing generate model auto shell script.')
    
    
#==================================================================================================
#
#           writeExtractSlicesAutoShellScriptUserSlices
#
#==================================================================================================
def writeExtractSlicesAutoShellScriptUserSlices(Domain,SliceParametersFile):


    fileName = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
    # write domain parameters to a textfile
    fid =  open(fileName,'w')
    fid.write('CALL_TYPE=EXTRACT_VELOCITY_SLICES\n')
    fid.write('MODEL_VERSION={0}\n'.format(Domain.MODEL_VERSION))
    fid.write('OUTPUT_DIR={0}\n'.format('temp'))
    fid.write('ORIGIN_LAT={0}\n'.format(Domain.ORIGIN_LAT))
    fid.write('ORIGIN_LON={0}\n'.format(Domain.ORIGIN_LON))
    fid.write('ORIGIN_ROT={0}\n'.format(Domain.ORIGIN_ROT))
    fid.write('EXTENT_X={0}\n'.format(Domain.EXTENT_X))
    fid.write('EXTENT_Y={0}\n'.format(Domain.EXTENT_Y))
    fid.write('EXTENT_ZMAX={0}\n'.format(Domain.EXTENT_ZMAX))
    fid.write('EXTENT_ZMIN={0}\n'.format(Domain.EXTENT_ZMIN))
    fid.write('EXTENT_Z_SPACING={0}\n'.format(Domain.EXTENT_Z_SPACING))
    fid.write('EXTENT_LATLON_SPACING={0}\n'.format(Domain.EXTENT_LATLON_SPACING))
    fid.write('MIN_VS={0}\n'.format(Domain.MIN_VS))
    fid.write('TOPO_TYPE={0}\n'.format(Domain.TOPO_TYPE))
    fid.write('EXTRACTED_SLICE_PARAMETERS_TEXTFILE={0}\n'.format(SliceParametersFile))
    fid.close()


    print('Completed writing generate model auto shell script.')
    
#==================================================================================================
#
#           writeExtractSlicesAutoShellScript
#
#==================================================================================================
def writeExtractSlicesAutoShellScript(Domain):


    fileName = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
    # write domain parameters to a textfile
    fid =  open(fileName,'w')
    fid.write('CALL_TYPE=EXTRACT_VELOCITY_SLICES\n')
    fid.write('MODEL_VERSION={0}\n'.format(Domain.MODEL_VERSION))
    fid.write('OUTPUT_DIR={0}\n'.format('temp'))
    fid.write('ORIGIN_LAT={0}\n'.format(Domain.ORIGIN_LAT))
    fid.write('ORIGIN_LON={0}\n'.format(Domain.ORIGIN_LON))
    fid.write('ORIGIN_ROT={0}\n'.format(Domain.ORIGIN_ROT))
    fid.write('EXTENT_X={0}\n'.format(Domain.EXTENT_X))
    fid.write('EXTENT_Y={0}\n'.format(Domain.EXTENT_Y))
    fid.write('EXTENT_ZMAX={0}\n'.format(Domain.EXTENT_ZMAX))
    fid.write('EXTENT_ZMIN={0}\n'.format(Domain.EXTENT_ZMIN))
    fid.write('EXTENT_Z_SPACING={0}\n'.format(Domain.EXTENT_Z_SPACING))
    fid.write('EXTENT_LATLON_SPACING={0}\n'.format(Domain.EXTENT_LATLON_SPACING))
    fid.write('MIN_VS={0}\n'.format(Domain.MIN_VS))
    fid.write('TOPO_TYPE={0}\n'.format(Domain.TOPO_TYPE))
    fid.write('EXTRACTED_SLICE_PARAMETERS_TEXTFILE={0}\n'.format(os.path.join(Domain.OUTPUT_DIR,'SliceParametersAuto.txt')))
    fid.close()


    print('Completed writing generate model auto shell script.')
    
    
# ==================================================================================================
#
#           clacModelCorners
#
# ==================================================================================================
def calcModelCorners(Domain):
    
    class domainLimits:
        latMax = -28
        latMin = -53
        lonMin = 160
        lonMax = -175
    
    class corners:
        CartLat = [0] * 4
        CartLon = [0] * 4
        Lat = [0] * 4
        Lon = [0] * 4

    corners.CartLat[3] = 0.5*(Domain.EXTENT_Y - Domain.EXTENT_LATLON_SPACING)
    corners.CartLat[0] = 0.5*(Domain.EXTENT_Y - Domain.EXTENT_LATLON_SPACING)
    corners.CartLat[2] = -0.5*(Domain.EXTENT_Y - Domain.EXTENT_LATLON_SPACING)
    corners.CartLat[1] = -0.5*(Domain.EXTENT_Y - Domain.EXTENT_LATLON_SPACING)

    corners.CartLon[3] = -0.5*(Domain.EXTENT_X - Domain.EXTENT_LATLON_SPACING)
    corners.CartLon[0] = 0.5*(Domain.EXTENT_X - Domain.EXTENT_LATLON_SPACING)
    corners.CartLon[2] = -0.5*(Domain.EXTENT_X - Domain.EXTENT_LATLON_SPACING)
    corners.CartLon[1] = 0.5*(Domain.EXTENT_X - Domain.EXTENT_LATLON_SPACING)

    FLAT_CONST = 298.256
    ERAD = 6378.139
    RPERD = 0.017453292

    arg = Domain.ORIGIN_ROT * RPERD
    cosA = np.cos(arg)
    sinA = np.sin(arg)

    arg = (90.0 - Domain.ORIGIN_LAT )*RPERD
    cosT = np.cos(arg)
    sinT = np.sin(arg)

    arg = Domain.ORIGIN_LON * RPERD
    cosP = np.cos(arg)
    sinP = np.sin(arg)

    amat = [0] * 9

    amat[0] = cosA * cosT * cosP + sinA * sinP
    amat[1] = sinA * cosT * cosP - cosA * sinP
    amat[2] = sinT * cosP
    amat[3] = cosA * cosT * sinP - sinA * cosP
    amat[4] = sinA * cosT * sinP + cosA * cosP
    amat[5] = sinT * sinP
    amat[6] = -cosA * sinT
    amat[7] = -sinA * sinT
    amat[8] = cosT

    det = amat[0] * (amat[4] * amat[8] - amat[7] * amat[5]) - amat[1] * (amat[3] * amat[8] - amat[6] * amat[5]) + amat[2] * (amat[3] * amat[7] -amat[6] *amat[4]);

    det = 1.0 / det
    ainv = [0] * 9

    ainv[0] = det * amat[0]
    ainv[1] = det * amat[3]
    ainv[2] = det * amat[6]
    ainv[3] = det * amat[1]
    ainv[4] = det * amat[4]
    ainv[5] = det * amat[7]
    ainv[6] = det * amat[2]
    ainv[7] = det * amat[5]
    ainv[8] = det * amat[8]


    g0 = 0.0
    b0 = 0.0

    for i in range(0, 4):
        coords = gcproj(corners.CartLon[i] ,corners.CartLat[i], ERAD, g0, b0, amat, ainv)
        corners.Lat[i] = coords.rlat
        corners.Lon[i] = coords.rlon

    for i in range(0, 4):
        if (corners.Lon[i]>=domainLimits.lonMax ) & ( corners.Lon[i]<=0):
            print('Warning: velocity model corner outside of allowable NZ limits.')
            # sys.exit()
        if (corners.Lat[i]>=domainLimits.latMax):
            print('Warning: velocity model corner outside of allowable NZ limits.')
            # sys.exit()
        if (corners.Lon[i]<=domainLimits.lonMin) & ( corners.Lon[i]>=0):
            print('Warning: velocity model corner outside of allowable NZ limits.')
            # sys.exit()
        if (corners.Lat[i]<=domainLimits.latMin):
            print('Warning: velocity model corner outside of allowable NZ limits.')
            # sys.exit()
    
    fileName = os.path.join(Domain.OUTPUT_DIR,'domainOutline.txt')
    with open(fileName, 'w') as fid:
        for i in range(0, 4):
            fid.write("{0}\t".format(corners.Lon[i]))
            fid.write("{0}\n".format(corners.Lat[i]))
       	fid.write("{0}\t".format(corners.Lon[0]))
       	fid.write("{0}\n".format(corners.Lat[0]))
       	fid.close
           
    fileNameBoundingBox =  os.path.join(Domain.OUTPUT_DIR,'PlotParameters.txt')
    fid = open(fileNameBoundingBox, 'w')
    xMin = min(corners.Lon) 
    xMax = max(corners.Lon) 
    extensionVal = 0.1
    
    if xMin < 0: # if xMin < 0 domain must cross 180
       xMin =  min(i for i in corners.Lon if i > 0)
       xMax =  max(i for i in corners.Lon if i < 0) + 360
       
    xMin -= extensionVal
    xMax += extensionVal
    
    from math import log10, floor
    def round_to_1SF(x):
        return round(x, -int(floor(log10(abs(x)))))

        
    
    
    yMin = min(corners.Lat) - extensionVal
    yMax = max(corners.Lat) + extensionVal
    
    majorTickPlotY = round_to_1SF((yMax-yMin)/5)
    minorTickPlotY = majorTickPlotY / 2
    
    majorTickPlotX = round_to_1SF((xMax-xMin)/5)
    minorTickPlotX = majorTickPlotX / 2
    
    
    fid.write('xMin={0}\n'.format(xMin))
    fid.write('xMax={0}\n'.format(xMax))
    fid.write('yMin={0}\n'.format(yMin))
    fid.write('yMax={0}\n'.format(yMax))
    fid.write('centreLon={0}\n'.format((xMin+xMax)/2))
    fid.write('centreLat={0}\n'.format((yMin+yMax)/2))
    fid.write('majorTickPlotLat={0}\n'.format(majorTickPlotY))
    fid.write('minorTickPlotLat={0}\n'.format(minorTickPlotY))
    
    fid.write('majorTickPlotLon={0}\n'.format(majorTickPlotX))
    fid.write('minorTickPlotLon={0}\n'.format(minorTickPlotX))

    fid.close()

    return corners
    
    

#==================================================================================================
#
#           writeGenerateModelShellScript
#
#==================================================================================================
def writeGenerateModelShellScript(Domain):
    print('Writing generate velocity model shell scrip.')

    fileName = 'Velocity-Model/Rapid_Model_Parameters_Generate.txt'
    # write domain parameters to a textfile
    fid =  open(fileName,'w')
    fid.write('CALL_TYPE=GENERATE_VELOCITY_MOD\n')
    fid.write('MODEL_VERSION={0}\n'.format(Domain.MODEL_VERSION))
    fid.write('OUTPUT_DIR={0}\n'.format(Domain.OUTPUT_DIR))
    fid.write('ORIGIN_LAT={0}\n'.format(Domain.ORIGIN_LAT))
    fid.write('ORIGIN_LON={0}\n'.format(Domain.ORIGIN_LON))
    fid.write('ORIGIN_ROT={0}\n'.format(Domain.ORIGIN_ROT))
    fid.write('EXTENT_X={0}\n'.format(Domain.EXTENT_X))
    fid.write('EXTENT_Y={0}\n'.format(Domain.EXTENT_Y))
    fid.write('EXTENT_ZMAX={0}\n'.format(Domain.EXTENT_ZMAX))
    fid.write('EXTENT_ZMIN={0}\n'.format(Domain.EXTENT_ZMIN))
    fid.write('EXTENT_Z_SPACING={0}\n'.format(Domain.HH))
    fid.write('EXTENT_LATLON_SPACING={0}\n'.format(Domain.HH))
    fid.write('MIN_VS={0}\n'.format(Domain.MIN_VS))
    fid.write('TOPO_TYPE={0}\n'.format(Domain.TOPO_TYPE))
    fid.close()

    fileName = 'generateVeloModel.sh'
    # write shell script file that will call the velocity model
    fid =  open(fileName,'w')
    fid.write('cd Velocity-Model\n')
    fid.write('rm -rf Rapid_Model\n')
    fid.write('./NZVM Rapid_Model_Parameters_Generate.txt')
    fid.close()
    print('Writing generate velocity model shell scrip. Complete.')


#==================================================================================================
#
#           writeExtractShellScript
#
#==================================================================================================
def writeExtractShellScript(Domain):
    fileName = 'extractVeloModel.sh'
    print('Writing extract slices from velocity model shell scrip.')

    # write domain parameters to a shell script file that will read the velocity model and extract slices
    fid = open(fileName, 'w')
    fid.write('cd Velocity-Model\n')
    fid.write('./NZVM Rapid_Model_Parameters_Extract.txt')
    fid.close()

    fileName = 'Velocity-Model/Rapid_Model_Parameters_Extract.txt'
    # write domain parameters to a textfile
    fid =  open(fileName,'w')
    fid.write('CALL_TYPE=GENERATE_VELOCITY_SLICES\n')
    fid.write('MODEL_VERSION={0}\n'.format(Domain.MODEL_VERSION))
    fid.write('OUTPUT_DIR={0}\n'.format(Domain.OUTPUT_DIR))
#    fid.write('ORIGIN_LAT={0}\n'.format(Domain.ORIGIN_LAT))
#    fid.write('ORIGIN_LON={0}\n'.format(Domain.ORIGIN_LON))
#    fid.write('ORIGIN_ROT={0}\n'.format(Domain.ORIGIN_ROT))
#    fid.write('EXTENT_X={0}\n'.format(Domain.EXTENT_X))
#    fid.write('EXTENT_Y={0}\n'.format(Domain.EXTENT_Y))
#    fid.write('EXTENT_ZMAX={0}\n'.format(Domain.EXTENT_ZMAX))
#    fid.write('EXTENT_ZMIN={0}\n'.format(Domain.EXTENT_ZMIN))
#    fid.write('EXTENT_Z_SPACING={0}\n'.format(Domain.HH))
#    fid.write('EXTENT_LATLON_SPACING={0}\n'.format(Domain.HH))
    fid.write('MIN_VS={0}\n'.format(Domain.MIN_VS))
    fid.write('TOPO_TYPE={0}\n'.format(Domain.TOPO_TYPE))
    fid.write('GENERATED_SLICE_PARAMETERS_TEXTFILE={0}\n'.format(Domain.EXTRACTED_SLICE_PARAMETERS_DIRECTORY))
    fid.close()

    print('Writing extract slices from velocity model shell scrip. Complete.')


#=================================================================================================
#
#           writeSliceParametersFileExtractAuto
#
#==================================================================================================
def writeSliceParametersFileExtractAuto(Domain):

    import numpy as np
    import os
    from subprocess import call
    class sliceParameters:
        modCornerLon = np.zeros(4)
        modCornerLat = np.zeros(4)
        numLatSlices = []
        numLonSlices = []

    fileName = os.path.join(Domain.OUTPUT_DIR,'domainOutline.txt')
    fid = open(fileName, 'r')

    for i in range(0,4):
        line = fid.readline()
        # lineSplit = line.splitlines()
        lineSplit = line.split('\t')
        sliceParameters.modCornerLon[i] = float(lineSplit[0])
        if sliceParameters.modCornerLon[i] < 0:
            sliceParameters.modCornerLon[i] += 360.0
        sliceParameters.modCornerLat[i] = float(lineSplit[1])
        
    fid.close()


    sliceParameters.numLatSlices = 5
    sliceParameters.numLonSlices = 5

    sliceRes = 350 # increase to change resolution
    # generate slice parameters file based on the corners of the velocity model domain
    lon1 = sliceParameters.modCornerLon[0]
    lon2 = sliceParameters.modCornerLon[1]
    lon3 = sliceParameters.modCornerLon[2]
    lon4 = sliceParameters.modCornerLon[3]

    lat1 = sliceParameters.modCornerLat[0]
    lat2 = sliceParameters.modCornerLat[1]
    lat3 = sliceParameters.modCornerLat[2]
    lat4 = sliceParameters.modCornerLat[3]

    latsA = np.linspace(lat1,lat2,sliceParameters.numLatSlices)
    latsB = np.linspace(lat4,lat3,sliceParameters.numLatSlices)

    lonsA = np.linspace(lon1,lon2,sliceParameters.numLonSlices)
    lonsB = np.linspace(lon4,lon3,sliceParameters.numLonSlices)

    directory ='Velocity-Model/SliceParametersNZ'
    if not os.path.exists(directory):
        os.makedirs(directory)

    fileName = os.path.join(Domain.OUTPUT_DIR,'SliceParametersAuto.txt')

    fid = open(fileName, 'w')
    fid.write('{0}\n'.format(sliceParameters.numLatSlices+sliceParameters.numLonSlices))
    for i in range(0,sliceParameters.numLatSlices):
        if lonsA[i] > 180.0:
            lonsA[i] -=360.0
        if lonsB[i] > 180.0:
            lonsB[i] -=360.0
        fid.write('{0} {1} {2} {3} {4}\n'.format(latsA[i],latsB[i],lonsA[i],lonsB[i],sliceRes))


    latsA = np.linspace(lat1,lat4,sliceParameters.numLatSlices)
    latsB = np.linspace(lat2,lat3,sliceParameters.numLatSlices)
    
    lonsA = np.linspace(lon1,lon4,sliceParameters.numLonSlices)
    lonsB = np.linspace(lon2,lon3,sliceParameters.numLonSlices)

    for i in range(0,sliceParameters.numLatSlices):
        if lonsA[i] > 180.0:
            lonsA[i] -=360.0
        if lonsB[i] > 180.0:
            lonsB[i] -=360.0
        fid.write('{0} {1} {2} {3} {4}\n'.format(latsA[i],latsB[i],lonsA[i],lonsB[i],sliceRes))
    fid.close()

    print('Write of extracted slice parameters file complete.')

    return sliceParameters

#==================================================================================================
#
#           readSliceParametersFileUserExtract
#
#==================================================================================================
def readSliceParametersFileUserExtract(Domain,sliceFileName):

    import numpy as np
    import os
    from subprocess import call
    class sliceParameters:
        modCornerLon = np.zeros(4)
        modCornerLat = np.zeros(4)
        numLatSlices = []
        numLonSlices = []
        depMin = []
        depMax = []
        

    fid = open(sliceFileName, 'r')
    
    line = fid.readline()
    numSlices = int(line)
    
    
    latA = np.zeros(numSlices)
    latB = np.zeros(numSlices)
    lonA = np.zeros(numSlices)
    lonB = np.zeros(numSlices)
    
    sliceParameters.depMin = np.zeros(numSlices)
    sliceParameters.depMax = np.zeros(numSlices)

    for i in range(0,numSlices):
        line = fid.readline()
        lineSplit = line.split()

        latA[i] = lineSplit[0]
        latB[i] = lineSplit[1]
        lonA[i] = lineSplit[2]
        lonB[i] = lineSplit[3]
        sliceParameters.depMin[i] = Domain.EXTENT_ZMIN
        sliceParameters.depMax[i] = Domain.EXTENT_ZMAX

        if lonA[i] < 0:
            lonA[i] += 360
        if lonB[i] < 0:
            lonB[i] += 360
    
    fid.close()
    
    sliceParameters.modCornerLon[0:2] = (min(min(lonA),min(lonB)))
    sliceParameters.modCornerLat[0:2] = (min(min(latA),min(latB)))
    sliceParameters.modCornerLon[2:4] = (max(max(lonA),max(lonB)))
    sliceParameters.modCornerLat[2:4] = (max(min(latA),max(latB)))
    

    sliceParameters.numLatSlices = round(numSlices/2)
    sliceParameters.numLonSlices = numSlices-sliceParameters.numLatSlices 
    
    
    fileNameBoundingBox =  os.path.join(Domain.OUTPUT_DIR,'PlotParameters.txt')
    fid = open(fileNameBoundingBox, 'w')
    xMin = min(sliceParameters.modCornerLon) 
    xMax = max(sliceParameters.modCornerLon) 
    extensionVal = 0.1
    
    if xMin < 0: # if xMin < 0 domain must cross 180
       xMin =  min(i for i in corners.Lon if i > 0)
       xMax =  max(i for i in corners.Lon if i < 0) + 360
       
    xMin -= extensionVal
    xMax += extensionVal
    
    from math import log10, floor
    def round_to_1SF(x):
        return round(x, -int(floor(log10(abs(x)))))
    
    
    yMin = min(sliceParameters.modCornerLat) - extensionVal
    yMax = max(sliceParameters.modCornerLat) + extensionVal
    
    majorTickPlotY = round_to_1SF((yMax-yMin)/5)
    minorTickPlotY = majorTickPlotY / 2
    
    majorTickPlotX = round_to_1SF((xMax-xMin)/5)
    minorTickPlotX = majorTickPlotX / 2
    
    
    fid.write('xMin={0}\n'.format(xMin))
    fid.write('xMax={0}\n'.format(xMax))
    fid.write('yMin={0}\n'.format(yMin))
    fid.write('yMax={0}\n'.format(yMax))
    fid.write('centreLon={0}\n'.format((xMin+xMax)/2))
    fid.write('centreLat={0}\n'.format((yMin+yMax)/2))
    fid.write('majorTickPlotLat={0}\n'.format(majorTickPlotY))
    fid.write('minorTickPlotLat={0}\n'.format(minorTickPlotY))
    
    fid.write('majorTickPlotLon={0}\n'.format(majorTickPlotX))
    fid.write('minorTickPlotLon={0}\n'.format(minorTickPlotX))

    fid.close()
    
    
    print('Slice parameters file read complete')

    return sliceParameters

#==================================================================================================
#
#           readSliceParametersFile
#
#==================================================================================================
def readSliceParametersFile(Domain,sliceFileName):

    import numpy as np
    import os
    from subprocess import call
    class sliceParameters:
        modCornerLon = np.zeros(4)
        modCornerLat = np.zeros(4)
        numLatSlices = []
        numLonSlices = []
        depMin = []
        depMax = []

    fid = open(sliceFileName, 'r')
    
    line = fid.readline()
    numSlices = int(line)
    
    
    latA = np.zeros(numSlices)
    latB = np.zeros(numSlices)
    lonA = np.zeros(numSlices)
    lonB = np.zeros(numSlices)
    
    sliceParameters.depMin = np.zeros(numSlices)
    sliceParameters.depMax = np.zeros(numSlices)

    for i in range(0,numSlices):
        line = fid.readline()
        lineSplit = line.split()

        latA[i] = lineSplit[0]
        latB[i] = lineSplit[1]
        lonA[i] = lineSplit[2]
        lonB[i] = lineSplit[3]
        sliceParameters.depMin[i] = lineSplit[4]
        sliceParameters.depMax[i] = lineSplit[5]

        if lonA[i] < 0:
            lonA[i] += 360
        if lonB[i] < 0:
            lonB[i] += 360
    
    fid.close()
    
    sliceParameters.modCornerLon[0:2] = (min(min(lonA),min(lonB)))
    sliceParameters.modCornerLat[0:2] = (min(min(latA),min(latB)))
    sliceParameters.modCornerLon[2:4] = (max(max(lonA),max(lonB)))
    sliceParameters.modCornerLat[2:4] = (max(min(latA),max(latB)))
    

    sliceParameters.numLatSlices = round(numSlices/2)
    sliceParameters.numLonSlices = numSlices-sliceParameters.numLatSlices 
    
    
    fileNameBoundingBox =  os.path.join(Domain.OUTPUT_DIR,'PlotParameters.txt')
    fid = open(fileNameBoundingBox, 'w')
    xMin = min(sliceParameters.modCornerLon) 
    xMax = max(sliceParameters.modCornerLon) 
    extensionVal = 0.1
    
    if xMin < 0: # if xMin < 0 domain must cross 180
       xMin =  min(i for i in corners.Lon if i > 0)
       xMax =  max(i for i in corners.Lon if i < 0) + 360
       
    xMin -= extensionVal
    xMax += extensionVal
    
    from math import log10, floor
    def round_to_1SF(x):
        return round(x, -int(floor(log10(abs(x)))))
    
    
    yMin = min(sliceParameters.modCornerLat) - extensionVal
    yMax = max(sliceParameters.modCornerLat) + extensionVal
    
    majorTickPlotY = round_to_1SF((yMax-yMin)/5)
    minorTickPlotY = majorTickPlotY / 2
    
    majorTickPlotX = round_to_1SF((xMax-xMin)/5)
    minorTickPlotX = majorTickPlotX / 2
    
    
    fid.write('xMin={0}\n'.format(xMin))
    fid.write('xMax={0}\n'.format(xMax))
    fid.write('yMin={0}\n'.format(yMin))
    fid.write('yMax={0}\n'.format(yMax))
    fid.write('centreLon={0}\n'.format((xMin+xMax)/2))
    fid.write('centreLat={0}\n'.format((yMin+yMax)/2))
    fid.write('majorTickPlotLat={0}\n'.format(majorTickPlotY))
    fid.write('minorTickPlotLat={0}\n'.format(minorTickPlotY))
    
    fid.write('majorTickPlotLon={0}\n'.format(majorTickPlotX))
    fid.write('minorTickPlotLon={0}\n'.format(minorTickPlotX))

    fid.close()
    
    
    print('Slice parameters file read complete')

    return sliceParameters

#==================================================================================================
#
#           writeSliceParametersFileAuto
#
#==================================================================================================
def writeSliceParametersFileAuto(Domain):

    import numpy as np
    import os
    from subprocess import call
    class sliceParameters:
        modCornerLon = np.zeros(4)
        modCornerLat = np.zeros(4)
        numLatSlices = []
        numLonSlices = []

    fileName = os.path.join(Domain.OUTPUT_DIR,'domainOutline.txt')
    fid = open(fileName, 'r')

    for i in range(0,4):
        line = fid.readline()
        # lineSplit = line.splitlines()
        lineSplit = line.split('\t')
        sliceParameters.modCornerLon[i] = float(lineSplit[0])
        if sliceParameters.modCornerLon[i] < 0:
            sliceParameters.modCornerLon[i] += 360.0
        sliceParameters.modCornerLat[i] = float(lineSplit[1])
        
    fid.close()


    sliceParameters.numLatSlices = 5
    sliceParameters.numLonSlices = 5

    sliceRes = 350 # increase to change resolution
    # generate slice parameters file based on the corners of the velocity model domain
    lon1 = sliceParameters.modCornerLon[0]
    lon2 = sliceParameters.modCornerLon[1]
    lon3 = sliceParameters.modCornerLon[2]
    lon4 = sliceParameters.modCornerLon[3]

    lat1 = sliceParameters.modCornerLat[0]
    lat2 = sliceParameters.modCornerLat[1]
    lat3 = sliceParameters.modCornerLat[2]
    lat4 = sliceParameters.modCornerLat[3]

    latsA = np.linspace(lat1,lat2,sliceParameters.numLatSlices)
    latsB = np.linspace(lat4,lat3,sliceParameters.numLatSlices)

    lonsA = np.linspace(lon1,lon2,sliceParameters.numLatSlices)
    lonsB = np.linspace(lon4,lon3,sliceParameters.numLatSlices)

    directory ='Velocity-Model/SliceParametersNZ'
    if not os.path.exists(directory):
        os.makedirs(directory)

    fileName = os.path.join(Domain.OUTPUT_DIR,'SliceParametersAuto.txt')

    fid = open(fileName, 'w')
    fid.write('{0}\n'.format(sliceParameters.numLatSlices+sliceParameters.numLonSlices))
    for i in range(0,sliceParameters.numLatSlices):
        if lonsA[i] > 180.0:
            lonsA[i] -=360.0
        if lonsB[i] > 180.0:
            lonsB[i] -=360.0
        fid.write('{0} {1} {2} {3} {4} {5} {6} {7} \n'.format(latsA[i],latsB[i],lonsA[i],lonsB[i],Domain.EXTENT_ZMIN,Domain.EXTENT_ZMAX, sliceRes,sliceRes))


    latsA = np.linspace(lat1,lat4,sliceParameters.numLonSlices)
    latsB = np.linspace(lat2,lat3,sliceParameters.numLonSlices)
    
    lonsA = np.linspace(lon1,lon4,sliceParameters.numLonSlices)
    lonsB = np.linspace(lon2,lon3,sliceParameters.numLonSlices)

    for i in range(0,sliceParameters.numLonSlices):
        if lonsA[i] > 180.0:
            lonsA[i] -=360.0
        if lonsB[i] > 180.0:
            lonsB[i] -=360.0
        fid.write('{0} {1} {2} {3} {4} {5} {6} {7} \n'.format(latsA[i],latsB[i],lonsA[i],lonsB[i],Domain.EXTENT_ZMIN,Domain.EXTENT_ZMAX, sliceRes,sliceRes))
    fid.close()

    print('Write of extracted slice parameters file complete.')

    return sliceParameters


# ==================================================================================================
#
#           convertSlicesForGMTPlottingAutoGenerated
#
# ==================================================================================================
def convertSlicesForGMTPlottingAutoGenerated(sliceParameters,Domain):
    import os
    import numpy as np
    
    directory = os.path.join(Domain.OUTPUT_DIR,'Generated_Slices')

    #directory = 'Velocity-Model/Rapid_Model/Generated_Slices/'

    
    # make the directory if it doesnt exist
    directorySave = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
    #directorySave = 'Velocity-Model/Rapid_Model/Reformatted_Slices'
    if not os.path.exists(directorySave):
        os.makedirs(directorySave)

    # do constant lat slices first
    for j in range(1, sliceParameters.numLatSlices+sliceParameters.numLonSlices+1):
        fileName = directory + '/GeneratedSlice'+ str(j) +'.txt'

        class sliceData:
            lat = []
            lon = []
            dep = []
            vp = []
            vs = []
            rho = []
            latA = []
            latB = []
            lonA = []
            lonB = []

        # read in header data first, close then reopen and read in data
        fid = open(fileName, 'r')
        temp = fid.readline()
        temp = fid.readline()
        temp = fid.readline()  # disregard first three lines

        line = fid.readline()
#        print(line)
        lineSplit = line.split('\t')
        sliceData.latA = float(lineSplit[1])
        line = fid.readline()
        lineSplit = line.split('\t')
        sliceData.latB = float(lineSplit[1])
        line = fid.readline()
        lineSplit = line.split('\t')
        sliceData.lonA = float(lineSplit[1])
        line = fid.readline()
        lineSplit = line.split('\t')
        sliceData.lonB = float(lineSplit[1])
        fid.close()

        # now reopen and read in data
        count = 0
        lineNum = 0
        with open(fileName) as fid:
            for line in fid:
                lineNum += 1
                if lineNum > 8: # results with the first seven header files being disregarded
                    count += 1
                    lineSplit = line.split('\t')
                    sliceData.lat.append(float(lineSplit[0]))
                    sliceData.lon.append(float(lineSplit[1]))
                    sliceData.dep.append(float(lineSplit[2])/1000)
                    sliceData.vp.append(float(lineSplit[3]))
                    sliceData.vs.append(float(lineSplit[4]))
                    sliceData.rho.append(float(lineSplit[5]))

        fileNameWriteVs = directorySave + '/' + 'ExtractedSlice'+ str(j)+ '_Vs' + '.txt'
        fileNameWriteVp = directorySave + '/' + 'ExtractedSlice'+ str(j)+ '_Vp' + '.txt'
        fileNameWriteRho = directorySave + '/' + 'ExtractedSlice'+ str(j)+ '_Rho' + '.txt'

        fidVs = open(fileNameWriteVs,'w')
        fidVp = open(fileNameWriteVp,'w')
        fidRho = open(fileNameWriteRho,'w')

        for i in range(0, len(sliceData.lat)):
            if sliceData.latA == sliceData.latB:
                if np.isnan(sliceData.vs[i]) == 0 :
                    fidVs.write('{0} {1} {2}\n'.format(sliceData.lon[i],sliceData.dep[i],sliceData.vs[i]))
                if np.isnan(sliceData.vp[i]) == 0:
                    fidVp.write('{0} {1} {2}\n'.format(sliceData.lon[i],sliceData.dep[i],sliceData.vp[i]))
                if np.isnan(sliceData.rho[i]) == 0:
                    fidRho.write('{0} {1} {2}\n'.format(sliceData.lon[i],sliceData.dep[i],sliceData.rho[i]))
            else :
                if np.isnan(sliceData.vs[i]) == 0 :
                    fidVs.write('{0} {1} {2}\n'.format(sliceData.lat[i],sliceData.dep[i],sliceData.vs[i]))
                if np.isnan(sliceData.vp[i]) == 0:
                    fidVp.write('{0} {1} {2}\n'.format(sliceData.lat[i],sliceData.dep[i],sliceData.vp[i]))
                if np.isnan(sliceData.rho[i]) == 0:
                    fidRho.write('{0} {1} {2}\n'.format(sliceData.lat[i],sliceData.dep[i],sliceData.rho[i]))
        fidVs.close()
        fidVp.close()
        fidRho.close()

        fileNameWriteParameters = directorySave + '/' + 'ExtractedSlice' + str(j) + '_Parameters' + '.txt'
        fid = open(fileNameWriteParameters, 'w')
        zMin = -Domain.EXTENT_ZMAX
        zMax = -Domain.EXTENT_ZMIN
#Domain.EXTENT_ZMIN,Domain.EXTENT_ZMAX
#        zMin += zMax
#        zMax = 0;
        fid.write('zMin={0}\n'.format(zMin))
        fid.write('zMax={0}\n'.format(zMax))
        if sliceData.latA == sliceData.latB:
            xMin = min([sliceData.lon[0],sliceData.lon[len(sliceData.lon)-1]])
            xMax = max([sliceData.lon[0],sliceData.lon[len(sliceData.lon)-1]])
        else :
            xMin = min([sliceData.lat[0],sliceData.lat[len(sliceData.lon)-1]])
            xMax = max([sliceData.lat[0],sliceData.lat[len(sliceData.lon)-1]])
        fid.write('xMin={0}\n'.format(xMin))
        fid.write('xMax={0}\n'.format(xMax))
        fid.close()

        fileNameWritePoints = directorySave + '/' + 'ExtractedSlice' + str(j) + '_EndPoints' + '.txt'
        fid = open(fileNameWritePoints, 'w')
        x1 = sliceData.lon[0]
        x2 = sliceData.lon[len(sliceData.lon)-1]
        y1 = sliceData.lat[0]
        y2 = sliceData.lat[len(sliceData.lon)-1]
        fid.write('x1={0}\n'.format(x1))
        fid.write('x2={0}\n'.format(x2))
        fid.write('y1={0}\n'.format(y1))
        fid.write('y2={0}\n'.format(y2))
        fid.close()


    fileNameBoundingBox = directorySave + '/' + 'BoundingBox.txt'
    fid = open(fileNameBoundingBox, 'w')
    xMin = min(sliceParameters.modCornerLon)
    xMax = max(sliceParameters.modCornerLon)
    yMin = min(sliceParameters.modCornerLat)
    yMax = max(sliceParameters.modCornerLat)
    fid.write('xMin={0}\n'.format(xMin))
    fid.write('xMax={0}\n'.format(xMax))
    fid.write('yMin={0}\n'.format(yMin))
    fid.write('yMax={0}\n'.format(yMax))
    fid.close()

    fileNameSliceIndicies = directorySave + '/' + 'SliceIndicies.txt'
    fid = open(fileNameSliceIndicies, 'w')
    for j in range(1, sliceParameters.numLatSlices + sliceParameters.numLonSlices + 1):
        fid.write('{0} '.format(j))
    fid.write('\n')
    fid.close()
    print('Converting slices for plotting in GMT. Complete.')
    
# ==================================================================================================
#
#           convertSlicesForGMTPlottingAutoGeneratedMulti
#
# ==================================================================================================
def convertSlicesForGMTPlottingAutoGeneratedMulti(sliceParameters,Domain):
    import os
    import numpy as np
    
    directory = os.path.join(Domain.OUTPUT_DIR,'Generated_Slices')

    #directory = 'Velocity-Model/Rapid_Model/Generated_Slices/'

    
    # make the directory if it doesnt exist
    directorySave = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
    #directorySave = 'Velocity-Model/Rapid_Model/Reformatted_Slices'
    if not os.path.exists(directorySave):
        os.makedirs(directorySave)

    # do constant lat slices first
    for j in range(1, sliceParameters.numLatSlices+sliceParameters.numLonSlices+1):
        fileName = directory + '/GeneratedSlice'+ str(j) +'.txt'

        class sliceData:
            lat = []
            lon = []
            dep = []
            vp = []
            vs = []
            rho = []
            latA = []
            latB = []
            lonA = []
            lonB = []

        # read in header data first, close then reopen and read in data
        fid = open(fileName, 'r')
        temp = fid.readline()
        temp = fid.readline()
        temp = fid.readline()  # disregard first three lines

        line = fid.readline()
#        print(line)
        lineSplit = line.split('\t')
        sliceData.latA = float(lineSplit[1])
        line = fid.readline()
        lineSplit = line.split('\t')
        sliceData.latB = float(lineSplit[1])
        line = fid.readline()
        lineSplit = line.split('\t')
        sliceData.lonA = float(lineSplit[1])
        line = fid.readline()
        lineSplit = line.split('\t')
        sliceData.lonB = float(lineSplit[1])
        fid.close()

        # now reopen and read in data
        count = 0
        lineNum = 0
        with open(fileName) as fid:
            for line in fid:
                lineNum += 1
                if lineNum > 8: # results with the first seven header files being disregarded
                    count += 1
                    lineSplit = line.split('\t')
                    sliceData.lat.append(float(lineSplit[0]))
                    sliceData.lon.append(float(lineSplit[1]))
                    sliceData.dep.append(float(lineSplit[2])/1000)
                    sliceData.vp.append(float(lineSplit[3]))
                    sliceData.vs.append(float(lineSplit[4]))
                    sliceData.rho.append(float(lineSplit[5]))

        fileNameWriteVs = directorySave + '/' + 'ExtractedSlice'+ str(j)+ '_Vs' + '.txt'
        fileNameWriteVp = directorySave + '/' + 'ExtractedSlice'+ str(j)+ '_Vp' + '.txt'
        fileNameWriteRho = directorySave + '/' + 'ExtractedSlice'+ str(j)+ '_Rho' + '.txt'

        fidVs = open(fileNameWriteVs,'w')
        fidVp = open(fileNameWriteVp,'w')
        fidRho = open(fileNameWriteRho,'w')

        for i in range(0, len(sliceData.lat)):
            if sliceData.latA == sliceData.latB:
                if np.isnan(sliceData.vs[i]) == 0 :
                    fidVs.write('{0} {1} {2}\n'.format(sliceData.lon[i],sliceData.dep[i],sliceData.vs[i]))
                if np.isnan(sliceData.vp[i]) == 0:
                    fidVp.write('{0} {1} {2}\n'.format(sliceData.lon[i],sliceData.dep[i],sliceData.vp[i]))
                if np.isnan(sliceData.rho[i]) == 0:
                    fidRho.write('{0} {1} {2}\n'.format(sliceData.lon[i],sliceData.dep[i],sliceData.rho[i]))
            else :
                if np.isnan(sliceData.vs[i]) == 0 :
                    fidVs.write('{0} {1} {2}\n'.format(sliceData.lat[i],sliceData.dep[i],sliceData.vs[i]))
                if np.isnan(sliceData.vp[i]) == 0:
                    fidVp.write('{0} {1} {2}\n'.format(sliceData.lat[i],sliceData.dep[i],sliceData.vp[i]))
                if np.isnan(sliceData.rho[i]) == 0:
                    fidRho.write('{0} {1} {2}\n'.format(sliceData.lat[i],sliceData.dep[i],sliceData.rho[i]))
        fidVs.close()
        fidVp.close()
        fidRho.close()

        fileNameWriteParameters = directorySave + '/' + 'ExtractedSlice' + str(j) + '_Parameters' + '.txt'
        fid = open(fileNameWriteParameters, 'w')

        zMin = -sliceParameters.depMax[j-1]
        zMax = -sliceParameters.depMin[j-1]

        fid.write('zMin={0}\n'.format(zMin))
        fid.write('zMax={0}\n'.format(zMax))
        if sliceData.latA == sliceData.latB:
            xMin = min([sliceData.lon[0],sliceData.lon[len(sliceData.lon)-1]])
            xMax = max([sliceData.lon[0],sliceData.lon[len(sliceData.lon)-1]])
        else :
            xMin = min([sliceData.lat[0],sliceData.lat[len(sliceData.lon)-1]])
            xMax = max([sliceData.lat[0],sliceData.lat[len(sliceData.lon)-1]])
        fid.write('xMin={0}\n'.format(xMin))
        fid.write('xMax={0}\n'.format(xMax))
        
        from math import log10, floor
        def round_to_1SF(x):
            return round(x, -int(floor(log10(abs(x)))))
        
        majorTickPlotX = round_to_1SF((xMax-xMin)/7)
        minorTickPlotX = majorTickPlotX / 2
        majorTickPlotZ = round_to_1SF((zMax-zMin)/5)
        minorTickPlotZ = majorTickPlotZ / 2
        fid.write('majorTickPlotZ={0}\n'.format(majorTickPlotZ))
        fid.write('minorTickPlotZ={0}\n'.format(minorTickPlotZ))
        fid.write('majorTickPlotX={0}\n'.format(majorTickPlotX))
        fid.write('minorTickPlotX={0}\n'.format(minorTickPlotX))
        
        
    
        fid.close()

        fileNameWritePoints = directorySave + '/' + 'ExtractedSlice' + str(j) + '_EndPoints' + '.txt'
        fid = open(fileNameWritePoints, 'w')
        x1 = sliceData.lon[0]
        x2 = sliceData.lon[len(sliceData.lon)-1]
        y1 = sliceData.lat[0]
        y2 = sliceData.lat[len(sliceData.lon)-1]
        fid.write('x1={0}\n'.format(x1))
        fid.write('x2={0}\n'.format(x2))
        fid.write('y1={0}\n'.format(y1))
        fid.write('y2={0}\n'.format(y2))
        fid.close()


    fileNameBoundingBox = directorySave + '/' + 'BoundingBox.txt'
    fid = open(fileNameBoundingBox, 'w')
    xMin = min(sliceParameters.modCornerLon)
    xMax = max(sliceParameters.modCornerLon)
    yMin = min(sliceParameters.modCornerLat)
    yMax = max(sliceParameters.modCornerLat)
    fid.write('xMin={0}\n'.format(xMin))
    fid.write('xMax={0}\n'.format(xMax))
    fid.write('yMin={0}\n'.format(yMin))
    fid.write('yMax={0}\n'.format(yMax))
    fid.close()

    fileNameSliceIndicies = directorySave + '/' + 'SliceIndicies.txt'
    fid = open(fileNameSliceIndicies, 'w')
    for j in range(1, sliceParameters.numLatSlices + sliceParameters.numLonSlices + 1):
        fid.write('{0} '.format(j))
    fid.write('\n')
    fid.close()
    print('Converting slices for plotting in GMT. Complete.')
    
# ==================================================================================================
#
#           convertSlicesForGMTPlottingAutoExtracted
#
# ==================================================================================================
def convertSlicesForGMTPlottingAutoExtracted(sliceParameters,Domain):
    import os
    import numpy as np
    
    directory = os.path.join(Domain.OUTPUT_DIR,'Extracted_Slices')


    # make the directory if it doesnt exist
    directorySave = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
    #directorySave = 'Velocity-Model/Rapid_Model/Reformatted_Slices'
    if not os.path.exists(directorySave):
        os.makedirs(directorySave)

    # do constant lat slices first
    for j in range(1, sliceParameters.numLatSlices+sliceParameters.numLonSlices+1):
        fileName = directory + '/ExtractedSlice'+ str(j) +'.txt'

        class sliceData:
            lat = []
            lon = []
            dep = []
            vp = []
            vs = []
            rho = []
            latA = []
            latB = []
            lonA = []
            lonB = []

        # read in header data first, close then reopen and read in data
        fid = open(fileName, 'r')
        temp = fid.readline()
        temp = fid.readline()  # disregard first two lines
        

        line = fid.readline()
#        print(line)
        lineSplit = line.split('\t')
        sliceData.latA = float(lineSplit[1])
        line = fid.readline()
        lineSplit = line.split('\t')
        sliceData.latB = float(lineSplit[1])
        line = fid.readline()
        lineSplit = line.split('\t')
        sliceData.lonA = float(lineSplit[1])
        line = fid.readline()
        lineSplit = line.split('\t')
        sliceData.lonB = float(lineSplit[1])
        fid.close()

        # now reopen and read in data
        count = 0
        lineNum = 0
        with open(fileName) as fid:
            for line in fid:
                lineNum += 1
                if lineNum > 8: # results with the first seven header files being disregarded
                    count += 1
                    lineSplit = line.split('\t')
                    sliceData.lat.append(float(lineSplit[0]))
                    sliceData.lon.append(float(lineSplit[1]))
                    sliceData.dep.append(float(lineSplit[2])/1000)
                    sliceData.vp.append(float(lineSplit[3]))
                    sliceData.vs.append(float(lineSplit[4]))
                    sliceData.rho.append(float(lineSplit[5]))

        fileNameWriteVs = directorySave + '/' + 'ExtractedSlice'+ str(j)+ '_Vs' + '.txt'
        fileNameWriteVp = directorySave + '/' + 'ExtractedSlice'+ str(j)+ '_Vp' + '.txt'
        fileNameWriteRho = directorySave + '/' + 'ExtractedSlice'+ str(j)+ '_Rho' + '.txt'

        fidVs = open(fileNameWriteVs,'w')
        fidVp = open(fileNameWriteVp,'w')
        fidRho = open(fileNameWriteRho,'w')

        for i in range(0, len(sliceData.lat)):
            if sliceData.latA == sliceData.latB:
                if np.isnan(sliceData.vs[i]) == 0 :
                    fidVs.write('{0} {1} {2}\n'.format(sliceData.lon[i],sliceData.dep[i],sliceData.vs[i]))
                if np.isnan(sliceData.vp[i]) == 0:
                    fidVp.write('{0} {1} {2}\n'.format(sliceData.lon[i],sliceData.dep[i],sliceData.vp[i]))
                if np.isnan(sliceData.rho[i]) == 0:
                    fidRho.write('{0} {1} {2}\n'.format(sliceData.lon[i],sliceData.dep[i],sliceData.rho[i]))
            else :
                if np.isnan(sliceData.vs[i]) == 0 :
                    fidVs.write('{0} {1} {2}\n'.format(sliceData.lat[i],sliceData.dep[i],sliceData.vs[i]))
                if np.isnan(sliceData.vp[i]) == 0:
                    fidVp.write('{0} {1} {2}\n'.format(sliceData.lat[i],sliceData.dep[i],sliceData.vp[i]))
                if np.isnan(sliceData.rho[i]) == 0:
                    fidRho.write('{0} {1} {2}\n'.format(sliceData.lat[i],sliceData.dep[i],sliceData.rho[i]))
        fidVs.close()
        fidVp.close()
        fidRho.close()

        fileNameWriteParameters = directorySave + '/' + 'ExtractedSlice' + str(j) + '_Parameters' + '.txt'
        fid = open(fileNameWriteParameters, 'w')
        zMin = -Domain.EXTENT_ZMAX
        zMax = -Domain.EXTENT_ZMIN
#Domain.EXTENT_ZMIN,Domain.EXTENT_ZMAX
#        zMin += zMax
#        zMax = 0;
        fid.write('zMin={0}\n'.format(zMin))
        fid.write('zMax={0}\n'.format(zMax))
        if sliceData.latA == sliceData.latB:
            xMin = min([sliceData.lon[0],sliceData.lon[len(sliceData.lon)-1]])
            xMax = max([sliceData.lon[0],sliceData.lon[len(sliceData.lon)-1]])
        else :
            xMin = min([sliceData.lat[0],sliceData.lat[len(sliceData.lon)-1]])
            xMax = max([sliceData.lat[0],sliceData.lat[len(sliceData.lon)-1]])
        fid.write('xMin={0}\n'.format(xMin))
        fid.write('xMax={0}\n'.format(xMax))
        from math import log10, floor
        def round_to_1SF(x):
            return round(x, -int(floor(log10(abs(x)))))
        
        majorTickPlotX = round_to_1SF((xMax-xMin)/7)
        minorTickPlotX = majorTickPlotX / 2
        majorTickPlotZ = round_to_1SF((zMax-zMin)/5)
        minorTickPlotZ = majorTickPlotZ / 2
        fid.write('majorTickPlotZ={0}\n'.format(majorTickPlotZ))
        fid.write('minorTickPlotZ={0}\n'.format(minorTickPlotZ))
        fid.write('majorTickPlotX={0}\n'.format(majorTickPlotX))
        fid.write('minorTickPlotX={0}\n'.format(minorTickPlotX))
    
        fid.close()

        fileNameWritePoints = directorySave + '/' + 'ExtractedSlice' + str(j) + '_EndPoints' + '.txt'
        fid = open(fileNameWritePoints, 'w')
        x1 = sliceData.lon[0]
        x2 = sliceData.lon[len(sliceData.lon)-1]
        y1 = sliceData.lat[0]
        y2 = sliceData.lat[len(sliceData.lon)-1]
        fid.write('x1={0}\n'.format(x1))
        fid.write('x2={0}\n'.format(x2))
        fid.write('y1={0}\n'.format(y1))
        fid.write('y2={0}\n'.format(y2))
        fid.close()


    fileNameBoundingBox = directorySave + '/' + 'BoundingBox.txt'
    fid = open(fileNameBoundingBox, 'w')
    xMin = min(sliceParameters.modCornerLon)
    xMax = max(sliceParameters.modCornerLon)
    yMin = min(sliceParameters.modCornerLat)
    yMax = max(sliceParameters.modCornerLat)
    fid.write('xMin={0}\n'.format(xMin))
    fid.write('xMax={0}\n'.format(xMax))
    fid.write('yMin={0}\n'.format(yMin))
    fid.write('yMax={0}\n'.format(yMax))
    fid.close()

    fileNameSliceIndicies = directorySave + '/' + 'SliceIndicies.txt'
    fid = open(fileNameSliceIndicies, 'w')
    for j in range(1, sliceParameters.numLatSlices + sliceParameters.numLonSlices + 1):
        fid.write('{0} '.format(j))
    fid.write('\n')
    fid.close()
    print('Converting slices for plotting in GMT. Complete.')

# ==================================================================================================
#
#           combinePDFsAuto
#
# ==================================================================================================
def combinePDFsAuto(Domain,sliceParameters):

	# Loading the pyPdf Library
	from PyPDF2 import PdfFileWriter, PdfFileReader
	# Creating a routine that appends files to the output file
	def append_pdf(input,output):
		[output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]
	
	##### Rho
	# Creating an object where pdf pages are appended to
	output = PdfFileWriter()
	for j in range(1, sliceParameters.numLatSlices + sliceParameters.numLonSlices + 1):
    		# Appending two pdf-pages from two different files
		rho = Domain.OUTPUT_DIR +'/Reformatted_Slices/CrossSection{0}_rho.pdf'.format(j)
		append_pdf(PdfFileReader(open(rho,"rb")),output)

	# Writing all the collected pages to a file
	output.write(open(Domain.OUTPUT_DIR + '/CrossSection_rho_slices.pdf',"wb"))

	##### Vp
	# Creating an object where pdf pages are appended to
	output = PdfFileWriter()
	for j in range(1, sliceParameters.numLatSlices + sliceParameters.numLonSlices + 1):
    		# Appending two pdf-pages from two different files
		vp = Domain.OUTPUT_DIR +'/Reformatted_Slices/CrossSection{0}_vp.pdf'.format(j)
		append_pdf(PdfFileReader(open(vp,"rb")),output)

	# Writing all the collected pages to a file
	output.write(open(Domain.OUTPUT_DIR + '/CrossSection_vp_slices.pdf',"wb"))

	##### Vs
	# Creating an object where pdf pages are appended to
	output = PdfFileWriter()
	for j in range(1, sliceParameters.numLatSlices + sliceParameters.numLonSlices + 1):
    		# Appending two pdf-pages from two different files
		vs = Domain.OUTPUT_DIR +'/Reformatted_Slices/CrossSection{0}_vs.pdf'.format(j)
		append_pdf(PdfFileReader(open(vs,"rb")),output)

	# Writing all the collected pages to a file
	output.write(open(Domain.OUTPUT_DIR + '/CrossSection_vs_slices.pdf',"wb"))


# =============================================================================
# 	for j in range(1, 11):
# 		rho = 'GMT/Plots/CrossSection{0}_rho.pdf'.format(j)
# 		vs = 'GMT/Plots/CrossSection{0}_vs.pdf'.format(j)
# 		vp = 'GMT/Plots/CrossSection{0}_vp.pdf'.format(j)
# 		os.remove(rho)
# 		os.remove(vs)
# 		os.remove(vp)
# 
# =============================================================================


def gcproj(xf, yf, ref_rad, g0, b0, amat, ainv):

    class coords:
        rlon = 0
        rlat = 0


    rperd = 0.017453292

    arg = (xf) / (ref_rad) - (b0)
    cosB = np.cos(arg)
    sinB = np.sin(arg)

    arg = (yf) / (ref_rad) - (g0)
    cosG = np.cos(arg)
    sinG = np.sin(arg)

    arg = np.sqrt(1.0 + sinB * sinB * sinG * sinG)
    xp = sinG * cosB * arg
    yp = sinB * cosG * arg
    zp = np.sqrt(1.0 - xp * xp - yp * yp)

    xg = xp * amat[0] + yp * amat[1] + zp * amat[2]
    yg = xp * amat[3] + yp * amat[4] + zp * amat[5]
    zg = xp * amat[6] + yp * amat[7] + zp * amat[8]

    if zg != 0:
        arg = np.sqrt(xg * xg + yg * yg) / zg
        rlat = 90.0 - np.arctan(arg) / rperd
       
    if zg < 0:
        rlat = rlat - 180.0
    else:
        rlat = rlat

    if xg != 0:
        arg = yg / xg;
        rlon = np.arctan(arg) / rperd
    else:
        rlon = 0


    if xg < 0:
        rlon = rlon - 180.0

    while rlon < -180.0:
        rlon = rlon + 360.0
    if rlon < -0.0:
        rlon = rlon + 360.0
    if rlon > 180.0:
        rlon = rlon - 360.0


    coords.rlat = rlat
    coords.rlon = rlon


    return coords
