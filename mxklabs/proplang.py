import lark


class Transform(lark.Transformer):
    def string(self, (s,)):
        return s[1:-1]
    def number(self, (n,)):
        return float(n)

    list = list
    pair = tuple
    dict = dict

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False


json_parser = lark.Lark(r"""
    main: decls asserts
    
    decls: (decl)+
    ?decl: fun
    
    fun: "(" "declare-fun" id "(" ")" "Bool" ")"
    
    asserts: (assert)+
    ?assert: boolexpr
    
    ?boolexpr: or
               | id
    
    or : "(" "or" boolexpr boolexpr ")"
    
    id: /[A-Za-z_][A-Za-z_0-9]*/

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='main', parser='lalr', lexer="standard", debug=True)

#, transformer=Transform()

text = '''
(declare-fun v1 () Bool)
'''

'''
(declare-fun v2 () Bool)
(declare-fun v3 () Bool)
(assert (or v1 (not v2))) 
(assert (or v2 (not v1))) 
(assert (or v1 v3)) 
(assert (or v1 (not v3)))
'''

print "tokens=%r" % list(json_parser.lexer_conf.tokens)
b = list(json_parser.lex(text))
a = json_parser.parse(text)

print("%s" % b)
#print(b.pretty())
#print("--")
