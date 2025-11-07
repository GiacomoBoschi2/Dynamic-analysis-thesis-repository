# calculates the total amount of classes, differentiating the amount of classes from the android package, the java package, and thirdiary packages.

import os


match_android  =["com.android.","android.",".android"]
match_java = [".java.","java."]
class_counter = {}
total_classes = 0
total_methods = 0
java_classes = 0
android_classes = 0
folder = "./Captures"
CLASS_PREFIX = "CLASS"
END_METHODS = "-"
START_METHODS = "METHODS"


def in_list(wl,target):
    for cand in wl:
        if cand in target:
            return True
    return False

def scan_capture(file_name):
        global total_classes
        global java_classes
        global android_classes
        global total_methods
        global class_counter
        lines = []
        with open(file_name,"r") as reader:
            lines = reader.readlines()

        #skip to first class
        i = 0
        while not CLASS_PREFIX in lines[i]:
             i+=1
            
        while i< len(lines):
            if CLASS_PREFIX in lines[i]:
                total_classes+=1
                
                name = lines[i].split(' ')[1].replace("\n","")
                if name in class_counter.keys():
                    class_counter[name] = class_counter[name] + 1 
                else:
                    class_counter[name] = 1

                
                for package in match_android:
                    if package in name:
                        android_classes+=1
                        break
                for package in match_java:
                    if package in name:
                        java_classes+=1
                        break
                i+=2
                while i <len(lines) and lines[i][0]!="-":
                    total_methods+=1
                    i+=1
                continue
            i+=1

def filtered_print(min_inst = 1,max_inst = 100,blacklist=[],whitelist = ["okhttp3"]):
    global class_counter
    for k in class_counter.keys():
        if class_counter[k] >=min_inst and class_counter[k] <=max_inst and not in_list(blacklist,k) and in_list(whitelist,k):
            print(f"{k}->{class_counter[k]} istances")


if __name__ == "__main__":
    for capture in os.listdir(folder):
        if capture.endswith(".data"):
            file_path = os.path.join(folder, capture)
            scan_capture(file_path)

    print("total classes: "+str(total_classes))
    print("android classes:"+str(android_classes))
    print("java classes: "+str(java_classes))
    print("non identified classes: "+str(total_classes-android_classes-java_classes))
    print("associated methods:"+str(total_methods))
    print("---------------")

    ordered_counter = {k: v for k, v in sorted(class_counter.items(), key=lambda item: item[1])}

    filtered_print(2,100,[], ["okhttp3","retrofit","gson","eventbus","glide","moshi","lottie","leakcanary","timber","room","coil","rxjava"])
    
