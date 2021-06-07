import json

def check_input(file):
    
    if file.endswith('.txt'):
        d = {}
        with open(file) as f:
            for line in f:
                (key, val) = line.split()
                d[key] = val
        return d
    
    elif file.endswith('.json'):
        with open(file) as f:
            d = json.load(f)
        return d
    
    else:
        print(file, "has an unknown file format")

        
def define_groups(d):
    
    teams = set([key.split('_')[0] for key in d.keys()])
    voters = set([key.split('_')[1] for key in d.keys()])
    print("There are", len(teams), "candidates and", len(voters), "applicants")
    return teams, voters


def easy_assignment():
    # returns groups based on sum of preferences and selcets random people for assignment if equal
    return 


def normal_assignment():
    # returns groups based on sum of preferences and prioritizes candidates when equal. If equal again then random
    return 

def complex_assignment():
    # returns groups based overall satisfaction optimization
    return 