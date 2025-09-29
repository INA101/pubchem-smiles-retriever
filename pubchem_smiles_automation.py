"""
PubChem SMILES Fetcher

Retrieves canonical SMILES representations for chemical compounds using the PubChem API.
Supports batch processing and file input.
"""

import requests
import pandas as pd
import time
import urllib.parse
from typing import List, Dict, Optional


def get_smiles_from_pubchem(compound_name: str) -> Optional[str]:
    """
    Fetch the SMILES string for a chemical compound from PubChem using its name.

    Args:
        compound_name (str): Name of the compound (e.g., 'mesitylene').

    Returns:
        str or None: SMILES string if found, else None if an error occurs.
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name"
    try:
        encoded_name = urllib.parse.quote(compound_name)

        # Get Compound ID (CID) from PubChem
        cid_url = f"{base_url}/{encoded_name}/cids/JSON"
        response = requests.get(cid_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Note: PubChem returns the first matching CID, which may not always be
        # the desired compound if multiple matches exist
        cid = data['IdentifierList']['CID'][0]

        # Fetch SMILES using the CID
        smiles_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/CanonicalSMILES/JSON"
        response = requests.get(smiles_url, timeout=10)
        response.raise_for_status()
        smiles_data = response.json()

        # CanonicalSMILES is preferred over ConnectivitySMILES for standardization
        properties = smiles_data['PropertyTable']['Properties'][0]
        if 'CanonicalSMILES' in properties:
            smiles = properties['CanonicalSMILES']
        elif 'ConnectivitySMILES' in properties:
            smiles = properties['ConnectivitySMILES']
        else:
            print(f"No SMILES found for {compound_name}")
            return None
        return smiles

    except (requests.exceptions.RequestException, KeyError, IndexError) as e:
        print(f"Error fetching SMILES for {compound_name}: {e}")
        return None


def batch_get_smiles(compound_names: List[str], delay: float = 0.2) -> pd.DataFrame:
    """
    Process a list of compounds to fetch their SMILES strings and return a DataFrame.

    Args:
        compound_names (List[str]): List of compound names to process.
        delay (float): Seconds to wait between API calls (default 0.2s respects PubChem rate limits).

    Returns:
        pd.DataFrame: Table with compound names, SMILES, and status.
    """
    results = []
    print(f"Processing {len(compound_names)} compounds...")

    for i, compound_name in enumerate(compound_names, 1):
        print(f"Processing {i}/{len(compound_names)}: {compound_name}")
        smiles = get_smiles_from_pubchem(compound_name)
        results.append({
            'Compound_Name': compound_name,
            'SMILES': smiles,
            'Status': 'Found' if smiles else 'Not Found'
        })
        if i < len(compound_names):
            time.sleep(delay)

    return pd.DataFrame(results)


def process_compounds_from_file(filename: str) -> pd.DataFrame:
    """
    Read compound names from a file and fetch their SMILES strings.

    Args:
        filename (str): Path to text file with one compound name per line.

    Returns:
        pd.DataFrame: Table with results (same as batch_get_smiles).
    """
    try:
        with open(filename, 'r') as f:
            compound_names = [line.strip() for line in f if line.strip()]
        return batch_get_smiles(compound_names)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return pd.DataFrame()


if __name__ == "__main__":
    # Example compound list
    compound_names = [
        "mesitylene",
        "5-ethyl-2-methylheptane",
        "undecane",
        "methyl octanoate",
        "methyl tridecanoate",
        "undecanoic acid",
        "octyl 10-undecenoate",
        "methyl tetradecanoate",
        "capric acid",
        "pentadecyl pentanoate",
        "methyl 14-methylpentadecanoate",
        "hexadecanoic acid",
        "methyl linoleate",
        "methyl oleate",
        "methyl stearate",
        "oleic acid",
        "octadecanoic acid",
        "1-fluorodecane",
        "methyl icosanoate",
        "octadecanal",
        "9-octadecanone",
        "4-ethyl-1-octyn-3-ol"
    ]

    results_df = batch_get_smiles(compound_names)

    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)
    print(results_df.to_string(index=False))

    results_df.to_csv("compound_smiles.csv", index=False)
    print(f"\nResults saved to 'compound_smiles.csv'")

    found_count = len(results_df[results_df['Status'] == 'Found'])
    total_count = len(results_df)
    print(f"\nSummary: {found_count}/{total_count} compounds found")

    # Uncomment to process compounds from a file:
    # results_df = process_compounds_from_file("compound_list.txt")