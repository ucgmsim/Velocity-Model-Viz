# python functions for automatic generation of velocity models
import numpy as np
import re

#==================================================================================================
#
#           calculateDomainExtents
#
#==================================================================================================
def readDomainExtents():

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
        EXTRACTED_SLICE_PARAMETERS_DIRECTORY='SliceParametersNZ'

        ORIGIN_LAT=0
        ORIGIN_LON=0
        EXTENT_X=0
        EXTENT_Y=0
        EXTENT_ZMAX=0

    print('Reading domain extents.')
    fileName = 'Rapid_Velocity_Model_Parameters_Full.txt'
    fid = open(fileName, 'r')

    with open(fileName) as openfileobject:
        for line in openfileobject:
            lineVal = line.rstrip()
            lineVal = lineVal.split('=')
            if 'MODEL_VERSION' in lineVal[0]:
                Domain.MODEL_VERSION = lineVal[1]
            if 'MIN_VS' in lineVal[0]:
                Domain.MIN_VS = float(lineVal[1])
            if 'TOPO_TYPE' in lineVal[0]:
                Domain.TOPO_TYPE = lineVal[1]
            if 'EXTENT_Z_SPACING' in lineVal[0]:
                Domain.EXTENT_Z_SPACING= float(lineVal[1])
            if 'EXTENT_LATLON_SPACING' in lineVal[0]:
                Domain.EXTENT_LATLON_SPACING = float(lineVal[1])
            if 'OUTPUT_DIR' in lineVal[0]:
                Domain.OUTPUT_DIR = lineVal[1]
            if 'EXTENT_ZMIN' in lineVal[0]:
                Domain.EXTENT_ZMIN = float(lineVal[1])
            if 'EXTENT_ZMAX' in lineVal[0]:
                Domain.EXTENT_ZMAX = float(lineVal[1])
            if 'ORIGIN_ROT' in lineVal[0]:
                Domain.ORIGIN_ROT = float(lineVal[1])
            if 'EXTRACTED_SLICE_PARAMETERS_DIRECTORY' in lineVal[0]:
                Domain.EXTRACTED_SLICE_PARAMETERS_DIRECTORY = lineVal[1]
            if 'ORIGIN_LAT' in lineVal[0]:
                Domain.ORIGIN_LAT = float(lineVal[1])
            if 'ORIGIN_LON' in lineVal[0]:
                Domain.ORIGIN_LON = float(lineVal[1])
            if 'EXTENT_X' in lineVal[0]:
                Domain.EXTENT_X = float(lineVal[1])
            if 'EXTENT_Y' in lineVal[0]:
                Domain.EXTENT_Y = float(lineVal[1])
            if 'EXTENT_Z_SPACING' in lineVal[0]:
                Domain.EXTENT_Z_SPACING = float(lineVal[1])



    print('Reading of domain extents. Complete.')
    return Domain

#==================================================================================================
#
#           writeGenerateModelShellScript
#
#==================================================================================================
def writeGenerateModelShellScript(Domain):
    print('Writing generate velocity model shell scrip.')
    fileName = 'generateVeloModel.sh'
    # write domain parameters to a shell script file that will call the velocity model
    fid =  open(fileName,'w')
    fid.write('cd Velocity-Model\n')
    fid.write('rm -rf Rapid_Model\n')
    fid.write('./NZVM -A GENERATE_VELOCITY_MOD ')
    fid.write('-B {0} '.format(Domain.MODEL_VERSION))
    fid.write('-C {0} '.format(Domain.OUTPUT_DIR))
    fid.write('-D {0} '.format(Domain.ORIGIN_LAT))
    fid.write('-E {0} '.format(Domain.ORIGIN_LON))
    fid.write('-F {0} '.format(Domain.ORIGIN_ROT))
    fid.write('-G {0} '.format(Domain.EXTENT_X))
    fid.write('-H {0} '.format(Domain.EXTENT_Y))
    fid.write('-I {0} '.format(Domain.EXTENT_ZMAX))
    fid.write('-J {0} '.format(Domain.EXTENT_ZMIN))
    fid.write('-K {0} '.format(Domain.EXTENT_Z_SPACING))
    fid.write('-L {0} '.format(Domain.EXTENT_LATLON_SPACING))
    fid.write('-M {0} '.format(Domain.MIN_VS))
    fid.write('-N {0} '.format(Domain.TOPO_TYPE))
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
    fid.write('./NZVM -A EXTRACT_VELOCITY_SLICES ')
    fid.write('-B {0} '.format(Domain.MODEL_VERSION))
    fid.write('-C {0} '.format(Domain.OUTPUT_DIR))
    fid.write('-D {0} '.format(Domain.ORIGIN_LAT))
    fid.write('-E {0} '.format(Domain.ORIGIN_LON))
    fid.write('-F {0} '.format(Domain.ORIGIN_ROT))
    fid.write('-G {0} '.format(Domain.EXTENT_X))
    fid.write('-H {0} '.format(Domain.EXTENT_Y))
    fid.write('-I {0} '.format(Domain.EXTENT_ZMAX))
    fid.write('-J {0} '.format(Domain.EXTENT_ZMIN))
    fid.write('-K {0} '.format(Domain.EXTENT_Z_SPACING))
    fid.write('-L {0} '.format(Domain.EXTENT_LATLON_SPACING))
    fid.write('-M {0} '.format(Domain.MIN_VS))
    fid.write('-N {0} '.format(Domain.TOPO_TYPE))
    fid.write('-O {0} '.format(Domain.EXTRACTED_SLICE_PARAMETERS_DIRECTORY))
    fid.close()


    print('Writing extract slices from velocity model shell scrip. Complete.')


