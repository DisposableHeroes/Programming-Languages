# Akshat Chandra

# This is my attempt to implement the language BASIC in the style of Python



NUMS = '0123456789'


# Class to check for errors incase input is not what we are expecting.


class Error:
    def __init__(self, token_start, token_end, error_type, info):
        self.token_start = token_start
        self.token_end = token_end
        self.error_type = error_type
        self.info = info
    
    def ret_string(self):
        result  = f'{self.error_type}: {self.info}\n'
        result += f'File {self.token_start.fn}, line {self.token_start.line + 1}'
    
        return result

class Illegal_Char(Error):
    def __init__(self, token_start, token_end, info):
        super().__init__(token_start, token_end, 'Illegal Character was entered', info)



class Invalid_Syntax(Error):
    def __init__(self, token_start, token_end, info =''):
        super().__init__(token_start, token_end, 'Invalid Syntax', info)

class RunTime_Error(Error):
    def __init__(self, token_start, token_end, info, error_trace):
        super().__init__(token_start, token_end, 'Runtime Error', info)
        self.error_trace = error_trace

    def ret_string(self):
        result  = self.ret_traceback()
        result += f'{self.error_type}: {self.info}'
 
        return result

    def ret_traceback(self):
        result = ''
        pos = self.token_start
        et = self.error_trace

        while et:
            result = f'  File {pos.fn}, line {str(pos.line + 1)}, in {et.display_name}\n' + result
            pos = et.parent_entry_pos
            et = et.parent

        return 'Traceback (most recent call last):\n' + result



class Position:
    def __init__(self, index, line, column, fn, ftxt):
        self.index = index
        self.line = line
        self.column = column
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line += 1
            self.column = 0

        return self

    def copy(self):
        return Position(self.index, self.line, self.column, self.fn, self.ftxt)


# Initialize Tokens


TKN_INT          = 'INT'
TKN_FLOAT        = 'FLOAT'
TKN_EOF          = 'EOF'
TKN_ADD          = 'ADD'
TKN_SUBTRACT     = 'SUBTRACT'
TKN_MULTIPLY     = 'MULTIPLY'
TKN_DIVIDE       = 'DIVIDE'
TKN_LPAR         = 'LPAR'
TKN_RPAR         = 'RPAR'




class Token:
    def __init__(self, type_, value=None, token_start=None, token_end=None):
        self.type = type_
        self.value = value

        if token_start:
            self.token_start = token_start.copy()
            self.token_end = token_start.copy()
            self.token_end.advance()

        if token_end:
            self.token_end = token_end.copy()

    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


# Create the Tokenizer

class Tokenizer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            
            elif self.current_char in NUMS:
                tokens.append(self.make_number())
            
    
            
            elif self.current_char == '+':
                tokens.append(Token(TKN_ADD, token_start=self.pos))
                self.advance()
            
            elif self.current_char == '-':
                tokens.append(Token(TKN_SUBTRACT, token_start = self.pos))
                self.advance()
            
            elif self.current_char == '*':
                tokens.append(Token(TKN_MULTIPLY, token_start=self.pos))
                self.advance()
            
            elif self.current_char == '/':
                tokens.append(Token(TKN_DIVIDE, token_start=self.pos))
                self.advance()
          
            
            elif self.current_char == '(':
                tokens.append(Token(TKN_LPAR, token_start=self.pos))
                self.advance()
            
            elif self.current_char == ')':
                tokens.append(Token(TKN_RPAR, token_start=self.pos))
                self.advance()
          
            
            else:
                token_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], Illegal_Char(token_start, self.pos, "'" + char + "'")

        tokens.append(Token(TKN_EOF, token_start=self.pos))
        return tokens, None


     # Check if input is an integer or float and return a token of the corresponding type

    def make_number(self):
        num_str = ''
        decimal_count = 0
        token_start = self.pos.copy()

        while self.current_char != None and self.current_char in NUMS + '.':
            if self.current_char == '.':

                if decimal_count == 1: break
                decimal_count += 1
                num_str += '.'

            else:
                num_str += self.current_char

            self.advance()

        if decimal_count == 0:
            return Token(TKN_INT, int(num_str), token_start, self.pos)
        else:
            return Token(TKN_FLOAT, float(num_str), token_start, self.pos)



# Create class for Nodes

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.token_start = self.tok.token_start
        self.token_end = self.tok.token_end

    def __repr__(self):
        return f'{self.tok}'




