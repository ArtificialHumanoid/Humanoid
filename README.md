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
googlesearch.search(str: term, int: num_results=10, str: lang="en") -> list
```

# `captcha_solver`

[![Test Status](https://github.com/lorien/captcha_solver/actions/workflows/test.yml/badge.svg)](https://github.com/lorien/captcha_solver/actions/workflows/test.yml)
[![Code Quality](https://github.com/lorien/captcha_solver/actions/workflows/check.yml/badge.svg)](https://github.com/lorien/captcha_solver/actions/workflows/test.yml)
[![Type Check](https://github.com/lorien/captcha_solver/actions/workflows/mypy.yml/badge.svg)](https://github.com/lorien/captcha_solver/actions/workflows/mypy.yml)
[![Test Coverage Status](https://coveralls.io/repos/github/lorien/captcha_solver/badge.svg)](https://coveralls.io/github/lorien/captcha_solver)
[![Documentation Status](https://readthedocs.org/projects/captcha_solver/badge/?version=latest)](https://captcha_solver.readthedocs.org)

Univeral API to work with captcha solving services.

Feel free to give feedback in Telegram groups: [@grablab](https://t.me/grablab) and [@grablab\_ru](https://t.me/grablab_ru)

## Installation

Run: `pip install -U captcha-solver`

## Twocaptcha Backend Example

Service website is https://2captcha.com?from=3019071

```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('twocaptcha', api_key='2captcha.com API HERE')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```

## Rucaptcha Backend Example

Service website is https://rucaptcha.com?from=3019071

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

Service website is http://getcaptchasolution.com/ijykrofoxz

```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('antigate', api_key='ANTIGATE_KEY')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```
