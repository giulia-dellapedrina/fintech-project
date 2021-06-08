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

def sort_dictionary(d):
    
    sorted_dict = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))     
    return sorted_dict

def easy_assignment(data, team_limit):
    '''returns groups based on sum of preferences and selects alphabthical order if score is equal'''

    sorted_dict = sort_dictionary(data)
    teams, voters = define_groups(data)
    assignments = {k: [] for k in teams}
    assigned = []
    for key, value in sorted_dict.items():
        team = key.split('_')[0]
        voter = key.split('_')[1]

        # Check if voter has already been assigned
        if voter in assigned: 
            print(voter, "has already been assigned to a team")

        # Check if team capacity has been reached
        elif len(assignments[team]) >= team_limit:
            print(team, "has reached maximum capacity")

        # Assign voter to the team
        else:
            assignments[team].append(voter)
            assigned.append(voter)
    
    return assignments


def normal_assignment():
    """ returns groups based on sum of preferences and prioritizes candidates when equal. If equal again then random """ 
    
    return 


def complex_assignment():
    """ returns groups based overall satisfaction optimization """
    
    return 