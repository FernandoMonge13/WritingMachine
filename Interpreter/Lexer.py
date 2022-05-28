from sly import Lexer

class BasicLexer(Lexer):
    errores = []

    tokens = { NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, PARA, TO, ARROW, EQEQ, SUMA}
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' , '[', ']'}

    #Tokens
    #Las siguentes son todas expresiones regulares
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FOR = r'FOR'
    PARA = r'PARA'
    TO = r'TO'
    ARROW = r'->'
    #NAME = r'[a-z][a-zA-Z0-9_]*'
    NAME = r'[a-z][a-zA-Z0-9_]{2,9}'
    STRING = r'\".*?\"'
    SUMA = r'Add'
    #UNO = r'1'

    EQEQ = r'=='

    #r'\d+' : expresion regular para uno o mas digitos
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    #r'#.*' : expresion regular para el simbolo de comentario y lo que siga
    @_(r'//.*')
    def COMMENT(self, t):
        pass

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
