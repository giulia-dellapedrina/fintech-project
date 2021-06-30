A Smart Contract Voting App
================================

Preliminary Steps
----------

**Ganache Installation**
>Install the **Ganache** and then open it, it will help you to create a local blockchain environment with some test nodes.




Simple Ballot
----------

**1.Compile Contract**
>Go to the **Remix IDE** (https://remix.ethereum.org/) and compile the **simple_ballot.sol**


**2.Deploy Contract**
>Change the Remix IDE environment to **Web3 Provider**  and enter the Ganache default server address:HTTP://127.0.0.1:7545, then you can find that the account addresses listed on Remix page correspond to the nodes in your Ganache local environment.   

>Next you can choose the **first** account in the list(which will then be the constructor of the contract, who has the right to assign vote to voters) to deploy the smart contract(need to pass the parameter---optionNames. For example,["a","b","c"]). 
>>Of course you can also select another account you prefer, but then you need to change the constructor address in **assign_vote_utils.py** accordingly(16th line of **assign_vote_utils.py**). For example you pick the 2nd account as your constructor,then you need to change the `w3.eth.accounts[0]` to `w3.eth.accounts[1]`.


**3.Obtain the address of deployed contract**
>Copy the address of the contract you just deployed(can be found in 'Deployed Contracts' on Remix)

**4.Assign Votes&Run App**
>Then you can run the flask app by entering following statements in your terminal:  
`python3 flask_simple_ballot.py 'addr'`  
Here the addr is the address you copied in step 3.

**5.Vote via browser**
>For those accounts which are assigned votes(accounts can be found either in Ganache or on Remix), they can login and vote via browser.



Two-Ways Ballot
----------

**1.Compile Contract**
>Go to the **Remix IDE** (https://remix.ethereum.org/) and compile the **two_ways_ballot.sol**

**2.Deploy Contract**
>Change the Remix IDE environment to **Web3 Provider**  and enter the Ganache default server address:HTTP://127.0.0.1:7545, then you can find that the account addresses listed on Remix page correspond to the nodes in your Ganache local environment.   

>Next you can choose the **first** account in the list(which will then be the constructor of the contract, who has the right to assign vote to voters) to deploy the smart contract.
>>when you deploy the contract, you will find you need to pass many parameters,including:  
>>1.**optionNames**,for example,["a","b","c"].  
>>2.**leaders**,the addresses of leaders.You can select some accounts from accounts list and copy their address,for example,["addr1","addr2","addr3"].The number of leaders must equal the number of options.
>>3.**points_per_voters**&**points_per_leaders**,points assigned to each voter and leader.

>>When you select the constructor to deploy the contract,you are free to choose any account in your list. but then you need to change the constructor address in **assign_vote_utils.py** accordingly(22th line of **assign_vote_utils.py**). For example you pick the 2nd account as your constructor,then you need to change the `w3.eth.accounts[0]` to `w3.eth.accounts[1]`.
  
**3.Obtain the address of deployed contract**
>Copy the address of the contract you just deployed(can be found in 'Deployed Contracts' on Remix)

**4.Assign Votes&Run App**
>Then you can run the flask app by entering following statements in your terminal:  
`python3 flask_two_ways_ballot.py 'addr'`  
Here the addr is the address you copied in step 3.
 
**5.Vote via browser**
>For those accounts which are assigned votes(accounts can be found either in Ganache or on Remix), they can login and vote via browser.

Privacy considerations
----------

**Simple Ballot**
In order to make it more difficult for people to know how individual voters have votes, we implemented a simple system using hashing function with a personal key. On the same page as the voting, the voter is asked to insert a personal key (5 digit long) which will then be used to hash their voting preferences before they are sent to the smart contract. In this way, their answers are hashed in a unique way based on the key they choose. The contract is set up so that what is stored in the voter variables is a hashed version of the option the voter has chosen, and only when points are assigned the key is used to find the options the voter has chosen. Although the assignment operation is public since the it done on the chain, the storing of hashed option chosen makes it more difficult to understand how an individual address has voted by inspecting the voter structure variables. 

We also considered implementing a more evolved approach, such as commit-reveal schemes which would keep all votes hidden until they are revealed, but could not since it went against the nature of the election. A solution like this would involve the voter having to submit information at two different points in time, first when they vote and also at the end of the voting session in order to reveal the votes. This would need a higher commitment from voters, as well as not allowing us to update the status in real time.

**Two Way Ballot**
In this case we did not implement the same privacy as before, since the pairs voting is public on the ballot status page graph.