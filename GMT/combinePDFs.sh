#!/usr/bin/env bash
PATH=$PATH:/Applications/GMT-5.2.1.app/Contents/Resources/bin:/

echo "Combining PDFs."
### stitch together all the extracted slice PDFs into one document for each vp vs and rho


while read line; do
    sliceNums=$line
done < "GMT/Cross_Sections/Cross_Section_Data/SliceIndicies.txt"



#### stitch together pdfs
stringRho=""

for sliceNum in ${sliceNums}
do
pdfRho="GMT/Plots/CrossSection${sliceNum}_rho.pdf"
stringRho="${stringRho} ${pdfRho}"
done

gmt psconvert -TF -F"GMT/Plots/ExtractedSlicesRho.pdf" $stringRho
rm $stringRho

stringVs=""

for sliceNum in ${sliceNums}
do
pdfVs="GMT/Plots/CrossSection${sliceNum}_vs.pdf"
stringVs="${stringVs} ${pdfVs}"
done

gmt psconvert -TF -F"GMT/Plots/ExtractedSlicesVs.pdf" $stringVs
rm $stringVs

stringVp=""

for sliceNum in ${sliceNums}
do
pdfVp="GMT/Plots/CrossSection${sliceNum}_vp.pdf"
stringVp="${stringVp} ${pdfVp}"
done

gmt psconvert -TF -F"GMT/Plots/ExtractedSlicesVp.pdf" $stringVp
rm $stringVp


echo "Combining PDFs. Complete."

