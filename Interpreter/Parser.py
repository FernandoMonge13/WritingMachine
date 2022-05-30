from sly import Lexer
from sly import Parser

#The parser is made up of grammar rules,
#we give our grammar rules to the parser generator,
#and the parser generator gives us a parser for that grammar
from Interpreter.Lexer import BasicLexer

class BasicParser(Parser):

    errores = []

    tokens = BasicLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = { }

    #Si la entrada es vacia, simplemente se ignora
    @_('')
    def statement(self, p):
        pass



    @_('FOR var_assign TO expr THEN statement')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    # @_('IF condition THEN statement')
    # def statement(self, p):
    #     return ('if_stmt', p.condition, ('branch', p.statement))

    @_('PARA NAME "(" ")" ARROW statement')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('NAME "(" ")"')
    def statement(self, p):
        return ('fun_call', p.NAME)

    @_('expr EQEQ expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('DEF "(" NAME "," expr ")"')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)

    @_('ADD "(" NAME "," expr ")"')
    def var_assign(self, p):
        return ('NewVar_assign', p.NAME, ('sum', ('var', p.NAME), p.expr))

    @_('ADD "(" NAME ")"')
    def var_assign(self, p):
        return ('NewVar_assign', p.NAME, ('sum', ('var', p.NAME), ('num', 1)))

    @_('PUT "(" NAME "," expr ")"')
    def var_assign(self, p):
        return ('NewVar_assign', p.NAME, p.expr)

    @_('EQUAL "(" expr "," expr ")"')
    def var_assign(self, p):
        return ('Equal', p.expr0, p.expr1)

    @_('AND "(" expr "," expr ")"')
    def var_assign(self, p):
        return ('And', p.expr0, p.expr1)

    @_('OR "(" expr "," expr ")"')
    def var_assign(self, p):
        return ('Or', p.expr0, p.expr1)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('sum', p.expr0, p.expr1)


    @_('SUMA "(" expr ")"')
    def expr(self, p):
        return ('sum', p.expr, ('num', 1))

    @_('SUMA "(" expr "," expr ")"')
    def expr(self, p):
        return ('sum', p.expr0, p.expr1)

    @_('SUBSTR "(" expr "," expr ")"')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('RANDOM "(" expr ")"')
    def expr(self, p):
        return ('Random', p.expr)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('MULT "(" expr "," expr ")"')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('DIV "(" expr "," expr ")"')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('expr ">" expr')
    def expr(self, p):
        return ('Greater', p.expr0, p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return ('Smaller', p.expr0, p.expr1)

    @_('GREATER "(" expr "," expr ")"')
    def expr(self, p):
        return ('Greater', p.expr0, p.expr1)

    @_('SMALLER "(" expr "," expr ")"')
    def expr(self, p):
        return ('Smaller', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('TRUE')
    def expr(self, p):
        return ('bool', p.TRUE)

    @_('FALSE')
    def expr(self, p):
        return ('bool', p.FALSE)

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('basic > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)