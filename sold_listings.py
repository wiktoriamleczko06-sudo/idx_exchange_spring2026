# -- Week 1 --

import os
os.chdir("/Users/wiktoriamleczko/Downloads/idxexchange")

import os
print(os.getcwd())

import pandas as pd

sold_transaction_files = ["CRMLSSold202401.csv", "CRMLSSold202402.csv", "CRMLSSold202403.csv", 
                            "CRMLSSold202404.csv", "CRMLSSold202405.csv", "CRMLSSold202406.csv", 
                            "CRMLSSold202407.csv", "CRMLSSold202408.csv", "CRMLSSold202409.csv", 
                            "CRMLSSold202410.csv", "CRMLSSold202411.csv", "CRMLSSold202412.csv", 
                            "CRMLSSold202501.csv", "CRMLSSold202502.csv", "CRMLSSold202503.csv", 
                            "CRMLSSold202504.csv", "CRMLSSold202505.csv", "CRMLSSold202506.csv", 
                            "CRMLSSold202507.csv", "CRMLSSold202508.csv", "CRMLSSold202509.csv",
                            "CRMLSSold202510.csv", "CRMLSSold202511.csv", "CRMLSSold202512.csv", 
                            "CRMLSSold202601.csv", "CRMLSSold202602.csv", "CRMLSSold202603.csv"]
    
#Contrating all monthly MLS files

sold_df = pd.concat([pd.read_csv(f) for f in sold_transaction_files])


# -- Week 2 --

# Unique Property Types Analysis
print("\nUnique Property Types:")
print(sold_df["PropertyType"].unique())

print(sold_df["PropertyType"].value_counts(normalize=True) * 100)

percentages = sold_df["PropertyType"].value_counts(normalize=True)

# Creating a Pie Chart for Property Type Distribution
import matplotlib.pyplot as plt

plt.figure()
percentages.plot(kind="pie", autopct='%1.1f%%')
plt.title("Sold Property Type Distribution (%)")
plt.ylabel("")
plt.show()

# Number of Rows BEFORE FILTER = 591416

sold_df= sold_df[sold_df["PropertyType"] == "Residential"]

# Number of Rows AFTER FILTER = 397427

# Structure Inspection 
print(sold_df.shape)      # rows, columns 
print(sold_df.columns)    # column names
sold_df.info()            # data types and counts

# Missing Value Analysis
sold_nulls = sold_df.isnull().sum()
sold_null_percent = (sold_nulls / len(sold_df)) * 100

sold_null_report = pd.DataFrame({
    'Column': sold_df.columns,
    'Missing Count': sold_nulls.values,
    'Percent Missing': sold_null_percent.values
})

print("\nMissing Value Report (Listed):")
print(sold_null_report.sort_values(by='Percent Missing', ascending=False))

# Columns with >90% missing
sold_high_missing = sold_null_report[sold_null_report['Percent Missing'] > 90]

print("Columns with >90% missing:")
print(sold_high_missing)

# Numeric Summary 
sold_numeric_cols = ["ClosePrice", "ListPrice", "OriginalListPrice", "LivingArea", "LotSizeAcres",
                       "BedroomsTotal", "BathroomsTotalInteger", "DaysOnMarket", "YearBuilt"]

sold_summary = sold_df[sold_numeric_cols].describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99])

print("Numeric Distribution Summary (LISTED)")
print(sold_summary)

for col in sold_numeric_cols:

    # Histograms
    plt.figure()
    listed_df[col].dropna().hist(bins=100)
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()

    # Boxplots
    plt.figure()
    listed_df.boxplot(column=col)
    plt.title(f"Boxplot of {col}")
    plt.show()
    

# -- Week 3 --

#Fetch the mortgage rate data from FRED
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

# Resample weekly rates to monthly averages
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed']
    .mean()
    .reset_index()
)

# Create a matching year_month key on the MLS datasets:Sold dataset — key off CloseDate
sold_df['year_month'] = pd.to_datetime(sold_df['CloseDate']).dt.to_period('M')


# Merge datasets 
sold_with_rates = sold_df.merge(mortgage_monthly, on='year_month', how='left')

#  Validation of the the merge
print(sold_with_rates['rate_30yr_fixed'].isnull().sum())

#Preview Dataset 
print(
sold_with_rates[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']].head())

