// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8;
contract Ballot{
    
    struct Voter{
        uint voter_points; // totally z points
        bool voted; // whether or not voted
        address voter_addr; // address of voter
        bytes32[] proposal_idx; //voted to which proposal
    }
    struct Option{
        string name; //name of optionq
        uint count; //number of accumulated votes
    }
    uint256 public deadline; //deadline of the voting
    address public chairperson; //promoter
    mapping(address=>Voter) public voters; //voters
    Option[] public Options; //array to store options with their current voted condition
    address[] public Valid_voter_address; //separately store all the addresses of authorized voters

    uint public num_options=0; //record the number of options
    uint public num_voters=0; //record the number of voters

    //create new ballot
    constructor(string[] memory optionNames){
        chairperson=msg.sender; 
        //initial setting of Options
        for (uint i=0;i<optionNames.length;i++){
            Options.push(Option({name:optionNames[i],count:0}));
            num_options++;
        }
        
        deadline=block.timestamp+24*60*60; //once the voters have votes, the countdown starts, voters have to accomplish voting within one day.

    }

    function Give_right_to_voters(address voter,uint points) public{
        require(msg.sender==chairperson); //must done by chairperson
        require(!voters[voter].voted); 
        require(voters[voter].voter_points==0); 
        voters[voter].voter_points=points; //give voter z points for this new ballot
        voters[voter].voter_addr=voter;

        Valid_voter_address.push(voter); //store the address
        num_voters++;

       
        }
    
    //do not use any state variable, so can be resitricted to pure
    function Sum(uint[] memory point_allocation) public pure returns(uint){
        uint sum=0;
        for (uint i=0;i<point_allocation.length;i++){
            sum+=point_allocation[i];
            }
        return sum;
    }
    
    function Vote(bytes32[] memory option_idx,uint[] memory point_allocation,uint256 key) public{
        //option_idx: voter's decision about to choose which options
        //point_allocation: how to allocation the N points to above options
        
        Voter storage v=voters[msg.sender]; // voter object
        require(block.timestamp<deadline,"Voting has finished!");//should vote before deadline
        
        //check whether the option_idx beyond the max possible option idx
        require(Sum(point_allocation)==v.voter_points,"Sum of your votes you have not equal to the sum of your votes allocated!"); 
        //the sum of voter's point allocation must equal points assigned to him/her
        require(!v.voted,"You have already voted!"); 
        v.voted=true;
        //v.voter_addr=msg.sender;
        v.proposal_idx=option_idx;
        

        for(uint256 j=0;j<num_options;j++){
            bytes32 hash;
            hash = keccak256(abi.encodePacked(j,key));
            for(uint i=0;i<option_idx.length;i++){
                if (option_idx[i] == hash){
                    Options[j].count+=point_allocation[i];
                }
        }   }
        
    }

}