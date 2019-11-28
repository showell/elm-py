
"""
parser : state -> state
capture : state -> (state, ast)
"""

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

class CaptureManyFailure:
    def __str__(self):
        return 'CaptureManyFailure'

def printState(state):
    (s, i) = state.position()
    print('state:\n' + s[i:i+50])

def transform(f, cap):

    def wrapper(state):
        res = cap(state) # transform
        if res is None:
            return
        state, ast = res
        return state, f(ast)
    return wrapper

def tokenChar(s, i):
    if i >= len(s):
        return False

    c = s[i]

    if c.isspace():
        return False

    if c in '(),[]=\\':
        return False

    return True

def parseAll(state):
    (s, i) = state.position()
    return state.setIndex(len(s))

def bigSkip(*fns):
    def wrapper(state):
        state = spaceOptional(state)
        for fn in fns:
            state = fn(state)
            if state is None: return
        state = spaceOptional(state)
        return state
    return wrapper

def captureSubBlock(keyword, f):
    def wrapper(state):
        state = bigSkip(
                spaceOptional,
                pKeyword(keyword),
                pLine,
                spaceOptional
                )(state)
        if not state:
            return

        return twoPass(parseMyLevel, f)(state)

    return wrapper

def parseSameLine(parse):
    return twoPassParse(
            pLine,
            parse)

def twoPassParse(parse1, parse2):
    def wrapper(state):
        (s, iOrig) = state.position()
        state1 = parse1(state)
        if state1 is None:
            return None

        (s, iEnd) = state1.position()

        lineText = s[iOrig:iEnd]
        subState = State(lineText, 0)

        state2 = parse2(subState)
        if state2 is None:
            return None

        (_, n) = state2
        return state.setIndex(iOrig + n)

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

        _, ast = res
        return (newState, ast)

    return wrapper

def grab(parse):

    def f(state):
        (s, iOrig) = state.position()
        newState = parse(state)
        if newState is None:
            return
        (_, iNew) = newState.position()
        text = s[iOrig:iNew]
        return (newState, text)

    return f

def skipManyCaptures(f):
    def wrapper(state):
        while True:
            res = f(state)
            if res is None:
                break
            state, _ = res
        return (state, Skip())

    return wrapper

def skip(parse):
    def f(state):
        newState = parse(state)
        if newState is None:
            return
        return (newState, Skip())

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
            state, ast = res
            asts.append(ast)

        asts = noSkips(asts)
        return (state, asts)
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
            state, ast = res
            asts.append(ast)

        if len(asts) == 0:
            return

        asts = noSkips(asts)
        return (state, asts)
    return wrapper

def noSkips(asts):
    return [a for a in asts if type(a) != Skip]

def fixAsts(asts):
    asts = noSkips(asts)
    if len(asts) == 1:
        return asts[0]
    return asts

def captureSeq(*fns):
    def wrapper(state):
        state = spaceOptional(state)

        asts = []
        for fn in fns:
            res = fn(state) # captureSeq
            if res is None:
                return
            state, ast = res
            if type(state) != State:
                print(fn)
                raise Exception('misconfigured')
            asts.append(ast)

        ast = fixAsts(asts)
        return (state, ast)
    return wrapper

class Skip:
    pass

def captureOneOf(*fns):
    def wrapper(state):
        for fn in fns:
            res = fn(state) # captureOneOf
            if res is not None:
                return res
    return wrapper

def peek(state, kw):
    (s, i) = state.position()
    return s[i:i+len(kw)] == kw

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

def pUntilIncluding(kw):
    if kw != kw.strip():
        raise Exception('do not pad until keywords')

    n = len(kw)

    def wrapper(state):
        (s, i) = state.position()
        while i < len(s):
            iEnd = i + n
            if s[i:iEnd] == kw:
                if isWord(s, i, iEnd):
                    return state.setIndex(iEnd)
            i += 1
    return wrapper

def pUntil(kw):
    if kw == '\n':
        raise Exception('use pLine for detecting end of line')
    if len(kw) == 1:
        raise Exception('use pUntilIncludingChar for single characters')
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

def pUntilLineEndsWith(kw):
    if kw == '\n':
        raise Exception('use pLine for detecting end of line')
    if kw != kw.strip():
        raise Exception('do not pad until keywords')
    kw = ' ' + kw
    n = len(kw)

    def wrapper(state):
        (s, i) = state.position()
        while i < len(s) and s[i] != '\n':
            i += 1
        if s[i-n:i] == kw:
            return state.setIndex(i-n+1)
    return wrapper

def pUntilChar(c):
    def wrapper(state):
        (s, i) = state.position()
        while i < len(s):
            if s[i] == c:
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

def isBeginWord(s, start):
    return start == 0 or s[start-1].isspace()

def isEndWord(s, end):
    return end >= len(s) or s[end].isspace()

def isWord(s, start, end):
    return isBeginWord(s, start) and isEndWord(s, end)

def token(state):
    (s, i) = state.position()

    if not tokenChar(s, i):
        return

    while tokenChar(s, i):
        i += 1
    return state.setIndex(i)

def readline(s, i):
    while i < len(s) and s[i] != '\n':
        i += 1

    # skip over blank lines
    while i < len(s) and s[i].isspace():
        i += 1
    return i

def indentLevel(s, i):
    if s[i].isspace():
        raise Exception('expected nonspace')
    i -= 1
    n = 0
    while i >= 0 and s[i] != '\n':
        n += 1
        if not s[i].isspace():
            raise Exception('expected space')
        i -= 1

    return n


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

def captureUntilKeywordEndsLine(keyword, fCapture):
    return \
        captureSeq(
            twoPass(
                pUntilLineEndsWith(keyword),
                fCapture
                ),
            skip(spaceOptional),
            skip(pKeyword(keyword)),
            skip(spaceOptional),
            )

def captureKeywordBlock(keyword):
    return captureSeq(
        grab(parseKeywordBlock(keyword)),
        skip(spaceOptional))

def parseRange(start, end):
    return bigSkip(
            spaceOptional,
            pKeyword(start),
            pUntilIncluding(end),
            spaceOptional
            )

