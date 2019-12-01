
"""
parser : state -> state
capture : state -> (state, ast)
"""

class Result:
    def __init__(self, state, ast):
        if type(state) != State:
            raise Exception('expected State')

        self.state = state
        self.ast = ast


class State:
    def __init__(self, s, i=0):
        self.s = s
        self.i = i

    def position(self):
        return (self.s, self.i)

    def setIndex(self, i):
        if i <= self.i:
            raise Exception('bad call to setIndex')
        return State(self.s, i)

    def maybeSetIndex(self, i):
        # only call this from things like spaceOptional and pLine

        if i == self.i:
            return self

        return self.setIndex(i)

    def incomplete(self):
        return self.i < len(self.s)

class CaptureManyFailure:
    def __str__(self):
        return 'CaptureManyFailure'

def transform(f, cap):
    def wrapper(state):
        res = cap(state) # transform
        if res is None:
            return
        return Result(res.state, f(res.ast))
    return wrapper

# PARSING HELPERS

def printState(state):
    (s, i) = state.position()
    print('state:\n' + s[i:i+50])

def isBeginWord(s, start):
    return start == 0 or s[start-1].isspace()

def isEndWord(s, end):
    return end >= len(s) or s[end].isspace()

def isWord(s, start, end):
    return isBeginWord(s, start) and isEndWord(s, end)

def tokenChar(s, i):
    if i >= len(s):
        return False

    c = s[i]

    if c.isspace():
        return False

    if c in '()<>-,[]=\\+-*/':
        return False

    return True

def emptyState(state):
    (s, i) = state.position()
    return i == len(s)

def peek(state, kw):
    (s, i) = state.position()
    return s[i:i+len(kw)] == kw

def readline(s, i):
    while i < len(s) and s[i] != '\n':
        i += 1

    # skip over blank lines and leading space
    while i < len(s) and s[i].isspace():
        i += 1
    return i

def indentLevel(s, i):
    if i >= len(s) or s[i] == '\n':
        return 0

    while i >= 0 and s[i] != '\n':
        i -= 1

    i += 1

    n = 0
    while i < len(s) and s[i] != '\n' and s[i].isspace():
        i += 1
        n += 1

    return n


# PARSING

def token(state):
    (s, i) = state.position()

    if not tokenChar(s, i):
        return

    while tokenChar(s, i):
        i += 1
    return state.setIndex(i)

def pChar(c):
    if len(c) != 1:
        raise Exception('pChar wants single character')

    def wrapper(state):
        (s, i) = state.position()
        if i >= len(s) or s[i] != c:
            return

        return state.setIndex(i+1)

    return wrapper

def parseAll(state):
    (s, i) = state.position()
    return state.setIndex(len(s))

def parseOperator(operators):
    def wrapper(state):
        (s, i) = state.position()
        for operator in operators:
            if peek(state, operator):
                return state.setIndex(i + len(operator))

    return wrapper

def spaceOptional(state):
    (s, i) = state.position()

    while i < len(s) and s[i].isspace():
        i += 1

    return state.maybeSetIndex(i)

def spaceRequired(state):
    (s, i) = state.position()

    iOrig = i

    while i < len(s) and s[i].isspace():
        i += 1

    if i == iOrig:
        return

    return state.setIndex(i)


def pKeyword(kw):
    if kw != kw.strip():
        raise Exception('do not pad until keywords; we already check boundaries')
    n = len(kw)

    def wrapper(state):
        (s, i) = state.position()
        iEnd = i + n
        if s[i : iEnd] == kw:
            if isWord(s, i, iEnd):
                return state.setIndex(iEnd)
    return wrapper

def pUntil(kw):
    if kw == '\n':
        raise Exception('use pLine for detecting end of line')
    if kw != kw.strip():
        raise Exception('do not pad until keywords; we already check boundaries')
    n = len(kw)

    def wrapper(state):
        (s, i) = state.position()
        while i < len(s):
            iEnd = i + n
            if s[i:iEnd] == kw:
                if isWord(s, i, iEnd):
                    return state.setIndex(i)
            i += 1
    return wrapper

def pLine(state):
    (s, i) = state.position()
    while i < len(s):
        if s[i] == '\n':
            return state.maybeSetIndex(i)
        i += 1
    # end of file is equivalent to newline
    return state.maybeSetIndex(i)

def parseMyLevel(state):
    (s, i) = state.position()

    level = indentLevel(s, i)

    i = readline(s, i)

    while i < len(s) and indentLevel(s, i) >= level:
        i = readline(s, i)

    return state.setIndex(i)

def parseBlock(state):
    (s, i) = state.position()
    level = indentLevel(s, i)

    i = readline(s, i)

    while i < len(s) and indentLevel(s, i) > level:
        i = readline(s, i)

    return state.setIndex(i)

