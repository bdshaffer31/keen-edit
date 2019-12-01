
class ColorSet:

    # Every color set should set these to color values
    # self.background_color
    # self.select_color
    # self.main_text_color
    # self.accent1_color
    # self.accent2_color
    # self.accent3_color
    # self.accent4_color
    # self.accent5_color
    # self.accent6_color
    # self.accent7_color
    # self.unaccent_color

    def set_solarized(self):
        darker_gains  =  '#bfbfbf'
        gainsboro = '#DCDCDC'
        dark_blue =  '#004a5d' # dark dark blue #002b36
        soft_slate =  '#657b83' #slate ish v similiar to base01
        orange =  '#cb4b16'
        red    =  '#dc322f'
        magenta = '#d33682'
        violet =  '#6c71c4'
        blue   =  '#268bd2'
        cyan   =  '#2aa198'
        green  =  '#859900'

        self.background_color = gainsboro #dark_brown1
        self.select_color  = darker_gains

        self.main_text_color = dark_blue #tan
        self.accent1_color   = cyan #pale_plum
        self.accent2_color   = magenta #rosey_pink
        self.accent3_color   = red #slate_foam
        self.accent4_color   = green #pumpkin
        self.accent5_color   = violet #olive
        self.accent6_color   = blue #light_moss
        self.accent7_color   = orange #light_orange
        self.unaccent_color  = soft_slate #light_brown

        self.pair_tokens_colors()


    def set_kimbie_dark(self):
        dark_brown0 = '#51412c'
        dark_brown1 = '#221a0f'
        light_brown = '#a57a4c'
        tan = '#d3af86'
        pale_plum = '#98676a'
        rosey_pink = '#dc3958'
        slate_foam = '#8ab1b0'
        pumpkin = '#f06431'
        olive = '#7e602c'
        light_moss = '#889b4a'
        light_orange = '#f79a32'

        self.background_color = dark_brown1
        self.select_color  = dark_brown0

        self.main_text_color  = tan
        self.accent1_color    = pale_plum
        self.accent2_color    = rosey_pink
        self.accent3_color    = slate_foam
        self.accent4_color    = pumpkin
        self.accent5_color    = olive
        self.accent6_color    = light_moss
        self.accent7_color    = light_orange
        self.unaccent_color   = light_brown

        self.pair_tokens_colors()
        
    def pair_tokens_colors(self):
        self.token_colors = {
            'Token.Keyword':               self.accent1_color, 
            'Token.Keyword.Constant':      self.accent1_color, 
            'Token.Keyword.Declaration':   self.accent1_color, 
            'Token.Keyword.Namespace':     self.accent1_color, 
            'Token.Keyword.Pseudo':        self.accent1_color, 
            'Token.Keyword.Reserved':      self.accent1_color,
            'Token.Keyword.Type':          self.accent1_color,

            'Token.Name':                  self.main_text_color,
            'Token.Name.Attribute':        self.accent2_color,
            'Token.Name.Builtin':          self.accent2_color,
            'Token.Name.Builtin.Pseudo':   self.accent2_color,
            'Token.Name.Class':            self.accent4_color,
            'Token.Name.Constant':         self.accent2_color,
            'Token.Name.Decorator':        self.accent2_color,
            'Token.Name.Entity':           self.accent2_color,
            'Token.Name.Exception':        self.accent2_color, 
            'Token.Name.Function':         self.accent3_color,
            'Token.Name.Function.Magic':   self.accent5_color,
            'Token.Name.Label':            self.accent2_color,
            'Token.Name.Namespace':        self.accent2_color,
            'Token.Name.Other':            self.accent2_color,
            'Token.Name.Tag':              self.accent2_color,
            'Token.Name.Variable':         self.accent2_color,
            'Token.Name.Variable.Class':   self.accent2_color,
            'Token.Name.Variable.Global':  self.accent2_color,
            'Token.Name.Variable.Instance':self.accent2_color,
            'Token.Name.Variable.Magic':   self.accent2_color,

            'Token.Literal':               self.accent1_color,
            'Token.Literal.Date':          self.accent1_color,
            'Token.Literal.String.Single': self.accent6_color,
            'Token.Literal.String.Double': self.accent6_color,
            'Token.Literal.String.Interpol':self.accent7_color,
            
            'Token.String':                self.accent6_color,
            'Token.String.Affix':          self.accent6_color,
            'Token.String.Backtick':       self.accent6_color,
            'Token.String.Char':           self.accent6_color,
            'Token.String.Delimiter':      self.accent6_color,
            'Token.String.Doc':            self.accent6_color,
            'Token.String.Double':         self.accent6_color,
            'Token.String.Escape':         self.accent6_color,
            'Token.String.Heredoc':        self.accent6_color,
            'Token.String.Interpol':       self.accent6_color,
            'Token.String.Other':          self.accent6_color,
            'Token.String.Regex':          self.accent6_color,
            'Token.String.Single':         self.accent6_color,
            'Token.String.Symbol':         self.accent6_color,

            'Token.Literal.Number':        self.accent7_color,
            'Token.Literal.Number.Bin':    self.accent7_color,
            'Token.Literal.Number.Float':  self.accent7_color,
            'Token.Literal.Number.Hex':    self.accent7_color,
            'Token.Literal.Number.Integer.Long':self.accent7_color,
            'Token.Literal.Number.Integer':self.accent7_color,
            'Token.Literal.Number.Oct':    self.accent7_color,
            'Token.Literal.Number.Integer':self.accent7_color,
            'Token.Number':                self.accent7_color,
            'Token.Number.Bin':            self.accent7_color,
            'Token.Number.Float':          self.accent7_color,
            'Token.Number.Hex':            self.accent7_color,
            'Token.Number.Integer':        self.accent7_color,
            'Token.Number.Integer.Long':   self.accent7_color,
            'Token.Number.Oct':            self.accent7_color,

            'Token.Operator':              self.accent6_color,
            'Token.Operator.Word':         self.accent6_color,

            'Token.Punctuation':           self.main_text_color,

            'Token.Comment':               self.unaccent_color,
            'Token.Comment.Hashbang':      self.unaccent_color,
            'Token.Comment.Multiline':     self.unaccent_color,
            'Token.Comment.Preproc':       self.unaccent_color,
            'Token.Comment.Single':        self.unaccent_color,
            'Token.Comment.Special':       self.unaccent_color,

            'Token.Generic':               self.accent3_color,
            'Token.Generic.Deleted':       self.accent3_color,
            'Token.Generic.Emph':          self.accent3_color,
            'Token.Generic.Error':         self.accent3_color,
            'Token.Generic.Heading':       self.accent3_color,
            'Token.Generic.Inserted':      self.accent3_color,
            'Token.Generic.Output':        self.accent3_color,
            'Token.Generic.Prompt':        self.accent3_color,
            'Token.Generic.Strong':        self.accent3_color,
            'Token.Generic.Subheading':    self.accent3_color,
            'Token.Generic.Traceback':     self.accent3_color, 
        }