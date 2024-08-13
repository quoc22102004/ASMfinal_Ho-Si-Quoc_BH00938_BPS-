import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Load the data from text files
customer_data = pd.read_csv('Dữ liệu khách hàng + quốc gia.txt')
market_trend = pd.read_csv('Dữ liệu market trend.txt')
website_access = pd.read_csv('Dữ liệu truy cập website.txt')
product_data = pd.read_csv('Dữ liệu về sản phẩm và giá.txt')
transaction_data = pd.read_csv('transaction.txt')
category_data = pd.read_csv('Category.txt')

# Print column names to debug
print("Transaction Data Columns:", transaction_data.columns)
print("Market Trend Data Columns:", market_trend.columns)

# Ensure the column names are as expected
# Check for leading/trailing spaces or case differences
transaction_data.columns = transaction_data.columns.str.strip()
market_trend.columns = market_trend.columns.str.strip()

# Verify that 'ProductID' exists in both DataFrames
if 'ProductID' not in transaction_data.columns or 'ProductID' not in market_trend.columns:
    raise KeyError("Column 'ProductID' not found in one of the DataFrames")

# Merge transaction_data with market_trend to get the sales trend
sales_data = transaction_data.merge(market_trend, how='left', on='ProductID')

# Filter relevant columns and handle missing values
sales_data = sales_data[['SaleDate', 'SaleAmount']]
sales_data['SaleDate'] = pd.to_datetime(sales_data['SaleDate'])
sales_data = sales_data.groupby('SaleDate').agg({'SaleAmount': 'sum'}).reset_index()

# Create features based on the date
sales_data['Year'] = sales_data['SaleDate'].dt.year
sales_data['Month'] = sales_data['SaleDate'].dt.month
sales_data['Day'] = sales_data['SaleDate'].dt.day

# Drop the original SaleDate column
sales_data = sales_data.drop(columns=['SaleDate'])

# Prepare the features and target variable
X = sales_data[['Year', 'Month', 'Day']]
y = sales_data['SaleAmount']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse:.2f}')

# Predict Future Sales
# Generate future dates (e.g., next 3 months)
future_dates = [datetime.now() + timedelta(days=x) for x in range(1, 91)]
future_data = pd.DataFrame({
    'Year': [date.year for date in future_dates],
    'Month': [date.month for date in future_dates],
    'Day': [date.day for date in future_dates]
})

# Predict future sales
future_sales_predictions = model.predict(future_data)

# Add predictions to the DataFrame
future_data['PredictedSales'] = future_sales_predictions

# Print the future sales predictions
print(future_data.head())

# Plotting future sales predictions
plt.figure(figsize=(12, 6))
plt.plot(future_dates, future_sales_predictions, label='Predicted Sales', color='blue')
plt.title('Future Sales Predictions')
plt.xlabel('Date')
plt.ylabel('Predicted Sales Amount ($)')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('future_sales_predictions.png')
plt.show()