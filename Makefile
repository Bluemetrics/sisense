api-test:
	python -m unittest discover

test-release:
	python setup.py sdist bdist_wheel
	python -m twine upload --repository testpypi dist/*

release:
	python setup.py sdist bdist_wheel
	python -m twine upload --repository pypi dist/*