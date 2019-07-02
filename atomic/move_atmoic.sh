# spits atomic dataset into 10000 folders so it is more managable


# set a variable to 0 so we can increment it
i=0
# glob for the files starting with b

echo $i

while [ $i -le 10000 ]
do
    mkdir sorted_structures/$i
    i=$(( $i + 1 ))    
done

#exit
i=0
for b in structures/*; do 
   
     FOLDER=$((RANDOM % 10000)) 
     cp -v -- "$b" sorted_structures/$FOLDER

     #mkdir fake_dir/F_${FOLDER}
     #echo $FOLDER

done
