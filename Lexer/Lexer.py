from sly import Lexer

class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ }
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    #Tokens
    #Las siguentes son todas expresiones regulares
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FOR = r'FOR'
    FUN = r'FUN'
    TO = r'TO'
    ARROW = r'->'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    EQEQ = r'=='

    #r'\d+' : expresion regular para uno o mas digitos
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    #r'#.*' : expresion regular para el simbolo de comentario y lo que siga
    @_(r'#.*')
    def COMMENT(self, t):
        pass

    #r'\n+' : expresion regular para salto de linea
    @_(r'\n+')
    def newline(self,t ):
        self.lineno = t.value.count('\n')



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
            for token in lex:
                print(token)