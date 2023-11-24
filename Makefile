.PHONY: build release clean

build:
	@pyproject-build

release: dist/icat_package_manager*
	@twine upload dist/*

clean:
	@rm -rf dist;
	@rm -rf build;
	@rm -rf icat_package_manager.egg-info
