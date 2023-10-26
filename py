import yfinance as yf
import pandas as pd
import numpy as np

# Define the list of stock tickers
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'GS', 'IBM', 'CVX', 'XOM', 'BA', 'LMT', 'DIS', 'NFLX', 'CSCO', 'INTC', 'NVDA', 'QCOM', 'AMAT', 'ADBE', 'CRM', 'ORCL', 'WMT', 'HD', 'NKE', 'SBUX', 'MCD', 'KO', 'PEP', 'JNJ', 'PFE', 'MRK', 'ABBV', 'T', 'VZ', 'CMCSA', 'TMUS', 'C', 'BAC', 'WFC', 'GS', 'BRK-B', 'UNH', 'CVS', 'CI', 'HUM', 'UNH', 'WBA', 'FDX', 'UPS', 'GLW', 'AAP', 'MMM', 'CAT', 'DE', 'BA', 'MELI', 'EBAY', 'AMZN', 'WMT', 'COST', 'TGT', 'HD', 'LOW', 'TJX', 'RL', 'GPS', 'LUV', 'AAL', 'DAL', 'UAL', 'GILD', 'AMGN', 'BIIB', 'REGN', 'AAPL', 'MSFT', 'GOOGL', 'META', 'SNAP', 'NFLX', 'DIS', 'CMCSA', 'T', 'VZ', 'TSLA', 'GM', 'F', 'CVS', 'WBA', 'CVS', 'RAD', 'KR', 'COST']

# Fetch stock data for the specified tickers
stock_data = yf.download(tickers, start="2023-01-01", end="2023-12-31")

# Calculate the correlation matrix
correlation_matrix = stock_data['Adj Close'].corr()

# Find pairs with a correlation coefficient over 0.9
high_correlation_pairs = []

for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        if correlation_matrix.iloc[i, j] > 0.9:
            high_correlation_pairs.append((correlation_matrix.columns[i], correlation_matrix.columns[j]))

if not high_correlation_pairs:
    print("No pairs with correlation over 0.9 found.")
else:
    print("Pairs with correlation over 0.9:")
    for pair in high_correlation_pairs:
        print(f"{pair[0]} and {pair[1]}")

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Define the pair of stocks and date range
stock_a_symbol = 'AAL'
stock_b_symbol = 'UAL'
start_date = '2015-01-01'
end_date = '2023-12-31'


# Fetch historical stock data
data = yf.download([stock_a_symbol, stock_b_symbol], start=start_date, end=end_date)['Adj Close']

# Calculate the spread between the two stocks
data['Spread'] = data[stock_a_symbol] - data[stock_b_symbol]

# Calculate the z-score of the spread (standardized distance from the mean)
data['Z-Score'] = (data['Spread'] - data['Spread'].mean()) / data['Spread'].std()

# Define entry and exit thresholds
entry_threshold = 1.0  # The z-score at which to enter the trade
exit_threshold = 0.0   # The z-score at which to exit the trade

# Initialize positions
position_a = 0
position_b = 0

# Lists to track trade signals and positions
trade_signals = []
positions = []

# Simulate the trading strategy
for index, row in data.iterrows():
    if row['Z-Score'] > entry_threshold:
        position_a = -1
        position_b = 1
        trade_signals.append("Short A, Long B")
    elif row['Z-Score'] < -entry_threshold:
        position_a = 1
        position_b = -1
        trade_signals.append("Short B, Long A")
    elif abs(row['Z-Score']) < exit_threshold:
        position_a = 0
        position_b = 0
        trade_signals.append("Exit")

    positions.append((position_a, position_b))

# Create a list of placeholders for trade signals
trade_signals = ['No Trade'] * len(data)

# Create a list of placeholders for trade signals
trade_signals = ['No Trade'] * len(data)

# Modify the trade signals only for data points where a signal is generated
for i in range(len(data)):
    row = data.iloc[i]  # Access the row by index
    if row['Z-Score'] > entry_threshold:
        position_a = -1
        position_b = 1
        trade_signals[i] = "Short A, Long B"
    elif row['Z-Score'] < -entry_threshold:
        position_a = 1
        position_b = -1
        trade_signals[i] = "Short B, Long A"
    elif abs(row['Z-Score']) < exit_threshold:
        position_a = 0
        position_b = 0
        trade_signals[i] = "Exit"

# Add the trade_signals list to the DataFrame
data['Trade_Signal'] = trade_signals
data['Position'] = positions



