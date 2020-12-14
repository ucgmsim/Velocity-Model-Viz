#!/usr/bin/env bash
#
# Script to plot the domain of the velocity model ontop of a map of NZ


SRTMDIR="GMT/Domain_On_Map/" # path to data

velModOutline="$1"/domainOutline.txt


ps="$1"/VelModDomainBox.ps   #name of output files
pdf="$1"/VelModDomainBox.pdf


#nz Wide
AREA=-R165/180/-48/-33
PROJ=-JT172.5/-40.5/10
DETAIL=-Df
ALL="$AREA $PROJ"



TOPO=${SRTMDIR}nztopo.grd #${SRTMDIR}srtm_71_21_v2.grd    #
ILLU=-I${SRTMDIR}nztopo_i5.grd #${SRTMDIR}srtm_71_21_v2_i5.grd #
PALETTE=-C${SRTMDIR}relief.cpt


gmt pscoast $ALL $DETAIL -Ba2f1 -Gc -K > $ps #as above, but now first command so ">" and no "-O" only
gmt pscoast $ALL $DETAIL -S135/206/235 -K -O >> $ps


# land and topography
gmt grdimage $TOPO $PALETTE $ALL -K -O >> $ps

# clear clippath
gmt pscoast -R -J -O -K -Q >> $ps

gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

#velModOutline="Velocity-Model/Data/SI_BASINS/Kaikoura_Polygon_WGS84.txt"
#gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

# mini map to the right
#nz Wide
source "$1"/PlotParameters.txt

#make topo map of region
AREA=-R$xMin/$xMax/$yMin/$yMax
PROJ=-JT$centreLon/$centreLat/10

xShift=14c
yShift=0c
DETAIL=-Df
ALL="$AREA $PROJ"

gmt pscoast $ALL $DETAIL -X$xShift -Y$yShift -Bxa${majorTickPlotX}"f"${minorTickPlotX} -Bya${majorTickPlotX}"f"${minorTickPlotX} -Gc -K -O >> $ps #as above, but now first command so ">" and no "-O" only
# gmt pscoast $ALL $DETAIL -S135/206/235 -K -O >> $ps

gmt pscoast $ALL $DETAIL -Gdarkseagreen2 -Scornflowerblue -K -O >> $ps 



# land and topography
#TOPO=${SRTMDIR}srtm_all_filt_nz.grd
#ILLU=-I${SRTMDIR}srtm_all_filt_i5_nz.grd
# gmt grdimage $TOPO $PALETTE $ALL -K -O  >> $ps

# clear clippath
gmt pscoast -R -J -O -K -Q >> $ps
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/Cheviot_Polygon_WGS84.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/Hanmer_Polygon_WGS84.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/Kaikoura_Polygon_WGS84.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/Marlborough_Polygon_WGS84_v0p1.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/Nelson_Polygon_WGS84.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/NewCanterburyBasinBoundary_WGS84_1m.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/NorthCanterbury_Polygon_WGS84.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/WaikatoHaurakiBasinEdge_WGS84.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/Wellington_Polygon_Wainuiomata_WGS84.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/mackenzie_basin_outline_nzmg.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps

velModOutline="GMT/Boundaries/wanaka_basin_outline_WGS84.txt"
gmt psxy $velModOutline -R -J $PERSP_MAP -W2p,black -O -K >> $ps


# if plot cross sections required
if [ "$2" ==  "PlotSliceLocations=true" ]
then
echo $2
#    # read file that contains how many slices there are
while read line; do
sliceNums=$line
done < "$1"/Reformatted_Slices/SliceIndicies.txt
#    echo $sliceNums

# loop over all slices
for sliceNum in ${sliceNums}
do

# load in the slice parameters to set the basemap
source "$1"/Reformatted_Slices/ExtractedSlice${sliceNum}_EndPoints.txt

gmt psxy -R -J $PERSP -W1p,black,- -O -K <<EOF>> $ps #-W2p,black -Sc0.1
$x1 $y1
$x2 $y2
EOF

#    #alignment; 2letter, L,C,R (left, center, right); T,M,B (top, middle, bottom)

if [ $sliceNum -gt 5 ]
then
loc="RT"

else
loc="LT"
fi
#alignment; 2letter, L,C,R (left, center, right); T,M,B (top, middle, bottom)
gmt pstext -J -R -N -O -K -Dj0.1/0.1 -F+j+f12,Helvetica,black+a0 <<END>>  $ps
$x2 $y2 $loc $sliceNum
END
done
fi ## end of the if statement L71


ps2pdf $ps $pdf
#rm $ps
