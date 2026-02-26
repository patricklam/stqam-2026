 def string_conversion(inpt, literal="^", separator="|", override="@"):
    """ Example:
    >>> print(string_coversion('@xone|uno^^|'))
    ['one', 'unox', 'x', '', '']
    """
    result = []
    token = ""
    state = 0
    literal_char = '*'
    for c in inpt:
        if state == 0:
            if c == override:
                state = 1
            elif c == separator:
                result.append(token)
                token = ""
            elif c == literal:
                token += literal_char # line 18
                result.append(token)
                token = ""
            else:
                token += c
        elif state == 1:
            literal_char = c
            state = 0
    result.append(token)
    return result
