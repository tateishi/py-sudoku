import unittest
from sudoku.model.place import Place
from sudoku.model.cell import Cell

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


class TestCellMethods(unittest.TestCase):
    def test_cell(self):
        c = Cell.from_number(1)
        self.assertEqual(str(c), '1')
        self.assertTrue(c.fixed)

    def test_cell_unknown(self):
        c = Cell.unknown()
        self.assertEqual(str(c), '[123456789]')
        self.assertFalse(c.fixed)

    def test_cell_discard(self):
        c = Cell.unknown()
        d = Cell.from_number(1)
        c = c.discard(1)
        d = d.discard(1)
        self.assertEqual(str(c), '[23456789]')
        self.assertEqual(str(d), '1')

    def test_cell_sub(self):
        c = Cell.unknown()
        d = Cell.from_number(1)
        c = c - 1
        d = d - 1
        self.assertEqual(str(c), '[23456789]')
        self.assertEqual(str(d), '1')

    def test_cell_discard_set(self):
        c = Cell.unknown()
        d = Cell.from_number(1)
        c = c.discard({1,2})
        d = d.discard({1,2})
        self.assertEqual(str(c), '[3456789]')
        self.assertEqual(str(d), '1')

    def test_cell_sub_set(self):
        c = Cell.unknown()
        d = Cell.from_number(1)
        c = c - {1,2}
        d = d - {1,2}
        self.assertEqual(str(c), '[3456789]')
        self.assertEqual(str(d), '1')

    def test_cell_discard_tuple(self):
        c = Cell.unknown()
        d = Cell.from_number(1)
        c = c.discard((1,2))
        d = d.discard((1,2))
        self.assertEqual(str(c), '[3456789]')
        self.assertEqual(str(d), '1')

    def test_cell_sub_tuple(self):
        c = Cell.unknown()
        d = Cell.from_number(1)
        c = c - (1,2)
        d = d - (1,2)
        self.assertEqual(str(c), '[3456789]')
        self.assertEqual(str(d), '1')

    def test_cell_discard_list(self):
        c = Cell.unknown()
        d = Cell.from_number(1)
        c = c.discard([1,2])
        d = d.discard([1,2])
        self.assertEqual(str(c), '[3456789]')
        self.assertEqual(str(d), '1')

    def test_cell_sub_list(self):
        c = Cell.unknown()
        d = Cell.from_number(1)
        c = c - [1,2]
        d = d - [1,2]
        self.assertEqual(str(c), '[3456789]')
        self.assertEqual(str(d), '1')


if __name__ == '__main__':
    unittest.main()
