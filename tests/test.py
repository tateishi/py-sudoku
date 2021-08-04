import unittest
from sudoku.model.place import Place

class TestPlaceMethods(unittest.TestCase):
    def test_place(self):
        p = Place(42)
        self.assertEqual(p.i, 42)
        self.assertEqual(p.x, 6)
        self.assertEqual(p.y, 4)
        self.assertEqual(p.b, 5)

    def test_str(self):
        p = Place(42)
        self.assertEqual(str(p), '42')

    def test_format(self):
        p = Place(42)
        self.assertEqual(f'{p}', '42')
        self.assertEqual(f'{p:xy}', '64')
        self.assertEqual(f'{p:xy,}', '6,4')
        self.assertEqual(f'{p:ixyb}', '42645')
        self.assertEqual(f'{p:ixyb,}', '42,6,4,5')
        self.assertEqual(f'{p:2ixyb}', '42 6 4 5')
        self.assertEqual(f'{p:<2ixyb}', '426 4 5 ')
        self.assertEqual(f'{p:<2ixyb,}', '42,6 ,4 ,5 ')


if __name__ == '__main__':
    unittest.main()
