def define_groups(l, team_limit):
    
    teams = set([l[i][0].split('-')[1] for i in range(len(l))])
    voters = set([l[i][0].split('-')[0] for i in range(len(l))])
    print("There are", len(teams), "candidates and", len(voters), "applicants")
    l.sort(key = lambda x: x[1], reverse = True)
    print(l)
    teams_allocation = {k: [[],[]] for k in teams}
    print(teams_allocation)
    assigned = []
    
    for item in range(len(l)):
        
        team = l[item][0].split('-')[1]
        voter = l[item][0].split('-')[0]
        
        # Check if voter has already been assigned
        if voter in assigned: 
            print(voter, "has already been assigned to a team")

        # Check if team capacity has been reached
        elif len(teams_allocation[team][0]) >= team_limit:
            print(team, "has reached maximum capacity")

        # Assign voter to the team
        else:
            teams_allocation[team][0].append(voter)
            assigned.append(voter)
            teams_allocation[team][1] = len(teams_allocation[team][0])
    
   
    teams_allocation_list = list(map(list, teams_allocation.items()))
    return teams, voters, teams_allocation_list
