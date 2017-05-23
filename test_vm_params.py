#!/usr/bin/python2

import sys
import os
import time
import config_vm as gp
import shutil
import shared
sys.path.append(os.path.abspath(os.path.curdir))

if __name__ == '__main__':        
    if not os.path.exists(gp.params_vel):
        print "Error: % must be in the directory" %gp.params_vel
        sys.exit(0)

    import params_vel as pv
    
    eq_src = gp.earthquakeSource(pv.mag,pv.centroidDepth,pv.MODEL_LON,pv.MODEL_LAT)
    domain = gp.Domain(eq_src, pv.output_directory, pv.extracted_slice_parameters_directory, model_ver=pv.model_version, min_vs=float(pv.min_vs), topo_type=pv.topo_type, hh=float(pv.hh), extent_zmin=float(pv.extent_zmin), rot=float(pv.MODEL_ROT), code=pv.code, extent_x=float(pv.extent_x), extent_y=float(pv.extent_y), extent_zmax=float(pv.extent_zmax),sim_duration=float(pv.sim_duration))
    #params_vel_backup = '%s.%s'%(gp.params_vel,time.strftime('%Y%m%d_%H%M%S'))
    params_vel_backup = '%s.%s'%(gp.params_vel,'bak')
    print "#####################   Backing up %s to %s"%(gp.params_vel,params_vel_backup)
    shutil.copyfile(gp.params_vel,params_vel_backup)
    domain.write()
    print "#####################  %s updated" %gp.params_vel
    shared.exe('diff -y %s %s'%(params_vel_backup,gp.params_vel))
    domain.estimate()







