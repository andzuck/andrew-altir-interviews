# Andrew Zuckerman's solution for account balance interpolation problem
# May need to run `pip install requests` before running this solution
# Transaction 9 had the value pending="True". For this solution, I ignore the pending attribute.

import json
import requests
from datetime import datetime

# Load transaction data from lambda aws url

def load_transactions():
	lambda_transactions_url = 'https://jpvxtx67i7w2q5rlvcz5j5vjha0dqwkw.lambda-url.us-east-2.on.aws/'

	response = requests.get(lambda_transactions_url)

	if response.status_code == 200:
	    data = json.loads(response.content)
	    print('Transaction data retreived.')
	    return data
	else:
	    print('Error:' + str(response.status_code))
	    return []


# Sort transactions by date
def sort_transactions_by_date(data):
	data['transactions'] = sorted(data['transactions'], key = lambda x: x['date'], reverse = True)
	return data


# For every transaction, compute previous balance by subtracting transaction amount
# (assuming a positive transaction is a deposit)
def compute_historical_data(data):
	historical_balances = []
	current_balance = float(data['account']['balances']['current'])
	prev_balance = current_balance

	for t in data['transactions']:

		# Round amount to cents (2 decimals)
		amount = round(prev_balance - float(t['amount']), 2)
		prev_balance = amount

		# convert date '2023-06-26' to new format '06/26/23'
		date_str = t['date']
		datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
		new_date_str = datetime_obj.strftime('%m/%d/%y')

		historical_data_point = { "date": new_date_str, "balance": { "amount": amount, } }

		historical_balances.append(historical_data_point)

	return historical_balances


data = load_transactions()
# (if transactions are guaranteed to be sorted chronologically, can comment out this next line)
data = sort_transactions_by_date(data)
historical_balances = compute_historical_data(data)

# Write output to file
with open('historical_balances.json', 'w') as hb:
    json.dump(historical_balances, hb)


