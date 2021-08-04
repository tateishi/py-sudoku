import unittest
from sudoku.model.place import Place
from sudoku.model.cell import Cell
from sudoku.model.grid import Grid
from sudoku.model.peer import Peer


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

    def test_cell_from_memo_set(self):
        c = Cell.from_memo({4, 2})
        self.assertEqual(str(c), '[24]')
        self.assertFalse(c.fixed)
        self.assertEqual(str(c-2), '[4]')

    def test_cell_from_memo_tuple(self):
        c = Cell.from_memo((4, 2))
        self.assertEqual(str(c), '[24]')
        self.assertFalse(c.fixed)
        self.assertEqual(str(c-2), '[4]')

    def test_cell_from_memo_list(self):
        c = Cell.from_memo([4, 2])
        self.assertEqual(str(c), '[24]')
        self.assertFalse(c.fixed)
        self.assertEqual(str(c-2), '[4]')

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

class TestGridMethods(unittest.TestCase):
    def test_grid(self):
        g = Grid(Place(42), Cell.unknown())
        self.assertEqual(f'{g.place}', '42')
        self.assertEqual(f'{g.place:ixyb,}', '42,6,4,5')
        self.assertEqual(f'{g.cell-1}', '[23456789]')


class TestPeerMethods(unittest.TestCase):
    def test_peer_col(self):
        p = Peer.col(1)
        self.assertEqual(f'{p}', '[1,10,19,28,37,46,55,64,73]')

    def test_peer_place_col(self):
        p = Peer.col(Place(1))
        self.assertEqual(f'{p}', '[1,10,19,28,37,46,55,64,73]')

    def test_peer_row(self):
        p = Peer.row(1)
        self.assertEqual(f'{p}', '[9,10,11,12,13,14,15,16,17]')

    def test_peer_place_row(self):
        p = Peer.row(Place(1))
        self.assertEqual(f'{p}', '[0,1,2,3,4,5,6,7,8]')

    def test_peer_blk(self):
        p = Peer.blk(1)
        self.assertEqual(f'{p}', '[3,4,5,12,13,14,21,22,23]')

    def test_peer_place_blk(self):
        p = Peer.blk(Place(1))
        self.assertEqual(f'{p}', '[0,1,2,9,10,11,18,19,20]')

    def test_peer_place(self):
        p = Peer.peers(Place(1))
        self.assertEqual(
            f'{p}',
            '[0,1,2,3,4,5,6,7,8,9,10,11,18,19,20,28,37,46,55,64,73]')


if __name__ == '__main__':
    unittest.main()
