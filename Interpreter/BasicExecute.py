from Interpreter.Lexer import BasicLexer
from Interpreter.Parser import BasicParser
import random

class BasicExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
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
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == 'condition_eqeq':
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]


        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0

        if node[0] == 'sum':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            print(env)
            return node[1]

        if node[0] == 'NewVar_assign':
            if(env.keys().__contains__(node[1])):
                self.env[node[1]] = self.walkTree(node[2])
                return self.env[node[1]]
            else:
                print("Undefined variable '"+node[1]+"' found!")
                return "Undefined variable '"+node[1]+"' found!"

        if node[0] == 'Random':
            return random.randint(0,self.walkTree(node[1]))

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return "Undefined variable '"+node[1]+"' found!"

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))

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
            BasicExecute(tree, env)