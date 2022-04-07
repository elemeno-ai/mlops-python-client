.PHONY: clean pip-testpypi wheel

clean:
	rm -rf dist

wheel:
	python setup.py bdist_wheel

_pip-testpypi: clean
	python setup.py sdist bdist_wheel
	twine upload --repository testpypi dist/*.whl

_pip-pypi: clean
	python setup.py sdist bdist_wheel
	twine upload --non-interactive dist/*.whl

_pip-pypi-elemeno: clean
	python setup.py sdist bdist_wheel
	twine upload --repository elemeno dist/*.whl

pip-testpypi: clean _pip-testpypi

pip-pypi: clean _pip-pypi

pip-pypi-elemeno: clean _pip-pypi-elemeno

bump-custom:
	bumpversion --new-version $(version) patch --verbose

bump-patch:
ifeq "${RELEASE}" "true"
	@echo "inside RELEASE"
	bumpversion patch --tag --tag-name RELEASE-v{new_version} patch --verbose
else
	@echo "no release"
	bumpversion patch --tag --verbose
	@echo "New version: v$$(python setup.py --version)"
	@echo "Make sure to push the new tag to GitHub"
endif

bump-minor:
	bumpversion minor --tag --verbose
	@echo "New version: v$$(python setup.py --version)"
	@echo "Make sure to push the new tag to GitHub"

bump-major:
	bumpversion major --tag --verbose
	@echo "New version: v$$(python setup.py --version)"
	@echo "Make sure to push the new tag to GitHub"

bump-dev:
	bumpversion build --tag --verbose
	@echo "New version: v$$(python setup.py --version)"
	@echo "Make sure to push the new tag to GitHub"