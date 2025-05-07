import pickle

filename = "stocks_db.pkl"

with open(filename, "rb") as f:
    data = pickle.load(f)

# Display structure
for stock in data:
    print(f"Symbol: {stock['symbol']}, Shares: {stock['shares']}")
    for entry in stock['history'][:5]:  # Show first 5 daily records
        print(f"  Date: {entry[0]}, Close: {entry[1]}, Volume: {entry[2]}")
