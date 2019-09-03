import json
import re
import nltk

from feature_extraction.lexer import Lexer
from feature_extraction.function_features import FunctionFeatures
from keyword_frequency import keyword_frequency

op_list = [r'\+', r'-', r'\*', r'/', r'%', r'&', r'\|', r'~', r'\^', r'<<', r'>>',
           r'&&', r'\|\|', r'!', r'<', r'>', r'<=', r'>=', r'==', r'(!=(?!=))|(<>)', r'===',
           r'!==', r'=', r'\*=', r'/=', r'%=', r'\+=', r'-=', r'<<=', r'>>=', r'&=',
           r'\|=', r'\^=', r'\.=', r'\+\+', r'--', r'=>', r'::', r'\(', r'\)', r'\$',
           r',', r'\.(?!\d|=)', r'\?', r':', r';', r'@', r'\\', r'\n', r'\[', r'\]',
           r'\{', r'\}', r' ', r'\t', r'\'', r'\"']

# ------------------------------------HELPER FUNCTIONS----------------------------------------------------------
# def flatten(S):
#     if S == []:
#         return S
#     if isinstance(S[0], list):
#         return flatten(S[0]) + flatten(S[1:])
#     return S[:1] + flatten(S[1:])

def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i


def make_list_of_strings(d):
    list_of_strings = []
    for key, value in d.iteritems():
        for i in range(len(value)):
            list_of_strings.append(key)
    return list_of_strings


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

#---------------------------------------------------------------------------------------------------------------


