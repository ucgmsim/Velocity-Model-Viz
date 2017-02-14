# load in libraries
from subprocess import call



call(['rm', '-rf', 'Rapid_Model']) 
call(['rm', '-rf', 'Velocity-Model/Rapid_Model'])
call(['rm', '-rf', 'Domain'])

call(['mv', '-rf', 'GMT/Plots'])
call(['rm', '-rf','gmt.conf'])
call(['rm', '-rf','gmt.history'])

call(['rm', 'extractVeloModel.sh'])
call(['rm', 'generateVeloModel.sh'])
call(['rm', '-rf','GMT/Cross_Sections/'])
call(['rm', '-rf','Velocity-Model/SliceParametersNZ'])
