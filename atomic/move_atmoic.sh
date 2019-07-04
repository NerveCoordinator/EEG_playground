# spits atomic dataset into 10000 folders so it is more managable

# folder counter
i=0

# make 10000 folders
while [ $i -le 10000 ]
do
    mkdir sorted_structures/$i
    i=$(( $i + 1 ))    
done

# glob for all the files in structures
for b in structures/*; do 
     # pick a random folder  
     FOLDER=$((RANDOM % 10000))      
     cp -v -- "$b" sorted_structures/$FOLDER
done
