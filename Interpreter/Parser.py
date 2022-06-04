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

    @_('COMMENT')
    def statement(self, p):
        return ('Comment', p.COMMENT)

    # @_('FOR var_assign TO expr THEN statement')
    # def statement(self, p):
    #     return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    # @_('IF condition THEN statement ELSE statement')
    # def statement(self, p):
    #     return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('IF "(" TRUE ")" "[" statement "]" ";"')
    def statement(self, p):
        return ('if_stmt', p.TRUE, [p.statement])

    @_('IF "(" FALSE ")" "[" statement "]" ";"')
    def statement(self, p):
        return ('if_stmt', p.FALSE, [p.statement])


    @_('IF "(" expr ")" "[" statement "]" ";"')
    def statement(self, p):
        return ('if_stmt', p.expr, [p.statement])

    @_('IF "(" expr ")" "[" statements "]" ";"')
    def statement(self, p):
        return ('if_stmt', p.expr, p.statements)

    @_('statement statement')
    def statements(self, p):
        return ('statement_list', [p.statement0, p.statement1])

    @_('statements statement')
    def statements(self, p):
        return ('statement_list', p.statements.append() + [p.statement])



    #Declaracion de sintaxis básica

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('expr ";"')
    def statement(self, p):
        return (p.expr)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr


    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('TRUE')
    def expr(self, p):
        return ('bool', p.TRUE)

    @_('FALSE')
    def expr(self, p):
        return ('bool', p.FALSE)


    @_('NAME "," NAME')
    def paramsFunction(self, p):
        return [p.NAME0, p.NAME1]

    @_('paramsFunction "," NAME')
    def paramsFunction(self, p):
        lista = []
        for i in p.paramsFunction:
            lista.append(i)
        lista.append(p.NAME)
        return lista

    @_('expr "," expr')
    def params(self, p):
        return [p.expr0, p.expr1]

    @_('params "," expr')
    def params(self, p):
        lista = []
        for i in p.params:
            lista.append(i)
        lista.append(p.expr)
        return lista




    #Definicion de funciones para la declaracion de variables
    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr ";"')
    def statement(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('DEF "(" NAME "," expr ")" ";"')
    def statement(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('PUT "(" NAME "," expr ")" ";"')
    def statement(self, p):
        return ('NewVar_assign', p.NAME, p.expr)




    #Definicion de funciones para la declaracion de funciones
    @_('PARA NAME "[" "]"')
    def statement(self, p):
        return ('fun_def', p.NAME)

    @_('PARA NAME "[" NAME "]"')
    def statement(self, p):
        print(p.NAME1)
        return ('fun_def', p.NAME0, [p.NAME1])

    @_('PARA NAME "[" paramsFunction "]"')
    def statement(self, p):
        return ('fun_def', p.NAME, p.paramsFunction)

    @_('FIN')
    def expr(self, p):
        return ('Fin', 1)


    @_('NAME "(" ")" ";"')
    def statement(self, p):
        return ('fun_call', p.NAME)

    @_('NAME "(" expr ")"  ";"')
    def statement(self, p):
        return ('fun_call', p.NAME, [p.expr])

    @_('NAME "(" params ")"  ";"')
    def statement(self, p):
        return ('fun_call', p.NAME, p.params)







    #Definición de funciones para las operaciones de suma
    @_('expr "+" expr')
    def expr(self, p):
        return ('sum', p.expr0, p.expr1)

    @_('expr expr')
    def expr(self, p):
        return ('sum', p.expr0, p.expr1)

    @_('SUMA "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('sum', p.params[0], p.params[1])
        print('Error: La cantidad de parametros no es correcta')

    @_('ADD "(" NAME ")"')
    def var_assign(self, p):
        return ('NewVar_assign', p.NAME, ('sum', ('var', p.NAME), ('num', 1)))

    @_('ADD "(" NAME "," expr ")"')
    def var_assign(self, p):
        return ('NewVar_assign', p.NAME, ('sum', ('var', p.NAME), p.expr))




    #Definición de funciones para las operaciones de resta
    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('SUBSTR "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('sub', p.params[0], p.params[1])
        print('Error: La cantidad de parametros no es correcta')



    #Definición de funciones para las operaciones de multiplicación
    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('MULT "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('mul', p.params[0], p.params[1])
        print('Error: La cantidad de parametros no es correcta')



    #Definición de funciones para las operaciones de división
    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('DIV "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('div', p.params[0], p.params[1])
        print('Error: La cantidad de parametros no es correcta')




    #Definición de funciones para las operaciones de comparaciones
    @_('expr ">" expr')
    def expr(self, p):
        return ('Greater', p.expr0, p.expr1)

    @_('GREATER "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('Greater', p.params[0], p.params[1])
        print('Error: La cantidad de parametros no es correcta')

    @_('expr "<" expr')
    def expr(self, p):
        return ('Smaller', p.expr0, p.expr1)

    @_('SMALLER "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('Smaller', p.params[0], p.params[1])
        print('Error: La cantidad de parametros no es correcta')

    @_('EQUAL "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('Equal', p.params[0], p.params[1])
        print('Error: La cantidad de parametros no es correcta')

    @_('expr EQEQ expr')
    def expr(self, p):
        return ('Equal', p.expr0, p.expr1)

    @_('AND "(" params ")"')
    def var_assign(self, p):
        if len(p.params) == 2:
            return ('And', p.params[0], p.params[1])
        print('Error: La cantidad de parametros no es correcta')


    @_('OR "(" params ")"')
    def var_assign(self, p):
        if len(p.params) == 2:
            return ('Or', p.params[0], p.params[1])
        print('Error: La cantidad de parametros no es correcta')





    #Definición de funcion para Random
    @_('RANDOM "(" expr ")"')
    def expr(self, p):
        return ('Random', p.expr)


    #Definición para la función de imprimir

    @_('STRING')
    def string(self, p):
        return ('String', p.STRING)

    @_('PRINT "(" paramsPrint ")" ";"')
    def statement (self, p):
        return ('Print', p.paramsPrint)

    @_('PRINT "(" expr ")" ";"')
    def statement (self, p):
        return ('Print', [p.expr])

    @_('PRINT "(" string ")" ";"')
    def statement (self, p):
        return ('Print', p.string)


    @_('params')
    def paramsPrint (self, p):
        return (p.params)

    @_('paramsPrint "," paramsPrint')
    def paramsPrint (self, p):
        return (p.paramsPrint0 , p.paramsPrint1)


    @_('string "," expr')
    def paramsPrint (self, p):
        return ([p.string, p.expr])

    @_('expr "," string')
    def paramsPrint (self, p):
        return ([p.expr, p.string])

    @_('string "," string')
    def paramsPrint (self, p):
        return ([p.string0, p.string1])


    @_('paramsPrint "," expr')
    def paramsPrint (self, p):
        return (p.paramsPrint.append(p.expr))

    @_('expr "," paramsPrint')
    def paramsPrint (self, p):
        return ([p.expr] + p.paramsPrint)


    @_('paramsPrint "," string')
    def paramsPrint (self, p):
        return (p.paramsPrint.append(p.string))

    @_('string "," paramsPrint')
    def paramsPrint (self, p):
        return ([p.string] + p.paramsPrint)















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