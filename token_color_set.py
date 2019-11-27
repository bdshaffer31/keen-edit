
class TokenColorSet:

    def __init__(self):
        # default theme
        base02 =  '#073642'
        base01 =  '#586e75'
        base03 =  '#002b36'
        base00 =  '#657b83'
        base0  =  '#839496'
        base1  =  '#93a1a1'
        base2  =  '#eee8d5'
        base3  =  '#fdf6e3'
        yellow =  '#b58900'
        orange =  '#cb4b16'
        red    =  '#dc322f'
        magenta = '#d33682'
        violet =  '#6c71c4'
        blue   =  '#268bd2'
        cyan   =  '#2aa198'
        green  =  '#859900'
        
        self.token_colors = {
            'Token.Keyword':               base02, 
            'Token.Keyword.Constant':      base02, 
            'Token.Keyword.Declaration':   base02, 
            'Token.Keyword.Namespace':     base02, 
            'Token.Keyword.Pseudo':        base02, 
            'Token.Keyword.Reserved':      base02,
            'Token.Keyword.Type':          base02,

            'Token.Name':                  orange,
            'Token.Name.Attribute':        orange,
            'Token.Name.Builtin':          orange,
            'Token.Name.Builtin.Pseudo':   orange,
            'Token.Name.Class':            orange,
            'Token.Name.Constant':         orange,
            'Token.Name.Decorator':        orange,
            'Token.Name.Entity':           orange,
            'Token.Name.Exception':        orange, 
            'Token.Name.Function':         orange,
            'Token.Name.Function.Magic':   orange,
            'Token.Name.Label':            orange,
            'Token.Name.Namespace':        orange,
            'Token.Name.Other':            orange,
            'Token.Name.Tag':              orange,
            'Token.Name.Variable':         orange,
            'Token.Name.Variable.Class':   orange,
            'Token.Name.Variable.Global':  orange,
            'Token.Name.Variable.Instance':orange,
            'Token.Name.Variable.Magic':   orange,

            'Token.Literal':               magenta,
            'Token.Literal.Date':          magenta,

            'Token.String':                violet,
            'Token.String.Affix':          violet,
            'Token.String.Backtick':       violet,
            'Token.String.Char':           violet,
            'Token.String.Delimiter':      violet,
            'Token.String.Doc':            violet,
            'Token.String.Double':         violet,
            'Token.String.Escape':         violet,
            'Token.String.Heredoc':        violet,
            'Token.String.Interpol':       violet,
            'Token.String.Other':          violet,
            'Token.String.Regex':          violet,
            'Token.String.Single':         violet,
            'Token.String.Symbol':         violet,

            'Token.Number':                blue,
            'Token.Number.Bin':            blue,
            'Token.Number.Float':          blue,
            'Token.Number.Hex':            blue,
            'Token.Number.Integer':        blue,
            'Token.Number.Integer.Long':   blue,
            'Token.Number.Oct':            blue,

            'Token.Operator':              green,
            'Token.Operator.Word':         green,

            'Token.Punctuation':           base00,

            'Token.Comment':               base03,
            'Token.Comment.Hashbang':      base03,
            'Token.Comment.Multiline':     base03,
            'Token.Comment.Preproc':       base03,
            'Token.Comment.Single':        base03,
            'Token.Comment.Special':       base03,

            'Token.Generic':               red,
            'Token.Generic.Deleted':       red,
            'Token.Generic.Emph':          red,
            'Token.Generic.Error':         red,
            'Token.Generic.Heading':       red,
            'Token.Generic.Inserted':      red,
            'Token.Generic.Output':        red,
            'Token.Generic.Prompt':        red,
            'Token.Generic.Strong':        red,
            'Token.Generic.Subheading':    red,
            'Token.Generic.Traceback':     red, 
        }

    def set_solarized(self):
        self.base02 =  '#073642'
        self.base01 =  '#586e75'
        self.base03 =  '#002b36'
        self.base00 =  '#657b83'
        self.base0  =  '#839496'
        self.base1  =  '#93a1a1'
        self.base2  =  '#eee8d5'
        self.base3  =  '#fdf6e3'
        self.yellow =  '#b58900'
        self.orange =  '#cb4b16'
        self.red    =  '#dc322f'
        self.magenta = '#d33682'
        self.violet =  '#6c71c4'
        self.blue   =  '#268bd2'
        self.cyan   =  '#2aa198'
        self.green  =  '#859900'