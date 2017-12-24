echo "Initialising"
rm dicom_images/*.dcm
cp $1/*.dcm dicom_images
clear
python del_images.py &
wait
clear
echo 'Creating Resampling set and converting'
python t2.py
wait
clear
echo 'Creating False Colored images'
python OP/t3.py
wait
clear
echo 'Contouring liver'
python liver_trace1.py &
wait
clear
echo 'Contouring tumor'
python tumor_trace1.py &
wait
clear
echo "DONE!"
echo 'Copying contents to RESULTS'
filename="$(date +"%d-%m-%y_%H-%M-%S")"
filename=$1_$filename
mkdir -p RESULTS/${filename}
mkdir -p RESULTS/${filename}/WINDOWED
cp OP/*jpg RESULTS/${filename}/WINDOWED
mkdir -p RESULTS/${filename}/ORIGINAL
cp OP_OG/*jpg RESULTS/${filename}/ORIGINAL
mkdir -p RESULTS/${filename}/JHS
cp JHS/*jpg RESULTS/${filename}/JHS
mkdir -p RESULTS/${filename}/Liver_OP
cp Liver_OP/*jpg RESULTS/${filename}/Liver_OP
mkdir -p RESULTS/${filename}/Tumor_OP
cp Tumor_OP/*jpg RESULTS/${filename}/Tumor_OP



