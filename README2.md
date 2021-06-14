A more complex smart contract which allows option(project) leaders to vote for voters.
==

>Based on the simple voting app I bulit before, in which only voters can vote, now I add a new character leader who can also assign points, but to normal voters rather than their corresponding options/projects. The final points of ProjectA-Voter1 is the sum of the points Voter1 assigns for ProjectA and the points LeaderA assigns for Voter1.

Test Steps
---------
**0.Ganache Installation**
>Install the **Ganache** and then open it, it will help you to create a local blockchain environment with some test nodes.


**1.Compile Contract**
>Go to the **Remix IDE** (https://remix.ethereum.org/) and compile the **sorting.sol**


**2.Deploy Contract**
>Change the Remix IDE environment to **Web3 Provider**  and enter the Ganache default server address:HTTP://127.0.0.1:7545, then you can find that the account addresses listed on Remix page correspond to the nodes in your Ganache local environment.   

>Next you can choose the **first** account in the list(which will then be the constructor of the contract, who has the right to assign vote to voters) to deploy the smart contract.
>>when you deploy the contract, you will find you need to pass many parameters,including:  
>>1.**optionNames**,for example,["a","b","c"].  
>>2.**leaders**,the addresses of leaders.You can select some accounts from accounts list and copy their address,for example,["addr1","addr2","addr3"].The number of leaders must equal the number of options.
>>3.**points_per_voters**&**points_per_leaders**,points assigned to each voter and leader.

>>When you select the constructor to deploy the contract,you are free to choose any account in your list. but then you need to change the constructor address in **ass_vote.py** accordingly(22th line of **ass_vote.py**). For example you pick the 2nd account as your constructor,then you need to change the `w3.eth.accounts[0]` to `w3.eth.accounts[1]`.

  
**3.Obtain the address of deployed contract**
>Copy the address of the contract you just deployed(can be found in 'Deployed Contracts' on Remix)

**4.Assign Votes&Run App**
>Then you can run the flask app by entering following statements in your terminal:  
`python3 flask_sorting.py 'addr' `  
Here the addr is the address you copied in step 3.

 
**5.Vote via browser**
>For those accounts which are assigned votes(accounts can be found either in Ganache or on Remix), they can login and vote via browser.




