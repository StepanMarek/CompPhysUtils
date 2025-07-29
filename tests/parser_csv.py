import unittest
from compphysutils.parser import parser

class ParserCSVTest(unittest.TestCase):

    def test_read(self):
        dataset = parser.readFile("parser_csv.csv", "csv", parserArgs="0 1 2")
        self.assertEqual(dataset[0][0], 1.0)
        self.assertEqual(dataset[1][0], 2.0)
        self.assertEqual(dataset[2][0], 5.0)

if __name__ == "__main__":
    unittest.main()