#==================================================================================================
#
#           investigateVelocityModelDomain
#
#==================================================================================================
def investigateVelocityModelDomain(domainLimits):

    import numpy as np
    import os
    from subprocess import call
    class sliceParameters:
        modCornerLon = np.zeros(4)
        modCornerLat = np.zeros(4)
        numLatSlices = []
        numLonSlices = []

    fileName = 'Velocity-Model/Rapid_Model/Log/VeloModCorners.txt'
    fid = open(fileName, 'r')
    temp = fid.readline()
    temp = fid.readline() # disregard first two lines

    for i in range(0,4):
        line = fid.readline()
        # lineSplit = line.splitlines()
        lineSplit = line.split('\t')
        sliceParameters.modCornerLon[i] = float(lineSplit[0])
        sliceParameters.modCornerLat[i] = float(lineSplit[1])

    fileName = 'Velocity-Model/Rapid_Model/Log/domainOutline.txt'

    # write domain corners to a file for GMT plotting
    fid = open(fileName, 'w')

    for i in range(0, 4):
        fid.write('{0}\t{1}\n'.format(sliceParameters.modCornerLon[i],sliceParameters.modCornerLat[i]))
    fid.write('{0}\t{1}\n'.format(sliceParameters.modCornerLon[0], sliceParameters.modCornerLat[0]))
    fid.close()

    print('Completed write of velocity model corners file.')
    # plot a map with the velocity model domain
    directory ='GMT/Plots/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    call(['bash', 'GMT/plotDomainBoxOnMap.sh'])
    print('Completed GMT plot of velocity model domain.')

    # check the velocity model corners are within the allowable limits
    flag = 0
    for i in range(0, 4):
        if sliceParameters.modCornerLon[i] > domainLimits.lonMax:
            flag = 1
        elif sliceParameters.modCornerLon[i] < domainLimits.lonMin:
            flag = 1
        elif sliceParameters.modCornerLat[i] > domainLimits.latMax:
            flag = 1
        elif sliceParameters.modCornerLat[i] < domainLimits.latMin:
            flag = 1

        if flag == 1:
            print('Velocity model exceeds the allowable domain limits.')
            exit(1)


    # generate slice parameters file based on the corners of the velocity model domain
    lonMin = np.min(sliceParameters.modCornerLon)
    lonMax = np.max(sliceParameters.modCornerLon)
    latMin = np.min(sliceParameters.modCornerLat)
    latMax = np.max(sliceParameters.modCornerLat)

    sliceParameters.numLatSlices = 5
    sliceParameters.numLonSlices = 5
    sliceRes = 25

    lats = np.linspace(latMin,latMax,sliceParameters.numLatSlices + 2)
    lons = np.linspace(lonMin, lonMax, sliceParameters.numLonSlices + 2)
    lats = lats[1:(sliceParameters.numLatSlices+1)]
    lons = lons[1:(sliceParameters.numLonSlices+1)]
    directory ='Velocity-Model/SliceParametersNZ'
    if not os.path.exists(directory):
        os.makedirs(directory)

    fileName = 'Velocity-Model/SliceParametersNZ/SliceParametersExtracted.txt'

    fid = open(fileName, 'w')
    fid.write('{0}\n'.format(sliceParameters.numLatSlices+sliceParameters.numLonSlices))
    for i in range(0,sliceParameters.numLatSlices):
        fid.write('{0} {1} {2} {3} {4}\n'.format(lats[i],lats[i],lonMin,lonMax,sliceRes))

    for i in range(0, sliceParameters.numLonSlices):
        fid.write('{0} {1} {2} {3} {4}\n'.format(latMin, latMax, lons[i], lons[i], sliceRes))

    fid.close()
    print('Write of extracted slice parameters file complete.')

    return sliceParameters

# ==================================================================================================
#
#           convertSlicesForGMTPlotting
#
# ==================================================================================================
def convertSlicesForGMTPlotting(sliceParameters):
    import os
    import numpy as np
    print('Converting slices for plotting in GMT.')

    directory = 'Velocity-Model/Rapid_Model/Extracted_Slices/'


    # make the directory if it doesnt exist
    directorySave = 'Velocity-Model/Rapid_Model/Reformatted_Slices'
    if not os.path.exists(directorySave):
        os.makedirs(directorySave)

    # do constant lat slices first
    for j in range(1, sliceParameters.numLatSlices+sliceParameters.numLonSlices+1):
        fileName = directory + 'ExtractedSlice'+ str(j) +'.txt'

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
                if lineNum > 7: # results with the first seven header files being disregarded
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
        zMin = min(sliceData.dep)
        zMax = max(sliceData.dep)
        zMin += zMax
        zMax = 0;
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

