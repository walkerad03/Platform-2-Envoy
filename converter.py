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
    crm_import = pd.read_excel(io=filename, dtype=str)
    crm_import = crm_import.replace('nan', '')

    print(f"Converting {filename}")

    envoy_import = pd.DataFrame()

    def _direct_copy(source_col: str, target_col: str) -> None:
        if source_col in crm_import.columns:
            envoy_import[target_col] = crm_import[source_col]

            if isinstance(envoy_import[target_col], str):
                envoy_import[target_col].str.rstrip()
        else:
            print(f"Column not found: {source_col}")

    _direct_copy("First Name", "First Name")
    _direct_copy("Last Name", "Last Name")

    if "Middle Name" in crm_import.columns:
        envoy_import["Middle Initial"] = crm_import["Middle Name"].fillna('').astype(str).str[0]

    _direct_copy("Suffix", "Suffix")
    _direct_copy("Salutation", "Mailing Name")
    _direct_copy("Email", "Email")
    _direct_copy("Mobile", "Phone Number")
    _direct_copy("Phone", "Second Phone Number")
    _direct_copy("Address1", "Address 1")
    _direct_copy("Address2", "Address 2")
    _direct_copy("City", "City")
    _direct_copy("State", "State")
    _direct_copy("Zip", "Zip Code")

    if "Birthday" in crm_import.columns:
        envoy_import["Birth Month"] = crm_import["Birthday"].fillna('').str.extract(r'-(\d{2})-', expand=False)
        envoy_import["Birth Day"] = crm_import["Birthday"].fillna('').str.extract(r'-(\d{2})$', expand=False)

    _direct_copy("Closing Anniversary", "Anniversary")
    _direct_copy("Pronouns", "Pronouns")
    _direct_copy("Custom Farm: FON", "FON")

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

    _direct_copy("Rank", "Rank")
    _direct_copy("Notes", "Contact Description")

    init_row_count = envoy_import.shape[0]
    # Drop columns where agent is listed as co-op agent.
    if ("Agent" in crm_import.columns):
        envoy_import = envoy_import.drop(crm_import[crm_import.Agent == "X"].index)

    postop_row_count = envoy_import.shape[0]
    print(f"Rows removed: {init_row_count - postop_row_count}")

    envoy_import.to_csv(output_filename, index=False)

    return output_filename
