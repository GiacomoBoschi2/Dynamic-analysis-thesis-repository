import os

total_sum = 0

def get_number(syscall_name,subfolder):
    global total_sum
    counter = 0
    with open(os.path.join(subfolder,syscall_name+".txt"),"r") as R:
        lines = R.readlines()
        for line in lines:
            if (syscall_name+"(") in line and not f".{syscall_name}" in line:
                counter+=1
    print(f"number of '{syscall_name} syscalls for app : {subfolder} = {counter}")
    total_sum+=counter


if __name__ == "__main__":
    TARGET = "pthread_create"
    target_folder = "./Trace results"
    subfolders = [x[0] for x in os.walk(target_folder)][1:]
    for subfolder in subfolders:
        try:
            get_number(TARGET,str(subfolder))
        except:
            print("could not find syscall file for "+subfolder)
    print("total syscalls traced:"+str(total_sum))