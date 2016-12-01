#!/bin/bash

# script to plot the extracted slice locations on a NZ map for reference

echo "Plotting velocity model cross section locations on map."

PATH=$PATH:/Applications/GMT-5.2.1.app/Contents/Resources/bin:/

SRTMDIR="GMT/Domain_On_Map/" # path to data

velModOutline="Velocity-Model/Rapid_Model/Log/domainOutline.txt"

ps=GMT/Plots/VelModSliceLocations.ps   #name of output files
pdf=GMT/Plots/VelModSliceLocations.pdf

source "GMT/Cross_Sections/Cross_Section_Data/BoundingBox.txt"

#make topo map of region
AREA=-R$xMin/$xMax/$yMin/$yMax
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

gmt psxy $velModOutline -R -J -W2p,black -O -K >> $ps

SRTMDIR="GMT/Cross_Sections/"

# read file that contains how many slices there are
while read line; do
    sliceNums=$line
done < ${SRTMDIR}"Cross_Section_Data/SliceIndicies.txt"

# loop over all slices
for sliceNum in 1 ${sliceNums}
do

# load in the slice parameters to set the basemap
source ${SRTMDIR}"Cross_Section_Data/ExtractedSlice${sliceNum}_EndPoints.txt"

gmt psxy -R -J $PERSP -W1p,black,- -O -K <<EOF>> $ps #-W2p,black -Sc0.1
$x1 $y1
$x2 $y2
EOF
#alignment; 2letter, L,C,R (left, center, right); T,M,B (top, middle, bottom)

if [ $x2 == $x1 ]
then
    loc="CT"
else
    loc="RM"
fi
#alignment; 2letter, L,C,R (left, center, right); T,M,B (top, middle, bottom)
gmt pstext -J -R -N -O -K -Dj0.1/0.1 -F+j+f12,Helvetica,black+a0 <<END>>  $ps
$x1 $y1 $loc $sliceNum
END


done
ps2pdf $ps $pdf
rm $ps

echo "Plotting velocity model cross section locations on map. Complete."