from ass_vote import Ass_vote
from flask import Flask,render_template,request,redirect,send_from_directory
from web3 import Web3
import json
import time
import os
import sys

contract_addr=sys.argv[1]
w3,vote_contract=Ass_vote(contract_addr) #this line of code can only run once(vote assignment to the same address can only happen once!)

vote_app=Flask(__name__)

@vote_app.route('/')
def welcome():
    return render_template('content.html')

@vote_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(vote_app.root_path,'static'),'favicon.ico')

@vote_app.route('/<filename>')
def ballot_status(filename):
    num_options=vote_contract.functions.num_options().call()
    status_data=[vote_contract.functions.Options(i).call() for i in range(num_options)]
    # with open('static/data/ballot_status.json','w') as f:
    #     json.dump(status_data,f)
    return render_template(filename,update=status_data)

@vote_app.route('/<filename>',methods=['POST','GET'])
def login(filename):

    if request.method=='GET':
       return render_template(filename,error_message='')
    #POST
    addr=request.form.get('Address')

    #all authorized voters' addresses
    num_voters=vote_contract.functions.num_voters().call()
    authorized_addrs=[vote_contract.functions.Valid_voter_address(i).call() for i in range(num_voters)]
    
    if addr not in authorized_addrs:
        return render_template(filename,error_message='You have no right to vote!')
    else:
        current_voter=vote_contract.functions.voters(addr).call()
        if current_voter[1]==True:
            return render_template(filename,error_message='You have already voted!')
        elif time.time()>vote_contract.functions.deadline().call():
            return render_template(filename,error_message='The ballout is over!')
        else:
            redirect_addr='/vote/'+addr
            return redirect(redirect_addr)

@vote_app.route('/vote/<addr>',methods=['POST','GET'])
def vote(addr):
    num_options=vote_contract.functions.num_options().call()
    status_data=[vote_contract.functions.Options(i).call() for i in range(num_options)]
    if request.method=='GET':
        return render_template('vote.html',data=status_data,error_message='')
    #receive post
    vote_info={} 
    for i,(opt,_) in enumerate(status_data):
        point=request.form.get(opt)
        if point:
            if not point.isdigit():
                return render_template('vote.html',data=status_data,error_message='Wrong input type,Only integers are accepted!')
            elif int(point)>0:
                vote_info[i]=int(point)
    
    option_idx=list(map(lambda x:int(x),vote_info.keys()))
    point_allocation=list(vote_info.values())

 
    voter_info=vote_contract.functions.voters(addr).call()
    num_points_given=voter_info[0]
    if sum(point_allocation)!=num_points_given:
        return render_template('vote.html',data=status_data,error_message='You have {} points totally!'.format(num_points_given))
    else:
        vote_yet=voter_info[1]
        if vote_yet:
            return render_template('vote.html',data=status_data,error_message='You have already voted!')
        vote_contract.functions.Vote(option_idx=option_idx,point_allocation=point_allocation).\
            transact(transaction={"from":addr})
        
        return render_template('vote_done.html')

if __name__=='__main__':
    vote_app.run()  
    
    
    


    
    
    
    
    
    
