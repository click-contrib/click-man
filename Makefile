tests:
	@tox

readme_pip:
	@pandoc README.md --from markdown --to rst -o README.rst

publish: tests readme_pip
	@python3 setup.py sdist register upload
