# Installation
Run
```bash
pip install Humanoid
```

or, for the latest,

```bash
pip install git+https://github.com/ArtificialHumanoid/Humanoid.git#subdirectory=build
```
.

# Issues, Pull Requests, and Commits
Issues and, of course, pull requests, are tracked via GitHub.  
Accordingly, all commit messages should be prefixed with “#” (followed by an issue or pull request numbered reference).

# `googlesearch`
googlesearch is a Python library for searching Google, easily. googlesearch uses requests and BeautifulSoup4 to scrape Google.


## Usage
To get results for a search term, simply use the search function in googlesearch. For example, to get results for "Google" in Google, just run the following program:
```python
googlesearch.search("Google")
```

## Additional options
By default, `googlesearch` returns 10 results. 
To get a 100 results on Google, for example:
```python
googlesearch.search("Google", num_results=100)
```
In addition, you can change the language Google searches in.
For example, to get results in French run the following program:
```python
googlesearch.search("Google", lang="fr")
```
To extract more information, such as the description or the result URL, use an advanced search:
```python
googlesearch.search("Google", advanced=True)
```
which returns `List[SearchResult]` with each result having the properties
- title
- url
- description.

If requesting more than 100 results, googlesearch will send multiple requests to go through the pages.
To increase the time between these requests, use sleep_interval:
```python
googlesearch.search("Google", sleep_interval=5, num_results=200)
```

# `captcha_solver`

[![Run-Time Status](https://GitHub.Com/ArtificialHumanoid/Humanoid/actions/workflows/Tests.yml/badge.svg)](https://GitHub.Com/ArtificialHumanoid/Humanoid/actions/workflows/Tests.yml/badge.svg)
[![Lint Status](https://GitHub.Com/ArtificialHumanoid/Humanoid/actions/workflows/Linters.yml/badge.svg)]((https://GitHub.Com/ArtificialHumanoid/Humanoid/actions/workflows/Linters.yml/badge.svg))
[![Documentation Status](https://readthedocs.org/projects/Humanoid/badge/?version=latest)](https://Humanoid.readthedocs.org)

Univeral API to work with captcha solving services.

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
