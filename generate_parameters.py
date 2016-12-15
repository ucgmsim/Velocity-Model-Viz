import numpy as np

# assume only two inputs (magnitude and epicentre)
class earthquakeSource:
    mag = 3.6
    centroidDepth = 5 #in km +ve downwards
    lon = 172.25
    lat = -43.6


# generate the domain extents based on the magnitude and epicentre

rawXYextent =  np.power(10 , ( 0.55 * earthquakeSource.mag - 1.2 ))
XYextent = round(2*rawXYextent,0)
rawZextent = 10 + earthquakeSource.centroidDepth + (10 * np.power((0.5*rawXYextent/earthquakeSource.centroidDepth),(0.3)))
Zextent = round(rawZextent,0)
timeExponent = max(1,0.5*earthquakeSource.mag - 1)
tmax = np.power(10, timeExponent)

class Domain:
#    MODEL_VERSION = '1.65_NZ'
    MODEL_VERSION = '1.02'
    MIN_VS = 0.5
    TOPO_TYPE = 'BULLDOZED'
    EXTENT_Z_SPACING = 0.1
    EXTENT_LATLON_SPACING = 0.1
    OUTPUT_DIR = 'Rapid_Model'
    EXTENT_ZMIN = 0
    ORIGIN_ROT = 0
    EXTRACTED_SLICE_PARAMETERS_DIRECTORY = 'SliceParametersNZ'

    ORIGIN_LAT = earthquakeSource.lat
    ORIGIN_LON = earthquakeSource.lon
    EXTENT_X = XYextent
    EXTENT_Y = XYextent
    EXTENT_ZMAX = Zextent
    T_MAX = tmax

fileName = 'Rapid_Velocity_Model_Parameters_Full.txt'
# write domain parameters to a shell script file that will call the velocity model
fid = open(fileName, 'w')
fid.write('MODEL_VERSION={0}\n'.format(Domain.MODEL_VERSION))
fid.write('OUTPUT_DIR={0}\n'.format(Domain.OUTPUT_DIR))
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

fileName = 'Rapid_Velocity_Model_Parameters_For_Domain_Plotting.txt'
# write domain parameters to a shell script file that will call the velocity model
fid = open(fileName, 'w')
fid.write('ORIGIN_LAT={0}\n'.format(Domain.ORIGIN_LAT))
fid.write('ORIGIN_LON={0}\n'.format(Domain.ORIGIN_LON))
fid.write('ORIGIN_ROT={0}\n'.format(Domain.ORIGIN_ROT))
fid.write('EXTENT_X={0}\n'.format(Domain.EXTENT_X))
fid.write('EXTENT_Y={0}\n'.format(Domain.EXTENT_Y))
fid.write('EXTENT_LATLON_SPACING={0}\n'.format(Domain.EXTENT_LATLON_SPACING))
fid.close()

fileName = 'Simulation_Duration.txt'
# write domain parameters to a shell script file that will call the velocity model
fid = open(fileName, 'w')
fid.write('T_MAX={0}\n'.format(Domain.T_MAX))
fid.close()


