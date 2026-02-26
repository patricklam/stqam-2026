def crash_midterm(inp:str) -> None:
    c = 0
    if len(inp) == 0:
        return
    if inp[0] >= '1' and inp[0] <= '9':
        c = int(inp[0])
    if c+4 <= len(inp) and inp[c] == '%':
        if inp[c+1] == '*':
            if inp[c+2] == '&':
                if inp[c+3] == '<':
                    raise Exception()

