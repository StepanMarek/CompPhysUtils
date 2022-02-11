VERSION := 0.0.6

WHEELFILE := dist/compphysutils-$(VERSION)-py3-none-any.whl
TARFILE := dist/compphysutils-$(VERSION).tar.gz

CRYSTALGENSOURCE := src/compphysutils/crystalgen/generator.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/Vector.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/VectorRepresentation.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/VectorReal.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/readCrystalChar.py
CRYSTALGENSOURCE += src/compphysutils/crystalgen/gencluster
CRYSTALGENSOURCE += src/compphysutils/crystalgen/__init__.py

PARSERSOURCE := src/compphysutils/parser/__init__.py
PARSERSOURCE += src/compphysutils/parser/parser.py
PARSERSOURCE += src/compphysutils/parser/post_process.py
PARSERSOURCE += src/compphysutils/parser/combine.py
PARSERSOURCE += src/compphysutils/parser/parsers/__init__.py
PARSERSOURCE += src/compphysutils/parser/parsers/aims.py
PARSERSOURCE += src/compphysutils/parser/parsers/cols.py
PARSERSOURCE += src/compphysutils/parser/parsers/eiger.py
PARSERSOURCE += src/compphysutils/parser/parsers/hlg.py

GRAPHICSSOURCE := src/compphysutils/graphics/__init__.py
GRAPHICSSOURCE += src/compphysutils/graphics/plotter.py
GRAPHICSSOURCE += src/compphysutils/graphics/plotconfig
GRAPHICSSOURCE += src/compphysutils/graphics/fitter.py
GRAPHICSSOURCE += src/compphysutils/graphics/transformer.py

BASESOURCE := src/compphysutils/__init__.py

install: $(WHEELFILE)
	pip3 install --force-reinstall $(WHEELFILE)

upload: $(WHEELFILE)
	python -m twine upload --repository testpypi $(WHEELFILE) $(TARFILE)

$(WHEELFILE): $(CRYSTALGENSOURCE) $(GRAPHICSSOURCE) $(BASESOURCE) $(PARSERSOURCE)
	python -m build
