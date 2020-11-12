# predicting-stockmarket-s-p500

Algorithm to predict s&amp;p500 using Linear Regression

Each row in the file contains a daily record of the price of the S&P500 Index from 1950 to 2015. The dataset is stored in sphist.csv.

The columns of the dataset are:

Date -- The date of the record.
Open -- The opening price of the day (when trading starts).
High -- The highest trade price during the day.
Low -- The lowest trade price during the day.
Close -- The closing price for the day (when trading is finished).
Volume -- The number of shares traded.
Adj Close -- The daily closing price, adjusted retroactively to include any corporate actions.


We'll be using this dataset to develop a predictive model. We will train the model with data from 1950-2012, and try to make predictions from 2013-2015.

We have to convert the Date column to a Pandas date type. This will allow us to do date comparisons with the column.

Datasets taken from the stock market need to be handled differently than datasets from other sectors when it comes time to make predictions. In a normal machine learning exercise, we treat each row as independent. Stock market data is sequential, and each observation comes a day after the previous observation. Thus, the observations are not all independent, and you can't treat them as such.

This means we have to be extra careful to not inject "future" knowledge into past rows when we do training and prediction. Injecting future knowledge will make our model look good when we're training and testing it, but will make it fail in the real world. This is how many algorithmic traders lose money.

The time series nature of the data means that can generate indicators to make our model more accurate. For instance, we can create a new column that contains the average price of the last 10 trades for each row. This will incorporate information from multiple prior rows into one, and will make predictions much more accurate.

When we do this, we have to be careful not to use the current row in the values we average. We want to teach the model how to predict the current price from historical prices. If we include the current price in the prices you average, it will be equivalent to handing the answers to the model upfront, and will make it impossible to use in the "real world", where you don't know the price upfront.

Here are some indicators that are interesting to generate for each row:

The average price from the past 5 days.
The average price for the past 30 days.
The average price for the past 365 days.
The ratio between the average price for the past 5 days, and the average price for the past 365 days.
The standard deviation of the price over the past 5 days.
The standard deviation of the price over the past 365 days.
The ratio between the standard deviation for the past 5 days, and the standard deviation for the past 365 days.

"Days" means "trading days" -- so if you're computing the average of the past 5 days, it should be the 5 most recent dates before the current one. Assume that "price" means the Close column. We have to be careful not to include the current price in these indicators! We're predicting the next day price, so our indicators are designed to predict the current price from the previous prices.

Some of these indicators require a year of historical data to compute. Our first day of data falls on 1950-01-03, so the first day we can start computing indicators on is 1951-01-03.

To compute indicators, you'll need to loop through each day from 1951-01-03 to 2015-12-07 (the last day you have prices for). For instance, if we were computing the average price from the past 5 days, we'd start at 1951-01-03, get the prices for each day from 1950-12-26 to 1951-01-02, and find the average. The reason why we start on the 26th, and take more than 5 calendar days into account is because the stock market is shutdown on certain holidays. Since we're looking at the past 5 trading days, we need to look at more than 5 calendar days to find them.

Since you're computing indicators that use historical data, there are some rows where there isn't enough historical data to generate them. Some of the indicators use 365 days of historical data, and the dataset starts on 1950-01-03. Thus, any rows that fall before 1951-01-03 don't have enough historical data to compute all the indicators. We'll need to remove these rows before you split the data.

We will use Mean Absolute Error, as an error metric, because it will show you how "close" we were to the price in intuitive terms. Mean Squared Error, is an alternative that is more commonly used, but makes it harder to intuitively tell how far off you are from the true price because it squares the error.

Future Iterations - 

We can improve the error of this model significantly by adding some more indicators.

The average volume over the past five days.
The average volume over the past year.
The ratio between the average volume for the past five days, and the average volume for the past year.
The standard deviation of the average volume over the past five days.
The standard deviation of the average volume over the past year.
The ratio between the standard deviation of the average volume for the past five days, and the standard deviation of the average volume for the past year.
The year component of the date.
The ratio between the lowest price in the past year and the current price.
The ratio between the highest price in the past year and the current price.
The month component of the date.
The day of week.
The day component of the date.
The number of holidays in the prior month.

We can also make significant structural improvements to the algorithm, and pull in data from other sources.

Accuracy would improve greatly by making predictions only one day ahead. For example, train a model using data from 1951-01-03 to 2013-01-02, make predictions for 2013-01-03, and then train another model using data from 1951-01-03 to 2013-01-03, make predictions for 2013-01-04, and so on. This more closely simulates what you'd do if you were trading using the algorithm.

We can also incorporate outside data, such as the weather in New York City.

We can also make the system real-time by writing an automated script to download the latest data when the market closes, and make predictions for the next day.





