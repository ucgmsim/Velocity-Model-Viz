#!/usr/bin/python2

import numpy as np
import sys
#import qcore
#sys.path.append(qcore.path) #qcore path should have been added to PYTHONPATH

import wct
import argparse
import os
import shared

params_vel = 'params_vel.py'

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
    def __init__(self, eq_src, output_dir, slice_params_dir, model_ver='1.65', min_vs=0.5, topo_type='SQUASHED_TAPERED', hh=0.1,
                 extent_zmin=0.0, rot=0.0, code='rt', extent_x=None,extent_y=None,extent_zmax=None,sim_duration=None,flo=None):
        self.MODEL_VERSION = model_ver
        self.MAG = eq_src.mag
        self.CENTROID_DEPTH = eq_src.centroidDepth

        self.MIN_VS = min_vs
        self.TOPO_TYPE = topo_type
        self.EXTENT_Z_SPACING = hh#extent_z_spac
        self.HH = hh # extent_latlon_spac
        self.OUTPUT_DIR = output_dir #os.path.join(os.path.abspath(os.curdir),output_dir)
        self.EXTENT_ZMIN = extent_zmin
        self.ORIGIN_ROT = rot
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

        if extent_x is None:
            self.EXTENT_X = XYextent
        else:
            self.EXTENT_X = extent_x
        if extent_y is None:
            self.EXTENT_Y = XYextent
        else:
            self.EXTENT_Y = extent_y
        if extent_zmax is None:
            self.EXTENT_ZMAX = Zextent
        else:
            self.EXTENT_ZMAX = extent_zmax

        if sim_duration is None:
            self.T_MAX = round(tmax,0)
        else:
            self.T_MAX = sim_duration

        if flo is None:
            self.FLO = self.MIN_VS/(5.0*self.HH)
        else:
            self.FLO = flo


        self.NX = self.i_divide(self.EXTENT_X, self.HH)
        self.NY = self.i_divide(self.EXTENT_Y, self.HH)
        self.NZ = self.i_divide(self.EXTENT_ZMAX, self.HH)

        extent_x = self.EXTENT_X
        while self.NX is None:
            extent_x += 1
            self.NX = self.i_divide(extent_x, self.HH)
        if extent_x != self.EXTENT_X:
            print "!!! Warning: extent_x is not divisible by hh. Increasing extent_x from %f to %f" %(self.EXTENT_X, extent_x)
            self.EXTENT_X = extent_x

        extent_y = self.EXTENT_Y
        while self.NY is None:
            extent_y += 1
            self.NY = self.i_divide(extent_y, self.HH)
        if extent_y != self.EXTENT_Y:
            print "!!! Warning: extent_y is not divisible by hh. Increasing extent_y from %f to %f" %(self.EXTENT_Y, extent_y)
            self.EXTENT_Y = extent_y

        extent_zmax = self.EXTENT_ZMAX
        while self.NZ is None:
            extent_zmax += 1
            self.NZ = self.i_divide(extent_zmax, self.HH)
        if extent_zmax != self.EXTENT_ZMAX:
            print "!!! Warning: extent_zmax is not divisible by hh. Increasing extent_zmax from %f to %f" %(self.EXTENT_ZMAX, extent_zmax)
            self.EXTENT_ZMAX = extent_zmax


    def i_divide(self, f_numerator, f_denominator):
        f_quotient= f_numerator/f_denominator
        if float(int(f_quotient))*f_denominator == f_numerator: #check if f_numerator was multiple of f_denominator
            return f_quotient
        else:
            return None



    def write(self):
        with open('params_vel.py', 'w') as fid:

            fid.write("# If you edited this file manually, run 'test_vm_params.py' for integrity check !!!\n\n")
            fid.write("# Section I. Basic parameters (Manual Edit allowed)\n")
            fid.write("mag = '{0:1.1f}'\n".format(self.MAG))
            fid.write("centroidDepth = '{0:3.2f}'\n".format(self.CENTROID_DEPTH))
            fid.write("MODEL_LAT = '{0}'\n".format(self.ORIGIN_LAT))
            fid.write("MODEL_LON = '{0}'\n".format(self.ORIGIN_LON))
            fid.write("MODEL_ROT = '{0}'\n".format(self.ORIGIN_ROT))
            fid.write("hh = '{0:1.3f}'\n".format(self.HH))
            fid.write("min_vs = '{0}'\n".format(self.MIN_VS))

            fid.write("model_version = '{0}'\n".format(self.MODEL_VERSION))
            fid.write("topo_type = '{0}'\n".format(self.TOPO_TYPE))
            fid.write("output_directory = '{0}'\n".format(self.OUTPUT_DIR))
            fid.write("extracted_slice_parameters_directory = '{0}'\n".format(self.EXTRACTED_SLICE_PARAMETERS_DIRECTORY))
            fid.write("code = '{0}'\n\n".format(self.CODE))
            fid.write("# Section II. Derived parameters that can be manually editted \n")
            fid.write("extent_x = '{0}'\n".format(self.EXTENT_X))
            fid.write("extent_y = '{0}'\n".format(self.EXTENT_Y))
            fid.write("extent_zmax = '{0}'\n".format(self.EXTENT_ZMAX))
            fid.write("extent_zmin = '{0}'\n".format(self.EXTENT_ZMIN))
            fid.write("sim_duration = '{0}'\n".format(self.T_MAX))
            fid.write("flo = '{0}'\n\n".format(self.FLO))

            fid.write("# Section III. Automated values. DO NOT EDIT (Manual changes will be ignored)\n")
            fid.write("nx = '{0:4.0f}'\n".format(self.NX)) 
            fid.write("ny = '{0:4.0f}'\n".format(self.NY))
            fid.write("nz = '{0:3.0f}'\n".format(self.NZ))
            fid.write("sufx = '_{0}01-h{1:1.3f}'\n\n".format(self.CODE, self.HH))

    def show_output(self):
        print "############  Generated %s\n\n"  %params_vel
        with open(params_vel,'r') as f:
            lines = f.readlines()
            #print lines
            for l in lines:
                print l.strip('\n')


    def estimate(self):
        db = wct.WallClockDB()
        print "############  Estimated Wallclock time" 
        (maxT,avgT,minT) = db.estimate_wall_clock_time(self.NX,self.NY,self.NZ,self.T_MAX,512)