class FeatureExtractor(object):

    def __init__(self, input_file):
        self.input_file = input_file
        lex = Lexer(input_file)
        lexer_dict, number_of_lines, number_of_chars = lex.lexer_output_to_dict()
        # with open('outputs/lexer_output_2.json', "w") as fout:
        #     json.dump(lexer_dict, fout, indent=2, separators=(',', ':'))
        self.lexer_dict = lexer_dict
        self.num_of_chars = number_of_chars
        self.num_of_lines = number_of_lines

    def extract_features(self):
        feature_dict = {}
        # with open(self.input_file, "r") as fin:
        #     _file = fin.read()
        # with open(self.input_file, "a") as fin:
        #     if not _file.rstrip(" ").rstrip("\n").endswith("?>"):
        #         fin.write("?>")
        with open(self.input_file, "r") as fin:
            _file = fin.read().rstrip()

        #-----------------------------NUMBER OF LINES-----------------------------------------------------------

        feature_dict["number_of_lines"] = self.num_of_lines

        #-----------------------------LENGTH IN CHARACTERS------------------------------------------------------

        feature_dict["length_in_characters"] = self.num_of_chars

        #-----------------------------CHARACTERS PER LINE-------------------------------------------------------

        if self.num_of_lines == 0:
            characters_per_line = 0
        else:
            characters_per_line = self.num_of_chars / self.num_of_lines

        feature_dict["characters_per_line"] = characters_per_line

        #-----------------------------NUMBER OF STRINGS---------------------------------------------------------

        if "CONSTANT_ENCAPSED_STRING" in self.lexer_dict:
            strings1 = make_list_of_strings(self.lexer_dict[ "CONSTANT_ENCAPSED_STRING"])
            strings1 = [value.rstrip("\'\"").lstrip("\"\'") for value in strings1]
        else:
            strings1 = []
        if "ENCAPSED_AND_WHITESPACE" in self.lexer_dict:
            strings2 = make_list_of_strings(self.lexer_dict["ENCAPSED_AND_WHITESPACE"])
        else:
            strings2 = []
        if "STRING" in self.lexer_dict:
            strings3 = make_list_of_strings(self.lexer_dict["STRING"])
        else:
            strings3 = []

        strings = list(flatten(map(nltk.word_tokenize, strings1 + strings2 + strings3)))

        feature_dict["number_of_strings"] = len(strings)

        #-----------------------------NUMBER OF HEX/OCTAL NUMBERS--------------------------------------------------------

        hex_oct_pattern = re.compile(r"(0?[xX][0-9a-fA-F]+)|(0[0-7]+)")
        hex_oct_numbers = []
        if "LNUMBER" in self.lexer_dict:
            for number in self.lexer_dict["LNUMBER"]:
                if hex_oct_pattern.match(number):
                    hex_oct_numbers.append(number)

        feature_dict["number_hex_octal_numbers"] = len(hex_oct_numbers) #search for hex and octal only in numbers, it may should saerch in strings, variables, function names etc

        #-----------------------------NUMBER OF UNICODE SYMBOLS--------------------------------------------------------

        # unicode_pattern = re.compile(r"[u]\s*['].+[']|[u][\"].+[\"]") #should consider multi-line strings
        # unicode_strings = re.finditer(unicode_pattern, _file)
        # hex_oct_strings = re.finditer(hex_oct_pattern, _file)
        # hex_oct_strings = [x.group(0) for x in hex_oct_strings]
        # unicode_strings = [x.group(0) for x in unicode_strings]
        # unicode_strings = [x[2:-1] for x in unicode_strings]
        # number_of_unicode_chars = 0
        # if unicode_strings:
        #     number_of_unicode_chars = reduce(lambda x, y:  x + y, [len(x) for x in unicode_strings])
        number_of_unicode_chars = 0
        for word in _file.split():
            for char in word:
                if ord(char) > 127:
                    number_of_unicode_chars += 1

        feature_dict["number_of_unicode_symbols"] = number_of_unicode_chars

        #-----------------------------AVERAGE STRING LENGTH--------------------------------------------------------

        if len(strings) != 0:
            all_strings_length = reduce(lambda x, y:  x + y, [len(x) for x in strings])
            feature_dict["average_string_length"] = float(all_strings_length) / len(strings)
        else:
            feature_dict["average_string_length"] = 0

        #-----------------------------PERCENTAGE OF WHITESPACES--------------------------------------------------------

        whitespaces = 0
        if "WHITESPACE" in self.lexer_dict:
            for key, value in self.lexer_dict["WHITESPACE"].iteritems():
                whitespaces += key.count(" ") * len(value)

        feature_dict["percentage_of_whitespaces"] = float(whitespaces) / self.num_of_chars

        #-----------------------------NUMBER OF COMMENTS--------------------------------------------------------

        number_of_comments = 0
        if "COMMENT" in self.lexer_dict:
            number_of_comments = len(self.lexer_dict["COMMENT"]) #should consider multi-line comments
        feature_dict["number_of_comments"] = number_of_comments

        #-----------------------------AVERAGE COMMENTS PER LINE-------------------------------------------------

        feature_dict["average_comments_per_line"] = float(number_of_comments) / self.num_of_lines

        #-----------------------------NUMBER OF WORDS-----------------------------------------------------------

        op_str = "|".join(op_list)
        words = [x.strip(" ") for x in re.split(op_str, _file) if (x is not None and x != "" and x != "\n")]
        feature_dict["number_of_words"] = len(words)

        #-----------------------------PERCENTAGE OF WORDS NOT IN COMMENTS---------------------------------------

        if "COMMENT" in self.lexer_dict:
            file_without_comments = _file
            comments = flatten([x.split(r"\n") for x in self.lexer_dict["COMMENT"]])
            for comment in comments:
                file_without_comments = file_without_comments.replace(comment, "")
            words_without_comments = [x.strip(" ") for x in re.split(op_str, file_without_comments)
                                      if (x is not None and x != "" and x != "\n")]
            percentage_of_words_not_in_comments = (float(len(words_without_comments)) / len(words)) * 100
            feature_dict["percentage_of_words_not_in_comments"] = percentage_of_words_not_in_comments
        else:
            feature_dict["percentage_of_words_not_in_comments"] = 100

        #-----------------------------------PERCENATGE OF HUMAN READABLE WORDS--------------------------------------

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

        feature_dict["percentage_of_human_readables"] = (float(readables) / len(words)) * 100

        #-----------------------------NUMBER OF FUNCTION CALLS--------------------------------------------------

        parser = FunctionFeatures(self.input_file)
        feature_dict["number_of_function_calls"] = parser.count_function_calls()

        #-----------------------------AVERAGE ARGUMENT LENGTH---------------------------------------------------

        feature_dict["average_argument_length"] = parser.compute_avg_argument_length()

        # keyword_frequency_dict = keyword_frequency(self.input_file)
        # feature_dict.update(keyword_frequency_dict)

        return feature_dict



