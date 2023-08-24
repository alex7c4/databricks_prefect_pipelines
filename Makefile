env:
	# brew install pyenv
	pip install -U poetry=="1.5.*"
	pyenv install --skip-existing 3.11
	pyenv local 3.11 && poetry env use $(shell pyenv which python3) && poetry install --no-interaction
	poetry run pip install --upgrade pip

env_rm:
	yes | poetry cache clear . --all && poetry env remove --all

fmt:
	# show changes
	poetry run isort --diff --color ./src ./tests
	poetry run black --diff --color ./src ./tests
	# change
	poetry run isort ./src ./tests
	poetry run black ./src ./tests

checks:
	poetry run isort --check ./src ./tests
	poetry run black --check ./src ./tests
	poetry run mypy ./src ./tests
	poetry run pylint ./src ./tests

pytest_ci:
	poetry run pytest -sv --junit-xml junit/test-results.xml ./tests

pytest:
	poetry run pytest --cache-clear --capture=no --verbose --disable-warnings --color=yes ./tests

lib:
	poetry build --format sdist

clean:
	rm -rf ./.*_cache ./dist ./.python-version
	find ./ -type d -name "__pycache__" -exec rm -rf {} +
