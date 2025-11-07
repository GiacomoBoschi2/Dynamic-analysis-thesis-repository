#Counts user-agents, amount of requests and Content-type
#To run this you need:
#A target folder (check main)
#A set of folders,one per target application, each containing the traffic data .txt file of the target application obtained from MobSF.


import os
user_agents = {}
content_types = {}
total_requests = 0

def scan_user_agents(traffic):
    with open(traffic,"r") as f:
        lines = f.readlines()
    
    for l in lines:
        if "user-agent:" in l.lower():
            agent = l.split(':')[1]
            if agent in user_agents.keys():
                user_agents[agent]+=1
            else:
                user_agents[agent] = 1

def count_requests(traffic):
    global total_requests
    with open(traffic,"r") as f:
        lines = f.readlines()
    
    for l in lines:
        if "REQUEST\n"==l:
            total_requests+=1

def scan_content_type(traffic):
    with open(traffic,"r") as f:
        lines = f.readlines()

    valid = False

    for l in lines:
        if "REQUEST\n"==l:
            valid = True
            continue

        if "content-type:" in l.lower() and valid:
            typec = l.split(':')[1]
            if ";" in typec: #ignores potential charsects specifications
                typec = typec.split(';')[0]
            typec = typec.replace('\n','')
            if typec in content_types.keys():
                content_types[typec]+=1
            else:
                content_types[typec] = 1
            valid = False


if __name__ == "__main__":
    target_folder = "./Applications data"
    subfolders = [x[0] for x in os.walk(target_folder)][1:]
    for subfolder in subfolders:
        traffic_file = os.path.join(subfolder,"traffic.txt")
        if os.path.exists(traffic_file):
            scan_user_agents(traffic_file)
            count_requests(traffic_file)
            scan_content_type(traffic_file)
        else:
            continue

    #print data
    print("-"*80)
    print(f"Extracted a total of : {total_requests} HTTP traffic requests")
    print("-"*80+"\n")

    print("-"*80)
    print(f"Content type statistics:")
    print("-"*80+"\n")

    contents_sorted = {k: v for k, v in sorted(content_types.items(), key=lambda item: item[1],reverse=True)}
    print(content_types)
    total_by_dict = 0
    for key in contents_sorted:
        print(f"{key.replace('\n','')}--> {content_types[key]} requests ({100*(round(content_types[key]/total_requests,2))}% of total)")
        total_by_dict += content_types[key]
    print(f"missing:{total_requests-total_by_dict} ({100*(round((total_requests-total_by_dict)/total_requests,2))}% of total)")

    print("-"*80)
    print(f"User agents found:")
    print("-"*80+"\n")

    agents_sorted = list(user_agents.keys())
    agents_sorted.sort()
    for key in agents_sorted:
        print(f"{key.replace('\n','')}--> {user_agents[key]} requests")


    