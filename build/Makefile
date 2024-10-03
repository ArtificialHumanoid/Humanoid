bootstrap: venv deps dirs

venv:
	virtualenv -p python3 .env

deps:
	.env/bin/pip install -r requirements_dev.txt
	.env/bin/pip install -e .

dirs:
	if [ ! -e var/run ]; then mkdir -p var/run; fi
	if [ ! -e var/log ]; then mkdir -p var/log; fi

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete
	find -name '__pycache__' -delete

test:
	make check \
	&& make pytest \
	&& tox -e py37-check


release:
	git push \
	&& git push --tags \
	&& make build \
	&& twine upload dist/*

check:
	echo "mypy" \
	&& make mypy \
	&& echo "pylint" \
	&& make pylint \
	&& echo "flake8" \
	&& make flake8 \
	&& echo "bandit" \
	&& make bandit

build:
	rm -rf *.egg-info
	rm -rf dist/*
	python -m build --sdist


coverage:
	pytest --cov captcha_solver --cov-report term-missing