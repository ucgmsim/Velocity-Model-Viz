# load in libraries
from subprocess import call

call(['rm', '-rf', 'Rapid_Model']) 
call(['rm', '-rf', 'Velocity-Model/Rapid_Model'])
call(['rm', '-rf', 'Domain'])

call(['rm', '-rf', 'GMT/Plots'])
call(['rm', '-rf','gmt.conf'])
call(['rm', '-rf','gmt.history'])

call(['rm', '-rf', 'extractVeloModel.sh'])
call(['rm', '-rf', 'generateVeloModel.sh'])
call(['rm', '-rf', 'GMT/Cross_Sections/'])
call(['rm', '-rf', 'Velocity-Model/SliceParametersNZ'])
call(['rm', '-rf', 'Velocity-Model/Rapid_Model_Parameters_Generate.txt'])
call(['rm', '-rf', 'Velocity-Model/Rapid_Model_Parameters_Extract.txt'])