def onlyIf(parse1, parse2):
    def wrapper(state):
        if parse1(state) is None:
            return
        return parse2(state)
    return wrapper

def parseKeywordBlock(keyword):
    def wrapper(state):
        state = spaceOptional(state)
        if state is None:
            return
        return onlyIf(
            pKeyword(keyword),
            parseBlock
            )(state)
    return wrapper

# CAPTURE

def captureUnReservedWord(reservedWords):
    def wrapper(state):
        state = spaceOptional(state)
        for word in reservedWords:
            if peek(state, word):
                return

        return grab(token)(state)

    return wrapper

def captureRange(start, end):
    return captureStuff(
            skip(pKeyword(start)),
            grab(pUntil(end)),
            skip(pKeyword(end))
            )

def captureSeq(start, delim, end, fCaptureItem):
    pStart = pChar(start)
    pDelim = pChar(delim)
    pEnd = pChar(end)


    def wrapper(state):
        state = spaceOptional(state)
        state = pStart(state)
        if state is None:
            return

        state = spaceOptional(state)

        ast = []
        while True:
            if peek(state, end):
                break

            res = fCaptureItem(state)
            if res is None:
                return

            ast.append(res.ast)
            state = res.state
            state = spaceOptional(state)

            if peek(state, delim):
                state = pDelim(state)
                state = spaceOptional(state)
                continue

            if peek(state, end):
                break

            return

        state = pEnd(state)
        state = spaceOptional(state)
        return Result(state, ast)

    return wrapper

def captureSubBlock(keyword, f):
    parse1 = pKeyword(keyword)

    def wrapper(state):
        state = spaceOptional(state)
        state = parse1(state)
        if state is None:
            return

        state = spaceOptional(state)

        return twoPass(parseMyLevel, f)(state)

    return wrapper

def twoPass(parse, f):
    def wrapper(state):
        (s, iOrig) = state.position()
        newState = parse(state)
        if newState is None:
            return None

        (s, i) = newState.position()
        blockText = s[iOrig:i]
        subState = State(blockText, 0)
        res = f(subState) # twoPass
        if res is None:
            return None

        state = spaceOptional(res.state)
        if not emptyState(state):
            return

        return Result(newState, res.ast)

    return wrapper

def grab(parse):

    def f(state):
        (s, iOrig) = state.position()
        newState = parse(state)
        if newState is None:
            return
        (_, iNew) = newState.position()
        text = s[iOrig:iNew]
        return Result(newState, text)

    return f

def skipManyCaptures(f):
    def wrapper(state):
        while True:
            res = f(state)
            if res is None:
                break
            state = res.state
        return Result(state, Skip())

    return wrapper

def skip(parse):
    def f(state):
        newState = parse(state) #skip
        if newState is None:
            return
        return Result(newState, Skip())

    return f

def captureZeroOrMore(f):
    def wrapper(state):
        asts = []
        while True:
            state = spaceOptional(state)

            if peek(state, 'STOP'):
                break

            res = f(state)
            if res is None: break
            state = res.state
            asts.append(res.ast)

        asts = noSkips(asts)
        return Result(state, asts)
    return wrapper

def captureOneOrMore(f):
    def wrapper(state):
        asts = []
        while True:
            state = spaceOptional(state)

            if peek(state, 'STOP'):
                break

            res = f(state)
            if res is None: break
            state = res.state
            asts.append(res.ast)

        if len(asts) == 0:
            return

        asts = noSkips(asts)
        return Result(state, asts)
    return wrapper

def noSkips(asts):
    return [a for a in asts if type(a) != Skip]

def fixAsts(asts):
    asts = noSkips(asts)
    if len(asts) == 1:
        return asts[0]
    return asts

def captureStuff(*fns):
    def wrapper(state):

        asts = []
        for fn in fns:
            state = spaceOptional(state)
            res = fn(state) # captureStuff
            if res is None:
                return
            state = res.state
            asts.append(res.ast)

        state = spaceOptional(state)

        ast = fixAsts(asts)
        return Result(state, ast)
    return wrapper

class Skip:
    pass

def captureOneOf(*fns):
    def wrapper(state):
        state = spaceOptional(state)
        for fn in fns:
            res = fn(state) # captureOneOf
            if res is not None:
                return res
    return wrapper

def captureUntilKeyword(keyword, fCapture):
    return \
        captureStuff(
            twoPass(
                pUntil(keyword),
                fCapture
                ),
            skip(pKeyword(keyword)),
            )

def captureKeywordBlock(keyword):
    return captureStuff(
        grab(parseKeywordBlock(keyword)),
        )

def captureOperator(operators):
    return grab(parseOperator(operators))

