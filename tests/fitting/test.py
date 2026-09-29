import unittest
from compphysutils.parser import parseDatasetConfig
from compphysutils.fitting.fitter import from_config

class FitTests(unittest.TestCase):

    def test_linear_quadratic(self):
        datasets = parseDatasetConfig("quadratic.cfg")
        from_config("quadratic.cfg", datasets)
