# Search Noise Generator

Lightweight Python utility that generates "search noise" by repeatedly performing (or simulating) web searches. It can perform simple DuckDuckGo HTML queries (when `requests` is available) or run in fully simulated mode to generate harmless, repeatable query traffic for testing, demos, or privacy experiments.

- Status: simple single-file script
- Language: Python
- Intended use: testing, demoing, or generating synthetic "search" activity for development and experimentation
- Warning: do not use to abuse or spam public search engines — respect rate limits and terms of service.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Options / Flags](#options--flags)
- [Terms file format](#terms-file-format)
- [Examples](#examples)
- [Notes / Troubleshooting](#notes--troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features
- Repeatedly issue searches (real HTML DuckDuckGo queries) or simulate search results locally.
- Several run modes: once, fixed count, or forever.
- Configurable delay and results-per-search.
- Uses built-in list of default search terms or loads a one-term-per-line file.

## Requirements
- Python 3.8+
- Optional: requests (to perform real DuckDuckGo HTML searches)
  - If requests is not installed, the script falls back to simulated results automatically.

## Installation
1. Clone or download the script into a working folder.
2. (Optional) Install requests to enable real web queries:
   - pip install requests

No other dependencies are required.

## Usage
Run the script with Python:
```bash
python search_noise.py [OPTIONS]
```

Basic modes:
- once — run a single search and exit
- count — run a fixed number of searches (use `--count N`)
- forever — run until interrupted

The script prints a live counter of searches performed and summarizes the total when it exits.

## Options / Flags
- --mode {once,count,forever} (default: forever)  
  Repeat mode: run once, for a count, or indefinitely.
- --count N (default: 10)  
  Number of searches when `--mode count` is used.
- --delay FLOAT (default: 2.0)  
  Seconds to wait between searches.
- --results INT (default: 5)  
  Number of results to fetch per search.
- --real-search (flag, default: on when requests is available)  
  If requests is installed this flag attempts to perform real DuckDuckGo HTML searches; otherwise the script simulates results.
- --terms-file PATH  
  Path to a plaintext file with one search term per line. If omitted the built-in list is used.

## Terms file format
If you supply `--terms-file path/to/file.txt` the file must contain one search term per line. Blank lines are ignored. Example:
```
weather today
pasta recipes
python tutorial
```
If the file cannot be read the script logs an error and falls back to the built-in default list.

## Examples
Run indefinitely (default) using simulation (when requests not installed):
```bash
python search_noise.py --mode forever --delay 1.5 --results 3
```

Run 20 searches with a 0.5s delay:
```bash
python search_noise.py --mode count --count 20 --delay 0.5 --results 5
```

Run a single search:
```bash
python search_noise.py --mode once --results 10
```

Use a custom terms file:
```bash
python search_noise.py --terms-file my_terms.txt --mode count --count 50
```

Enable real DuckDuckGo HTML requests (requires requests installed):
```bash
pip install requests
python search_noise.py --mode count --count 10 --real-search
```
