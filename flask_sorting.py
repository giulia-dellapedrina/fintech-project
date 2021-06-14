from ass_vote2 import Ass_vote
from flask import Flask,render_template,request,redirect,send_from_directory
from collections import defaultdict
from web3 import Web3
import json
import time
import os
import sys

contract_addr=sys.argv[1]
w3,sorting_contract=Ass_vote(contract_addr) 

vote_app2=Flask(__name__,static_folder='static',template_folder='templates2')

@vote_app2.route('/')
def welcome():
    return render_template('content.html')

@vote_app2.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(vote_app2.root_path,'static'),'favicon.ico')

@vote_app2.route('/ballot_status.html')
def ballot_status():
    #voter_info
    num_voters=sorting_contract.functions.num_voters().call()
    voter_addrs=[sorting_contract.functions.Valid_voter_address(i).call() for i in range(num_voters)]
    voter_names=[sorting_contract.functions.voters(addr).call()[2] for addr in voter_addrs]
    #option_info
    num_options=sorting_contract.functions.num_options().call()
    options=[sorting_contract.functions.Options(i).call() for i in range(num_options)]

    res=defaultdict(dict)
    for name in voter_names:
        for option in options:
            res[name+'-'+option]['voter2option']=sorting_contract.functions.voter_option_match(name,option).call()[1]
            res[name+'-'+option]['option2voter']=sorting_contract.functions.option_voter_match(option,name).call()[1]
   
    res_list=[[k,sum(v.values())] for k,v in res.items()]
    return render_template('ballot_status.html',data=res_list)
    
@vote_app2.route('/login.html',methods=['POST','GET'])
def login():
    if request.method=='GET':
       return render_template('login.html',error_message='')
    #POST
    tp=request.form.get('type')
    if not tp:
        return render_template('login.html',error_message='Please select your identity first!')
    else:
        addr=request.form.get('Address')
        #voter
        if tp=='voter':
            #all authorized voters' addresses
            num_voters=sorting_contract.functions.num_voters().call()
            authorized_addrs=[sorting_contract.functions.Valid_voter_address(i).call() for i in range(num_voters)]
            
            if addr not in authorized_addrs:
                return render_template('login.html',error_message='You have no right to vote!')
            else:
                current_voter=sorting_contract.functions.voters(addr).call()
                if current_voter[1]==True:
                    return render_template('login.html',error_message='You have already voted!')
                elif time.time()>sorting_contract.functions.deadline().call():
                    return render_template('login.html',error_message='The ballout is over!')
                else:
                    redirect_addr='/voter/'+addr
                    return redirect(redirect_addr)
        #leader
        num_leaders=sorting_contract.functions.num_options().call()
        leaders=[sorting_contract.functions.leader_address(i).call() for i in range(num_leaders)]
        if addr not in leaders:
            return render_template('login.html',error_message='You are not legal leader!')
        else:
            current_leader=sorting_contract.functions.Leaders(addr).call()
            if current_leader[2]==True:
                    return render_template('login.html',error_message='You have already voted!')
            elif time.time()>sorting_contract.functions.deadline().call():
                    return render_template('login.html',error_message='The ballout is over!')
            else:
                redirect_addr='/leader/'+addr
                return redirect(redirect_addr)


@vote_app2.route('/voter/<addr>',methods=['POST','GET'])
def voter_vote(addr):
    num_options=sorting_contract.functions.num_options().call()
    option_names=[sorting_contract.functions.Options(i).call() for i in range(num_options)]

    if request.method=='GET':
        return render_template('voter_vote.html',data=option_names,error_message='')
    #receive post
    vote_info={} 
    for opt in option_names:
        point=request.form.get(opt)
        if point:
            if not point.isdigit():
                return render_template('voter_vote.html',data=option_names,error_message='Wrong input type,Only integers are accepted!')
            elif int(point)>0:
                vote_info[opt]=int(point)
    
    option_names,point_allocation=list(vote_info.keys()),list(vote_info.values())
    
    voter_info=sorting_contract.functions.voters(addr).call()
    num_points_given=voter_info[0]
    if sum(point_allocation)!=num_points_given:
        return render_template('voter_vote.html',data=option_names,error_message='You have {} points totally!'.format(num_points_given))
    else:
        vote_yet=voter_info[1]
        if vote_yet:
            return render_template('voter_vote.html',data=option_names,error_message='You have already voted!')
        sorting_contract.functions.Vote(option_names=option_names,point_allocation=point_allocation).\
            transact(transaction={"from":addr})
        
        return render_template('vote_done.html')

@vote_app2.route('/leader/<addr>',methods=['POST','GET'])
def leader_vote(addr):
    #leader_info
    leader_info=sorting_contract.functions.Leaders(addr).call()
    
    #voter_addrs
    voter_count=sorting_contract.functions.num_voters().call()
    voter_addrs=[sorting_contract.functions.Valid_voter_address(i).call() for i in range(voter_count)]

    name2addr={} #name-->address
    for addr in voter_addrs:
        name=sorting_contract.functions.voters(addr).call()[2]
        name2addr[name]=addr
    
    if request.method=='GET':
        return render_template('leader_vote.html',data=list(name2addr.keys()),error_message='')
    vote_info={} #name-->point
    for name in list(name2addr.keys()):
        point=request.form.get(name)
        if point:
            if not point.isdigit():
                return render_template('leader_vote.html',data=list(name2addr.keys()),error_message='Wrong input type,Only integers are accepted!')
            elif int(point)>0:
                vote_info[name]=int(point)

    addr_list=[] #voter address list
    point_assign_list=[]
    for k,v in vote_info.items():
        addr_list.append(name2addr[k])
        point_assign_list.append(v)
    
    num_points_given=leader_info[1]
    if sum(point_assign_list)!=num_points_given:
        return render_template('leader_vote.html',data=list(name2addr.keys()),error_message='You have {} points totally!'.format(num_points_given))
    else:
        assign_yet=leader_info[2]
        if assign_yet:
            return render_template('leader_vote.html',data=list(name2addr.keys()),error_message='You have already assigned!')
        sorting_contract.functions.Vote_leader(addr_list,point_assign_list).transact(transaction={'from':leader_info[3]})
        
        return render_template('vote_done.html')
    
if __name__=='__main__':
    vote_app2.run()
