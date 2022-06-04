from sly import Lexer

class BasicLexer(Lexer):

    tokens = {NAME, NUMBER, STRING, IF, IFELSE, PARA, EQEQ,
              SUMA, MULT, DIV, SUBSTR, RANDOM, ADD, DEF, PUT, TRUE, FALSE, EQUAL,
              AND, OR, GREATER, SMALLER, FIN, COMMENT, PRINT}
    ignore = '\t '

    literals = {'=', '+', '-', '/', '*', '(', ')', ',', ';' , '[', ']', '<', '>'}

    #Tokens
    #Las siguentes son todas expresiones regulares
    # PARAMETROS = r'([a-zA-Z0-9_@]{2,9},\s?)+'
    # PARAMETROS = r'\[\s*([a-zA-Z0-9_@]{2,9})(,(\s?)*[a-zA-Z0-9_@]{2,9})+\s*\]'

    IF = r'If'
    IFELSE = r'ELSE'
    PARA = r'PARA'
    FIN = r'FIN'
    NAME = r'[a-z][a-zA-Z0-9_@]{2,9}'
    STRING = r'\".*?\"'

    TRUE = r'TRUE'
    FALSE = r'FALSE'

    DEF = r'Def'
    ADD = r'Add'
    PUT = r'Put'

    SUMA = r'Sum'
    MULT = r'Mult'
    DIV = r'Div'
    SUBSTR = r'Substr'
    RANDOM = r'Random'
    GREATER = r'Greater'
    SMALLER = r'Smaller'

    EQUAL = r'Equal'
    EQEQ = r'=='
    AND = r'And'
    OR = r'Or'

    COMMENT = r'//.*'
    PRINT = r'PrintLine'

    #r'\d+' : expresion regular para uno o mas digitos
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    #r'\d+' : expresion regular para uno o mas digitos
    @_(r'[+-]?([0-9]*[.])?[0-9]+')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    #r'#.*' : expresion regular para el simbolo de comentario y lo que siga
    @_('COMMENT')
    def COMMENT(self, t):
        return t

    #r'\n+' : expresion regular para salto de linea
    @_(r'\n+')
    def newline(self,t ):
        self.lineno = t.value.count('\n')

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print("Undefined name '%s'" % p.NAME)
            return 0

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1


if __name__ == '__main__':
    lexer = BasicLexer()
    env = {}
    while True:
        try:
            text = input('basic > ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            try:
                for token in lex:
                    print(token)
            except EOFError:
                break
