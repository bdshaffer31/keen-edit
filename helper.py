tokens = """Keyword
Keyword.Constant
Keyword.Declaration
Keyword.Namespace
Keyword.Pseudo
Keyword.Reserved
Keyword.Type
Name
Name.Attribute
Name.Builtin
Name.Builtin.Pseudo
Name.Class
Name.Constant
Name.Decorator
Name.Entity
Name.Exception
Name.Function
Name.Function.Magic
Name.Label
Name.Namespace
Name.Other
Name.Tag
Name.Variable
Name.Variable.Class
Name.Variable.Global
Name.Variable.Instance
Name.Variable.Magic
Literal
Literal.Date
String
String.Affix
String.Backtick
String.Char
String.Delimiter
String.Doc
String.Double
String.Escape
String.Heredoc
String.Interpol
String.Other
String.Regex
String.Single
String.Symbol
Number
Number.Bin
Number.Float
Number.Hex
Number.Integer
Number.Integer.Long
Number.Oct
Operator
Operator.Word
Punctuation
Comment
Comment.Hashbang
Comment.Multiline
Comment.Preproc
Comment.Single
Comment.Special
Generic
Generic.Deleted
Generic.Emph
Generic.Error
Generic.Heading
Generic.Inserted
Generic.Output
Generic.Prompt
Generic.Strong
Generic.Subheading
Generic.Traceback"""

split_tokens = tokens.split('\n')
for token in split_tokens:
    # add spaces
    fist_str = '\'' + 'Token.' + token + '\'' + ':' + (' ' * (22-len(token)))

    print( fist_str + 'self.color, ' )