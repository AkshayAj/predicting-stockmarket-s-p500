import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

df = pd.read_csv('sphist.csv')

df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True)

df = df.sort_values(by='Date', ascending=True) 

# Create indicators
df["avg_5"] = df["Close"].rolling(5).mean().shift(1)
df["avg_30"] = df["Close"].rolling(30).mean().shift(1)
df["avg_365"] = df["Close"].rolling(365).mean().shift(1)
df["std_5"] = df["Close"].rolling(5).std().shift(1)
df["std_365"] = df["Close"].rolling(365).std().shift(1)

df["avg_5/avg_365"] = df["avg_5"]/df["avg_365"]
df["std_5/std_365"] = df["std_5"]/df["std_365"]

df = df[df["Date"] > datetime(year=1951, month=1, day=3)]

# df.dropna(axis=0, inplace=True)

# Create train and test dataframes
train = df[df["Date"] < datetime(year=2013, month=1, day=1)]
test = df[df["Date"] >= datetime(year=2013, month=1, day=1)]

lr = LinearRegression()
features = ["avg_5", "avg_30", "avg_365", "std_5", "std_365", "avg_5/avg_365", "std_5/std_365"]

lr.fit(train[features], train["Close"])

predictions = lr.predict(train[features])
test_predictions = lr.predict(test[features])

mae = mean_absolute_error(test_predictions, test["Close"])
mse = mean_squared_error(test_predictions, test["Close"])

print("MAE: ", mae)
print("MSE: ", mse)