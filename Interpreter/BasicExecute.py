from Interpreter.Lexer import BasicLexer
from Interpreter.Parser import BasicParser
import random
import Hardware.Hardware as machine



class BasicExecute:
    actions = machine.Hardware()
    # actions = ""

    isExecuting = False
    errores = []
    toPrint = []

    lastTree = None

    def __init__(self, varDictionary, funDictionary):
        self.varDictionary = varDictionary
        self.funDictionary = funDictionary

    def startExecute(self, tree, lastTree, varDictionary, funDictionary):
        self.lastTree = lastTree
        result = self.walkTree(tree)
        self.lastTree = tree

        self.walkTree(('call_main'))

        if result is not None and (isinstance(result, int) or isinstance(result, float)):
            if(result%1==0):
                print(int(result))
            else:
                print(result)

        if isinstance(result, str) and result[0] == '"':
            print(result)

        if isinstance(result, str) and (result == 'TRUE' or result == 'FALSE'):
            print(result)

    def walkTree(self, node):


        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node


        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'Comment':
            pass


        if node[0] == 'Equal':
            if self.walkTree(node[1]) == self.walkTree(node[2]):
                return 'TRUE'
            else:
                return 'FALSE'

        if node[0] == 'And':
            if (self.walkTree(node[1]) == 'TRUE' or self.walkTree(node[2]) == 'FALSE') and (self.walkTree(node[2]) == 'TRUE' or self.walkTree(node[1]) == 'FALSE'):
                if self.walkTree(node[1]) == self.walkTree(node[2]) == 'TRUE':
                    return 'TRUE'
                else:
                    return 'FALSE'
            else:
                self.errores.append("Error: Operador And solo acepta valores de tipo boolean")

        if node[0] == 'Or':
            if (self.walkTree(node[1]) == 'TRUE' or self.walkTree(node[2]) == 'FALSE') and (self.walkTree(node[2]) == 'TRUE' or self.walkTree(node[1]) == 'FALSE'):
                if self.walkTree(node[1]) == 'TRUE' or self.walkTree(node[2]) == 'TRUE':
                    return 'TRUE'
                else:
                    return 'FALSE'
            else:
                self.errores.append("Error: Operador Or solo acepta valores de tipo boolean" )

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'bool':
            if node[1] == 'TRUE':
                return node[1]
            elif node[1] == 'FALSE':
                return node[1]
            else:
                self.errores.append("Error: No se ha ingresado un valor de tipo boolean" )

        if node[0] == 'if_stmt':
            if self.walkTree(node[1]) == 'TRUE':
                return self.walkTree(node[2])
            elif self.walkTree(node[1]) == 'FALSE':
                return self.walkTree(node[3])
            else:
                self.errores.append("Error: If solo puede recibir valores booleanos")

        if node[0] == 'statement_list':
            for i in node[1]:
                self.walkTree(i)

        if node[0] == 'fun_def':
            if not self.funDictionary.keys().__contains__(node[1]):
                self.funDictionary[node[1]] = [node[2], node[3]]
                print(self.funDictionary)
            else:
                self.errores.append(f"Error: La funcion {node[1]} ya definida")


        if node[0] == 'call_main':
            return self.walkTree(self.funDictionary['MAIN'])

        if node[0] == 'params':
            return print("Params: " + str(node[1]))

        if node[0] == 'fun_call':
            try:
                new_varDictionary = self.varDictionary.copy()
                new_funDictionary = self.funDictionary.copy()

                new_execute = BasicExecute(new_varDictionary, new_funDictionary)
                new_execute.isExecuting = self.isExecuting

                new_lastTree = None

                instructionsAux = []

                print("Funcion llamada: ", node[1])
                print("Cantidad de parametros ingresados: ", len(node[2]))
                print("Cantidad de parametros esperados: ", len(self.funDictionary[node[1]][0]))
                print("Los parametros son iguales: ", len(node[2]) == len(self.funDictionary[node[1]][0]))

                if len(node[2])==len(self.funDictionary[node[1]][0]):

                    for i in range(len(node[2])):
                        instructionsAux.append(('var_assign', self.funDictionary[node[1]][0][i], node[2][i]))


                    instructionsAux.append(self.funDictionary[node[1]][1])

                    instructions = instructionsAux
                    # print(instructions)

                    for instruction in instructions:
                        new_tree = instruction
                        new_execute.startExecute(new_tree, new_lastTree, new_varDictionary, new_funDictionary)
                        new_lastTree = new_tree

                else:
                    self.errores.append(f"La cantidad de parametros es diferente a la cantidad de parametros definidos para la funcion {node[1]}")

            except LookupError:
                self.errores.append("Undefined function '%s'" % node[1])


        if node[0] == 'sum':
            if isinstance(self.walkTree(node[1]), float) and isinstance(self.walkTree(node[2]), float):
                return self.walkTree(node[1]) + self.walkTree(node[2])
            else:
                self.errores.append("Error: Suma solo acepta valores numericos")
        elif node[0] == 'sub':
            if isinstance(self.walkTree(node[1]), float) and isinstance(self.walkTree(node[2]), float):
                return self.walkTree(node[1]) - self.walkTree(node[2])
            else:
                self.errores.append("Error: Resta solo acepta valores numericos")
        elif node[0] == 'mul':
            if isinstance(self.walkTree(node[1]), float) and isinstance(self.walkTree(node[2]), float):
                return self.walkTree(node[1]) * self.walkTree(node[2])
            else:
                self.errores.append("Error: Multiplicacion solo acepta valores numericos")
        elif node[0] == 'div':
            if isinstance(self.walkTree(node[1]), float) and isinstance(self.walkTree(node[2]), float):
                return self.walkTree(node[1]) / self.walkTree(node[2])
            else:
                self.errores.append("Error: Division solo acepta valores numericos")
        elif node[0] == 'Greater':
            if isinstance(self.walkTree(node[1]), float) and isinstance(self.walkTree(node[2]), float):
                if self.walkTree(node[1]) > self.walkTree(node[2]):
                    return "TRUE"
                else:
                    return "FALSE"
            else:
                self.errores.append("Error: El procedimiento Greater solo acepta valores numericos")
        elif node[0] == 'Smaller':
            if isinstance(self.walkTree(node[1]), float) and isinstance(self.walkTree(node[2]), float):
                if self.walkTree(node[1]) < self.walkTree(node[2]):
                    return "TRUE"
                else:
                    return "FALSE"
            else:
                self.errores.append("Error: El procedimiento Smaller solo acepta valores numericos")

        if node[0] == 'var_assign':
            self.varDictionary[node[1]] = self.walkTree(node[2])
            # print(self.varDictionary)
            return node[1]

        if node[0] == 'NewVar_assign':
            if(self.varDictionary.keys().__contains__(node[1])):
                if isinstance(self.walkTree(node[2]), float) and isinstance(self.varDictionary[node[1]], float):
                    self.varDictionary[node[1]] = self.walkTree(node[2])
                elif (self.walkTree(node[2]) == 'TRUE' or self.walkTree(node[2]) == 'FALSE') and (self.varDictionary[node[1]] == 'TRUE' or self.varDictionary[node[1]] == 'FALSE'):
                    self.varDictionary[node[1]] = self.walkTree(node[2])
                else:
                    if isinstance(self.varDictionary[node[1]], float):
                        self.errores.append(f"Error: No se puede asignar el valor asignado a la variable {node[1]}, ya que esta es un numero")
                    elif self.varDictionary[node[1]] == 'TRUE' or self.varDictionary[node[1]] == 'FALSE':
                        self.errores.append(f"Error: No se puede asignar el valor asignado a la variable {node[1]}, ya que esta es un booleano")
                    else:
                        self.errores.append(f"Error: No se puede asignar el valor asignado a la variable {node[1]}, ya que no se reconoce el tipo de dato")

            else:
                self.errores.append("Undefined variable '"+node[1]+"' found!")


        if node[0] == 'Random':
            if isinstance(self.walkTree(node[1]), float):
                if self.walkTree(node[1])%1==0:
                    return random.randint(0, int(self.walkTree(node[1])))
                else:
                    self.errores.append("Error: El procedimiento Random solo acepta valores enteros")
            else:
                self.errores.append("Error: El procedimiento Random solo acepta valores numericos")

        if node[0] == 'var':
            try:
                return self.varDictionary[node[1]]
            except LookupError:
                self.errores.append("Undefined variable '"+node[1]+"' found!")


        if node[0] == 'String':
            return node[1]

        if node[0] == 'Print':
            if self.isExecuting:
                for i in range(len(node[1])):
                    self.toPrint.append(print(self.walkTree(node[1][i])))



        if node[0] == 'while_stmt':
            while self.walkTree(node[1]) == 'TRUE':
                self.walkTree(node[2])

        if node[0] == 'until_stmt':
            self.walkTree(node[2])
            while self.walkTree(node[1]) == 'FALSE':
                self.walkTree(node[2])

        if node[0] == 'repeat_stmt':
            for i in range(int(self.walkTree(node[1]))):
                self.walkTree(node[2])


        #A partir de aqui, cosas de Hardware


        if node[0] == 'UseColor':
            if isinstance(self.walkTree(node[1]), float) and (self.walkTree(node[1])==1 or self.walkTree(node[1])==2):
                if self.isExecuting:
                    if self.walkTree(node[1]) == 1:
                        self.actions.down_black()
                    elif self.walkTree(node[1]) == 2:
                        self.actions.down_blue()
            else:
                self.errores.append("Error: UseColor solo acepta valores enteros entre 1 y 2")

        if node[0] == 'ContinueUp':
            if self.isExecuting:
                if (self.actions.y + self.walkTree(node[1])) <= 10:
                    for i in range(self.actions.y, self.actions.y + int(self.walkTree(node[1]))):
                        self.actions.y_plus()

                    self.actions.y += int(self.walkTree(node[1]))
                else:
                    self.errores.append("Error: ContinueUp fuera de rango")


        if node[0] == 'ContinueDown':
            if self.isExecuting:
                if (self.actions.y - self.walkTree(node[1])) >= 1:  #5    3
                    aux =  self.actions.y
                    while aux > self.actions.y - int(self.walkTree(node[1])):
                        self.actions.y_minus()
                        aux-=1
                    self.actions.y = aux
                else:
                    self.errores.append("Error: ContinueDown fuera de rango")

        if node[0] == 'ContinueLeft':
            if self.isExecuting:
                if (self.actions.x - self.walkTree(node[1])) >= 1:
                    aux = self.actions.x
                    while aux > self.actions.x - int(self.walkTree(node[1])):
                        self.actions.x_minus()
                        print("LEFT")
                        aux -= 1
                    self.actions.x = aux
                else:
                    self.errores.append("Error: ContinueDown fuera de rango")

        if node[0] == 'ContinueRight':
            if self.isExecuting:
                if (self.actions.x + self.walkTree(node[1])) <= 9:
                    for i in range(self.actions.x, self.actions.x + int(self.walkTree(node[1]))):
                        self.actions.x_plus()

                    self.actions.x += int(self.walkTree(node[1]))
                    # print(self.actions.x)
                else:
                    self.errores.append("Error: ContinueRight fuera de rango")

        if node[0] == 'Pos':
            if isinstance(self.walkTree(node[1]), float) and isinstance(self.walkTree(node[2]), float):
                if self.isExecuting:
                    self.actions.x_movement(int(self.walkTree(node[1])))
                    self.actions.y_movement(int(self.walkTree(node[2])))
            else:
                self.errores.append("Error: Pos(x,y) solo acepta valores numericos")

        if node[0] == 'PosX':
            if isinstance(self.walkTree(node[1]), float):
                if self.isExecuting:
                    self.actions.x_movement(int(self.walkTree(node[1])))

        if node[0] == 'PosY':
            if isinstance(self.walkTree(node[1]), float):
                if self.isExecuting:
                    self.actions.y_movement(int(self.walkTree(node[1])))


        if node[0] == 'Down':
            if self.isExecuting:
                self.actions.down_black()

        if node[0] == 'Up':
            if self.isExecuting:
                self.actions.up()

        if node[0] == 'Beginning':
            if self.isExecuting:
                self.actions.x_movement(1)
                self.actions.y_movement(1)

        if node[0] == 'Speed':
            if isinstance(self.walkTree(node[1]), float):
                if 1<=self.walkTree(node[1])<=5:
                    if self.isExecuting:
                        self.actions.set_speed(int(self.walkTree(node[1])))
                else:
                    self.errores.append("Error: Speed solo acepta valores entre 1 y 5")
            else:
                self.errores.append("Error: Speed solo acepta valores numericos")

    def clearExecution(self):
        self.isExecuting = False
        self.toPrint = []
        self.errores = []
        self.varDictionary = {}
        self.funDictionary = {}


if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    varDictionary = {}
    funDictionary = {}

    execute = BasicExecute(varDictionary, funDictionary)
    lastTree = None

    while True:
        try:
            text = input('basic > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            execute.startExecute(tree, lastTree, varDictionary, funDictionary)
            lastTree = tree