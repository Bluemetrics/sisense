api-test:
	python -m unittest discover

test-release:
	mv dist dist_bkp
	python setup.py sdist bdist_wheel
	python -m twine upload --repository testpypi dist/*
	mv dist_bkp/* dist/
	rm -R dist_bkp

release:
	mv dist dist_bkp
	python setup.py sdist bdist_wheel
	python -m twine upload --repository pypi dist/*
	mv dist_bkp/* dist/
	rm -R dist_bkp