all: lint

test: lint
	pytest

lint:
	flake8 app.py --max-line-length=88
	black --check app.py

clean:
	rm -rf __pycache__ tests/__pycache__
