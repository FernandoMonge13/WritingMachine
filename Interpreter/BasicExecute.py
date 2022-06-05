from Interpreter.Lexer import BasicLexer
from Interpreter.Parser import BasicParser
import random
import Hardware.Hardware as machine



class BasicExecute:
    actions = machine.Hardware()

    instructionsFunction = []
    paramsFunction = {}
    functionName = ""

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
            if self.walkTree(node[1]) == self.walkTree(node[2]) == 'TRUE':
                return 'TRUE'
            else:
                return 'FALSE'

        if node[0] == 'Or':
            if self.walkTree(node[1]) == 'TRUE' or self.walkTree(node[2]) == 'TRUE':
                return 'TRUE'
            else:
                return 'FALSE'

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'bool':
            if node[1] == 'TRUE':
                return node[1]
            elif node[1] == 'FALSE':
                return node[1]

        if node[0] == 'if_stmt':
            if self.walkTree(node[1]) == 'TRUE':
                return self.walkTree(node[2])
            elif self.walkTree(node[1]) == 'FALSE':
                return self.walkTree(node[3])
            else:
                print("Error: if solo puede recibir valores booleanos")

        if node[0] == 'statement_list':
            # print(f"El nodo completo es {node}")
            # print("Entro al execute: ", node[1])
            for i in node[1]:
                # print(f"El nodo es {i}")
                self.walkTree(i)

        if node[0] == 'fun_def':
            # print("Entrando a fun_def")
            self.funDictionary[node[1]] = [node[2], node[3]]
            print(self.funDictionary)


        if node[0] == 'call_main':
            return self.walkTree(self.funDictionary['MAIN'])



        if node[0] == 'params':
            return print("Params: " + str(node[1]))

        if node[0] == 'fun_call':
            try:
                new_varDictionary = self.varDictionary.copy()
                new_funDictionary = self.funDictionary.copy()

                new_execute = BasicExecute(new_varDictionary, new_funDictionary)
                new_lastTree = None

                instructionsAux = []


                if len(node[2])==len(self.funDictionary[node[1]][0]):
                    # print("Los parametros son iguales")

                    for i in range(len(node[2])):
                        instructionsAux.append(('var_assign', self.funDictionary[node[1]][0][i], node[2][i]))

                else:
                    return print("La cantidad de parametros es diferente a la cantidad de parametros definidos")


                instructionsAux.append(self.funDictionary[node[1]][1])

                instructions = instructionsAux
                print(instructions)

                for instruction in instructions:
                    new_tree = instruction
                    new_execute.startExecute(new_tree, new_lastTree, new_varDictionary, new_funDictionary)
                    new_lastTree = new_tree


            except LookupError:
                print("Undefined function '%s'" % node[1])


        if node[0] == 'sum':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        elif node[0] == 'Greater':
            if self.walkTree(node[1]) > self.walkTree(node[2]):
                return "TRUE"
            else:
                return "FALSE"
        elif node[0] == 'Smaller':
            if self.walkTree(node[1]) < self.walkTree(node[2]):
                return "TRUE"
            else:
                return "FALSE"

        if node[0] == 'var_assign':
            self.varDictionary[node[1]] = self.walkTree(node[2])
            # print(self.varDictionary)
            return node[1]

        if node[0] == 'NewVar_assign':
            if(self.varDictionary.keys().__contains__(node[1])):
                self.varDictionary[node[1]] = self.walkTree(node[2])
                return self.varDictionary[node[1]]
            else:
                print("Undefined variable '"+node[1]+"' found!")
                return "Undefined variable '"+node[1]+"' found!"

        if node[0] == 'Random':
            return random.randint(0,self.walkTree(node[1]))

        if node[0] == 'var':
            try:
                return self.varDictionary[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return "Undefined variable '"+node[1]+"' found!"

        if node[0] == 'String':
            return node[1]

        if node[0] == 'Print':
            # print(f"El nodo que entro es {node}")
            for i in range(len(node[1])):
                print(self.walkTree(node[1][i]))


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

            if self.walkTree(node[1]) == 1:
                self.actions.down_black()
            elif self.walkTree(node[1]) == 2:
                self.actions.down_blue()

        if node[0] == 'ContinueUp':

            if (self.actions.y + self.walkTree(node[1])) <= 10:
                for i in range(self.actions.y, self.actions.y + int(self.walkTree(node[1]))):
                    self.actions.y_plus()

                self.actions.y += int(self.walkTree(node[1]))
            else:
                print("Error: ContinueUp fuera de rango")

        if node[0] == 'ContinueDown':
            if (self.actions.y - self.walkTree(node[1])) >= 1:  #5    3
                aux =  self.actions.y
                while aux > self.actions.y - int(self.walkTree(node[1])):
                    self.actions.y_minus()
                    aux-=1
                self.actions.y = aux
            else:
                print("Error: ContinueDown fuera de rango")

        if node[0] == 'ContinueLeft':

            if (self.actions.x - self.walkTree(node[1])) >= 1:
                aux = self.actions.x
                while aux > self.actions.x - int(self.walkTree(node[1])):
                    self.actions.x_minus()
                    print("LEFT")
                    aux -= 1
                self.actions.x = aux
            else:
                print("Error: ContinueDown fuera de rango")

        if node[0] == 'ContinueRight':

            if (self.actions.x + self.walkTree(node[1])) <= 9:
                for i in range(self.actions.x, self.actions.x + int(self.walkTree(node[1]))):
                    self.actions.x_plus()

                self.actions.x += int(self.walkTree(node[1]))
                print(self.actions.x)
            else:
                print("Error: ContinueRight fuera de rango")

        if node[0] == 'Pos':
            self.actions.x_movement(int(self.walkTree(node[1])))
            self.actions.y_movement(int(self.walkTree(node[2])))

        if node[0] == 'PosX':
            self.actions.x_movement(int(self.walkTree(node[1])))

        if node[0] == 'PosY':
            self.actions.y_movement(int(self.walkTree(node[1])))

        if node[0] == 'Down':
            self.actions.down_black()

        if node[0] == 'Up':

            self.actions.up()

        if node[0] == 'Beginning':
            self.actions.x_movement(1)
            self.actions.y_movement(1)

        if node[0] == 'Speed':
            self.actions.set_speed(int(self.walkTree(node[1])))


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