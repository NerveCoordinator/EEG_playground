# Assumes you already split dataset into 10,000 folders via move_atomic.sh
# expands a subset of them to a form usable by gpt-2

# the structure of the training data is something like:
# numbers numbers numbers
# numbers numbers numbers
# <row 1 id information> <ground truth value>
# <row 2 id information> <ground truth value>

# but because of how gpt-2 works we have to split this into: 

# numbers numbers numbers
# numbers numbers numbers
# <row 1 id information> <ground truth value>

# numbers numbers numbers
# numbers numbers numbers
# <row 2 id information> <ground truth value>

# this is because when testing we don't be able to see
# the ground truth value for the previous row. If we feed
# it in anyway we'd have a compounding error since the
# previous row we predict will be at least slightly wrong.

# I suspect this can be overcome by restructuring gpt-2,
# probably by having it give multiple outputs at once 
# or maybe selective hiding of information while training?
# but I don't know how to do that yet. I just want to see
# if this works in a basic capacity first.


import random        
import os
import shutil

# move these down
output = ""
structures = {}
count = 0

# these really should be command line arguments
folder_start = 2501
folder_end = 3500

# generate path for this range of folders
folder_dir = os.getcwd() + '/expanded_structures/' + str(folder_start) + "_" + str(folder_end)

# delete folder if it exists already 
if os.path.exists(folder_dir):
    shutil.rmtree(folder_dir)

# create folder for range and subfolders train test and validate
for name in ["", "/test", "/train", "/validate"]:
    path = folder_dir + name
    print(path) # let user know which folders we got through in case one already exists
    if (os.path.exists(path)):
        print("exists")
        exit()
    else:
        os.mkdir(path)

# for each folder in our subrange of the 10,000 folders
for x in range(folder_start,folder_end):
    # get folder path
    struct_dir = os.getcwd() + "/sorted_structures/" + str(x) + "/"
    for filename in os.listdir(struct_dir):
        # open folder
        with open(struct_dir+filename) as f:
            # add each line to a dict named structures
            for line in f:
                if len(line) < 2:
                    continue
                try:
                    # [:-4] cuts off the '.xyz' file extension
                    # we get the filename again later, so we can use it as an id
                    structures[filename[:-4]] += line
                except:
                    structures[filename[:-4]] = line

# for our training and testing set 
for file_name in ["train", "test"]:
    # open train.csv or test.csv
    with open(file_name + ".csv") as f:        
        # keep track of number of lines with count
        count = 0
        # last_name keeps all data from same file together in train or validation 
        last_name = ""
        # assumes we're a test datapoint since we use this variable in final_filename
        file_name_choice = "test"
        for i, line in enumerate(f):
            count += 1   
            # for if we want a tiny dataset to practice with
            ## if count>50:
            ##    break

            # break csv into pieces
            space_line = line.split(",")  
            # atom name
            name = space_line[1]
            
            # if this is a training data point
            # and if the name is different from
            # the last data point
            if file_name == "train" and name != last_name:
                # mark this as training
                file_name_choice = file_name
                last_name = name
                # but 1/10 times mark it as validate
                if (random.randint(1,10) == 1):
                    file_name_choice = "validate"
            
            line_meta_data = line.split(",")[2:]
            meta_str = ",".join(line_meta_data)
            output_file = ""
            try:            
                curr_struct = structures[name].split("\n")
                #print(curr_struct)
                num_rows = int(curr_struct[0])
                #print(structures[name])
                output_file = "\n".join(curr_struct) + "\n" + meta_str
                
            except:  
                continue
            final_filename = folder_dir + "/" + file_name_choice + "/" + str(i) + "_" +name + ".xyz" #+ name + "_" str(i) ".xyz"#str(i) 
            #print(final_filename)
            #exit()
            #print(final_filename)
            
            with open(final_filename, "w") as  f:
                f.write(output_file)            
               
            #print("---")
            
            #print(file_name)
            #print(output_file)
            
            
