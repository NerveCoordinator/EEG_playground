# Takes a range of the 10,000 files of the split dataset 
# expands them to a form usable by gpt-2

import random        
import os

output = ""

structures = {}


count = 0

folder_start = 2501
folder_end = 3500

folder_dir = os.getcwd() + '/expanded_structures/' + str(folder_start) + "_" + str(folder_end)
import shutil
if os.path.exists(folder_dir):
    shutil.rmtree(folder_dir)
for name in ["", "/test", "/train", "/validate"]:
    path = folder_dir + name
    print(path)
    if (os.path.exists(path)):
        print("exists")
        exit()
    else:
        os.mkdir(path)

for x in range(folder_start,folder_end):
    struct_dir = os.getcwd() + "/sorted_structures/" + str(x) + "/"
    for filename in os.listdir(struct_dir):
        with open(struct_dir+filename) as f:
            for line in f:
                if len(line) < 2:
                    continue
                try:
                    structures[filename[:-4]] += line
                except:
                    structures[filename[:-4]] = line
                  
for file_name in ["train", "test"]:
    with open(file_name + ".csv") as f:        
        count = 0
        last_name = ""
        file_name_choice = "test"
        for i, line in enumerate(f):
            count += 1            
            #if count>50:
            #    break

            space_line = line.split(",")  
            name = space_line[1]
            if file_name == "train" and name != last_name:
                file_name_choice = file_name
                last_name = name
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
            
            
