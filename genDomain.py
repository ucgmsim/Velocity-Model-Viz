#!/usr/bin/python3


# load in libraries
import subprocess
import numpy as np
import os
import sys

def main():
    # =============================================================================
    if len(sys.argv) == 1:
        sys.exit("Please provide a parameters text file. Exiting.")
    #=============================================================================
    paramsFileName = sys.argv[1]
    
    
    # use parametric functions to define velocity model domain parameters
    from velModFunctions import readDomainExtents
    Domain = readDomainExtents(paramsFileName.replace('.py',''))
    
    # clean the CD
    subprocess.call(['rm', '-rf', Domain.OUTPUT_DIR])
    subprocess.call(['rm', '-rf', 'temp'])
    subprocess.call(['mkdir', Domain.OUTPUT_DIR])
    
    
    # make symlink for NZVM data 
    dst = 'Data'
    if not os.path.exists(dst):
        src = 'Velocity-Model/Data'
        os.symlink(src, dst)
        
    if Domain.INVESTIGATION_TYPE == 'AUTO_EXTRACT':
        from velModFunctions import calcModelCorners
        corners = calcModelCorners(Domain)
        
        from velModFunctions import writeGenerateExtractSlicesAutoShellScript
        writeGenerateExtractSlicesAutoShellScript(Domain)
    
        # Plot the domain on the map
        # calling from subprocess can supress GMT warnings 
        exe = ['GMT/plotDomainBoxOnMap.sh',Domain.OUTPUT_DIR]
        p = subprocess.Popen( exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        rtrncode = p.wait()
        print ("Completed plotting of domain on map.")
    
        # write the Cross section file
        from velModFunctions import writeSliceParametersFileExtractAuto
        sliceParameters = writeSliceParametersFileExtractAuto(Domain)
        
        # Generate VM
        vmParametersFile = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
        subprocess.call(['./Velocity-Model/NZVM', vmParametersFile])
        
        # write the extract VM config file
        from velModFunctions import writeExtractSlicesAutoShellScript
        writeExtractSlicesAutoShellScript(Domain)
        
        # Call extract from VM
        vmParametersFile = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
        subprocess.call(['./Velocity-Model/NZVM', vmParametersFile])
    
        
        # move extracted slices into the output directory
        subprocess.call(['cp', '-r', 'temp/Extracted_Slices',Domain.OUTPUT_DIR])
        
        # convert slices for plotting
        from velModFunctions import convertSlicesForGMTPlottingAutoExtracted
        convertSlicesForGMTPlottingAutoExtracted(sliceParameters,Domain)
        
        # plot slices 
        dataDirectory = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
        subprocess.call(['GMT/plotVeloModCrossSections.sh',dataDirectory])
        
        # plot slice locations
        # calling from subprocess can supress GMT warnings 
        exe = ['GMT/plotDomainBoxOnMap.sh',Domain.OUTPUT_DIR,"PlotSliceLocations=true"]
        p = subprocess.Popen( exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        rtrncode = p.wait()
        print ("Completed plotting of slice locations on map.")
    
        # concatenate into summary PDF
        from velModFunctions import combinePDFsAuto
        combinePDFsAuto(Domain,sliceParameters)
        print ("Completed concatenation of PDFs.")
        
        # remove unnecessary files
        fileName = os.path.join(Domain.OUTPUT_DIR,'domainOutline.txt')
        subprocess.call(['rm', fileName])
        fileName = os.path.join(Domain.OUTPUT_DIR,'VelModDomainBox.ps')
        subprocess.call(['rm', fileName])
        fileName = os.path.join(Domain.OUTPUT_DIR,'PlotParameters.txt')
        subprocess.call(['rm', fileName])
        fileName = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
        subprocess.call(['rm', fileName])
        fileName = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
        subprocess.call(['rm','-rf', fileName])
        subprocess.call(['rm', '-rf', 'temp'])
        subprocess.call(['rm','-rf', 'gmt.conf'])
        subprocess.call(['rm','-rf', 'gmt.history'])
        print ("Process complete.")
    
    
    elif Domain.INVESTIGATION_TYPE == 'AUTO_GENERATE':
        from velModFunctions import calcModelCorners
        corners = calcModelCorners(Domain)
        
        from velModFunctions import writeGenerateSlicesAutoShellScript
        writeGenerateSlicesAutoShellScript(Domain)
        
        # write the Cross section file
        from velModFunctions import writeSliceParametersFileAuto
        sliceParameters = writeSliceParametersFileAuto(Domain)
        
        # extract from VM
        vmParametersFile = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
        p = subprocess.Popen(['./Velocity-Model/NZVM', vmParametersFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        print(output, err)
        
        
        # move extracted slices into the output directory
        subprocess.call(['cp', '-r', 'temp/Generated_Slices',Domain.OUTPUT_DIR])
        print("Generated slice files moved.")
        
        # convert slices for plotting
        from velModFunctions import convertSlicesForGMTPlottingAutoGenerated
        convertSlicesForGMTPlottingAutoGenerated(sliceParameters,Domain)
        
        # plot slices 
        dataDirectory = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
        subprocess.call(['GMT/plotVeloModCrossSections.sh',dataDirectory])
        
        # plot slice locations
        # calling from subprocess can supress GMT warnings 
        exe = ['GMT/plotDomainBoxOnMap.sh',Domain.OUTPUT_DIR,"PlotSliceLocations=true"]
        p = subprocess.Popen( exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        rtrncode = p.wait()
        print ("Completed plotting of slice locations on map.")
    
        # concatenate into summary PDF
        from velModFunctions import combinePDFsAuto
        combinePDFsAuto(Domain,sliceParameters)
        print ("Completed concatenation of PDFs.")
        
        # remove unnecessary files
        fileName = os.path.join(Domain.OUTPUT_DIR,'domainOutline.txt')
        subprocess.call(['rm', fileName])
        fileName = os.path.join(Domain.OUTPUT_DIR,'VelModDomainBox.ps')
        subprocess.call(['rm', fileName])
        fileName = os.path.join(Domain.OUTPUT_DIR,'PlotParameters.txt')
        subprocess.call(['rm', fileName])
        fileName = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
        subprocess.call(['rm', fileName])
        fileName = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
        subprocess.call(['rm','-rf', fileName])
        subprocess.call(['rm', '-rf', 'temp'])
        subprocess.call(['rm','-rf', 'gmt.conf'])
        subprocess.call(['rm','-rf', 'gmt.history'])
        print ("Process complete.")
    
    
    
    elif (Domain.INVESTIGATION_TYPE == "USER_GENERATE"):
        from velModFunctions import readSliceParametersFile
        from velModFunctions import writeGenerateSlicesAutoShellScriptSpecificSlices
        from velModFunctions import convertSlicesForGMTPlottingAutoGeneratedMulti
        from velModFunctions import combinePDFsAuto
    
    
        for i in range(0, len(Domain.SLICE_PARAMETERS_TEXTFILES)):
            sliceParameters = readSliceParametersFile(Domain,Domain.SLICE_PARAMETERS_TEXTFILES[i])
            writeGenerateSlicesAutoShellScriptSpecificSlices(Domain,Domain.SLICE_PARAMETERS_TEXTFILES[i])
            vmParametersFile = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
            subprocess.call(['./Velocity-Model/NZVM', vmParametersFile])
            
            # move extracted slices into the output directory
            subprocess.call(['cp', '-r', 'temp/Generated_Slices',Domain.OUTPUT_DIR])
            print("Generated slice files moved.")
            
            # convert slices for plotting
            convertSlicesForGMTPlottingAutoGeneratedMulti(sliceParameters,Domain)
            
            # plot slices 
            dataDirectory = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
            subprocess.call(['GMT/plotVeloModCrossSections.sh',dataDirectory])

            # plot slice locations 
            # calling from subprocess can supress GMT warnings 
            exe = ['GMT/plotDomainBoxOnMap.sh',Domain.OUTPUT_DIR,"PlotSliceLocations=true"]
            p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            exe = ['GMT/plotDomainBoxOnMap.sh',Domain.OUTPUT_DIR,"PlotSliceLocations=true"]
            p = subprocess.Popen( exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
            rtrncode = p.wait()
            print ("Completed plotting of slice locations on map.")
    
            # concatenate into summary PDF
            
            combinePDFsAuto(Domain,sliceParameters)
            print ("Completed concatenation of PDFs.")
            dirName = os.path.join(Domain.OUTPUT_DIR,'Slice_set_{0}'.format(i+1))
        
            subprocess.call(['mkdir', dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'Generated_Slices'),dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'CrossSection_vp_slices.pdf'), dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'CrossSection_vs_slices.pdf'), dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'CrossSection_rho_slices.pdf'), dirName])
            subprocess.call(['cp', Domain.SLICE_PARAMETERS_TEXTFILES[i], dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'VelModDomainBox.pdf'), dirName])
    
            # remove unnecessary files
            fileName = os.path.join(Domain.OUTPUT_DIR,'VelModDomainBox.ps')
            subprocess.call(['rm', fileName])
            fileName = os.path.join(Domain.OUTPUT_DIR,'PlotParameters.txt')
            subprocess.call(['rm', fileName])
            fileName = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
            subprocess.call(['rm', fileName])
            fileName = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
            subprocess.call(['rm','-rf', fileName])
            subprocess.call(['rm', '-rf', 'temp'])
        
        # remove unnecessary files
        subprocess.call(['rm','-rf', 'gmt.conf'])
        subprocess.call(['rm','-rf', 'gmt.history'])
        print ("Process complete.")
        
    elif (Domain.INVESTIGATION_TYPE == "USER_EXTRACT"):
        from velModFunctions import readSliceParametersFileUserExtract
        from velModFunctions import writeGenerateExtractSlicesAutoShellScript
        from velModFunctions import convertSlicesForGMTPlottingAutoExtracted
        from velModFunctions import combinePDFsAuto
        from velModFunctions import writeExtractSlicesAutoShellScriptUserSlices
        from velModFunctions import calcModelCorners
    
        corners = calcModelCorners(Domain)
                
        sliceParameters = readSliceParametersFileUserExtract(Domain,Domain.SLICE_PARAMETERS_TEXTFILES[i])
            
        writeGenerateExtractSlicesAutoShellScript(Domain)
        vmParametersFile = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
           
        subprocess.call(['./Velocity-Model/NZVM', vmParametersFile])
    
        for i in range(0,2):# len(Domain.SLICE_PARAMETERS_TEXTFILES)):
            # write the extract VM config file
            writeExtractSlicesAutoShellScriptUserSlices(Domain,Domain.SLICE_PARAMETERS_TEXTFILES[i])
            
            # Call extract from VM
            vmParametersFile = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
            subprocess.call(['./Velocity-Model/NZVM', vmParametersFile])
        
        
        # move extracted slices into the output directory
            subprocess.call(['cp', '-r', 'temp/Extracted_Slices',Domain.OUTPUT_DIR])
            print("Extracted slice files moved.")
            
            # convert slices for plotting
    
            convertSlicesForGMTPlottingAutoExtracted(sliceParameters,Domain)
            
            # plot slices 
            dataDirectory = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
            subprocess.call(['GMT/plotVeloModCrossSections.sh',dataDirectory])

            # plot slice locations
            # calling from subprocess can supress GMT warnings 
            exe = [ 'GMT/plotDomainBoxOnMap.sh',Domain.OUTPUT_DIR,"PlotSliceLocations=true"]
            p = subprocess.Popen( exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
            rtrncode = p.wait()
            print ("Completed plotting of slice locations on map.")
    
            # concatenate into summary PDF
            combinePDFsAuto(Domain,sliceParameters)
            print ("Completed concatenation of PDFs.")
            
            dirName = os.path.join(Domain.OUTPUT_DIR,'Slice_set_{0}'.format(i+1))
            subprocess.call(['mkdir', dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'Extracted_Slices'),dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'CrossSection_vp_slices.pdf'), dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'CrossSection_vs_slices.pdf'), dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'CrossSection_rho_slices.pdf'), dirName])
            subprocess.call(['cp', Domain.SLICE_PARAMETERS_TEXTFILES[i], dirName])
            subprocess.call(['mv', os.path.join(Domain.OUTPUT_DIR,'VelModDomainBox.pdf'), dirName])
    
            # remove unnecessary files
            fileName = os.path.join(Domain.OUTPUT_DIR,'VelModDomainBox.ps')
            subprocess.call(['rm', fileName])
            fileName = os.path.join(Domain.OUTPUT_DIR,'Auto_VM_Parameters.txt')
            subprocess.call(['rm', fileName])
            fileName = os.path.join(Domain.OUTPUT_DIR,'Reformatted_Slices')
            subprocess.call(['rm','-rf', fileName])
        
        fileName = os.path.join(Domain.OUTPUT_DIR,'PlotParameters.txt')
        subprocess.call(['rm', fileName])
        fileName = os.path.join(Domain.OUTPUT_DIR,'domainOutline.txt')
        subprocess.call(['rm', fileName])
        dirName = os.path.join(Domain.OUTPUT_DIR,'VM_Binaries')
        subprocess.call(['mkdir', dirName])
        subprocess.call(['mv', 'temp',dirName])
        
        # remove unnecessary files
        subprocess.call(['rm','-rf', 'gmt.conf'])
        subprocess.call(['rm','-rf', 'gmt.history'])
        print ("Process complete.")

if __name__ == "__main__":
    main()

    
