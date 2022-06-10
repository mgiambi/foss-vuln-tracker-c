import itertools


class Line:
    """
    This class represents a single line of code.

    Attributes
    ----------
    line_number: int
        the number of the line in the file
    line_text: str
        the text of the line
    method_start: int
        the first line number of the method in which the line is contained; if the line is not
        part of a method, it's -1
    method_end: int
        the last line number of the method in which the line is contained; if the line is not
        part of a method, it's -1
    method_name: str
        the name of the method which the line is a part of; if the line is not part of a method,
        it's empty
    line_def: list of Token
        the def of the line, as described in the reference paper
    line_ref: list of Token
        the ref of the line, as described in the reference paper
    line_rel: list of Token
        the rel of the line, as described in the reference paper
    line_tokens: list of Token
        the list of tokens in the line
    """

    def __init__(self, line_number=None, line_text=None, method_start=-1, method_end=-1, method_name=""):
        self.line_number = line_number
        self.line_text = line_text
        self.method_start = method_start
        self.method_end = method_end
        self.method_name = method_name
        self.line_def = []
        self.line_ref = []
        self.line_rel = []
        self._line_tokens = []
        self.equals_list = ['EQUAL', 'PLUSEQUAL', 'MINUSEQUAL', 'TIMESEQUAL']

    @property
    def line_tokens(self):
        return self._line_tokens

    @line_tokens.setter
    def line_tokens(self, value):
        """
        When the tokens for the line are extracted, this sets the def and ref of the line, using
        the methodology described in the paper.
        """

        self._line_tokens = value

        self.line_def.clear()
        for token_1, token_2 in self.__pairwise(self._line_tokens):
            if (token_1.type == 'ID' or token_1.type == 'DOT_ID') and (token_2.type in self.equals_list or token_2.type == 'END'):
                self.line_def.append(token_1)

        self.line_ref.clear()
        for token_1, token_2 in self.__pairwise(self._line_tokens):
            if (token_1.type == 'ID' or token_1.type == 'DOT_ID') and token_2.type not in self.equals_list:
                self.line_ref.append(token_1)

    def __pairwise(self, iterable):
        a, b = itertools.tee(iterable)
        next(b, None)

        return zip(a, b)
