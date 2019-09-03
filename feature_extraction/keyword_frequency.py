keywords = ['__halt_compiler', 'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch',
           'class', 'clone', 'const', 'continue', 'declare', 'default', 'die', 'do', 'echo', 'else',
           'elseif', 'empty', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile',
           'eval', 'exit', 'extends', 'final', 'for', 'foreach', 'function', 'global', 'goto', 'if',
           'implements', 'include', 'include_once', 'instanceof', 'insteadof', 'interface', 'isset',
           'list', 'namespace', 'new', 'or', 'print', 'private', 'protected', 'public', 'require',
           'require_once', 'return', 'static', 'switch', 'throw', 'trait', 'try', 'unset', 'use',
           'var', 'while', 'xor']


def keyword_frequency(input_file):
    with open(input_file, "r") as f:
        _file = f.read()

    total = 0
    keyword_counter = {}
    for keyword in keywords:
        occurrences = _file.count(keyword)
        keyword_counter["keyword_" + keyword] = occurrences
        total += occurrences

    if total == 0:
        for keyword, occ in keyword_counter.iteritems():
            keyword_counter[keyword] = 0
    else:
        for keyword, occ in keyword_counter.iteritems():
            keyword_counter[keyword] = float(keyword_counter[keyword]) / total
    return keyword_counter
