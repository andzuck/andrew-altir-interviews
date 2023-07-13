# Andrew Zuckerman's solution for account balance interpolation problem
# May need to run `pip install requests` or `pip install datetime` before running this solution
# Transaction 9 had the value pending="True". For the solution, I ignored the pending attribute.

import json
import requests
from datetime import datetime, timedelta

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
	prev_balance = float(data['account']['balances']['current'])
	prev_date = datetime.strptime(data['transactions'][0]['date'], '%Y-%m-%d').strftime('%m/%d/%y')

	# Add first data point
	historical_data_point = { "date": prev_date, "balance": { "amount": prev_balance, } }
	historical_balances.append(historical_data_point)
	amount = round(prev_balance - float(data['transactions'][0]['amount']), 2)
	prev_balance = amount

	for i in range(1, len(data['transactions'])):

		t = data['transactions'][i]

		# Convert datetime object to new string format '06/26/23'
		date = datetime.strptime(t['date'], '%Y-%m-%d')

		# Round amount to cents (2 decimals)
		amount = round(prev_balance - float(t['amount']), 2)

		# While there are still transactions for the date we're keeping track of, keep determining end of day transactions
		if date == prev_date:
			prev_balance = amount
		# Otherwise, we've found a demarcation between days
		else:
			
			# We want to save the account balance for the day of this new date we're seeing			

			# Save datapoint
			historical_data_point = { "date": date.strftime('%m/%d/%y'), "balance": { "amount": prev_balance, } }
			historical_balances.append(historical_data_point)
			prev_date = date
			
			# For all days between our most recent datapoint and the one saved before that, add end-of-day balances
			n = len(historical_balances)
			while n > 1 and datetime.strptime(historical_balances[n - 1]['date'], '%m/%d/%y') != datetime.strptime(historical_balances[n - 2]['date'], '%m/%d/%y') - timedelta(days=1):
				date = date + timedelta(days=1)
				historical_balances.insert(n - 1, {"date": date.strftime('%m/%d/%y'), "balance": { "amount": prev_balance,}})

			prev_balance = amount

	# Add last data point with final end of day balance we know
	last_date = datetime.strptime(historical_balances[len(historical_balances) - 1]['date'], '%m/%d/%y')
	historical_data_point = { "date": (last_date - timedelta(days=1)).strftime('%m/%d/%y'), "balance": { "amount": prev_balance, } }
	historical_balances.append(historical_data_point)
	
	return historical_balances


data = load_transactions()
# (if transactions are guaranteed to be sorted chronologically, can comment out this next line)
data = sort_transactions_by_date(data)
historical_balances = compute_historical_data(data)

# Write output to file
with open('historical_balances.json', 'w') as hb:
    json.dump(historical_balances, hb)


