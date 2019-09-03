import json
import os
import re
from pprint import pprint

op_list = [r'\+', r'-', r'\*', r'/', r'%', r'&', r'\|', r'~', r'\^', r'<<', r'>>',
           r'&&', r'\|\|', r'!', r'<', r'>', r'<=', r'>=', r'==', r'(!=(?!=))|(<>)', r'===',
           r'!==', r'=', r'\*=', r'/=', r'%=', r'\+=', r'-=', r'<<=', r'>>=', r'&=',
           r'\|=', r'\^=', r'\.=', r'\+\+', r'--', r'=>', r'::', r'\(', r'\)', r'\$',
           r',', r'\.(?!\d|=)', r'\?', r':', r';', r'@', r'\\', r'\n', r'\[', r'\]',
           r'\{', r'\}', r' ', r'\t', r'\'', r'\"']

keywords = ['__halt_compiler', 'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch',
            'class', 'clone', 'const', 'continue', 'declare', 'default', 'die', 'do', 'echo', 'else',
            'elseif', 'empty', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile',
            'eval', 'exit', 'extends', 'final', 'for', 'foreach', 'function', 'global', 'goto', 'if',
            'implements', 'include', 'include_once', 'instanceof', 'insteadof', 'interface', 'isset',
            'list', 'namespace', 'new', 'or', 'print', 'private', 'protected', 'public', 'require',
            'require_once', 'return', 'static', 'switch', 'throw', 'trait', 'try', 'unset', 'use',
            'var', 'while', 'xor']

language_constructs = ['__halt_compiler', 'clone', 'die', 'echo', 'empty',
                       'eval', 'exit', 'include', 'include_once', 'isset', 'list', 'print', 'require',
                       'require_once', 'unset']

with open(os.path.join("php_functions", "php_function_list.json"), "r") as f:
    predefined_functions = json.load(f)


ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def find_number_of_repetitions(word):
    chars = list(word)
    max_reps = 1
    for index, char in enumerate(chars):
        reps = 1
        for next_char in chars[index + 1:]:
            if next_char == char:
                reps += 1
            else:
                break
        if reps > max_reps:
            max_reps = reps
    return max_reps

class FunctionOccurences(object):

    def __init__(self, input_file):
        self.input_file = input_file

    def get_occurences_per_function(self):
        with open(self.input_file, "r") as fin:
            _file = fin.read().rstrip()
        all_functions = predefined_functions + language_constructs
        function_counter = {}
        for func in all_functions:
            # occurrences = _file.count(func)
            # if occurrences != 0:
            # #     function_counter["keyword_" + func] = occurrences
            indexes = [(m.start(), m.end()) for m in re.finditer(func, _file)]
            func_occ = 0
            for tup in indexes:
                if _file[tup[0] - 1] not in ascii_letters and _file[tup[1]] not in ascii_letters:
                    func_occ += 1
            if func_occ:
                function_counter[func] = func_occ
        return function_counter

    def get_occurences_in_percentage_per_function(self):
        with open(self.input_file, "r") as fin:
            _file = fin.read().rstrip()
        all_functions = predefined_functions + language_constructs
        function_counter = {}
        total = 0
        for func in all_functions:
            # occurrences = _file.count(func)
            # if occurrences != 0:
            # #     function_counter["keyword_" + func] = occurrences
            indexes = [(m.start(), m.end()) for m in re.finditer(func, _file)]
            func_occ = 0
            for tup in indexes:
                if _file[tup[0] - 1] not in ascii_letters and _file[tup[1]] not in ascii_letters:
                    func_occ += 1
                    total += 1
            if func_occ:
                function_counter[func] = func_occ
        for func, count in function_counter.iteritems():
            function_counter[func] = float(count) / total
        return function_counter

    def get_all_function_used(self):
        with open(self.input_file, "r") as fin:
            _file = fin.read().rstrip()
        all_functions = predefined_functions + language_constructs
        function_list = []
        for func in all_functions:
            indexes = [(m.start(), m.end()) for m in re.finditer(func, _file)]
            func_occ = 0
            for tup in indexes:
                if _file[tup[0] - 1] not in ascii_letters and _file[tup[1]] not in ascii_letters:
                    func_occ += 1
                    break
            if func_occ:
                function_list.append(func)
        return function_list

    def find_human_readables(self):

        with open(self.input_file, "r") as fin:
            _file = fin.read().rstrip()
        op_str = "|".join(op_list)
        words = [x.strip(" ") for x in re.split(op_str, _file) if (x is not None and x != "" and x != "\n")]

        readables = 0
        for word in words:
            chars = len(word)

            alphabetic_chars = re.findall('[a-zA-Z]', word)
            percentage_of_alphabetical = (float(len(alphabetic_chars)) / chars) * 100
            is_alphabetical_ok = percentage_of_alphabetical > 70

            vowels = re.findall('[AaEeIiOoUuYy]', word)
            percentage_of_vowels = (float(len(vowels)) / chars) * 100
            is_vowel_ok = percentage_of_vowels > 20 and percentage_of_vowels < 60

            is_length_ok = chars < 15

            is_repetitions_ok = find_number_of_repetitions(word) < 3

            if is_alphabetical_ok and is_vowel_ok and is_length_ok and is_repetitions_ok:
                readables += 1

        return (float(readables) / len(words)) * 100

        # if __name__=='__main__':
    #
    #     funcs = get_them()
    #     pprint(funcs)
