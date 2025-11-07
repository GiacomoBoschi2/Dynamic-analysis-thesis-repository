from io import TextIOWrapper
import os


#TODO: improve javascript dumping and use python APIs,from Frida 17 Java bridge is no longer included by default, so use Frida < 17 or install manually via npm

#constants
folder = "./Loaded classes captures"
blacklist  =["android.","java.","org.json","sun.",".android",".java","javax"] #ignore classes that match these strings (not tpls)
whitelist = ["okhttp3","retrofit","gson","eventbus","glide","moshi","lottie","leakcanary","timber","room","coil","rxjava","dagger","fullstory"] # insert partial or full package tpl name
CLASS_PREFIX = "CLASS"
END_METHODS = "-"
START_METHODS = "METHODS"

#end output
class_frequencies = {}
match_frequency = {}
full_tree_frequency = {}
for cand in whitelist:
    match_frequency[cand] = 0


def scan_capture(file_name):
        whitelist_matches = []
        lines = []
        with open(file_name,"r") as reader:
            lines = reader.readlines()

        #skip to first class
        i = 0
        while not CLASS_PREFIX in lines[i]:
             i+=1
            
        while i< len(lines):
            if CLASS_PREFIX in lines[i]:
                valid = True
                name = lines[i].split(' ')[1].replace("\n","")
                for package in blacklist:
                    if package in name:
                        valid = False
                        break

                if valid:
                    for package in whitelist:
                        if package in name and not package in whitelist_matches:
                            whitelist_matches.append(package)
                            match_frequency[package]+=1
                            full_tree_frequency[package] = [name]
                            break
                        elif package in name:
                            full_tree_frequency[package].append(name)
                        
                    if name in class_frequencies.keys():
                        class_frequencies[name]+=1
                    else:
                        class_frequencies[name] = 1
            i+=1
        
        print(f"TPL candidates for {file_name}:"+str(whitelist_matches))
        print("----")
             

def print_by_whitelist(whitelist = whitelist):
    for key in class_frequencies.keys():
        for candidate in whitelist:
            if candidate.lower() in key.lower():
                print(key,class_frequencies[key])
                break
    
#prints filtering by number of instances
def print_by_frequency(min_freq=1,max_freq=1000):
    for key in class_frequencies.keys():
        if class_frequencies[key] >= min_freq and class_frequencies[key]<=max_freq:
            print(key,class_frequencies[key])


#prints absolute and relative frequency of TPL candidates
def print_candidates_frequency():
    total = sum(match_frequency.values())
    print("Total candidates found: "+ str(total))
    print("Absolute frequency:")
    print(match_frequency)
    perc = {}
    for key in match_frequency.keys():
        perc[key] = 100*(round(match_frequency[key]/total,2))
    print("Relative frequency:")
    print(perc)


if __name__ == "__main__":
    for capture in os.listdir(folder):
        if capture.endswith(".data"):
            file_path = os.path.join(folder, capture)
            scan_capture(file_path)

    print_by_whitelist()
    print_candidates_frequency()
        




