# -- Week 1 --

import os
os.chdir("/Users/wiktoriamleczko/Downloads/idxexchange")

import os
print(os.getcwd())

import pandas as pd

listed_transaction_files = ["CRMLSListing202401.csv", "CRMLSListing202402.csv", "CRMLSListing202403.csv", 
                            "CRMLSListing202404.csv", "CRMLSListing202405.csv", "CRMLSListing202406.csv", 
                            "CRMLSListing202407.csv", "CRMLSListing202408.csv", "CRMLSListing202409.csv", 
                            "CRMLSListing202410.csv", "CRMLSListing202411.csv", "CRMLSListing202412.csv", 
                            "CRMLSListing202501.csv", "CRMLSListing202502.csv", "CRMLSListing202503.csv", 
                            "CRMLSListing202504.csv", "CRMLSListing202505.csv", "CRMLSListing202506.csv", 
                            "CRMLSListing202507.csv", "CRMLSListing202508.csv", "CRMLSListing202509.csv",
                            "CRMLSListing202510.csv", "CRMLSListing202511.csv", "CRMLSListing202512.csv", 
                            "CRMLSListing202601.csv", "CRMLSListing202602.csv", "CRMLSListing202603.csv"]
    
#Contrating all monthly MLS files

listed_df = pd.concat([pd.read_csv(f) for f in listed_transaction_files])


# -- Week 2 --

# Unique Property Types Analysis
print("\nUnique Property Types:")
print(listed_df["PropertyType"].unique())

print(listed_df["PropertyType"].value_counts(normalize=True) * 100)

percentages = listed_df["PropertyType"].value_counts(normalize=True)

# Creating a Pie Chart for Property Type Distribution
import matplotlib.pyplot as plt

plt.figure()
percentages.plot(kind="pie", autopct='%1.1f%%')
plt.title("Listed Property Type Distribution (%)")
plt.ylabel("")
plt.show()

# Number of Rows BEFORE FILTER = 591416

listed_df= listed_df[listed_df["PropertyType"] == "Residential"]

# Number of Rows AFTER FILTER = 397427

# Structure Inspection 
print(listed_df.shape)      # rows, columns 
print(listed_df.columns)    # column names
listed_df.info()            # data types and counts

# Missing Value Analysis
listed_nulls = listed_df.isnull().sum()
listed_null_percent = (listed_nulls / len(listed_df)) * 100

listed_null_report = pd.DataFrame({
    'Column': listed_df.columns,
    'Missing Count': listed_nulls.values,
    'Percent Missing': listed_null_percent.values
})

print("\nMissing Value Report (Listed):")
print(listed_null_report.sort_values(by='Percent Missing', ascending=False))

# Columns with >90% missing
listed_high_missing = listed_null_report[listed_null_report['Percent Missing'] > 90]

print("Columns with >90% missing:")
print(listed_high_missing)

# Numeric Summary 
listed_numeric_cols = ["ClosePrice", "ListPrice", "OriginalListPrice", "LivingArea", "LotSizeAcres",
                       "BedroomsTotal", "BathroomsTotalInteger", "DaysOnMarket", "YearBuilt"]

listed_summary = listed_df[listed_numeric_cols].describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99])

print("Numeric Distribution Summary (LISTED)")
print(listed_summary)

for col in listed_numeric_cols:

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

# Create a matching year_month key on the MLS datasets: Listings dataset — key off ListingContractDate
listed_df['year_month'] = pd.to_datetime(listed_df['ListingContractDate']).dt.to_period('M')


# Merge datasets 
listings_with_rates = listed_df.merge(mortgage_monthly, on='year_month', how='left')

#  Validation of the the merge
print(listings_with_rates['rate_30yr_fixed'].isnull().sum())

#Preview Dataset 
print(listing_with_rates[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']].head())

