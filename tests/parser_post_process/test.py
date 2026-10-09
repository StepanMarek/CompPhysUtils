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

target_files["gap"] = [
    "gap.dat",
    "gap_frac.dat"
]
target_contents["gap"] = [
"""1.5
""",
"""1.7
"""
]

class PostProcessTest(unittest.TestCase):

    def run_file_test(self, name):
        
        parse_dataset_config(name+".cfg")

        for i in range(len(target_files[name])):
            with self.subTest(i=target_files[name][i]):
                result = open(target_files[name][i], "r")
                self.assertEqual(result.read(), target_contents[name][i])
                result.close()

    def test_average(self):
        self.run_file_test("average")

    def test_gap(self):
        self.run_file_test("gap")

    target_files["scale"] = ["scale.dat"]
    target_contents["scale"] = ["""0.0 1.0 0.5
2.0 2.0 1.0
4.0 3.0 2.0
6.0 4.0 2.5
"""
    ]

    def test_scale(self):
        self.run_file_test("scale")

    def test_plane_rotate(self):

        datasets = parse_dataset_config("plane-rotate.cfg")
        dataset = datasets["coords"]

        self.assertAlmostEqual(dataset[0][0], -1, 4)
        self.assertAlmostEqual(dataset[0][1], 1, 4)
        self.assertAlmostEqual(dataset[0][2], 0, 4)

        self.assertAlmostEqual(dataset[1][0], 0.577692, 4)
        self.assertAlmostEqual(dataset[1][1], 0.577666, 4)
        self.assertAlmostEqual(dataset[1][2], -1.154359, 4)

        self.assertAlmostEqual(dataset[2][0], 0, 4)
        self.assertAlmostEqual(dataset[2][1], 0, 4)
        self.assertAlmostEqual(dataset[2][2], 0, 4)

    target_files["mirror"] = ["mirror.dat"]
    target_contents["mirror"] = ["""-1.0 2.0
-2.0 4.0
-3.0 6.0
-4.0 8.0
"""
    ]

    def test_mirror(self):
        self.run_file_test("mirror")
