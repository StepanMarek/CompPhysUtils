VERSION := 0.5.0

WHEELFILE := dist/compphysutils-$(VERSION)-py3-none-any.whl
TARFILE := dist/compphysutils-$(VERSION).tar.gz

CRYSTALGENSOURCE := compphysutils/crystalgen/generator.py
CRYSTALGENSOURCE += compphysutils/crystalgen/Vector.py
CRYSTALGENSOURCE += compphysutils/crystalgen/VectorRepresentation.py
CRYSTALGENSOURCE += compphysutils/crystalgen/VectorReal.py
CRYSTALGENSOURCE += compphysutils/crystalgen/readCrystalChar.py
CRYSTALGENSOURCE += compphysutils/crystalgen/gencluster
CRYSTALGENSOURCE += compphysutils/crystalgen/__init__.py

PARSERSOURCE := compphysutils/parser/__init__.py
PARSERSOURCE += compphysutils/parser/parser.py
PARSERSOURCE += compphysutils/parser/post_processor.py
PARSERSOURCE += compphysutils/parser/combine.py
PARSERSOURCE += compphysutils/parser/savepoint.py
PARSERSOURCE += compphysutils/parser/parsecoords
PARSERSOURCE += compphysutils/parser/runparser.py
PARSERSOURCE += compphysutils/parser/runcombine.py
PARSERSOURCE += compphysutils/parser/parsers/__init__.py
PARSERSOURCE += compphysutils/parser/parsers/cols.py
PARSERSOURCE += compphysutils/parser/parsers/csv.py
PARSERSOURCE += compphysutils/parser/parsers/eiger.py
PARSERSOURCE += compphysutils/parser/parsers/image.py
PARSERSOURCE += compphysutils/parser/parsers/coord-xyz.py
PARSERSOURCE += compphysutils/parser/parsers/coord-tm.py
PARSERSOURCE += compphysutils/parser/parsers/coord-aims.py
PARSERSOURCE += compphysutils/parser/parsers/coord-cub.py
PARSERSOURCE += compphysutils/parser/combine_commands/translate.py

GRAPHICSSOURCE := compphysutils/graphics/__init__.py
GRAPHICSSOURCE += compphysutils/graphics/Figure.py
GRAPHICSSOURCE += compphysutils/graphics/backends/__init__.py
GRAPHICSSOURCE += compphysutils/graphics/backends/pgfplots.py
GRAPHICSSOURCE += compphysutils/graphics/backends/matplotlib.py
GRAPHICSSOURCE += compphysutils/graphics/plotter.py
GRAPHICSSOURCE += compphysutils/graphics/plot_types/__init__.py
GRAPHICSSOURCE += compphysutils/graphics/plot_types/line.py
GRAPHICSSOURCE += compphysutils/graphics/plot_types/scatter.py
GRAPHICSSOURCE += compphysutils/graphics/plot_types/errorbar.py
GRAPHICSSOURCE += compphysutils/graphics/plot_types/level.py
GRAPHICSSOURCE += compphysutils/graphics/plot_types/quiver.py
GRAPHICSSOURCE += compphysutils/graphics/plot_types/coord.py
GRAPHICSSOURCE += compphysutils/graphics/plot_types/loglog.py
GRAPHICSSOURCE += compphysutils/graphics/plot_types/colormap.py
GRAPHICSSOURCE += compphysutils/graphics/plotconfig.py
GRAPHICSSOURCE += compphysutils/graphics/plotcoords
GRAPHICSSOURCE += compphysutils/graphics/plot3dcoords
GRAPHICSSOURCE += compphysutils/graphics/atom_plot.py
GRAPHICSSOURCE += compphysutils/graphics/transformer.py
GRAPHICSSOURCE += compphysutils/graphics/transforms/log.py
GRAPHICSSOURCE += compphysutils/graphics/decorator.py
GRAPHICSSOURCE += compphysutils/graphics/decorate/line.py
GRAPHICSSOURCE += compphysutils/graphics/decorate/image.py
GRAPHICSSOURCE += compphysutils/graphics/decorate/text.py
GRAPHICSSOURCE += compphysutils/graphics/decorate/arrow.py
GRAPHICSSOURCE += compphysutils/graphics/decorate/rect.py
GRAPHICSSOURCE += compphysutils/graphics/decorate/__init__.py

FITTINGSOURCE := compphysutils/fitting/__init__.py
FITTINGSOURCE += compphysutils/fitting/fitter.py
FITTINGSOURCE += compphysutils/fitting/fit_types/__init__.py
FITTINGSOURCE += compphysutils/fitting/fit_types/linear.py

BASESOURCE := compphysutils/__init__.py
BASESOURCE += compphysutils/util.py

.PHONY: install

install: $(WHEELFILE)
	#pip3 install --break-system-packages --force-reinstall $(WHEELFILE)
	pip3 install --force-reinstall $(WHEELFILE)

upload-test: $(WHEELFILE)
	python -m twine upload --repository testpypi $(WHEELFILE) $(TARFILE)

upload: $(WHEELFILE)
	python -m twine upload --verbose $(WHEELFILE) $(TARFILE)

$(WHEELFILE): $(CRYSTALGENSOURCE) $(GRAPHICSSOURCE) $(BASESOURCE) $(PARSERSOURCE) $(FITTINGSOURCE) MANIFEST.in pyproject.toml
	python -m build

test: install
	cd tests/ && python -m unittest

