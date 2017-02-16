import numpy as np
import sys
import wct

# assume only two inputs (magnitude and epicentre)
class earthquakeSource:
    def __init__(self, mag, centroidDepth, lon, lat):
        self.mag = float(mag)
        self.centroidDepth = float(centroidDepth)  # in km +ve downwards
        self.lon = float(lon)
        self.lat = float(lat)

    def __str__(self):
        return "mag = %s centroidDepth = %s lon= %s lat = %s" % (self.mag, self.centroidDepth, self.lon, self.lat)


class Domain:
    def __init__(self, eq_src, output_dir, slice_params_dir, model_ver='1.65_NZ', min_vs=0.5, topo_type='BULLDOZED',
                 extent_z_spac=0.1, extent_latlon_spac=0.1, extent_zmin=0, origin_rot=0, code='rt'):
        self.MODEL_VERSION = model_ver
        self.MIN_VS = min_vs
        self.TOPO_TYPE = topo_type
        self.EXTENT_Z_SPACING = extent_z_spac
        self.HH = extent_latlon_spac
        self.OUTPUT_DIR = output_dir
        self.EXTENT_ZMIN = extent_zmin
        self.ORIGIN_ROT = origin_rot
        self.EXTRACTED_SLICE_PARAMETERS_DIRECTORY = slice_params_dir
        self.CODE = code
        self.ORIGIN_LAT = eq_src.lat
        self.ORIGIN_LON = eq_src.lon
	    
        # generate the domain extents based on the magnitude and epicentre

        rawXYextent = np.power(10, (0.55 * eq_src.mag - 1.2))
        XYextent = round(2 * rawXYextent, 0)
        rawZextent = 10 + eq_src.centroidDepth + (10 * np.power((0.5 * rawXYextent / eq_src.centroidDepth), (0.3)))
        Zextent = round(rawZextent, 0)
        timeExponent = max(1, 0.5 * eq_src.mag - 1)
        tmax = np.power(10, timeExponent)


        self.EXTENT_X = XYextent
        self.EXTENT_Y = XYextent
        self.EXTENT_ZMAX = Zextent
        self.T_MAX = round(tmax,0)
        

        self.NX = 2*self.EXTENT_X / self.HH
        self.NY = 2*self.EXTENT_Y / self.HH
        self.NZ = self.EXTENT_ZMAX / self.HH
        


    def write(self):
        with open('params_vel.py', 'w') as fid:
            fid.write("model_version = '{0}'\n".format(self.MODEL_VERSION))
            fid.write("output_directory = '{0}'\n".format(self.OUTPUT_DIR))
            fid.write("model_lat = '{0}'\n".format(self.ORIGIN_LAT))
            fid.write("model_lon = '{0}'\n".format(self.ORIGIN_LON))
            fid.write("model_rot = '{0}'\n".format(self.ORIGIN_ROT))
            fid.write("extent_x = '{0}'\n".format(self.EXTENT_X))
            fid.write("extent_y = '{0}'\n".format(self.EXTENT_Y))
            fid.write("extent_zmax = '{0}'\n".format(self.EXTENT_ZMAX))
            fid.write("extent_zmin = '{0}'\n".format(self.EXTENT_ZMIN))
            fid.write("min_vs = '{0}'\n".format(self.MIN_VS))
            fid.write("topo_type = '{0}'\n".format(self.TOPO_TYPE))
            fid.write("extracted_slice_parameters_directory = '{0}'\n\n".format(self.EXTRACTED_SLICE_PARAMETERS_DIRECTORY))

            fid.write("code = '{0}'\n".format(self.CODE))
            fid.write("hh = '{0:1.3f}'\n".format(self.HH))
            fid.write("nx = '{0:4.0f}'\n".format(self.NX)) 
            fid.write("ny = '{0:4.0f}'\n".format(self.NY))
            fid.write("nz = '{0:3.0f}'\n".format(self.NZ))
            fid.write("sim_duration = '{0}'\n".format(self.T_MAX))
            fid.write("sufx = '_{0}01-h{1:1.3f}'\n\n".format(self.CODE, self.HH))


    def estimate(self):
        db = wct.WallClockDB()
        (maxT,avgT,minT) = db.estimate_wall_clock_time(self.NX,self.NY,self.NZ,self.T_MAX,512)


if len(sys.argv) != 5:
    print "Usage %s mag centroidDepth lon lat" % sys.argv[0]
    sys.exit()

mag, centroidDepth, lon, lat, = sys.argv[1:]
eq_src = earthquakeSource(mag, centroidDepth, lon, lat)
print eq_src
output_dir = "Rapid_Model"
slice_params_dir = "SliceParametersNZ"
domain = Domain(eq_src, output_dir, slice_params_dir)
domain.write()
# domain.estimate()






