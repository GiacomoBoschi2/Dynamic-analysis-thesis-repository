import os


black_list = ["android.", "java."]
library_tree = {}
syscall_use = {}

def detect_syscalls(library,syscalls,subfolder):
    global library_tree
    for syscall in syscalls:
        reading_stack = False
        with open(os.path.join(subfolder,syscall+".txt"),"r") as R:
            lines = R.readlines()
            for line in lines:
                if "JAVA STACK" in line:
                    reading_stack = True
                elif reading_stack:
                    try:
                        if line[:-1].endswith(")"):
                            package = line.split(' ')[6]
                            actor = package.split('(')[0]

                            #check blacklist does not match actor
                            valid = True
                            for p in black_list:
                                if p in library:
                                    valid = False
                                    break
                            
                            if library in actor and valid :
                                syscall_use[library][syscall] = True
                                if actor in library_tree.keys():
                                    if syscall in library_tree[actor].keys():
                                        library_tree[actor][syscall]+=1
                                    else:
                                        library_tree[actor][syscall] = 1
                                else:
                                    library_tree[actor] =  {syscall:1}
                        else:
                            reading_stack = False
                    except:
                        continue


if __name__ == "__main__":
    TARGET = ["okhttp3","retrofit","gson","eventbus","glide","moshi","lottie","leakcanary","timber","room","coil","rxjava","dagger","fullstory"]
    SYSCALLS = ["open","close","socket","ioctl","pthread_create","sendto","recvfrom"]
    for lib in TARGET:
        syscall_use[lib] = {}
        for sysc in SYSCALLS:
            syscall_use[lib][sysc] = False
    
    
    target_folder = "./Trace results"
    subfolders = [x[0] for x in os.walk(target_folder)][1:]
    for subfolder in subfolders:
        try:
            for lib in TARGET:
             detect_syscalls(lib,SYSCALLS,str(subfolder))
        except :
            continue

    #output 
    print(f"Library tree for {TARGET}:")
    for key in library_tree.keys():
        print(key)
        print(library_tree[key])
    
    print(f"syscall usage:")
    for key in syscall_use:
     print(f"{key} -> {syscall_use[key]}")


