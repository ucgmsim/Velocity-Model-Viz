#!/bin/bash
#
# Script to plot Vs Vp and rho cross sections in GMT
echo "Plotting velocity model cross sections."
PATH=$PATH:/Applications/GMT-5.1.2.app/Contents/Resources/bin:/

cp -R Velocity-Model/Rapid_Model/Reformatted_Slices/. GMT/Cross_Sections/Cross_Section_Data
gmt gmtset FONT_ANNOT_PRIMARY 7
gmt gmtset FONT_LABEL 9
SRTMDIR="GMT/Cross_Sections/"

# read file that contains how many slices there are
while read line; do
    sliceNums=$line
done < ${SRTMDIR}"Cross_Section_Data/SliceIndicies.txt"

# loop over all slices
for sliceNum in 1 ${sliceNums}
do

# load in the slice parameters to set the basemap
source ${SRTMDIR}"Cross_Section_Data/ExtractedSlice${sliceNum}_Parameters.txt"

AREA=-R$xMin/$xMax/$zMin/$zMax
PROJ=-JX17.63c/10.8c


################# Vs
ps="GMT/Plots/CrossSection${sliceNum}_vs.ps"
pdf="GMT/Plots/CrossSection${sliceNum}_vs.pdf"

sliceData=${SRTMDIR}"Cross_Section_Data/ExtractedSlice${sliceNum}_Vs.txt";

gmt psbasemap $AREA $PROJ -Bxa1f0.25+l'Latitude or Longitude' -Bya10f2.5+l'Elevation (km)' -BNesW -P -K -Y+16.5c -X+2.4c > $ps

# make CPT files (if necessary)
BASECPT_VS_PLOT=GMT/CPT/Vs_Plot.cpt
BASECPT_VS_BAR=GMT/CPT/Vs_Bar.cpt
ZMIN=0.25
ZMAX=5.25
ZINC=0.01
#gmt makecpt -Cjet -T$ZMIN/$ZMAX/$ZINC > $BASECPT_VS_PLOT
ZINC=0.25
ZINCPLOT=0.5;
#gmt makecpt -Cjet -T$ZMIN/$ZMAX/$ZINC > $BASECPT_VS_BAR
gmt psxy $sliceData -R -J -Ss2.0p -C$BASECPT_VS_PLOT -i0,1,2 -O -K >> $ps
echo "Slice ${sliceNum} Vs" | gmt pstext -R -J -F+cTL -F+f18p -X-2 -Y2 -P -K -O  >> $ps

gmt psscale -C$BASECPT_VS_BAR -X2 -Y-2 -D8.5/-.5/12.5/0.3h -K -O -Np -Ba${ZINCPLOT}f${ZINC}:"Shear wave velocity, V@-s@- (km/s)": >> $ps

#rm $BASECPT_VS_PLOT $BASECPT_VS_BAR
gmt psxy -R -J -O -T >> $ps

ps2pdf $ps $pdf
#rm $ps

################# Vp
ps="GMT/Plots/CrossSection${sliceNum}_vp.ps"
pdf="GMT/Plots/CrossSection${sliceNum}_vp.pdf"
sliceData=${SRTMDIR}"Cross_Section_Data/ExtractedSlice${sliceNum}_Vp.txt";

gmt psbasemap $AREA $PROJ -Bxa1f0.25+l'Latitude or Longitude' -Bya10f2.5+l'Elevation (km)' -BNesW -P -K -Y+16.5c -X+2.4c > $ps

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
#rm $ps

################# Vs
ps="GMT/Plots/CrossSection${sliceNum}_rho.ps"
pdf="GMT/Plots/CrossSection${sliceNum}_rho.pdf"

sliceData=${SRTMDIR}"Cross_Section_Data/ExtractedSlice${sliceNum}_Rho.txt";

gmt psbasemap $AREA $PROJ -Bxa1f0.25+l'Latitude or Longitude' -Bya10f2.5+l'Elevation (km)' -BNesW -P -K -Y+16.5c -X+2.4c > $ps

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
#rm $ps

done
echo "Plotting velocity model cross sections. Complete."