# Print the first few rows of the data
print(data.head())

# Visualize the spread and trading signals
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Spread'], label='Spread', color='blue')
plt.xlabel('Date')
plt.ylabel('Spread')
plt.title('Pairs Trading Spread')
for idx, row in data.iterrows():
    if row['Trade_Signal'] == "Short A, Long B":
        plt.axvline(x=idx, color='red', linestyle='--')
    elif row['Trade_Signal'] == "Short B, Long A":
        plt.axvline(x=idx, color='green', linestyle='--')
plt.legend(loc='best')
plt.show()

# Calculate daily returns
data['Returns_A'] = data[stock_a_symbol].pct_change()
data['Returns_B'] = data[stock_b_symbol].pct_change()

# Define initial capital (starting portfolio value)
initial_capital = 100000  # Adjust this value as needed

# Create lists to track portfolio values and returns for pairs trading
portfolio_values_pairs = [initial_capital]
portfolio_returns_pairs = [0.0]

# Create lists to track portfolio values and returns for the "Hold Equal A and B" strategy
portfolio_values_equal = [initial_capital]
portfolio_returns_equal = [0.0]

# Simulate the portfolio value and returns for both strategies
for i in range(1, len(data)):
    previous_portfolio_value_pairs = portfolio_values_pairs[-1]
    previous_portfolio_value_equal = portfolio_values_equal[-1]

    returns_a = data['Returns_A'].iloc[i]
    returns_b = data['Returns_B'].iloc[i]

    # Calculate portfolio returns based on positions in Stock A and Stock B for the pairs trading strategy
    portfolio_returns_pairs.append(positions[i-1][0] * returns_a + positions[i-1][1] * returns_b)

    # Calculate portfolio value for the pairs trading strategy
    portfolio_value_pairs = previous_portfolio_value_pairs + previous_portfolio_value_pairs * portfolio_returns_pairs[-1]
    portfolio_values_pairs.append(portfolio_value_pairs)

    # Calculate portfolio returns for the "Hold Equal A and B" strategy
    portfolio_returns_equal.append(0.5 * returns_a + 0.5 * returns_b)

    # Calculate portfolio value for the "Hold Equal A and B" strategy
    portfolio_value_equal = previous_portfolio_value_equal + previous_portfolio_value_equal * portfolio_returns_equal[-1]
    portfolio_values_equal.append(portfolio_value_equal)

# Calculate cumulative returns for both strategies
cumulative_returns_pairs = np.cumsum(portfolio_returns_pairs)
cumulative_returns_equal = np.cumsum(portfolio_returns_equal)

# Plot cumulative returns for both strategies
plt.figure(figsize=(12, 6))
plt.plot(data.index, cumulative_returns_pairs, label='Pairs Trading', color='blue')
plt.plot(data.index, cumulative_returns_equal, label='Hold Equal A and B', color='green')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.title('Pairs Trading vs. Hold Equal A and B Cumulative Returns')
plt.legend(loc='best')
plt.show()

# Calculate the spread between the two stocks
data['Spread'] = data[stock_a_symbol] - data[stock_b_symbol]

# Calculate the historical average of the spread
historical_average = data['Spread'].mean()

# Create a list of historical averages with the same length as the data
historical_average_values = [historical_average] * len(data)

# Plot the spread and historical average
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Spread'], label='Spread', color='blue')
plt.plot(data.index, historical_average_values, label='Historical Average', color='red', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Spread')
plt.title('Pairs Trading Spread with Historical Average')
plt.legend(loc='best')
plt.show()

# Calculate the spread between the two stocks
data['Spread'] = data[stock_a_symbol] - data[stock_b_symbol]

# Calculate the historical mean and standard deviation of the spread
historical_mean = data['Spread'].mean()
historical_std = data['Spread'].std()

# Calculate the Z-score of the spread
data['Z-Score'] = (data['Spread'] - historical_mean) / historical_std

# Plot the Z-score
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Z-Score'], label='Z-Score', color='purple')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.axhline(1, color='red', linestyle='--', linewidth=1, label='Z-Score = 1')
plt.axhline(-1, color='green', linestyle='--', linewidth=1, label='Z-Score = -1')
plt.xlabel('Date')
plt.ylabel('Z-Score')
plt.title('Pairs Trading Z-Score')
plt.legend(loc='best')
plt.show()
