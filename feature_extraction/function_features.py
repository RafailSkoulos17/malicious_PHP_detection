import re

from phply.phpast import resolve_magic_constants
from phply.phpparse import make_parser
from phply import phplex


class FunctionFeatures(object):

    def __init__(self, input_file):
        self.input_file = input_file

    def count_function_calls(self):
        # with open(self.input_file, "r") as fin:
        #     _file = fin.read()
        # with open(self.input_file, "a") as fin:
        #     if not _file.rstrip(" ").rstrip("\n").endswith("?>"):
        #         fin.write("?>")
        with open(self.input_file, "r") as fin:
            _file = fin.read()
        parser = make_parser()

        lexer = phplex.lexer.clone()
        lexer.filename = self.input_file.replace("\\", "/")
        output = parser.parse(_file, lexer=lexer)
        try:
            resolve_magic_constants(output)
            function_calls = str(output).count("FunctionCall")
        except RuntimeError:
            function_calls = None
        return function_calls

    def compute_avg_argument_length(self):
        # with open(self.input_file, "r") as fin:
        #     _file = fin.read()
        # with open(self.input_file, "a") as fin:
        #     if not _file.rstrip(" ").rstrip("\n").endswith("?>"):
        #         fin.write("?>")
        with open(self.input_file, "r") as fin:
            _file = fin.read()
        parser = make_parser()
        lexer = phplex.lexer.clone()
        lexer.filename = self.input_file
        output = parser.parse(_file, lexer=lexer)
        try:
            resolve_magic_constants(output)
        except RuntimeError:
            avg_length_of_arguments_to_function = None
            return avg_length_of_arguments_to_function
        indexes = [m.end() for m in re.finditer('FunctionCall', str(output))]
        func_args = []
        for index in indexes:
            pars = 1
            count = 0
            for char in str(output)[index+1:]:
                count += 1
                if char == '(':
                    pars += 1
                elif char == ')':
                    pars -= 1
                if pars == 0:
                    func_args.append(str(output)[index:index+count+1])
                    break
        functions = []
        for func in func_args:
            for ind, char2 in enumerate(func):
                if char2 == "'":
                    function_name = ""
                    for char in func[ind + 1:]:
                        if char == "'":
                            break
                        function_name += char
                    functions.append(function_name)
                    break

        functions = list(set(functions))
        functions = [x for x in functions if not x.startswith("$")]
        func_dict = {}
        for func in functions:
            indexes = [(m.start(), m.end()) for m in re.finditer(func, _file)]
            func_dict[func] = indexes

        for key, value in func_dict.iteritems():
            for tup in value:
                start_char = tup[0]
                if _file[start_char - 9:start_char - 1] == "function":
                    func_dict[key].remove(tup)
        func_args_dict = {}
        for key, value in func_dict.iteritems():
            func_args_dict[key] = []
            for tup in value:
                end_line = tup[1]
                pars = 1
                count = 0
                arguments = ""
                for char in _file[end_line+1:]:
                    count += 1
                    if char == '(':
                        pars += 1
                    elif char == ')':
                        pars -= 1
                    if pars == 0:
                        arguments = _file[end_line+1:end_line+count]
                        break
                func_args_dict[key].append(arguments)
        total_length = 0
        for key, value in func_args_dict.iteritems():
            for arg in value:
                total_length += len(arg)
        if len(func_args_dict) == 0:
            avg_length_of_arguments_to_function = 0
        else:
            avg_length_of_arguments_to_function = float(total_length) / len(func_args_dict)
        return avg_length_of_arguments_to_function

# if __name__ == "__main__":
#     p = Parser("../inputs/sample_file_2.php")
#     p.count_function_calls()
