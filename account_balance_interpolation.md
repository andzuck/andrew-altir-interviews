# Account Balance Interpolation

Altir maintains historical account balances for all bank accounts on its platform. However, Plaid, our banking API provider, only returns a given account's balance at the time transactions are fetched. 

As such, it's important for us to be able to determine an account's historical bank balances given:
 
 1. Its current balance
 2. A list of transactions.

The task at hand is to write code that calls our mocked version of Plaid's API ([lambda URL](https://jpvxtx67i7w2q5rlvcz5j5vjha0dqwkw.lambda-url.us-east-2.on.aws/)), computes the end-of-day balance for all days between the first and last returned transaction, and writes the result to a JSON file.

Please fork this repository, implement the described functionality in the language of your choice, and email us both your code and the resulting JSON file. Your code should be readable, modular, and performant.

Your output should match the following format:
```
[
    {
        "date": "05/10/23",
        "balance": {
            "amount": 100,
        }
    },
    {
        "date": "05/09/23",
        "balance": {
            "amount": 100,
        }
    },
    ...
]
```