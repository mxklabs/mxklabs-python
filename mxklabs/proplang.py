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
    ?value: dict
          | list
          | string
          | SIGNED_NUMBER      -> number
          | "true"             -> true
          | "false"            -> false
          | "null"             -> null

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : string ":" value

    string : ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='value', parser='lalr', transformer=Transform())

text = '{"key": ["item0", "item1", 3.14]}'
b = json_parser.parse(text)

print(b)
print("--")
