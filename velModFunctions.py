# python functions for automatic generation of velocity models
import numpy as np
import re
import os 

#==================================================================================================
#
#           readDomainExtents
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
    from params_vel import *

    Domain.MODEL_VERSION = model_version
    Domain.MIN_VS = float(min_vs)
    Domain.TOPO_TYPE = topo_type
    Domain.EXTENT_Z_SPACING= float(hh)
    Domain.EXTENT_LATLON_SPACING = float(hh)
    Domain.HH = float(hh)
    Domain.OUTPUT_DIR = output_directory
    Domain.EXTENT_ZMIN = float(extent_zmin)
    Domain.EXTENT_ZMAX = float(extent_zmax)
    Domain.ORIGIN_ROT = float(MODEL_ROT)
    Domain.EXTRACTED_SLICE_PARAMETERS_DIRECTORY = extracted_slice_parameters_directory
    Domain.ORIGIN_LAT = float(MODEL_LAT)
    Domain.ORIGIN_LON = float(MODEL_LON)
    Domain.EXTENT_X = float(extent_x)
    Domain.EXTENT_Y = float(extent_y)
    Domain.NX = float(nx)
    Domain.NY = float(ny)
    Domain.NZ = float(nz)
    Domain.SIM_DURATION = float(sim_duration)
    print('Reading of domain extents. Complete.')
    return Domain

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
    fid.write('CALL_TYPE=EXTRACT_VELOCITY_SLICES\n')
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
    fid.write('EXTRACTED_SLICE_PARAMETERS_TEXTFILE={0}\n'.format(Domain.EXTRACTED_SLICE_PARAMETERS_DIRECTORY))
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
    sliceRes = 300 # increase to change resolution 

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

# ==================================================================================================
#
#           combinePDFs
#
# ==================================================================================================
def combinePDFs():

	# Loading the pyPdf Library
	from pyPdf import PdfFileWriter, PdfFileReader
	# Creating a routine that appends files to the output file
	def append_pdf(input,output):
		[output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]
	
	##### Rho
	# Creating an object where pdf pages are appended to
	output = PdfFileWriter()
	for j in range(1, 11):
    		# Appending two pdf-pages from two different files
		rho = 'GMT/Plots/CrossSection{0}_rho.pdf'.format(j)
		append_pdf(PdfFileReader(open(rho,"rb")),output)

	# Writing all the collected pages to a file
	output.write(open('GMT/Plots/CrossSection_rho_slices.pdf',"wb"))

	##### Vp
	# Creating an object where pdf pages are appended to
	output = PdfFileWriter()
	for j in range(1, 11):
    		# Appending two pdf-pages from two different files
		vp = 'GMT/Plots/CrossSection{0}_vp.pdf'.format(j)
		append_pdf(PdfFileReader(open(vp,"rb")),output)

	# Writing all the collected pages to a file
	output.write(open('GMT/Plots/CrossSection_vp_slices.pdf',"wb"))

	##### Vs
	# Creating an object where pdf pages are appended to
	output = PdfFileWriter()
	for j in range(1, 11):
    		# Appending two pdf-pages from two different files
		vs = 'GMT/Plots/CrossSection{0}_vs.pdf'.format(j)
		append_pdf(PdfFileReader(open(vs,"rb")),output)

	# Writing all the collected pages to a file
	output.write(open('GMT/Plots/CrossSection_vs_slices.pdf',"wb"))


	for j in range(1, 11):
		rho = 'GMT/Plots/CrossSection{0}_rho.pdf'.format(j)
		vs = 'GMT/Plots/CrossSection{0}_vs.pdf'.format(j)
		vp = 'GMT/Plots/CrossSection{0}_vp.pdf'.format(j)
		os.remove(rho)
		os.remove(vs)
		os.remove(vp)

# ==================================================================================================
#
#           genModelCorners
#
# ==================================================================================================
def genModelCorners(Domain):
    class corners:
        CartLat = [0] * 4
        CartLon = [0] * 4
        Lat = [0] * 4
        Lon = [0] * 4

    corners.CartLat[3] = 0.5*(Domain.EXTENT_Y - Domain.HH)
    corners.CartLat[0] = 0.5*(Domain.EXTENT_Y - Domain.HH)
    corners.CartLat[2] = -0.5*(Domain.EXTENT_Y - Domain.HH)
    corners.CartLat[1] = -0.5*(Domain.EXTENT_Y - Domain.HH)

    corners.CartLon[3] = -0.5*(Domain.EXTENT_X - Domain.HH)
    corners.CartLon[0] = 0.5*(Domain.EXTENT_X - Domain.HH)
    corners.CartLon[2] = -0.5*(Domain.EXTENT_X - Domain.HH)
    corners.CartLon[1] = 0.5*(Domain.EXTENT_X - Domain.HH)

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

    with open('Domain/domainOutline.txt', 'w') as fid:
        for i in range(0, 4):
            fid.write("{0}\t".format(corners.Lon[i]))
            fid.write("{0}\n".format(corners.Lat[i]))
       	fid.write("{0}\t".format(corners.Lon[0]))
       	fid.write("{0}\n".format(corners.Lat[0]))
       	fid.close

    return corners

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
        rlat = 0.0

    if xg != 0:
        arg = yg / xg;
        rlon = np.arctan(arg) / rperd
    else:
        rlon = 0


    if xg < 0:
        rlon = rlon - 180.0

    while rlon < -180.0:
        rlon = rlon + 360.0

    coords.rlat = rlat
    coords.rlon = rlon

    return coords
