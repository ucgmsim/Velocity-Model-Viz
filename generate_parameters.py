import numpy as np
import sys

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
        self.EXTENT_LATLON_SPACING = extent_latlon_spac
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

    def write(self):
        with open('params_vel.py', 'w') as fid:
            fid.write("MODEL_VERSION = '{0}'\n".format(self.MODEL_VERSION))
            fid.write("OUTPUT_DIR = '{0}'\n".format(self.OUTPUT_DIR))
            fid.write("ORIGIN_LAT = '{0}'\n".format(self.ORIGIN_LAT))
            fid.write("ORIGIN_LON = '{0}'\n".format(self.ORIGIN_LON))
            fid.write("ORIGIN_ROT = '{0}'\n".format(self.ORIGIN_ROT))
            fid.write("EXTENT_X = '{0}'\n".format(self.EXTENT_X))
            fid.write("EXTENT_Y = '{0}'\n".format(self.EXTENT_Y))
            fid.write("EXTENT_ZMAX = '{0}'\n".format(self.EXTENT_ZMAX))
            fid.write("EXTENT_ZMIN = '{0}'\n".format(self.EXTENT_ZMIN))
            fid.write("EXTENT_Z_SPACING = '{0}'\n".format(self.EXTENT_LATLON_SPACING))
            fid.write("EXTENT_LATLON_SPACING = '{0}'\n".format(self.EXTENT_LATLON_SPACING))
            fid.write("MIN_VS = '{0}'\n".format(self.MIN_VS))
            fid.write("TOPO_TYPE= '{0}'\n\n".format(self.TOPO_TYPE))

            fid.write("CODE = '{0}'\n".format(self.CODE))
            fid.write("HH = '{0:1.3f}'\n".format(self.EXTENT_LATLON_SPACING))
            fid.write("NX = '{0:4.0f}'\n".format(2*self.EXTENT_X / self.EXTENT_LATLON_SPACING))  # EXTENT_X/HH
            fid.write("NY = '{0:4.0f}'\n".format(2*self.EXTENT_Y / self.EXTENT_LATLON_SPACING))
            fid.write("NZ = '{0:3.0f}'\n".format(self.EXTENT_ZMAX / self.EXTENT_LATLON_SPACING))
            fid.write("SIM_DURATION = '{0}'\n".format(self.T_MAX))
            fid.write("SUFX = '_{0}01-h{1:1.3f}'\n".format(self.CODE, self.EXTENT_LATLON_SPACING))
            fid.close()


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







