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

    # @_('FOR var_assign TO expr THEN statement')
    # def statement(self, p):
    #     return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    # Definicion de condicionales
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

    @_('IFELSE "(" expr ")" "[" statement "]" "[" statement "]" ";"')
    def statement(self, p):
        return ('if_stmt', p.expr, p.statement0, p.statement1)

    @_('IFELSE "(" expr ")" "[" statements "]" "[" statements "]" ";"')
    def statement(self, p):
        return ('if_stmt', p.expr, p.statements0, p.statements1)

    @_('IFELSE "(" expr ")" "[" statements "]" "[" statement "]" ";"')
    def statement(self, p):
        return ('if_stmt', p.expr, p.statements, p.statement)

    @_('IFELSE "(" expr ")" "[" statement "]" "[" statements "]" ";"')
    def statement(self, p):
        return ('if_stmt', p.expr, p.statement, p.statements)


    #Definicion para while
    @_('WHILE "[" expr "]" "[" statement "]" ";"')
    def statement(self, p):
        return ('while_stmt', p.expr, [p.statement])

    @_('WHILE "[" expr "]" "[" statements "]" ";"')
    def statement(self, p):
        return ('while_stmt', p.expr, p.statements)

    #Definicion para until
    @_('UNTIL "[" expr "]" "[" statement "]" ";"')
    def statement(self, p):
        return ('until_stmt', p.expr, [p.statement])

    @_('UNTIL "[" expr "]" "[" statements "]" ";"')
    def statement(self, p):
        return ('until_stmt', p.expr, p.statements)

    #Definicion para repeat
    @_('REPEAT expr "[" statement "]" ";"')
    def statement(self, p):
        return ('repeat_stmt', p.expr, ('statement_list', [p.statement]) )

    @_('REPEAT expr "[" statements "]" ";"')
    def statement(self, p):
        return ('repeat_stmt', p.expr, p.statements)



    # Definicion de statements
    @_('statement statement')
    def statements(self, p):
        # print(p.statement0, p.statement1)
        return ('statement_list', [p.statement0, p.statement1])

    @_('statements statement')
    def statements(self, p):
        # print("\n",1, p.statements[1] + [p.statement], "\n")
        return ('statement_list', p.statements[1] + [p.statement])

    @_('COMMENT statement')
    def statement(self, p):
        print(p.statement)
        return ('statement', p.statement)

    @_('COMMENT statements')
    def statement(self, p):
        print(p.statements)
        return p.statements




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



    #Definicion para la funcion MAIN
    @_('PARA MAIN "[" "]" statements FIN')
    def statement(self, p):
        return ('fun_def', p.MAIN, [], p.statements)

    @_('PARA MAIN "[" "]" statement FIN')
    def statement(self, p):
        return ('fun_def', p.MAIN, [], ('statement_list',[p.statement]))

    #Definicion de funciones para la declaracion de funciones
    @_('PARA NAME "[" "]"  statements FIN')
    def statement(self, p):
        return ('fun_def', p.NAME, [], p.statements)

    @_('PARA NAME "[" NAME "]" statements FIN')
    def statement(self, p):
        return ('fun_def', p.NAME0, [p.NAME1], p.statements)

    @_('PARA NAME "[" paramsFunction "]" statements FIN')
    def statement(self, p):
        return ('fun_def', p.NAME, p.paramsFunction, p.statements)

    @_('PARA NAME "[" "]"  statement FIN')
    def statement(self, p):
        return ('fun_def', p.NAME, [], ('statement_list',[p.statement]))

    @_('PARA NAME "[" NAME "]" statement FIN')
    def statement(self, p):
        return ('fun_def', p.NAME0, [p.NAME1], ('statement_list',[p.statement]))

    @_('PARA NAME "[" paramsFunction "]" statement FIN')
    def statement(self, p):
        return ('fun_def', p.NAME, p.paramsFunction, ('statement_list',[p.statement]))


    @_('MAIN "(" ")" ";"')
    def statement(self, p):
        return ('fun_call', p.MAIN, [])


    @_('NAME "(" ")" ";"')
    def statement(self, p):
        return ('fun_call', p.NAME, [])


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
        self.errores.append('Error: La cantidad de parametros no es correcta')

    @_('ADD "(" NAME ")" ";"')
    def statement(self, p):
        return ('NewVar_assign', p.NAME, ('sum', ('var', p.NAME), ('num', 1)))

    @_('ADD "(" NAME "," expr ")" ";"')
    def statement(self, p):
        return ('NewVar_assign', p.NAME, ('sum', ('var', p.NAME), p.expr))




    #Definición de funciones para las operaciones de resta
    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('SUBSTR "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('sub', p.params[0], p.params[1])
        self.errores.append('Error: La cantidad de parametros no es correcta')



    #Definición de funciones para las operaciones de multiplicación
    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('MULT "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('mul', p.params[0], p.params[1])
        self.errores.append('Error: La cantidad de parametros no es correcta')



    #Definición de funciones para las operaciones de división
    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('DIV "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('div', p.params[0], p.params[1])
        self.errores.append('Error: La cantidad de parametros no es correcta')




    #Definición de funciones para las operaciones de comparaciones
    @_('expr ">" expr')
    def expr(self, p):
        return ('Greater', p.expr0, p.expr1)

    @_('GREATER "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('Greater', p.params[0], p.params[1])
        self.errores.append('Error: La cantidad de parametros no es correcta')

    @_('expr "<" expr')
    def expr(self, p):
        return ('Smaller', p.expr0, p.expr1)

    @_('SMALLER "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('Smaller', p.params[0], p.params[1])
        self.errores.append('Error: La cantidad de parametros no es correcta')

    @_('EQUAL "(" params ")"')
    def expr(self, p):
        if len(p.params) == 2:
            return ('Equal', p.params[0], p.params[1])
        self.errores.append('Error: La cantidad de parametros no es correcta')

    @_('expr EQEQ expr')
    def expr(self, p):
        return ('Equal', p.expr0, p.expr1)

    @_('AND "(" params ")"')
    def var_assign(self, p):
        if len(p.params) == 2:
            return ('And', p.params[0], p.params[1])
        self.errores.append('Error: La cantidad de parametros no es correcta')


    @_('OR "(" params ")"')
    def var_assign(self, p):
        if len(p.params) == 2:
            return ('Or', p.params[0], p.params[1])
        self.errores.append('Error: La cantidad de parametros no es correcta')





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



    #Definiciones para la parte de Hardware
    @_('USECOLOR expr ";"')
    def statement(self, p):
        return ('UseColor', p.expr)

    @_('CONTINUEUP expr ";"')
    def statement(self, p):
        return ('ContinueUp', p.expr)

    @_('CONTINUEDOWN expr ";"')
    def statement(self, p):
        return ('ContinueDown', p.expr)

    @_('CONTINUELEFT expr ";"')
    def statement(self, p):
        return ('ContinueLeft', p.expr)

    @_('CONTINUERIGHT expr ";"')
    def statement(self, p):
        return ('ContinueRight', p.expr)

    @_('POS "(" expr "," expr ")" ";"')
    def statement(self, p):
        return ('Pos', p.expr0, p.expr1)

    @_('POSX expr ";"')
    def statement(self, p):
        return ('PosX', p.expr)

    @_('POSY expr ";"')
    def statement(self, p):
        return ('PosY', p.expr)

    @_('DOWN ";"')
    def statement(self, p):
        return ('Down',1)

    @_('UP ";"')
    def statement(self, p):
        return ('Up', 1)

    @_('BEGINNING ";"')
    def statement(self, p):
        return ('Beginning', 1)

    @_('SPEED expr ";"')
    def statement(self, p):
        return ('Speed', p.expr)

    @_('RUN "[" statements "]" ";"')
    def statement(self, p):
        return ('statement_list', p.statements)

    def error(self, p):
        self.errores.append(f"Parsing error at token {str(p)}")
        print(f"Parsing error at token {str(p)}")

    # @_('expr PLUS expr')
    # def expr(self, p):
    #     line   = p.lineno      # line number of the PLUS token
    #     index  = p.index       # Index of the PLUS token in input text

    def limpiarErrores(self):
        self.errores=[]

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