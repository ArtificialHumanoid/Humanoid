# Issues, Pull Requests, and Commits
Issues and, of course, pull requests, are tracked via GitHub.  
Accordingly, all commit messages should be prefixed with “#” (followed by an issue or pull request numbered reference).

# `googlesearch`
googlesearch is a Python library for searching Google, easily. googlesearch uses requests and BeautifulSoup4 to scrape Google. 

## Installation
To install, run the following command:
```bash
python3 -m pip install googlesearch-python
```

## usage
To get results for a search term, simply use the search function in googlesearch. For example, to get results for "Google" in Google, just run the following program:
```python
from googlesearch import search
search("Google")
```

## Additional options
googlesearch supports a few additional options. By default, googlesearch returns 10 results. This can be changed. To get a 100 results on Google for example, run the following program.
```python
from googlesearch import search
search("Google", num_results=100)
```
In addition, you can change the language google searches in. For example, to get results in French run the following program:
```python
from googlesearch import search
search("Google", lang="fr")
```
## googlesearch.search
```python
googlesearch.search(term: str, num_results: int = 10, lang: str = "en") -> list
```

# `captcha_solver`

[![Run-Time Status](https://GitHub.Com/ArtificialHumanoid/Humanoid/actions/workflows/Tests.yml/badge.svg)](https://GitHub.Com/ArtificialHumanoid/Humanoid/actions/workflows/Tests.yml/badge.svg)
[![Lint Status](https://GitHub.Com/ArtificialHumanoid/Humanoid/actions/workflows/Linters.yml/badge.svg)]((https://GitHub.Com/ArtificialHumanoid/Humanoid/actions/workflows/Linters.yml/badge.svg))
[![Documentation Status](https://readthedocs.org/projects/Humanoid/badge/?version=latest)](https://Humanoid.readthedocs.org)

Univeral API to work with captcha solving services.

## Installation

Run: `pip install -U captcha-solver`

## Twocaptcha Backend Example

Service website is https://2captcha.com

```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('twocaptcha', api_key='2captcha.com API HERE')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```

## Rucaptcha Backend Example

Service website is https://rucaptcha.com

```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('rucaptcha', api_key='RUCAPTCHA_KEY')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```

## Browser Backend Example
```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('browser')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```

## Antigate Backend Example

Service website is http://getcaptchasolution.com

```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('antigate', api_key='ANTIGATE_KEY')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```
