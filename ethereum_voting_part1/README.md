A simple Voting Smart Contract
================================

Test Steps
----------

**0.Ganache Installation**
>Install the **Ganache** and then open it, it will help you to create a local blockchain environment with some test nodes.


**1.Compile Contract**
>Go to the **Remix IDE** (https://remix.ethereum.org/) and compile the **vote.sol**


**2.Deploy Contract**
>Change the Remix IDE environment to **Web3 Provider**  and enter the Ganache default server address:HTTP://127.0.0.1:7545, then you can find that the account addresses listed on Remix page correspond to the nodes in your Ganache local environment.   

>Next you can choose the **first** account in the list(which will then be the constructor of the contract, who has the right to assign vote to voters) to deploy the smart contract(need to pass the parameter---optionNames. For example,["a","b","c"]). 
>>Of course you can also select another account you prefer, but then you need to change the constructor address in **ass_vote.py** accordingly(16th line of **ass_vote.py**). For example you pick the 2nd account as your constructor,then you need to change the `w3.eth.accounts[0]` to `w3.eth.accounts[1]`.

  
**3.Obtain the address of deployed contract**
>Copy the address of the contract you just deployed(can be found in 'Deployed Contracts' on Remix)

**4.Assign Votes&Run App**
>Then you can run the flask app by entering following statements in your terminal:  
`python3 flask_app.py 'addr' `  
Here the addr is the address you copied in step 3.

 
**5.Vote via browser**
>For those accounts which are assigned votes(accounts can be found either in Ganache or on Remix), they can login and vote via browser.



