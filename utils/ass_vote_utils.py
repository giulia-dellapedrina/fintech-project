from web3 import Web3
import json
import sys
from flask import Flask

def one_way_ass_vote(addr): #addr means the address of smart contract
    w3=Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545")) 
    with open('utils/abi/one_way_abi.json','r') as f:
        abi=json.load(f)
    vote_contract=w3.eth.contract(address=addr,abi=abi)
    
    '''
    Here I just set number of voters and amount assigned to each voter both equal 5,you are free to change them.
    But notice that the num_voters should not exceed the number of node in Ganache test environment!!!
    
    '''
    num_voters=5
    amount_per_voter = 5
    print('Start assigning votes...')
    for i in range(1,num_voters+1):
        vote_contract.functions.Give_right_to_voters(w3.eth.accounts[i],amount_per_voter).transact(transaction={'from':w3.eth.accounts[0]})#here i use the first address-->w3.eth.accounts[0] as the contract constructor 
    print('Assignment Done!')
    return w3,vote_contract


def two_ways_ass_vote(addr):
    w3=Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545")) 
    with open('utils/abi/two_ways_abi.json','r') as f:
        abi=json.load(f)
    sorting_contract=w3.eth.contract(address=addr,abi=abi)
    
    '''
    When I deploy the contract, I choose the first account as the contract constructor--->w3.eth.accounts[0],
    and initalize 3 options with 3 leaders --->w3.eth.accounts[1],w3.eth.accounts[2],w3.eth.accounts[3]
   
    So I set the voters from 4th account,here I simply set 5 voters, you are free to choose more voters, but be attention not to exceed the number of nodes in Ganache test
    environment...
    '''
    num_voters=5
    names=['a','b','c','d','e'] #simple example
    print('Start assigning votes to voters...')
    for i in range(4,num_voters+4):
        sorting_contract.functions.Give_right_to_voters(w3.eth.accounts[i],names[i-4]).transact(transaction={'from':w3.eth.accounts[0]})
    print('Assignment Done!')
    return w3,sorting_contract