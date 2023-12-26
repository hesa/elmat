# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later


check: python clean check-reuse build
	@echo "\n\n\n   Yay.... check succeeded :)\n\n\n"

check-reuse: clean
	reuse --suppress-deprecation lint


python: py-test py-lint

py-test:
	PYTHONPATH=python/ python3 -m pytest --log-cli-level=10 tests/

py-lint:
	PYTHONPATH=. flake8

check-py-cli:
	@echo -n "Check cli (-h): "
	@PYTHONPATH=./python python3 ./elmat/__main__.py -h > /dev/null
	@echo "OK"

build:
	rm -fr build
	python3 setup.py sdist
	@echo
	@echo "build ready :)"

py-release: check clean build
	./devel/check-release.sh
	@echo
	@echo "To upload: "
	@echo "twine upload --repository elmat --verbose  dist/*"

clean:
	find . -name "*~"    | xargs rm -fr
	find . -name "*.pyc" | xargs rm -fr
	find . -name ".#*" | xargs rm -fr
	rm -f .coverage
	rm -fr python/elmat.egg-info
	rm -fr python/*elmat.egg*
	rm -fr python/dist
	rm -fr python/build
