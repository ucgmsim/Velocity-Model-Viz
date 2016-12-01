#!/usr/bin/env bash
#
# Script to plot the domain of the velocity model ontop of a map of NZ
echo "Plotting velocity model domain on map."
PATH=$PATH:/Applications/GMT-5.2.1.app/Contents/Resources/bin:/ # add the path to gmt to the PATH variable
SRTMDIR="GMT/Domain_On_Map/" # path to data

velModOutline="Velocity-Model/Rapid_Model/Log/domainOutline.txt"


ps=GMT/Plots/VelModDomainBox.ps   #name of output files
pdf=GMT/Plots/VelModDomainBox.pdf
#make topo map of region
AREA=-R165/180/-48/-33
PROJ=-JT172.5/-40.5/10
DETAIL=-Df
ALL="$AREA $PROJ"

TOPO=${SRTMDIR}nztopo.grd #${SRTMDIR}srtm_71_21_v2.grd    #
ILLU=-I${SRTMDIR}nztopo_i5.grd #${SRTMDIR}srtm_71_21_v2_i5.grd #
PALETTE=-C${SRTMDIR}relief.cpt


gmt pscoast $ALL $DETAIL -Ba2.0f1.0 -Gc -K > $ps #as above, but now first command so ">" and no "-O" only
gmt pscoast $ALL $DETAIL -S135/206/235 -K -O >> $ps



# land
gmt grdimage $TOPO $ILLU $PALETTE $ALL -K -O >> $ps

# clear clippath
gmt pscoast -R -J -O -K -Q >> $ps

gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps


ps2pdf $ps $pdf
rm $ps


echo "Plotting velocity model domain on map. Complete."
