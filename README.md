
# PyJack

PyJack is a Python script designed for checking and validating links on websites. It utilizes multithreading and various Python libraries to efficiently scan a website and report broken or invalid links.

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

- `-u`, `--url`: Specify the base URL to check.
- `-d`, `--depth`: Define the depth of the link check.
- `-t`, `--threads`: Set the number of threads for concurrent checking.
- `--timeout`: Set the timeout for link checking.
- `--verify`: Enable or disable SSL verification.

For example:

```
python pyjack.py -u https://example.com -d 2 -t 10 --timeout 5 --verify
```

