import unittest
from compphysutils.parser import parseDatasetConfig as parse_dataset_config

target_files = {}
target_contents = {}

target_files["average"] = [
    "average.dat",
    "average_all.dat"
]
target_contents["average"] = [
"""4.0 0.5 4.0
""",
"""3.0 0.0 4.0
"""]

class PostProcessTest(unittest.TestCase):

    def run_file_test(self, name):
        
        parse_dataset_config(name)

        for i in range(len(target_files[name])):
            with self.subTest(i=target_files[name][i]):
                result = open(target_files[name][i], "r")
                self.assertEqual(result.read(), target_contents[name][i])
                result.close()

    def test_average(self):
        self.run_file_test("average")