class BinOpNode:
    def __init__(self, left_node, bo_token, right_node):
        self.left_node = left_node
        self.bo_token = bo_token
        self.right_node = right_node

        self.token_start = self.left_node.token_start
        self.token_end = self.right_node.token_end

    def __repr__(self):
        return f'({self.left_node}, {self.bo_token}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, bo_token, node):
        self.bo_token = bo_token
        self.node = node

        self.token_start = self.bo_token.token_start
        self.token_end = node.token_end

    def __repr__(self):
        return f'({self.bo_token}, {self.node})'





# Check if errors in parsing

class ParseChecker:
    def __init__(self):
        self.error = None
        self.node = None
 
    def register(self, res):
        if isinstance(res, ParseChecker):
            if res.error: self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


# Implement the Parser

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_index = -1
        self.advance()

    def advance(self, ):
        self.tok_index += 1
        if self.tok_index < len(self.tokens):
            self.current_token = self.tokens[self.tok_index]
        return self.current_token

    def parse(self):
        res = self.expression()
        if not res.error and self.current_token.type != TKN_EOF:
            return res.failure(Invalid_Syntax(
                self.current_token.token_start, self.current_token.token_end,
                "Expected '+', '-', '*', '/'"
            ))
        return res

 

     # Add and Subtract according to the grammar

    def expression(self):

        return self.binary_operation(self.term, (TKN_ADD, TKN_SUBTRACT))

    # Multiply and Divide according to the grammar

    def term(self):
        return self.binary_operation(self.factor, (TKN_MULTIPLY, TKN_DIVIDE))

    def factor(self):
        res = ParseChecker()
        tok = self.current_token

        if tok.type in (TKN_ADD, TKN_SUBTRACT):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        elif tok.type in (TKN_INT, TKN_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TKN_LPAR:
            res.register(self.advance())
            expression = res.register(self.expression())
            if res.error: return res
            if self.current_token.type == TKN_RPAR:
                res.register(self.advance())
                return res.success(expression)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_token.token_start, self.current_token.token_end,
                    "Expected ')'"
                ))

        return res.failure(Invalid_Syntax(
            tok.token_start, tok.token_end,
            "Expected an Integer or Float"
        ))





    def binary_operation(self, func,bo):

        res = ParseChecker()
        left = res.register(func())
        if res.error: return res

        while self.current_token.type in bo:

            bo_token = self.current_token
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, bo_token, right)

        return res.success(left)



class RunTime_Result:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self



class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.error_trace()


    def set_pos(self, token_start=None, token_end=None):
        self.token_start = token_start
        self.token_end = token_end
        return self

    def error_trace(self, error=None):
        self.error = error
        return self


    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).error_trace(self.error), None
        

    def subtract(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).error_trace(self.error), None
 

    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).error_trace(self.error), None
        else:
            return None, Value.illegal_operation(self, other)

    def divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTime_Error(
                    other.token_start, other.token_end,
                    'Division by zero',
                    self.error
                )

            return Number(self.value / other.value).error_trace(self.error), None
       
    
    def __repr__(self):
        return str(self.value)




# Class to show where the Error came from 



class Error_Trace:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
       



# Create the Interpreter


class Interpreter:
    def visit(self, node, error):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, error)

    def no_visit_method(self, node, error):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    

    def visit_NumberNode(self, node, error):
        return RunTime_Result().success(
            Number(node.tok.value).error_trace(error).set_pos(node.token_start, node.token_end)
        )


    # Handle Binary Operations

    def visit_BinOpNode(self, node, error):
        res = RunTime_Result()
        left = res.register(self.visit(node.left_node, error))
        if res.error: return res
        right = res.register(self.visit(node.right_node, error))
        if res.error: return res

        if node.bo_token.type == TKN_ADD:
            result, error = left.add(right)
        elif node.bo_token.type == TKN_SUBTRACT:
            result, error = left.subtract(right)
        elif node.bo_token.type == TKN_MULTIPLY:
            result, error = left.multiply(right)
        elif node.bo_token.type == TKN_DIVIDE:
            result, error = left.divide(right)
        

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.token_start, node.token_end))


    # Handle Unary Operations
    
    def visit_UnaryOpNode(self, node, error_trace):
        res = RunTime_Result()
        number = res.register(self.visit(node.node, error_trace))
        if res.error: return res

        error = None

        if node.bo_token.type == TKN_SUBTRACT:
            number, error = number.multiply(Number(-1))
       

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.token_start, node.token_end))

    
   

def run(fn, text):
    # Generate tokens
    tokenizer = Tokenizer(fn, text)
    tokens, error = tokenizer.make_tokens()
    if error: return None, error
    
    # Generate Abstract Syntax Tree
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    error = Error_Trace('<Program>')
    result = interpreter.visit(ast.node, error)

    return result.value, result.error
