import error

DIGITS = '.0123456789'
OPREROTS = {'+':'PLS','-':'MIN','*':'MUL','/':'DIV','(':'LPR',')':'RPR'}

class Token:
    '''Token: type-STR value-INT or FLOAT'''
    def __init__(self,type,value=None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        if self.value: return f"{self.type}:{self.value}"
        return f"{self.type}"
    
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.i = 0
        self.current_token = self.tokens[self.i]

    def advance(self):
        self.i += 1
        if self.i < len(self.tokens):
            self.current_token = self.tokens[self.i]
            return self.current_token

    def parse(self):
        return self.exper()

    def factor(self):
        '''factor (single number) - @returns int or float'''
        token = self.current_token
        if token.type in ('PLS','MIN'):
            self.advance()
            value = self.factor()
            if token.type == 'MIN': value *= -1
            return value
        elif token.type == 'LPR':
            self.advance()
            res = self.exper()
            if self.current_token.type == 'RPR':    
                return res
            else:
                return None,error.SyntaxError(f'Expect ")" but {self.current_tok.type} found')
        elif token.type in ('INT','FLOAT'):
            self.advance()
            return token.value
    
    def term(self):
        '''term (multiply and devide) - @returns int or float'''
        left = self.factor()
        opr = self.current_token.type
        while opr in ('MUL','DIV'):
            self.advance()
            right = self.factor()

            if opr == 'MUL':
                left = left * right
            elif opr == 'DIV':
                left = left / right
            
            opr = self.current_token.type
        return left

    def exper(self):
        '''exper (plus and minus) - @returns int or float'''
        left = self.term()
        opr = self.current_token.type
        while opr in ('PLS','MIN'):
            self.advance()
            right = self.term()

            if opr == 'PLS':
                left = left + right
            elif opr == 'MIN':
                left = left - right
            
            opr = self.current_token.type
        return left


def make_number(x, line):
    i = x
    dots = 0
    number = ''
    while line[i] in DIGITS:
        number += line[i]
        if line[i] == '.':dots += 1 
        if dots > 1: return None,None,error.SyntaxError('Unexpected "." found')
        i+=1
        if i >= len(line): break
    if dots > 0:
        return float(number),i-1,None
    else:
        return int(number),i-1,None


def make_tokens(line):
    tokens = []
    i = 0
    while True:
        if i >= len(line): break
        c = line[i]
        
        if c == ' ':
            pass
        elif c in OPREROTS:
            tokens.append(Token(OPREROTS[c]))
        elif c in DIGITS:
            number,i,err = make_number(i,line)
            if not err:
                if isinstance(number,int): tokens.append(Token('INT',number))
                elif isinstance(number,float): tokens.append(Token('INT',number))
            else:
                return None,err
        else:
            return None,error.SyntaxError(f'Invalid Charactor "{c}"')
        i+=1
    return tokens,None


while True:
    inpt = input('> ')
    if inpt == 'exit': break

    tokens,err = make_tokens(inpt)
    if err:
        print(err.as_string())
        continue
    parser = Parser(tokens)
    print(parser.parse())

exit()