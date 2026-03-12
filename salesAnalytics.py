import numpy as np

sales = np.array([
    [1200, 1300, 1250, 1400, 1500, 1600, 1700, 1650, 1750, 1800, 1900, 2000],
    [800, 850, 900, 950, 1000, 1100, 1050, 1200, 1250, 1300, 1350, 1400],
    [1500, 1400, 1450, 1500, 1550, 1600, 1700, 1750, 1800, 1850, 1900, 1950],
    [500, 600, 550, 650, 700, 750, 800, 850, 900, 950, 1000, 1100],
    [2000, 2100, 2200, 2150, 2250, 2300, 2400, 2450, 2500, 2550, 2600, 2700]
])

products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

product_total_sales = np.sum(sales, axis=1)
print("Total Yearly Sales per Product:")
for i in range(len(products)):
    print(products[i], product_total_sales[i])

monthly_total_sales = np.sum(sales, axis=0)
print("\nMonthly Total Sales:")
for i in range(len(months)):
    print(months[i], monthly_total_sales[i])

best_product_index = np.argmax(product_total_sales)
print("\nBest Selling Product:", products[best_product_index])

best_month_index = np.argmax(monthly_total_sales)
print("Best Sales Month:", months[best_month_index])

mean_sales = np.mean(sales, axis=1)
print("\nMean Sales per Product:")
for i in range(len(products)):
    print(products[i], round(mean_sales[i],2))

std_sales = np.std(sales, axis=1)
print("\nStandard Deviation per Product:")
for i in range(len(products)):
    print(products[i], round(std_sales[i],2))

monthly_growth = np.diff(sales, axis=1)
growth_percentage = (monthly_growth / sales[:, :-1]) * 100
print("\nGrowth Percentage Between Months:")
print(np.round(growth_percentage,2))

declining_products = []
for i in range(sales.shape[0]):
    if np.any(np.diff(sales[i]) < 0):
        declining_products.append(products[i])

print("\nProducts with Declining Sales:")
if declining_products:
    for p in declining_products:
        print(p)
else:
    print("None")

top3_indices = np.argsort(monthly_total_sales)[-3:][::-1]
print("\nTop 3 Sales Months:")
for i in top3_indices:
    print(months[i], monthly_total_sales[i])

avg_growth = np.mean(np.diff(sales, axis=1), axis=1)
predicted_sales = sales[:, -1] + avg_growth

print("\nPredicted Sales for Next Month:")
for i in range(len(products)):
    print(products[i], int(predicted_sales[i]))