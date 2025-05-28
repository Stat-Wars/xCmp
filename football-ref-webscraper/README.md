# Web Scraping Tools for [Pro-Football-Reference](https://www.pro-football-reference.com)

This repository contains tools to scrape NFL statistics from [Pro-Football-Reference](https://www.pro-football-reference.com).  
Requires **Python 3.11+**.

## Installation

Install dependencies via `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Advanced Passing Tables

Advanced passing data is only available for 2018 and later. Tables are saved to a csv in the ```./tables/adv_passing``` directory.

Usage:

```bash
python adv_pass.py -y <year> 
```

Args:
| Argument     | Type   | Default         | Description                                       |
|--------------|--------|-----------------|---------------------------------------------------|
| `--year, -y` | `int`  | `2024`          | The NFL season to scrape data for                 |