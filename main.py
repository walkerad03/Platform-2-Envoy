import pandas as pd
import sys

crm_import = pd.read_excel(io=sys.argv[1])

envoy_import = pd.DataFrame()

envoy_import["First Name"] = crm_import["First Name"]
envoy_import["Last Name"] = crm_import["Last Name"]
envoy_import["Middle Initial"] = crm_import["Middle Name"].fillna('').astype(str).str[0]
envoy_import["Suffix"] = crm_import["Suffix"]
envoy_import["Mailing Name"] = crm_import["Salutation"]
envoy_import["Email"] = crm_import["Email"]
envoy_import["Phone Number"] = crm_import["Mobile"]
envoy_import["Second Phone Number"] = crm_import["Phone"]
envoy_import["Address 1"] = crm_import["Address1"]
envoy_import["Address 2"] = crm_import["Address2"]
envoy_import["City"] = crm_import["City"]
envoy_import["State"] = crm_import["State"]
envoy_import["Zip Code"] = crm_import["Zip"]
envoy_import["Birth Month"] = crm_import["Birthday"].str.extract(r'-(\d{2})-', expand=False)
envoy_import["Birth Day"] = crm_import["Birthday"].str.extract(r'-(\d{2})$', expand=False)
envoy_import["Anniversary"] = pd.to_datetime(crm_import["Closing Anniversary"], format='').dt.strftime('%m/%d/%Y')
envoy_import["Pronouns"] = crm_import["Pronouns"]
envoy_import["FON"] = crm_import["Custom Farm: FON"]

# Farms

envoy_import["Rank"] = crm_import["Rank"]
envoy_import["Notes"] = crm_import["Contact Description"]

envoy_import.to_csv("output.csv")
