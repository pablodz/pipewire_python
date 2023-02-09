.DEFAULT_GOAL := help

apt-packages-ubuntu: ## Install packages needed
	sudo add-apt-repository ppa:pipewire-debian/pipewire-upstream -y
	sudo apt update
	sudo apt-get install pipewire -y

deps:  ## Install dependencies
	python -m pip install --upgrade pip
	python -m pip install black coverage flake8 flit mccabe mypy pylint pytest pytest-cov tox tox-gh-actions

publish:  ## Publish to PyPi
	python -m flit publish

push:  ## Push code with tags
	git push && git push --tags

test:  ## Run tests [LOCALHOST]
	python -m pytest -ra

tox:  ## Run tox
	python3 -m tox
	ls -la

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'