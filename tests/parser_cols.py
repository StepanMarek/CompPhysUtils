import unittest
import compphysutils.parser as parser

class ParserColsTest(unittest.TestCase):

    def test_read(self):
        dataset = parser.readFile("parser_cols.out", "cols", parserArgs="0 1")
        self.assertEqual(dataset[0][0], 1.0)
        self.assertEqual(dataset[0][1], 2.0)
        self.assertEqual(dataset[1][0], 4.0)
        self.assertEqual(dataset[1][1], 9.0)

    def test_write(self):
        dataset = [[2.0, 4.0],[3.0, 7.0]]
        parser.writeFile("parser_cols.write", "cols", dataset)
        with open("parser_cols.write", "r") as file:
            self.assertEqual(file.readline().split(), ["2.0", "3.0"])
            self.assertEqual(file.readline().split(), ["4.0", "7.0"])

if __name__ == "__main__":
    unittest.main()
