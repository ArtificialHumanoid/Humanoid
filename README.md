# Installation
<!--
Run
```bash
pip install Humanoid
```

or, for the latest,
-->

```bash
pip install git+https://github.com/ArtificialHumanoid/Humanoid#subdirectory=build
```
.

# Issues, Pull Requests, and Commits
Issues and, of course, pull requests, are tracked via GitHub.  
Accordingly, all commit messages should be prefixed with “#” (followed by an issue or pull request numbered reference).

# `humanoid.actions.internet_search`
The internet search actions provide a Python interface for searching Google. They use requests and BeautifulSoup4 to scrape Google.


## Usage
To get results for a search term, use the search function. For example, to get results for "Google" in Google, run the following program:
```python
from humanoid.actions.internet_search.google import search

search("Google")
```

## Additional options
By default, `search` returns 10 results.
To get a 100 results on Google, for example:
```python
from humanoid.actions.internet_search.google import search

search("Google", num_results=100)
```
In addition, you can change the language Google searches in.
For example, to get results in French run the following program:
```python
from humanoid.actions.internet_search.google import search

search("Google", lang="fr")
```
To extract more information, such as the description or the result URL, use an advanced search:
```python
from humanoid.actions.internet_search.google import search

search("Google", advanced=True)
```
which returns `List[SearchResult]` with each result having the properties
- title
- url
- description.

If requesting more than 100 results, `search` will send multiple requests to go through the pages.
To increase the time between these requests, use sleep_interval:
```python
from humanoid.actions.internet_search.google import search

search("Google", sleep_interval=5, num_results=200)
```

TLS certificate verification is enabled by default. A trusted environment that
requires the legacy unverified connection path can disable verification:

```python
from humanoid.actions.internet_search.google import search

search("Google", verify=False)
```

This still uses HTTPS, but it does not verify the server certificate. Requests
may emit an insecure-request warning, and normal callers should leave
verification enabled.

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

## Branching and Publication
Publication to package repositories only occurs on the `Dev` and `Prod` branches using the `Package` workflow. When `Exploration` is merged into `Dev`, this workflow automatically increments the patch version.
