"""
This module contains a function to convert a Pl@tform export file to
Envoy format using pandas.

The module requires the following dependency:
- `pandas`

Author: Walker Davis
Date: June 22, 2023
"""

import pandas as pd


def convert_to_envoy(filename: str, output_filename: str) -> None:
    """
    Converts an Excel file to Envoy format and saves it as a CSV file.

    Parameters
    ----------
    filename : str
        The path to the Excel file to be converted.
    output_filename : str
        The desired name for the output CSV file.

    Returns
    -------
    None

    Notes
    -----
    - The function reads the Excel file using pandas and performs the
        necessary transformations to convert it to Envoy format.
    - The resulting DataFrame is then saved as a CSV file with the
        specified output filename.
    """
    crm_import = pd.read_excel(io=filename)

    envoy_import = pd.DataFrame()

    envoy_import["First Name"] = crm_import["First Name"]
    envoy_import["Last Name"] = crm_import["Last Name"]
    envoy_import["Middle Initial"] = crm_import["Middle Name"].fillna('').astype(str).str[0]
    envoy_import["Suffix"] = crm_import["Suffix"]
    envoy_import["Mailing Name"] = crm_import["Salutation"]
    envoy_import["Email"] = crm_import["Email"]
    envoy_import["Phone Number"] = crm_import["Mobile"].astype("Int64")
    envoy_import["Second Phone Number"] = crm_import["Phone"].astype("Int64")
    envoy_import["Address 1"] = crm_import["Address1"]
    envoy_import["Address 2"] = crm_import["Address2"]
    envoy_import["City"] = crm_import["City"]
    envoy_import["State"] = crm_import["State"]
    envoy_import["Zip Code"] = crm_import["Zip"]
    envoy_import["Birth Month"] = crm_import["Birthday"].fillna('').str.extract(r'-(\d{2})-', expand=False)
    envoy_import["Birth Day"] = crm_import["Birthday"].fillna('').str.extract(r'-(\d{2})$', expand=False)
    envoy_import["Anniversary"] = pd.to_datetime(crm_import["Closing Anniversary"]).dt.strftime('%m/%d/%Y')
    envoy_import["Pronouns"] = crm_import["Pronouns"]
    envoy_import["FON"] = crm_import["Custom Farm: FON"]

    custom_farm_cols = [col for col in crm_import.columns if 'Custom Farm:' in col]

    for index, row in crm_import.iterrows():
        farms = []
        for col in custom_farm_cols:
            if row[col] == 'X':
                farm_name = col.replace('Custom Farm: ', '')
                if farm_name == "FON":
                    continue
                farms.append(farm_name)

        envoy_import.at[index, 'Farms'] = ';'.join(farms)

    envoy_import["Rank"] = crm_import["Rank"]
    envoy_import["Notes"] = crm_import["Contact Description"]

    envoy_import.to_csv(f"{output_filename}", index=False)

    return output_filename
