import os
import sys
import json

import ply.lex as lex
from phply import phplex


class Lexer(object):

    def __init__(self, input_file):
        self.input_file = input_file

    def find_tok_value(self, line):
        indexes = [pos for pos, char in enumerate(line) if char == ","]
        start = indexes[0] + 1
        end = indexes[-2] - 1
        return line[start: end + 1].strip("'")

    def find_all_functions(self, lexer_dict, php_functions):
        if "FUNCTION" not in lexer_dict.keys():
            lexer_dict["FUNCTION"] = {}

        if "STRING" in lexer_dict.keys():
            to_be_deleted = []
            for variable, values in lexer_dict["STRING"].iteritems():
                if variable in php_functions:
                    if variable in lexer_dict["FUNCTION"].keys():
                        lexer_dict["FUNCTION"][variable] += values
                    else:
                        lexer_dict["FUNCTION"][variable] = values
                    to_be_deleted.append(variable)

            for variable in to_be_deleted:
                del lexer_dict["STRING"][variable]

    def lexer_output_to_dict(self):
        with open(os.path.join("php_functions", "php_function_list.json"), "r") as f:
            php_functions = json.load(f)
        with open(self.input_file, "r") as fin:
            old_stdout = sys.stdout
            sys.stdout = open("lexer_output.txt", "w")
            lex.runmain(lexer=phplex.full_lexer, data=fin.read().rstrip())
            sys.stdout = old_stdout
        linepos = 0
        lineno = 0
        f = open("lexer_output.txt", "r")
        lexer_dict = {}
        for line in f.readlines():
            toks = line.split(",")
            linepos = int(toks[-1].rstrip(")\n"))
            lineno = int(toks[-2])
            toktype = toks[0].lstrip("(")
            tokvalue = self.find_tok_value(line)
            if toktype not in lexer_dict.keys():
                lexer_dict[toktype] = {}
                lexer_dict[toktype][tokvalue] = [(lineno, linepos)]
            else:
                if tokvalue not in lexer_dict[toktype].keys():
                    lexer_dict[toktype][tokvalue] = [(lineno, linepos)]
                else:
                    lexer_dict[toktype][tokvalue].append((lineno, linepos))
        self.find_all_functions(lexer_dict, php_functions)
        number_of_lines = int(lineno)
        number_of_chars = int(linepos)
        return lexer_dict, number_of_lines, number_of_chars

