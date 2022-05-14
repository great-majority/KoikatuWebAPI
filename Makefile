.PHONY:\
	format\
	check\
	install\

install:
	poetry install

format:
	poetry run isort ./kkwebapi
	poetry run black ./kkwebapi

check:
	poetry run flake8 ./kkwebapi --count --show-source --statistics
	poetry run black ./kkwebapi --check --diff
	poetry run isort ./kkwebapi --check-only