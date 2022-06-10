from src.lexer.lexer_rules import extract_tokens
from src.lexer.token import Token


class Tokenizer:

    def __init__(self):
        pass

    def tokenize(self, lines):
        """
        This method takes a list of code lines and runs the lexer to extract tokens.

        Parameters
        ----------
        lines: list of Line
            the list of code lines

        Returns
        -------
        list of Line
            the list of input lines with tokens
        """

        is_comment = False
        is_string = False
        tokenized_lines = lines

        for line in tokenized_lines:

            line_tokens = extract_tokens(line.line_text)
            tokens = []

            #
            #   This block catches some token types that are not easily identifiable via lexer rules
            #

            for token in line_tokens:
                # Catch custom types and classes
                if tokens and token.type == 'ID':
                    if tokens[-1].type == 'ID':
                        last_token = tokens.pop()
                        tokens.append(Token('ID_TYPE', last_token.value))

                tokens.append(token)

                # Catch strings
                if tokens and is_string:
                    last_token = tokens.pop()
                    tokens.append(Token('STRING', last_token.value))

                # Catch inline comments
                if tokens and token.type == 'COMMENTINLINE':
                    break

                # Catch multiline comments
                if tokens and is_comment and token.type != 'COMMENTEND':
                    last_token = tokens.pop()
                    tokens.append(Token('COMMENT', last_token.value))

                # Catch struct and class variables
                if len(tokens) >= 3 and tokens[-1].type == 'ID' and tokens[-2].type == 'DOT' and tokens[-3].type == 'ID':
                    last_element = tokens.pop()
                    tokens.pop()
                    third_to_last_element = tokens.pop()
                    tokens.append(
                        Token('DOT_ID', third_to_last_element.value + '.' + last_element.value))

                # Catch scope resolution operator (C++)
                if len(tokens) >= 4 and tokens[-2].type == 'POINTS' and tokens[-3].type == 'POINTS' and tokens[-4].type == 'ID':
                    last_element = tokens.pop()
                    tokens.pop()
                    tokens.pop()
                    fourth_to_last_element = tokens.pop()
                    tokens.append(Token('SCOPE_ID', fourth_to_last_element.value + '::' + last_element.value))

                # Catch function calls
                if len(tokens) >= 2 and tokens[-1].type == 'LPAREN' and (tokens[-2].type == 'ID' or tokens[-2].type == 'DOT_ID' or tokens[-2].type == 'SCOPE_ID'):
                    tokens.pop()
                    last_token = tokens.pop()
                    tokens.append(Token('ID_FUNCTION', last_token.value))
                    tokens.append(Token('LPAREN', '('))

                if token.type == 'COMMENTSTART':
                    is_comment = True
                if token.type == 'COMMENTEND':
                    is_comment = False

                if token.type == 'QUOTE':
                    if is_string:
                        is_string = False
                    else:
                        is_string = True

            line.line_tokens = tokens

        return tokenized_lines
