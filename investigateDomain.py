
# load in libraries
from subprocess import call
import numpy as np
import sys
import qcore
sys.path.append(qcore.path)
import wct
from inspect import getsourcefile
mydir=os.path.dirname(abspath(getsourcefile(lambda:0)))

# prescribe the domain limits, the box
class domainLimits:
    latMax = -33
    latMin = -48
    lonMin = 165
    lonMax = 180
numCores = 512

# use parametric functions to define velocity model domain parameters
from velModFunctions import readDomainExtents
Domain = readDomainExtents()
call(['mkdir', 'Domain'])
call(['cp', 'params_vel.py', 'Domain'])

from velModFunctions import genModelCorners
corners = genModelCorners(Domain)
for i in range(0, 4):
    if (corners.Lon[i]>=domainLimits.lonMax):
        print('Warning: velocity model corner outside of allowable limits.')
        break
    if (corners.Lat[i]>=domainLimits.latMax):
        print('Warning: velocity model corner outside of allowable limits.')
        break
    if (corners.Lon[i]<=domainLimits.lonMin):
        print('Warning: velocity model corner outside of allowable limits.')
        break
    if (corners.Lat[i]<=domainLimits.latMin):
        print('Warning: velocity model corner outside of allowable limits.')
        break

        
    corners.Lat[i]


call(['bash', os.path.join(mydir,'GMT/plotDomainBoxOnMapInterrogation.sh')])

db = wct.WallClockDB()
(maxT,avgT,minT) = db.estimate_wall_clock_time(Domain.NX,Domain.NY,Domain.NZ,Domain.SIM_DURATION,numCores)
