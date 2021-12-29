VERSION := 0.0.4

WHEELFILE := dist/compphysutils-$(VERSION)-py3-none-any.whl
TARFILE := dist/compphysutils-$(VERSION).tar.gz

CRYSTALGENSOURCE := src/compphysutils/crystalgen/generator.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/Vector.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/VectorRepresentation.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/VectorReal.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/readCrystalChar.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/gencluster
CRYSTALGENSOURCE += src/compphysutils/crystalgen/__init__.py

install: $(WHEELFILE)
	pip3 install --force-reinstall $(WHEELFILE)

upload: $(WHEELFILE)
	python -m twine upload --repository testpypi $(WHEELFILE) $(TARFILE)

$(WHEELFILE): $(CRYSTALGENSOURCE) 
	python -m build
