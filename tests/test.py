import unittest
from compphysutils.graphics.plotter import fromConfig as from_config

class PGFGraphicsTest(unittest.TestCase):
    """
    So far, only tries to run the graphics, does not check the consistency of the actual results
    """

    def test_arrow(self):
        from_config("arrow.cfg")

    def test_axes_linewidth(self):
        from_config("axes_linewidth.cfg")

    def test_axis_labels(self):
        from_config("axis_labels.cfg")

    def test_axline(self):
        from_config("axline.cfg")

    def test_colorline(self):
        from_config("colorline.cfg")

    def test_colormap(self):
        from_config("colormap.cfg")

    def test_colormap_nonorth(self):
        from_config("colormap_nonorth.cfg")

    def test_errorbar(self):
        from_config("errorbar.cfg")

    def test_fill_between(self):
        from_config("fill_between.cfg")

    def test_hide(self):
        from_config("hide.cfg")

    def test_inset_axes(self):
        from_config("inset_axes.cfg")

    def test_legend_cols(self):
        from_config("legend_cols.cfg")

    def test_legend_pos(self):
        from_config("legend_pos.cfg")

    def test_level(self):
        from_config("level.cfg")

    def test_lims(self):
        from_config("lims.cfg")

    def test_line(self):
        from_config("line.cfg")

    def test_linlog(self):
        from_config("linlog.cfg")

    def test_loglog(self):
        from_config("loglog.cfg")

    def test_quiver(self):
        from_config("quiver.cfg")

    def test_rect_patch(self):
        from_config("rect_patch.cfg")

    def test_scatter(self):
        from_config("scatter.cfg")

    def test_text(self):
        from_config("text.cfg")

    def test_tick_labels(self):
        from_config("tick_labels.cfg")

    def test_tick_rotation(self):
        from_config("tick_rotation.cfg")

    def test_tick_swap(self):
        from_config("tick_swap.cfg")

    def test_twinx(self):
        from_config("twinx.cfg")

    def test_twiny(self):
        from_config("twiny.cfg")

    def test_width_height(self):
        from_config("width_height.cfg")

