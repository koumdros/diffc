#!/usr/bin/python2.4

""" diffc
 http://code.google.com/p/diffc/

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

""" description
A simple and lightweight diff tool computing and providing the colored difference between two texts/files.

"""

__author__ = "Toshiyuki Fukuzawa"

import sys
import re
import os
import subprocess
import signal

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
    """Class computing word diff and coloring the terminal output
    """

    P_TRD_RANGE = re.compile("^[\d,]*(a|c|d)[\d,]*$")
    P_TRD_LEFT = re.compile("^<")
    P_TRD_RIGHT = re.compile("^>")
    P_TRD_SEPARATOR = re.compile("^\\-+$")

    P_UNI_RANGE = re.compile("^@@[\\s\\d\\-\\+,]+@@$")
    P_UNI_LEFT = re.compile("^\\-")
    P_UNI_RIGHT = re.compile("^\\+")

    LINE_BREAK = "\n"

    def __init__(self):
        """Initilization of instance variables
        """
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
        """Appending color sequences to the input string
        """
        output = []

        self.check_diff_type(input)

        for line in input:
            if self.is_info(line):
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

    def is_info(self, line):
        if self.P_TRD_RANGE.match(line) or self.P_UNI_RANGE.match(line):
            return True

        return False

    def check_diff_type(self, input):
        # returns immediately if already know the diff type
        if self.is_traditional_diff_style or self.is_unified_diff_style:
            return

        # first, checking with the range patterns
        for line in input:
            if self.P_TRD_RANGE.match(line):
                self.is_traditional_diff_style = True
                return

            if self.P_UNI_RANGE.match(line):
                self.is_unified_diff_style = True
                return

        # second, with the diff patterns
        for line in input:
            if self.P_TRD_LEFT.match(line) or self.P_TRD_RIGHT.match(line):
                self.is_traditional_diff_style = True
                return

            if self.P_UNI_LEFT.match(line) or self.P_UNI_RIGHT.match(line):
                self.is_unified_diff_style = True
                return

    def diff(self, args):
        diff_cmd = "diff"
        if 'DIFFC_DIFF_CMD' in os.environ:
            diff_cmd = os.environ['DIFFC_DIFF_CMD']

        args.insert(0, diff_cmd)

        result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()

        return result

def signal_handler(signum, frame):
    pass

if __name__ == "__main__":
    d = Diffc()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)

    lines = []
    if len(sys.argv) > 1 :
        lines = d.diff(sys.argv[1:])
    else:
        try : 
            lines = sys.stdin.readlines()
        except IOError:
            print("Interrupted.") 
            exit()

    input = map(lambda x: re.sub("[\r\n]*$","",x), lines)
    output = d.color(input)
    for r in output :
        print(r)

