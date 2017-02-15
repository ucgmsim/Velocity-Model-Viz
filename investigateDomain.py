
# load in libraries
from subprocess import call
import numpy as np
import wct

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
genModelCorners(Domain)


call(['bash', 'GMT/plotDomainBoxOnMapInterrogation.sh'])

db = wct.WallClockDB()
(maxT,avgT,minT) = db.estimate_wall_clock_time(Domain.NX,Domain.NY,Domain.NZ,Domain.SIM_DURATION,numCores)
