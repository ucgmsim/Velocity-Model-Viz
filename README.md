# Auto-Vel-Mod-Generation

1) Clone the Velocity model into this directory.

2) cd into Velocity-Model

3) execute 'make' or 'make parallel'

4) run generate_parameters.py using Mw, lat, lon and depth (this generates params_vel.py which can then be edited if desired)

5) run investigateDomain.py This plots the domain on a NZ map for interrogation purposes. Plot is housed in Domain subdir.

6) change / manually update the parameters in params_vel.py if desired (repeat steps 5 and 6 as necessary)

7) run genDomain.py resulting VM will be stored in Rapid_Model with slice plots and domain location
