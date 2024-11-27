import os
import shutil

def generate_static_files_list(source):
    filelist = []
    directory_files = os.listdir(source)

    for file in directory_files:
        filelist.append(os.path.join(source, file))
    for file in filelist:
        if not os.path.isfile(file):
            subfolder_files = generate_static_files_list(file)
            filelist += subfolder_files
    
    #
    return filelist

def copy_static_to_public(filelist, destination):
    
    if os.path.exists(destination):
        print(f"deleting {destination}...")
        shutil.rmtree(destination)
    
    os.mkdir(destination)

    for file in filelist:
        destination_path = destination + file.split("/", 1)[1]
        if not os.path.isfile(file):
            os.mkdir(destination_path)
        else: 
            shutil.copy(file, destination_path)
        print(f"Processing: {file}")
        print(f"Destination: {destination_path}")

