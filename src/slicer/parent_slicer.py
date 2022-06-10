from src.change.line import Line


class ParentSlicer:

    def __init__(self):
        pass

    def _intersection(self, list_1, list_2):
        """
        This method checks whether two lists of tokens have at least one element in common.
        """
        if not list_1 or not list_2:
            return False

        for token_1 in list_1:
            for token_2 in list_2:
                if token_1.type == token_2.type and token_1.value == token_2.value:
                    return True

        return False

    # Checks whether s is a control flow statement, and t is a statement whose
    # execution is affected by s

    def _is_predicate_of(self, s_line, t_line, lines):
        """
        This method checks whether s is a control flow statement, and t is a statement whose execution
        is affected by s.

        Parameters
        ----------
        s_line: Line
            the s statement
        t_line: Line
            the t statement
        lines: list of Line
            the code lines of the method which s and t are part of
        """

        s_line_number = s_line.line_number
        t_line_number = t_line.line_number
        first_line = lines[0].line_number
        last_line = lines[-1].line_number

        s_token_types = [token.type for token in t_line.line_tokens]
        t_token_types = [token.type for token in s_line.line_tokens]

        if any(x in s_token_types for x in ['FOR', 'WHILE', 'IF', 'ELIF']):
            line_number = s_line_number
            left_paren_count = 0
            right_paren_count = 0
            do = False

            current_line = next((line for line in lines if line.line_number == line_number))

            while line_number in range(current_line.method_start, current_line.method_end + 1) and current_line.line_number is not None:
                current_tokens = [token.type for token in current_line.line_tokens]
                left_paren_count += current_tokens.count('LCURPAREN')
                right_paren_count += current_tokens.count('RCURPAREN')

                # If it's the first iteration...
                if current_line.line_number == s_line_number:
                    # If s in an 'else if' statement, add 'fake' parenthesis
                    if right_paren_count - left_paren_count == 0:
                        left_paren_count += 1
                    # If s is a 'do..while, it must be saved so the loop can go backwards'
                    if right_paren_count == 1 and left_paren_count == 0 and 'WHILE' in s_token_types:
                        do = True
                # If s and t are the same line, return True
                if t_line_number == s_line_number:
                    return True
                # If t is outside the loop block, return False
                elif right_paren_count - left_paren_count == 0 and current_line.line_number != s_line_number:
                    return False
                # If end or beginning of code block is reached, return False (NOT SURE THIS LINE IS NECESSARY)
                elif line_number == first_line or line_number == last_line:
                    return False
                # If t is inside the loop
                elif t_line_number == line_number:
                    # If s is an if statement...
                    if any(x in s_token_types for x in ['IF', 'ELIF']):
                        # ... and t is and 'else if' or 'else' that is part of the same block, return False
                        if right_paren_count - left_paren_count == 1 and any(x in t_token_types for x in ['IF', 'ELIF', 'ELSE']):
                            return False
                        # otherwise, return True
                        else:
                            return True
                    else:
                        return True

                if do:
                    line_number -= 1
                else:
                    line_number += 1

                current_line = next((line for line in lines if line.line_number == line_number), Line())

        return False
