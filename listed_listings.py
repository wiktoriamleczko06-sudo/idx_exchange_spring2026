# IMPORTING MY FILES INTO

import os
os.chdir("/Users/wiktoriamleczko/Downloads/idx_exchange")

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

# Number of Rows BEFORE FILTER = 591416

listed_res_proptype = listed_df[listed_df["PropertyType"] == "Residential"]

# Number of Rows AFTER FILTER = 397427