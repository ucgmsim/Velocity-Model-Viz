#!/usr/bin/env python3

# load in libraries
from subprocess import call
import numpy as np
import sys
import os 

def main(): 
    # =============================================================================
     if len(sys.argv) == 1:
         sys.exit("Please provide a parameters text file. Exiting.")
    # =============================================================================
    
    paramsFileName = sys.argv[1]
    # use parametric functions to define velocity model domain parameters
    from velModFunctions import readDomainExtents
    Domain = readDomainExtents(paramsFileName.replace('.py',''))
    
    
    # clean the CD
    call(['rm', '-rf', Domain.OUTPUT_DIR])
    call(['rm', '-rf', 'temp'])
    call(['mkdir', Domain.OUTPUT_DIR])
    
    from velModFunctions import calcModelCorners
    corners = calcModelCorners(Domain)
    
    
    # Plot the domain on the map 
    import subprocess 
    # calling from subprocess can supress GMT warnings 
    exe = ['bash','GMT/plotDomainBoxOnMap.sh',Domain.OUTPUT_DIR]
    p = subprocess.Popen( exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    rtrncode = p.wait()
    print ("Completed plotting of domain on map.")
    
    call(['cp', paramsFileName, Domain.OUTPUT_DIR])
    
    # remove unnecessary files
    fileName = os.path.join(Domain.OUTPUT_DIR,'domainOutline.txt')
    call(['rm', fileName])
    fileName = os.path.join(Domain.OUTPUT_DIR,'VelModDomainBox.ps')
    call(['rm', fileName])
    fileName = os.path.join(Domain.OUTPUT_DIR,'PlotParameters.txt')
    call(['rm', fileName])
    call(['rm','-rf', 'gmt.conf'])
    call(['rm','-rf', 'gmt.history'])
    
    print ("Process complete.")

if __name__ == "__main__":
    main()