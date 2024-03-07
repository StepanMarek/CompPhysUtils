VERSION := 0.4.1

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
PARSERSOURCE += src/compphysutils/parser/post_processor.py
PARSERSOURCE += src/compphysutils/parser/combine.py
PARSERSOURCE += src/compphysutils/parser/savepoint.py
PARSERSOURCE += src/compphysutils/parser/parsecoords
PARSERSOURCE += src/compphysutils/parser/runparser
PARSERSOURCE += src/compphysutils/parser/runcombine
PARSERSOURCE += src/compphysutils/parser/parsers/__init__.py
PARSERSOURCE += src/compphysutils/parser/parsers/cols.py
PARSERSOURCE += src/compphysutils/parser/parsers/csv.py
PARSERSOURCE += src/compphysutils/parser/parsers/eiger.py
PARSERSOURCE += src/compphysutils/parser/parsers/image.py

GRAPHICSSOURCE := src/compphysutils/graphics/__init__.py
GRAPHICSSOURCE += src/compphysutils/graphics/plotter.py
GRAPHICSSOURCE += src/compphysutils/graphics/plot_types/__init__.py
GRAPHICSSOURCE += src/compphysutils/graphics/plot_types/line.py
GRAPHICSSOURCE += src/compphysutils/graphics/plot_types/scatter.py
GRAPHICSSOURCE += src/compphysutils/graphics/plot_types/errorbar.py
GRAPHICSSOURCE += src/compphysutils/graphics/plot_types/level.py
GRAPHICSSOURCE += src/compphysutils/graphics/plot_types/quiver.py
GRAPHICSSOURCE += src/compphysutils/graphics/fit_types/__init__.py
GRAPHICSSOURCE += src/compphysutils/graphics/fit_types/linear.py
GRAPHICSSOURCE += src/compphysutils/graphics/plotconfig
GRAPHICSSOURCE += src/compphysutils/graphics/fitter.py
GRAPHICSSOURCE += src/compphysutils/graphics/transformer.py
GRAPHICSSOURCE += src/compphysutils/graphics/transforms/log.py
GRAPHICSSOURCE += src/compphysutils/graphics/decorator.py
GRAPHICSSOURCE += src/compphysutils/graphics/decorate/line.py
GRAPHICSSOURCE += src/compphysutils/graphics/decorate/image.py
GRAPHICSSOURCE += src/compphysutils/graphics/decorate/__init__.py

BASESOURCE := src/compphysutils/__init__.py

install: $(WHEELFILE)
	pip3 install --break-system-packages --force-reinstall $(WHEELFILE)

upload-test: $(WHEELFILE)
	python -m twine upload --repository testpypi $(WHEELFILE) $(TARFILE)

upload: $(WHEELFILE)
	python -m twine upload --verbose $(WHEELFILE) $(TARFILE)

$(WHEELFILE): $(CRYSTALGENSOURCE) $(GRAPHICSSOURCE) $(BASESOURCE) $(PARSERSOURCE)
	python -m build
