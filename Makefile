install:
	pipenv install .

install_dev:
	pipenv install --editable .

shell:
	pipenv shell

which:
	pipenv --venv

remove:
	pipenv --rm

pip_install:
	pip install -r requirements.txt

dump_requirements:
	pipenv requirements > requirements.txt
