.DEFAULT_GOAL := help
.PHONY: coverage deps help lint publish push test tox

apt-packages-ubuntu: ## Install packages needed
	sudo add-apt-repository ppa:pipewire-debian/pipewire-upstream -y
	sudo apt update
	sudo apt-get install pipewire -y

deps:  ## Install dependencies
	python -m pip install --upgrade pip
	python -m pip install black coverage flake8 flit mccabe mypy pylint pytest pytest-cov tox tox-gh-actions

# coverage:  ## Run tests with coverage
# 	python -m coverage erase
# 	python -m coverage run --include=pipewire_python/* -m pytest -ra
# 	python -m coverage report -m
# 	python -m coverage xml

# lint:  ## Lint and static-check
# 	python -m flake8 pipewire_python
# 	python -m pylint pipewire_python
# 	python -m mypy pipewire_python

publish:  ## Publish to PyPi
	python -m flit publish

push:  ## Push code with tags
	git push && git push --tags

test:  ## Run tests [LOCALHOST]
	python -m pytest -ra

tox:  ## Run tox
	python3 -m tox
	ls -la
