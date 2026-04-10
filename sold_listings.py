# IMPORTING MY FILES INTO

import os
os.chdir("/Users/wiktoriamleczko/Downloads/idx_exchange")

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

# Number of Rows BEFORE FILTER = 853946

sold_res_proptype = sold_df[sold_df["PropertyType"] == "Residential"]

# Number of Rows AFTER FILTER = 540734