#!/bin/bash
#
# Script to plot Vs Vp and rho cross sections in GMT



gmt gmtset FONT_ANNOT_PRIMARY 7
gmt gmtset FONT_LABEL 9

SRTMDIR="GMT/Cross_Sections/"

# read file that contains how many slices there are
while read line; do
    sliceNums=$line
done < "$1"/SliceIndicies.txt

# loop over all slices
for sliceNum in 1 ${sliceNums}
do

# load in the slice parameters to set the basemap
source "$1"/ExtractedSlice${sliceNum}_Parameters.txt

AREA=-R$xMin/$xMax/$zMin/$zMax
PROJ=-JX17.63c/10.8c


################# Vs
ps="$1"/CrossSection${sliceNum}_vs.ps
pdf="$1"/CrossSection${sliceNum}_vs.pdf

sliceData="$1"/ExtractedSlice${sliceNum}_Vs.txt



gmt psbasemap $AREA $PROJ -Bxa${majorTickPlotX}"f"${minorTickPlotX}+l'Longitude' -Bya${majorTickPlotZ}"f"${minorTickPlotZ}+l'Elevation - Z (km)' -BNesW -P -K -Y+16.5c -X+2.4c > $ps

# make CPT files (if necessary)
BASECPT_VS_PLOT=GMT/CPT/Vs2_Plot.cpt
BASECPT_VS_BAR=GMT/CPT/Vs2_Bar.cpt
ZMIN=0.25
ZMAX=4.25
ZINC=0.01
gmt makecpt -Cjet -T$ZMIN/$ZMAX/$ZINC -Do -M > $BASECPT_VS_PLOT
ZINC=0.125
ZINCPLOT=0.5;
gmt makecpt -Cjet -T$ZMIN/$ZMAX/$ZINC -Do -M > $BASECPT_VS_BAR
gmt psxy $sliceData -R -J -Ss2.0p -C$BASECPT_VS_PLOT -i0,1,2 -O -K >> $ps
echo "Slice ${sliceNum} Vs" | gmt pstext -R -J -F+cTL -F+f18p -X-2 -Y2 -P -K -O  >> $ps

gmt psscale -C$BASECPT_VS_BAR -X2 -Y-2 -D8.5/-.5/12.5/0.3h -K -O -Np -Ba${ZINCPLOT}f${ZINC}:"Shear wave velocity, V@-s@- (km/s)": >> $ps

rm $BASECPT_VS_PLOT $BASECPT_VS_BAR
gmt psxy -R -J -O -T >> $ps

ps2pdf $ps $pdf
rm $ps

################# Vp
ps="$1"/CrossSection${sliceNum}_vp.ps
pdf="$1"/CrossSection${sliceNum}_vp.pdf
sliceData="$1"/ExtractedSlice${sliceNum}_Vp.txt

gmt psbasemap $AREA $PROJ -Bxa${majorTickPlotX}"f"${minorTickPlotX}+l'Longitude' -Bya${majorTickPlotZ}"f"${minorTickPlotZ}+l'Elevation - Z (km)' -BNesW -P -K -Y+16.5c -X+2.4c > $ps

# make CPT files (if necessary)
BASECPT_VP_PLOT=GMT/CPT/Vp_Plot.cpt
BASECPT_VP_BAR=GMT/CPT/Vp_Bar.cpt
ZMIN=1.5
ZMAX=9.5
ZINC=0.01
#gmt makecpt -Cjet -T$ZMIN/$ZMAX/$ZINC > $BASECPT_VP_PLOT
ZINC=0.5
ZINCPLOT=1;
#gmt makecpt -Cjet -T$ZMIN/$ZMAX/$ZINC > $BASECPT_VP_BAR
gmt psxy $sliceData -R -J -Ss2.0p -C$BASECPT_VP_PLOT -i0,1,2 -O -K >> $ps
echo "Slice ${sliceNum} Vp" | gmt pstext -R -J -F+cTL -F+f18p -X-2 -Y2 -P -K -O  >> $ps

gmt psscale -C$BASECPT_VP_BAR -X2 -Y-2 -D8.5/-.5/12.5/0.3h -K -O -Np -Ba${ZINCPLOT}f${ZINC}:"Primary wave velocity, V@-p@- (km/s)": >> $ps

#rm $BASECPT_VP_PLOT $BASECPT_VP_BAR
gmt psxy -R -J -O -T >> $ps

ps2pdf $ps $pdf
rm $ps

################# Vs
ps="$1"/CrossSection${sliceNum}_rho.ps
pdf="$1"/CrossSection${sliceNum}_rho.pdf

sliceData="$1"/ExtractedSlice${sliceNum}_Rho.txt

gmt psbasemap $AREA $PROJ -Bxa${majorTickPlotX}"f"${minorTickPlotX}+l'Longitude' -Bya${majorTickPlotZ}"f"${minorTickPlotZ}+l'Elevation - Z (km)' -BNesW -P -K -Y+16.5c -X+2.4c > $ps

# make CPT files (if necessary)
BASECPT_RHO_PLOT=GMT/CPT/Rho_Plot.cpt
BASECPT_RHO_BAR=GMT/CPT/Rho_Bar.cpt
ZMIN=1.6
ZMAX=3.6
ZINC=0.01
#gmt makecpt -Cjet -T$ZMIN/$ZMAX/$ZINC > $BASECPT_RHO_PLOT
ZINC=0.1
ZINCPLOT=0.2;
#gmt makecpt -Cjet -T$ZMIN/$ZMAX/$ZINC > $BASECPT_RHO_BAR
gmt psxy $sliceData -R -J -Ss2.0p -C$BASECPT_RHO_PLOT -i0,1,2 -O -K >> $ps
echo "Slice ${sliceNum} Rho" | gmt pstext -R -J -F+cTL -F+f18p -X-2 -Y2 -P -K -O  >> $ps

gmt psscale -C$BASECPT_RHO_BAR -X2 -Y-2 -D8.5/-.5/12.5/0.3h -K -O -Np -Ba${ZINCPLOT}f${ZINC}:"Density, rho (T/m^3)": >> $ps

#rm $BASECPT_RHO_PLOT $BASECPT_RHO_BAR
gmt psxy -R -J -O -T >> $ps

ps2pdf $ps $pdf
rm $ps

done
echo "Plotting velocity model cross sections. Complete."
