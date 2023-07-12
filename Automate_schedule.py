import pandas as pd
import numpy as np
import schedule
import time

def generate_report():
    # Read data from CSV file
    data = pd.read_csv('sales_data.csv')

    # Perform data analysis and generate report
    report = pd.DataFrame()

    # Example analysis: Total units sold by product color
    report['Total Units Sold'] = data.groupby('product_color')['units_sold'].sum()

    # Example analysis: Average rating by product variation size
    report['Average Rating'] = data.groupby('product_variation_size_id')['rating'].mean()

    # Example analysis: Total revenue by currency
    data['revenue'] = data['units_sold'] * data['price']
    report['Total Revenue'] = data.groupby('currency_buyer')['revenue'].sum()

    # Example analysis: Top merchants by rating
    top_merchants = data.groupby('merchant_name')['merchant_rating'].mean()
    report['Top Merchants'] = top_merchants.nlargest(5)

    # Example analysis: Items with the best top sales
    top_sales = data.nlargest(10, 'units_sold')[['title', 'units_sold']]
    report['Items with Top Sales'] = top_sales.set_index('title')['units_sold']

    # Recommendations to improve sales and widen profit margins
    recommendations = pd.DataFrame()
    recommendations['Item'] = data['title']
    recommendations['Recommendation'] = np.where(data['price'] > data['retail_price'], 'Lower the price to attract more customers.', 'Consider increasing the price to improve profit margins.')
    recommendations = recommendations.groupby('Item')['Recommendation'].apply(lambda x: ' '.join(x)).reset_index()
    report['Recommendations'] = recommendations.set_index('Item')['Recommendation']

    # Save report to CSV file
    report.to_csv('sales_report.csv')

    # Generate recommendations text file
    with open('recommendations.txt', 'w', encoding='utf-8') as file:
        file.write('Recommendations:\n\n')
        for item, recommendation in zip(recommendations['Item'], recommendations['Recommendation']):
            file.write(f'{item}: {recommendation}\n')

# Get user input for scheduling the report generation
schedule_time = input('Enter the time for scheduling the report generation (HH:MM format): ')

# Set the number of times the code will run
number_of_runs = 5

# Schedule the code to run
for i in range(number_of_runs):
    # Schedule the code to run every day at the specified time
    schedule.every().day.at(schedule_time).do(generate_report)
    
    # Delay the code execution for 24 hours
    time.sleep(86400)

    # Run the pending scheduled jobs
    schedule.run_pending()
