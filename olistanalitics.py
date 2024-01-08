# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 13:09:16 2024

@author: REMLEX
"""

# It use to access directory and manipulating directory
import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('C:/Users/REMLEX/Desktop/Python course/Data/Ecommerce Orders Project')

#  Check your working directory
print(os.getcwd())

# =============================================================================
# Loading Files
# =============================================================================

# Load the orders data
orders_data = pd.read_excel('orders.xlsx')

# Load the payment data
payments_data = pd.read_excel('order_payment.xlsx')

# Load the customer data
# If it is csv file you will use pd.read_csv('filename.csv)
customers_data = pd.read_excel('customers.xlsx')


# =============================================================================
# Describing the data
# =============================================================================
orders_data.info()
payments_data.info()
customers_data.info()

# =============================================================================
# Handling missing data
# =============================================================================
# Check for missing data in orders data
orders_data.isnull().sum()
payments_data.isnull().sum()
customers_data.isnull().sum()

# Filling in the missing values in orders data with a default value
orders_data = orders_data.fillna('N/A')
# Check if there are null value in orders_data2
orders_data.isnull().sum()

# Drop rows with missing values in payment datavalue
payments_data = payments_data.dropna()
# Check if there are null value in payment_data2
payments_data.isnull().sum()
payments_data.info()


# =============================================================================
# Remove Duplicate in data analytics
# =============================================================================
# Check for duplicate in our orders data
orders_data.duplicated().sum()

# Remove duplicate from orders data
orders_data = orders_data.drop_duplicates()
orders_data.duplicated().sum()

# Check for duplicate in our payments data
payments_data.duplicated().sum()

# Remove duplicate from orders data
payments_data = payments_data.drop_duplicates()


# Check for duplicate in our customers data
customers_data.duplicated().sum()


# =============================================================================
# Filtering the Data
# =============================================================================
# Select a subset of the orders data based on the order status
invoiced_orders_data = orders_data[orders_data['order_status'] == 'invoiced']
# Reset the index
invoiced_orders_data = invoiced_orders_data.reset_index(drop=True)


# Select a subset of the payments data where payment type = Credite Card and payment vlaue > 1000
credit_card_payment = payments_data[
    (payments_data['payment_type'] == 'credit_card') & 
    (payments_data['payment_value'] > 1000)
    ]


# Select a subset of customer based on customer state = SP
customers_data.info()
customers_data_state = customers_data[customers_data['customer_state'] == 'SP']


# =============================================================================
# Merging and Joining Different Dataframe
# =============================================================================

# Merge orders data with payment data on order_id column
merged_data = pd.merge(orders_data, payments_data, on='order_id')

# Join the merged data with our customers data on the customer_id column
joined_data = pd.merge(merged_data, customers_data, on='customer_id')


# If there is error install "pip install matplotlib and pip install seaborn"
# =============================================================================
# Data Visualization
# =============================================================================

# Create a field called comth_year from order_purchase_timestamp
joined_data['month_year'] = joined_data['order_purchase_timestamp'].dt.to_period('M')
joined_data['week_year'] = joined_data['order_purchase_timestamp'].dt.to_period('W')
joined_data['year'] = joined_data['order_purchase_timestamp'].dt.to_period('Y')


grouped_data = joined_data.groupby('month_year')['payment_value'].sum()
grouped_data = grouped_data.reset_index()

# Convert month_year from Period into String
grouped_data['month_year'] = grouped_data['month_year'].astype(str)

grouped_data.info()

# Creating a plot
# Note: X-axis is month_year while Y-axis payment_value
# plt.plot(x, y)
plt.plot(grouped_data['month_year'], grouped_data['payment_value'], color='red', marker='o')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month and Year')
plt.ylabel('Payment Value')
plt.title('Payment Value by Month and Year')
plt.xticks(rotation = 90, fontsize=8)
plt.yticks(fontsize=8)

# =============================================================================
# Exporting Data
# =============================================================================
# Exporting Data
joined_data.to_excel('payment_value_by_month_year.xlsx', index=False)
grouped_data.to_excel('grouped_data_by_month_year.xlsx', index=False)


# Scatter Plot
# =============================================================================
# Aggregate payment_value and payment_installments by customer
# =============================================================================

# Create the DataFrame
scatter_df = joined_data.groupby('customer_unique_id').agg({'payment_value': 'sum', 'payment_installments': 'sum'})

plt.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Value Vs Installments by Customers')
plt.show()

# =============================================================================
# Using Seaborn to create scatter plot
# =============================================================================

sns.set_theme(style='darkgrid') #darkgrid, whitegrid, dark white
sns.scatterplot(data=scatter_df, x='payment_value', y='payment_installments')
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Value Vs Installments by Customers')
plt.show()


# =============================================================================
# Creating a bar chart
# =============================================================================

# Group two column payment_type and month_year Aggregate by payment_value
bar_chart_df = joined_data.groupby(['payment_type', 'month_year'])['payment_value'].sum()  # Aggregate by payment_value
bar_chart_df = bar_chart_df.reset_index()

pivot_data = bar_chart_df.pivot(index='month_year', columns='payment_type', values='payment_value')

pivot_data.plot(kind='bar', stacked='True')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month of Payment')
plt.ylabel('Payment Value')
plt.title('Payment per Payment Type by Month')


# =============================================================================
# Creating a Box Plot
# =============================================================================
payment_values = joined_data['payment_value']
payment_types = joined_data['payment_type']

# Creating a separate box plot per payment type
plt.boxplot([ payment_values[payment_types == 'credit_card'],
              payment_values[payment_types == 'boleto'],
              payment_values[payment_types == 'voucher'],
              payment_values[payment_types == 'debit_card']],
              labels = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
          )

plt.xlabel('Payment Type')
plt.ylabel('Payment Value')
plt.title('Box Plot showing Payment Value ranges by Payment Type')

plt.tight_layout()
plt.show()

# joined_data.info()

# =============================================================================
# Creating a subplot (3 plot in one)
# =============================================================================
# Creating a subplot (3 plot in one)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10,10))

# ax1 which is boxplot
ax1.boxplot([ payment_values[payment_types == 'credit_card'],
              payment_values[payment_types == 'boleto'],
              payment_values[payment_types == 'voucher'],
              payment_values[payment_types == 'debit_card']],
              labels = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
          )
ax1.set_xlabel('Payment Type')
ax1.set_ylabel('Payment Value')
ax1.set_title('Box Plot showing Payment Value ranges by Payment Type')


# ax2 which is stack bar chart
pivot_data.plot(kind='bar', stacked='True', ax=ax2)
ax2.ticklabel_format(useOffset=False, style='plain', axis='y')
# Set label and title
ax2.set_xlabel('Month of Payment')
ax2.set_ylabel('Payment Value')
ax2.set_title('Payment per Payment Type by Month')


# ax3 which is Scatter chart
ax3.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
# Set label and title
ax3.set_xlabel('Payment Value')
ax3.set_ylabel('Payment Installments')
ax3.set_title('Payment Value Vs Installments by Customers')

fig.tight_layout()

plt.savefig('my_plot.png')











