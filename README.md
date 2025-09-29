# pubchem-smiles-retriever
Python script to fetch SMILES strings from PubChem API for chemical compounds.
# PubChem SMILES Retriever

A Python script to fetch SMILES strings for chemical compounds from the PubChem API. Handles batch processing, errors, and saves results to CSV—great for cheminformatics workflows.

## Quick Demo
Run the script and it processes a list of compounds, printing progress and saving `compound_smiles.csv`.

## Setup
1. Clone this repo: `git clone https://github.com/INA101/pubchem-smiles-retriever.git`
2. Install deps: `pip install requests pandas`
3. Run: `python pubchem_smiles.py`

## Features
- API queries with delays to respect rate limits.
- Error handling for bad names or network issues.
- Optional: Load compounds from a text file.
- Outputs: DataFrame + CSV with name, SMILES, and status.

## Example Output
| Compound_Name | SMILES                  | Status |
|---------------|-------------------------|--------|
| mesitylene   | CC1=C(C=C(C=C1)C)C     | Found  |
| oleic acid   | CCCCCCCCC=CCCCCCCCC(=O)O | Found |

Built with Python 3. Questions? Open an issue!

## License
MIT License—feel free to use or fork.
