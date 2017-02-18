
# load in libraries
from subprocess import call
import numpy as np


# prescribe the domain limits, the box
class domainLimits:
    latMax = -33
    latMin = -48
    lonMin = 165
    lonMax = 180

# use parametric functions to define velocity model domain parameters
from velModFunctions import readDomainExtents
Domain = readDomainExtents()

# write a shell script to call velocity model code
from velModFunctions import writeGenerateModelShellScript
writeGenerateModelShellScript(Domain)

# execute shell script to generate velocity model
print('Generating velocity model.')
call(['bash', 'generateVeloModel.sh'])
print('Generating velocity model. Complete.')


# read the velocity model corners file and plot the domain on a map
from velModFunctions import investigateVelocityModelDomain
sliceParameters = investigateVelocityModelDomain(domainLimits)

# generate shell script to extract slices
from velModFunctions import writeExtractShellScript
writeExtractShellScript(Domain)
print('Extracting slices from velocity model.')
call(['bash', 'extractVeloModel.sh'])
print('Extracting slices from velocity model. Complete.')

# convert extracted slices for plotting in GMT
from velModFunctions import convertSlicesForGMTPlotting
convertSlicesForGMTPlotting(sliceParameters)
call(['mkdir', 'GMT/Cross_Sections'])
call(['mkdir', 'GMT/Cross_Sections/Cross_Section_Data'])
call(['bash', 'GMT/plotVeloModCrossSections.sh'])
call(['bash', 'GMT/plotVeloModCrossSectionLocations.sh'])
from velModFunctions import combinePDFs
combinePDFs()

# Relocate files and remove generated components
call(['rm', '-rf', 'Rapid_Model']) # remove folder if already in existence
call(['mkdir', 'Rapid_Model'])
print('Moving finalised velocity model.')

call(['mv', 'Velocity-Model/Rapid_Model', 'Rapid_Model'])
print('Moving finalised velocity model. Complete.')
print('Generating model params and cords.')
import gen_cords
import params_vel
gen_cords.main(outdir=os.path.join(os.curdir,params_vel.output_directory,"Rapid_Model/Velocity_Model"))

print('Generating model params and cords. Complete.')

print('Moving velocity model plots.')
call(['mv', 'GMT/Plots', 'Rapid_Model'])
print('Moving velocity model plots. Complete.')


print('Removing generated scripts.')
call(['rm', 'extractVeloModel.sh'])
call(['rm', 'Velocity-Model/Rapid_Model_Parameters_Generate.txt'])
call(['rm', 'generateVeloModel.sh'])
call(['rm', 'Velocity-Model/Rapid_Model_Parameters_Extract.txt'])
call(['rm', '-rf','GMT/Cross_Sections/'])
call(['rm', '-rf','Velocity-Model/SliceParametersNZ'])
call(['rm', '-rf','gmt.conf'])
call(['rm', '-rf','gmt.history'])
call(['cp', 'params_vel.py', 'Rapid_Model/Rapid_Model/Velocity-Model/'])

print('Rapid model generation complete.')



