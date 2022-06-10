class Token:

    """
    This class represents a token. A token is a single element that is part of a code line, be it
    a variable name, a type, or any simbol used in the programming language.

    Attributes
    ----------
    type: str
        the token type, as defined in the lexer_rules file
    value: str
        the token value
    """

    def __init__(self, type_, value):
        self.type = type_
        self.value = value
