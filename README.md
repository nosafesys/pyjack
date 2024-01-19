
# PyJack

PyJack is a Python script designed for checking if a link is broken, and thus hijackable.

It fetches web pages and searches for links within href attributes found in the source of the web page. 

Links are categorized as either internal och external. 
Internal links are relative paths or links with the domain of the target (this includes subdomains).
External links are links that point to other domains than that of the target.

By default PyJack checks all external links for broken ones but specifically identifies social links.

## Requirements

- Python 3
- Libraries: `requests`, `bs4 (BeautifulSoup)`, `urllib3`, `argparse`, `colorama`, `threading`

## Installation

1. Clone the repository or download the script.
2. Install the required libraries using pip:
   ```
   pip install requests beautifulsoup4 urllib3 argparse colorama
   ```

## Usage

To use PyJack, run the script from the command line with the following syntax:

```
python pyjack.py [options]
```

Options include:

- `url`: Specify the base URL to check.
- `-d`, `--depth`: Define the depth of the search.
- `-t`, `--threads`: Set the number of threads for concurrent checking of broken links.
- `-o`, `--timeout`: Set the timeout for each HTTP request.
- `--verify`: Enable or disable SSL/TLS verification.

For example:

```
python pyjack.py https://example.com -d 2 -t 10 --timeout 5 --verify
```

