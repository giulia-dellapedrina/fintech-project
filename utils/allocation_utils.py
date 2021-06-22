import json
import pandas as pd

def define_groups(d):
    
    voters = set([key[0] for key in d.keys()])
    teams = set([key[1] for key in d.keys()])
    print("There are", len(teams), "candidates and", len(voters), "applicants")
    return teams, voters


def sort_dictionary(d):
    
    sorted_dict = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))     
    return sorted_dict

def split_names(string, separator):
    
    if len(string.split(separator))>2:
        print('Invalid assignment due to name glitch')
        pass  
    else:
        a = string.split(separator)[0]
        b = string.split(separator)[1]
    
    return a, b

    
def organize_input_dict(d):    
    
    final_dict = {} 
    for key, value in d.items():
        a, b = split_names(key, '-')
        new_k = (a, b)
        
        # Extract Scorings
        score_a = value[str(a)+str(2)+str(b)]
        score_b = value[str(b)+str(2)+str(a)]
        score_sum = score_a + score_b
        
        # Assign Scorings to a list for the given tuple in the final dict
        final_dict[new_k] = [score_a, score_b, score_sum]
        
    df = pd.DataFrame.from_dict(final_dict, orient='index',
                       columns=['voter2team', 'team2voter', 'sum'])
    
    return final_dict, final_df
    

def run_assignment(data, team_limit, assignment_method):
    '''returns groups based on sum of preferences and selects alphabthical order if score is equal'''

    final_d, final_df = organize_input_dict(data)
    
    # Define assignment method
    if assignment_method == 'simple':
        sorted_df = final_df.sort_values(by=['sum'], ascending=False)
    elif assignment_method == 'team_priority':
        sorted_df = final_df.sort_values(by=['sum', 'team2voter'], ascending=False)
    elif assignment_method == 'voter_priority':
        sorted_df = final_df.sort_values(by=['sum', 'voter2team'], ascending=False)
    else:
        print('Assignment method not given or not mapped!')
    
    sorted_dict = sorted_df.to_dict('index')
    
    teams, voters = define_groups(final_d)
    assignments = {k: [] for k in teams}
    assigned = []
    for key, value in sorted_dict.items():
        team = key[1]
        voter = key[0]

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
