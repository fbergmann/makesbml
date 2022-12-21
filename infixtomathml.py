

import sys
import re

def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'

token_exprs = [
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'\:=',                   RESERVED),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r';',                     RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'\*',                    RESERVED),
    (r'/',                     RESERVED),
    (r'<=',                    RESERVED),
    (r'<',                     RESERVED),
    (r'>=',                    RESERVED),
    (r'>',                     RESERVED),
    (r'!=',                    RESERVED),
    (r'=',                     RESERVED),
    (r'and',                   RESERVED),
    (r'or',                    RESERVED),
    (r'not',                   RESERVED),
    (r'if',                    RESERVED),
    (r'then',                  RESERVED),
    (r'else',                  RESERVED),
    (r'while',                 RESERVED),
    (r'do',                    RESERVED),
    (r'end',                   RESERVED),
    (r'[0-9]+',                INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

def call_lexer(characters):
    return lex(characters, token_exprs)


# Binary Tree in Python

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        #self.mathml = ''

    # Traverse preorder
    def traversePreOrder(self):
        mathml = ''
        if self.val == '+':
           mathml += '<apply> <plus/>' 
        if self.val == '-':
           mathml += '<apply> <minus/>' 
        if self.val == '*':
           mathml += '<apply> <times/>' 
        if self.val == '/':
           mathml += '<apply> <divide/>' 
           
        if not (self.val in ['+', '-', '*', '/']):
           mathml = mathml + '<ci>' + self.val + '</ci>'
            
        print(self.val, end=' ')
        
        if self.left:
            mathml += self.left.traversePreOrder()
        if self.right:
            mathml += self.right.traversePreOrder()
        if self.val in ['+', '-', '*', '/']:
           mathml += '</apply>'
        return mathml

    # Traverse inorder
    def traverseInOrder(self):
        if self.left:
            self.left.traverseInOrder()
        print(self.val, end=' ')
        if self.right:
            self.right.traverseInOrder()

    # Traverse postorder
    def traversePostOrder(self):
        if self.left:
            self.left.traversePostOrder()
        if self.right:
            self.right.traversePostOrder()
        print(self.val, end=' ')

class InfixToMathML:
    def __init__(self, infix):
        self.tokenPtr = 0
        self.token = None
        self.tokens = call_lexer(infix)
        
    def nextToken(self):
        if self.tokenPtr >= len (self.tokens):
            self.token = [0, 'None']
        else:   
            self.token = self.tokens[self.tokenPtr]
            self.tokenPtr += 1
    
    def factor (self):
        if self.token[1] == 'ID':
            n = Node(self.token[0])
            self.nextToken()
            return n
        if self.token[0] == '(':
            self.nextToken()
            n = self.expression()
    
            if self.token[0] != ')':
                raise Exception ('Missing right parenthesis')
            self.nextToken()
            return n

    def term (self):
        n1 = self.factor()
        while self.token[0] in ['*', '/']:
            op = self.token[0]
            self.nextToken()
            n2 = self.factor()
            n3 = Node (op)   
            n3.left = n1
            n3.right = n2
            n1 = n3
        return n1
                   
    def expression(self):
        n1 = self.term()
        #print ('n1 = ', n1.val)
        while self.token[0] in ['+', '-']:
            op = self.token[0]
            self.nextToken()
            n2 = self.term()
            n3 = Node (op)   
            n3.left = n1
            n3.right = n2
            n1 = n3      
        return n1
        
    def stmt (self):
        return self.expression()   

    def parse (self):
        self.nextToken()
        return self.stmt ()
    
    def getMathML (self):
        tree = self.parse ()
        mathml = '<math xmlns="http://www.w3.org/1998/Math/MathML">' + '\n'
        m = tree.traversePreOrder()
        mathml += m + '\n' + '</math>'
        return mathml
