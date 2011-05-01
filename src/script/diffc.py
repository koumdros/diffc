#!/usr/bin/python

__author__ = "Toshiyuki Fukuzawa"

import sys
import re

from diff_match_patch import diff_match_patch

class Color:
    "Color definition based on ANSI standard terminal attributes"

    # Background colors
    BG_RED = "\x1b[41m"
    BG_GREEN = "\x1b[42m"

    # Foreground colors
    FG_BLACK = "\x1b[30m"
    FG_RED = "\x1b[31m"
    FG_GREEN = "\x1b[32m"
    FG_MEGENTA = "\x1b[35m"
    FG_CYAN = "\x1b[36m"

    # Default
    DEFAULT = "\x1b[0m"

class Diffc:

    P_TRD_RANGE = re.compile("^[\d,]*(a|c|d)[\d,]*$")
    P_TRD_LEFT = re.compile("^<")
    P_TRD_RIGHT = re.compile("^>")
    P_TRD_SEPARATOR = re.compile("^\\-+$")

    P_UNI_RANGE = re.compile("^@@[\\s\\d\\-\\+,]+@@$")
    P_UNI_LEFT = re.compile("^\\-")
    P_UNI_RIGHT = re.compile("^\\+")

    LINE_BREAK = "\n"

    def __init__(self):
        self.left_buf = []
        self.center_buf = []
        self.right_buf = []

        self.is_traditional_diff_style = False
        self.is_unified_diff_style = False

        self.word_diff_proc = diff_match_patch()

        self.color_info = Color.FG_CYAN

        self.color_left_context = Color.FG_RED
        self.color_left_diff = Color.BG_RED + Color.FG_BLACK

        self.color_right_context = Color.FG_GREEN
        self.color_right_diff = Color.BG_GREEN + Color.FG_BLACK

    def color(self, input):
        output = []

        for line in input:
            if self.P_TRD_RANGE.match(line):
                self.is_traditional_diff_style = True
                output += self.calc_word_diff()
                output += [ self.color_info + line + Color.DEFAULT ]
                continue

            if self.P_UNI_RANGE.match(line):
                self.is_unified_diff_style = True
                output += self.calc_word_diff()
                output += [ self.color_info + line + Color.DEFAULT ]
                continue

            if self.is_traditional_diff_style:
                if self.P_TRD_LEFT.match(line):
                    self.left_buf += [line]
                    continue

                if self.P_TRD_RIGHT.match(line):
                    self.right_buf += [line]
                    continue

                if self.P_TRD_SEPARATOR.match(line):
                    self.center_buf += [line]
                    continue

            if self.is_unified_diff_style:
                if self.P_UNI_LEFT.match(line):
                    self.left_buf += [line]
                    continue

                if self.P_UNI_RIGHT.match(line):
                    self.right_buf += [line]
                    continue

            output += self.calc_word_diff()
            output += [line]

        output += self.calc_word_diff()

        return output

    def calc_word_diff(self):
        if not self.left_buf and not self.right_buf :
            return self.center_buf

        ret = []

        left_str = ""
        right_str = ""

        left_header = ""
        right_header = ""

        if self.is_traditional_diff_style:
            left_header = "< "
            right_header = "> "
        elif self.is_unified_diff_style:
            left_header = "\\-"
            right_header = "\\+"
        
        left_str = self.LINE_BREAK.join( map(lambda x: re.sub("^" + left_header, "", x), self.left_buf) )
        right_str = self.LINE_BREAK.join( map(lambda x: re.sub("^" + right_header, "", x), self.right_buf) )

        diffs = self.word_diff_proc.diff_main(left_str, right_str)
        
        left_colored_strs = []
        right_colored_strs = []
        for (op, data) in diffs:
            if op == self.word_diff_proc.DIFF_INSERT:
                right_colored_strs += [self.append_color(data, self.color_right_diff)]
            elif op == self.word_diff_proc.DIFF_DELETE:
                left_colored_strs += [self.append_color(data, self.color_left_diff)]
            elif op == self.word_diff_proc.DIFF_EQUAL:
                left_colored_strs += [self.append_color(data, self.color_left_context)]
                right_colored_strs += [self.append_color(data, self.color_right_context)]

        ret += self.split_into_diff_lines(left_header.replace("\\", ""), self.color_left_context, "".join(left_colored_strs))
        ret += self.center_buf
        ret += self.split_into_diff_lines(right_header.replace("\\", ""), self.color_right_context, "".join(right_colored_strs))

        self.clear_buf()

        return ret

    def append_color(self, str, color):
        if len(str) == 0:
            return str

        return color + str.replace(self.LINE_BREAK, Color.DEFAULT + self.LINE_BREAK + color) + Color.DEFAULT

    def split_into_diff_lines(self, header_str, color, base_str):
        if not base_str:
            return []

        return map(lambda x: ''.join(
                [color, header_str, Color.DEFAULT, x]), base_str.split(self.LINE_BREAK))

    def clear_buf(self):
        self.left_buf[:] = []
        self.center_buf[:] = []
        self.right_buf[:] = []

if __name__ == "__main__":
    d = Diffc()
    input = map(lambda x: re.sub("[\r\n]*$","",x), sys.stdin.readlines())
    output = d.color(input)
    for r in output :
        print(r)

