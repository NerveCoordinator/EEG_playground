# For splitting up atomic data from here https://www.kaggle.com/c/champs-scalar-coupling/data
# for each file in the structures folder, move to either train, test, or validate.

'''
with open("pkfs_Train.fasta") as f:
    data = f.read()
    #print(data)
    for line in f:#data.split("\n"):    
        line2 = f.next()
        print(line)
        print(line2)
'''

import random        
import os

output = ""


structures = {}

struct_dir = os.getcwd() + "/structures/"

count = 0
for filename in os.listdir(struct_dir):
    with open(struct_dir+filename) as f:
            for line in f:
                if len(line) < 2:
                    continue
                try:
                    structures[filename[:-4]] += line
                    #print(filename)
                except:
                    structures[filename[:-4]] = line
    
    count += 1
    '''    
    if count > 5:
        break 
    '''
              
   # do your stuff





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
            final_filename = file_name_choice + "/" + str(i) + "_" +name + ".xyz" #+ name + "_" str(i) ".xyz"#str(i) 
            #print(final_filename)
            #print(final_filename)
            
            with open(final_filename, "w") as  f:
                f.write(output_file)            
               
            #print("---")
            
            #print(file_name)
            #print(output_file)
            
            
