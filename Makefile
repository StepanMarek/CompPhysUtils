VERSION := 0.0.5

WHEELFILE := dist/compphysutils-$(VERSION)-py3-none-any.whl
TARFILE := dist/compphysutils-$(VERSION).tar.gz

CRYSTALGENSOURCE := src/compphysutils/crystalgen/generator.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/Vector.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/VectorRepresentation.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/VectorReal.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/readCrystalChar.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/gencluster
CRYSTALGENSOURCE += src/compphysutils/crystalgen/__init__.py

GRAPHICSSOURCE := src/compphysutils/graphics/__init__.py
GRAPHICSSOURCE += src/compphysutils/graphics/parser.py
GRAPHICSSOURCE += src/compphysutils/graphics/colsParser.py
GRAPHICSSOURCE += src/compphysutils/graphics/hlgParser.py
GRAPHICSSOURCE += src/compphysutils/graphics/aimsParser.py
GRAPHICSSOURCE += src/compphysutils/graphics/eigerParser.py
GRAPHICSSOURCE += src/compphysutils/graphics/post_process.py
GRAPHICSSOURCE += src/compphysutils/graphics/combine.py
GRAPHICSSOURCE += src/compphysutils/graphics/plotter.py
GRAPHICSSOURCE += src/compphysutils/graphics/plotconfig
GRAPHICSSOURCE += src/compphysutils/graphics/fitter.py
GRAPHICSSOURCE += src/compphysutils/graphics/transformer.py

BASESOURCE := src/compphysutils/__init__.py

install: $(WHEELFILE)
	pip3 install --force-reinstall $(WHEELFILE)

upload: $(WHEELFILE)
	python -m twine upload --repository testpypi $(WHEELFILE) $(TARFILE)

$(WHEELFILE): $(CRYSTALGENSOURCE) $(GRAPHICSSOURCE) $(BASESOURCE)
	python -m build
