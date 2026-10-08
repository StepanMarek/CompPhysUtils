import unittest
from compphysutils.parser.combine import runGroupData
import configparser

target_files = {}
target_files["scale"] = [
    "scale.dat",
    "scale_all.dat"
]
target_contents = {}
target_contents["scale"] = [
"""2.0 3.0 3.0
4.0 6.0 6.0
6.0 9.0 9.0
8.0 12.0 12.0
""",
"""1.5 1.5 1.5 1.5 a
3.0 3.0 3.0 3.0 b
4.5 4.5 4.5 4.5 c
4.0 4.0 4.0 4.0 d
"""
]

target_files["translate"] = [
    "translate.dat",
    "translate_all.dat"
]
target_contents["translate"] = [
"""1.0 0.0 0.0
2.0 1.0 1.0
3.0 2.0 2.0
4.0 3.0 3.0
""",
"""1.5 2.5 2.5 1.0 a
2.5 3.5 3.5 2.0 b
3.5 4.5 4.5 3.0 c
3.0 4.0 4.0 4.0 d
"""
]

target_files["join-partial"] = [
    "join-partial.dat"
]
target_contents["join-partial"] = [
"""1.0 -1.0 2.0 3.0
2.0 -2.0 4.0 6.0
3.0 -3.0 6.0 9.0
4.0 -4.0 8.0 12.0
"""]

class CombineTests(unittest.TestCase):

    def run_file_test(self, name):
        
        # Load the config
        cfg = configparser.ConfigParser()
        cfg.read(name+".cfg")
        datasets = runGroupData(cfg, {}, name+".cfg")

        for i in range(len(target_files[name])):
            with self.subTest(i=target_files[name][i]):
                result = open(target_files[name][i], "r")
                self.assertEqual(result.read(), target_contents[name][i])
                result.close()

    def test_scale(self):
        self.run_file_test("scale")

    def test_translate(self):
        self.run_file_test("translate")

    def test_join_partial(self):
        self.run_file_test("join-partial")
