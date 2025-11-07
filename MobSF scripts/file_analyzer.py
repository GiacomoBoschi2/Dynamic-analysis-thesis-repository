#looks for files that match tpl names and does some counting of file extensions 
#it requires the .txt https traffic dumps of MobSF
#To run this you need:
#A target folder (check main)
#A set of folders,one per target application, each containing the application data .tar file of the target application obtained from MobSF.


import tarfile
import os
import tempfile



file_extensions = {

}
file_total = 0

detected={
    "okhttp":[],
    "picasso":[],
    "coil":[],
    "gson":[],
    "eventbus":[],
    "retrofit":[],
    "moshi":[],
    "room":[],
    "fullstory":[],
    "dagger":[],
    "glide":[],
    "timber":[],
    "rxjava":[]
}

#https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
def map_extensions(startpath):
    global file_total
    for root, dirs, files in os.walk(startpath):
        for f in files:
            file_total+=1
            extension = "none"
            if "." in str(f):
                extension = str(f).split('.')[-1]

            if extension in file_extensions.keys():
                file_extensions[extension]+=1
            else:
                file_extensions[extension]=1


def check_whitelist(startpath):
    for root, dirs, files in os.walk(startpath):
        for dir in dirs:
            str_dir = str(dir).lower()
            dir_path = os.path.join(root, dir)

            for k in detected.keys():
                if k in str_dir:
                    detected[k].append(os.path.relpath(dir_path, os.path.abspath(startpath)))

        for f in files:
            str_file = str(f).lower()
            dir_path = os.path.join(root, f)

            for k in detected.keys():
                if k in str_file:
                    detected[k].append(os.path.relpath(dir_path, os.path.abspath(startpath)))



def scan_files(tar_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        with tarfile.open(tar_file,"r") as tar:
            tar.extractall(path=temp_dir)
            map_extensions(temp_dir)
            check_whitelist(temp_dir)


if __name__=="__main__":
    target_folder = "./Applications data"
    
    subfolders = [x[0] for x in os.walk(target_folder)][1:]
    for subfolder in subfolders:
        scan_files(os.path.join(subfolder,"files.tar"))
   
    file_extensions = {k: v for k, v in sorted(file_extensions.items(), key=lambda item: item[1],reverse=True)}

    print("total files:"+str(file_total))
    for f in file_extensions.keys():
        print(f"{f}->{file_extensions[f]}  ({100*(round(file_extensions[f]/file_total,2))})")
    
    print("\n\nFiles related to TPLs")
    for f in detected.keys():
        print(f"{f}->{detected[f]}")