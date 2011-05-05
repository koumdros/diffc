#!/usr/bin/python

import unittest

import diffc
from diffc import Color

class TestDiffc(unittest.TestCase):

    def setUp(self):
        global CI, CD, CL, CLD, CR, CRD
        
        self.diffc = diffc.Diffc()

        CI = self.diffc.color_info
        CD = Color.DEFAULT
        CL = self.diffc.color_left_context
        CLD = self.diffc.color_left_diff
        CR = self.diffc.color_right_context
        CRD = self.diffc.color_right_diff

    def test_trd_single_line(self):
        global CI, CD, CL, CLD, CR, CRD

        diff = ['1c1',
                '< check this dokument. On',
                '---',
                '> check this document. On']

        result = self.diffc.color(diff)

        expected = [
            CI + '1c1' + CD,
            CL + '< ' + CD \
                + CL + 'check this do' + CD \
                + CLD + 'k' + CD \
                + CL + 'ument. On' + CD,
            '---',
            CR + '> ' + CD \
                + CR + 'check this do' + CD \
                + CRD + 'c' + CD \
                + CR + 'ument. On' + CD
            ]

        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

    def test_trd_multiple_lines(self):
        global CI, CD, CL, CLD, CR, CRD

        diff = ['1,2c1,2', 
                '< aaa', 
                '< bbb', 
                '---', 
                '> axa', 
                '> byb']

        result = self.diffc.color(diff)

        expected = [
             CI + '1,2c1,2' + CD,
             CL + '< ' + CD + CL + 'a' + CD + CLD + 'a' + CD + CL + 'a' + CD,
             CL + '< ' + CD + CL + 'b' + CD + CLD + 'b' + CD + CL + 'b' + CD,
             '---',
             CR + '> ' + CD + CR + 'a' + CD + CRD + 'x' + CD + CR + 'a' + CD,
             CR + '> ' + CD + CR + 'b' + CD + CRD + 'y' + CD + CR + 'b' + CD
             ]

        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

    def test_trd_multiple_diffs(self):
        global CI, CD, CL, CLD, CR, CRD

        diff = ['1,2c1,2', 
            '< aaa', 
            '< bbb', 
            '---', 
            '> axa',
            '> byb',
            '4,5c4,5',
            '< ddd',
            '< eee',
            '---',
            '> dxd',
            '> eze']

        result = self.diffc.color(diff)

        expected = [
            CI + '1,2c1,2' + CD,
            CL + '< ' + CD + CL + 'a' + CD + CLD + 'a' + CD + CL + 'a' + CD,
            CL + '< ' + CD + CL + 'b' + CD + CLD + 'b' + CD + CL + 'b' + CD,
            '---',
            CR + '> ' + CD + CR + 'a' + CD + CRD + 'x' + CD + CR + 'a' + CD,
            CR + '> ' + CD + CR + 'b' + CD + CRD + 'y' + CD + CR + 'b' + CD,
            CI + '4,5c4,5' + CD,
            CL + '< ' + CD + CL + 'd' + CD + CLD + 'd' + CD + CL + 'd' + CD,
            CL + '< ' + CD + CL + 'e' + CD + CLD + 'e' + CD + CL + 'e' + CD,
            '---',
            CR + '> ' + CD + CR + 'd' + CD + CRD + 'x' + CD + CR + 'd' + CD,
            CR + '> ' + CD + CR + 'e' + CD + CRD + 'z' + CD + CR + 'e' + CD]

        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

    def test_trd_del_only(self):
        global CI, CD, CL, CLD, CR, CRD

        diff = ['1,3d0', '< aaa', '< bbb', '< ccc']

        result = self.diffc.color(diff)

        expected = [
            CI + '1,3d0' + CD,
            CL + '< ' + CD + CLD + 'aaa' + CD,
            CL + '< ' + CD + CLD + 'bbb' + CD,
            CL + '< ' + CD + CLD + 'ccc' + CD]

        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

    def test_trd_insert_only(self):
        global CI, CD, CL, CLD, CR, CRD

        diff = ['0a1,3', '> aaa', '> bbb', '> ccc']

        result = self.diffc.color(diff)

        expected = [
            CI + '0a1,3' + CD,
            CR + '> ' + CD + CRD + 'aaa' + CD,
            CR + '> ' + CD + CRD + 'bbb' + CD,
            CR + '> ' + CD + CRD + 'ccc' + CD]

        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

    def test_empty(self):
        diff = []
        result = self.diffc.color(diff)

        self.assertEqual(0, len(result))

    def test_info_only(self):
        diff = ['test', 'info']
        result = self.diffc.color(diff)

        expected = diff
        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

    def test_uni_single_line(self):
        global CI, CD, CL, CLD, CR, CRD

        diff = [
            '@@ -1 +1 @@',
            '-check this dokument. On', 
            '+check this document. On']

        result = self.diffc.color(diff)

        expected = [
            CI + '@@ -1 +1 @@' + CD,
            CL + '-' + CD + CL + 'check this do' + CD \
                + CLD + 'k' + CD + CL + 'ument. On' + CD,
            CR + '+' + CD + CR + 'check this do' + CD \
                + CRD + 'c' + CD + CR + 'ument. On' + CD]

        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

    def test_uni_multiple_diff(self):
        global CI, CD, CL, CLD, CR, CRD

        diff = [             
            '@@ -1,5 +1,5 @@',
            '-aaa',
            '-bbb',
            '+axa',
            '+byb',
            ' ccc',
            '-ddd',
            '-eee',
            '+dxd',
            '+eze']

        result = self.diffc.color(diff)

        expected = [
            CI + '@@ -1,5 +1,5 @@' + CD,
            CL + '-' + CD + CL + 'a' + CD + CLD + 'a' + CD + CL + 'a' + CD,
            CL + '-' + CD + CL + 'b' + CD + CLD + 'b' + CD + CL + 'b' + CD,
            CR + '+' + CD + CR + 'a' + CD + CRD + 'x' + CD + CR + 'a' + CD,
            CR + '+' + CD + CR + 'b' + CD + CRD + 'y' + CD + CR + 'b' + CD,
            ' ccc',
            CL + '-' + CD + CL + 'd' + CD + CLD + 'd' + CD + CL + 'd' + CD,
            CL + '-' + CD + CL + 'e' + CD + CLD + 'e' + CD + CL + 'e' + CD,
            CR + '+' + CD + CR + 'd' + CD + CRD + 'x' + CD + CR + 'd' + CD,
            CR + '+' + CD + CR + 'e' + CD + CRD + 'z' + CD + CR + 'e' + CD]

        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

    def test_uni_insert_only(self):
        global CI, CD, CL, CLD, CR, CRD

        diff = [
            '@@ -0,0 +1,3 @@',
            '+aaa', 
            '+bbb',
            '+ccc']

        result = self.diffc.color(diff)

        expected = [
            CI + '@@ -0,0 +1,3 @@' + CD,
            CR + '+' + CD + CRD + 'aaa' + CD,
            CR + '+' + CD + CRD + 'bbb' + CD,
            CR + '+' + CD + CRD + 'ccc' + CD]

        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

    def test_space(self):
        global CI, CD, CL, CLD, CR, CRD

        diff = ['1c1', 
                '< aa',
                '---',
                '> aa   ']

        result = self.diffc.color(diff)

        expected = [
            CI + '1c1' + CD,
            CL + '< ' + CD + CL + 'aa' + CD,
            '---',
            CR + '> ' + CD + CR + 'aa' + CD + CRD + '   ' + CD]

        self.assertEqual(len(expected), len(result))

        for i, v in enumerate(expected):
            self.assertEqual(v, result[i])

if __name__ == "__main__":
    unittest.main()