#if __name__ == '__main__':        
def main():


    parser = argparse.ArgumentParser()

    parser.add_argument("mag",type=float)
    parser.add_argument("centroidDepth",type=float)
    parser.add_argument("lon",type=float)
    parser.add_argument("lat",type=float)

    parser.add_argument("--model_version", default='1.65')
    parser.add_argument("--min_vs",type=float, default=0.5)
    parser.add_argument("--topo_type",default='BULLDOZED')
    parser.add_argument("--hh",type=float, default=0.1)
    parser.add_argument("--extent_zmin",type=float,default=0.0)

    parser.add_argument("--extent_x",type=float)
    parser.add_argument("--extent_y",type=float)
    parser.add_argument("--extent_zmax",type=float)
    parser.add_argument("--sim_duration",type=float)
    parser.add_argument("--flo",type=float)

    parser.add_argument("--rot",type=float,default=0.0)
    parser.add_argument("--code",default='rt')
    parser.add_argument("--output_dir",default="Rapid_Model")
    parser.add_argument("--slice_params_dir",default="SliceParametersNZ/SliceParametersExtracted.txt")

    args = parser.parse_args()
    eq_src = earthquakeSource(args.mag, args.centroidDepth, args.lon, args.lat)
    print eq_src
    #output_dir = "Rapid_Model"
    #slice_params_dir = "SliceParametersNZ/SliceParametersExtracted.txt"
    domain = Domain(eq_src, args.output_dir, args.slice_params_dir,model_ver=args.model_version,min_vs=args.min_vs,topo_type=args.topo_type,hh=args.hh, extent_zmin=args.extent_zmin,rot=args.rot,code=args.code,extent_x=args.extent_x, extent_y=args.extent_y, extent_zmax=args.extent_zmax, sim_duration=args.sim_duration,flo=args.flo)
    domain.write()
    domain.show_output()
    domain.estimate()


if __name__=='__main__':
    main()

