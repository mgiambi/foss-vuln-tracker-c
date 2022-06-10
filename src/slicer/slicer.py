from src.slicer.forward_slicer import ForwardSlicer
from src.slicer.backward_slicer import BackwardSlicer
from src.change.change import ModifiedFile
from src.change.line import Line
from typing import List


class Slicer:

    def __init__(self):
        self.forward_slicer = ForwardSlicer()
        self.backward_slicer = BackwardSlicer()

    def remove_useless_lines(self, lines):
        """
        This methods filters a code segment to remove all the lines that are useless for slicing,
        meaning all lines that do not contain a variable or are #define statements. This is done prior
        to slicing to improve performance.

        Parameters
        ----------
        lines: list of Line
            the code lines to filter

        Returns
        -------
        list of Line:
            the filtered code lines
        """
        clean_lines = []

        for line in lines:
            if line.line_tokens and line.line_tokens[0].type != 'HASH':
                for token in line.line_tokens:
                    if line.line_tokens and (token.type == 'ID' or token.type == 'DOT_ID' or token.type == 'SCOPE_ID'):
                        clean_lines.append(line)
                        break

        return clean_lines

    def __combine_slices(self, slice_new, slice_old, diff):
        """
        This method combines the slices for the new and old revision of a file, creating a new slice with
        only the code lines that are shared between the two.

        Parameters
        ----------
        slice_new: list of Line
            the lines in the new revision slice
        slice_old: list of Line
            the lines in the old revision slice

        Returns
        -------
        list of Line:
            the combined slice
        """
        evidence_lines = []
        used_numbers = []
        #slice_new_line_numbers = [str(line.line_number) for line in slice_new]
        #slice_old_line_numbers = [str(line.line_number) for line in slice_old]

        #for _tuple in diff.range:
            #if _tuple[0] in slice_old_line_numbers and _tuple[1] in slice_new_line_numbers:
                #evidence_lines.append([line for line in slice_new if str(line.line_number) == _tuple[1]][0])

        for line_1 in slice_new:
            for line_0 in slice_old:
                if line_1.line_text == line_0.line_text and line_1.line_number not in used_numbers:
                    evidence_lines.append(line_1)
                    used_numbers.append(line_1.line_number)
                    break

        return evidence_lines

    def make_slice(self, change: ModifiedFile, light: bool) -> List[Line]:
        slice_new = []
        slice_old = []
        used_numbers = []

        # make forward and backward slice for both the new revision and old revision of the input file
        for_slice_new = self.forward_slicer._forward_slice(change.new_revision, change.added_lines)
        bck_slice_new = self.backward_slicer._backward_slice(change.new_revision, change.added_lines, light)

        for_slice_old = self.forward_slicer._forward_slice(change.old_revision, change.removed_lines)
        bck_slice_old = self.backward_slicer._backward_slice(change.old_revision, change.removed_lines, light)

        # combine forward and backward slice of the new revision, making a union between the two lists
        for line in for_slice_new:
            if line.line_number not in used_numbers:
                slice_new.append(line)
                used_numbers.append(line.line_number)

        for line in bck_slice_new:
            if line.line_number not in used_numbers:
                slice_new.append(line)
                used_numbers.append(line.line_number)

        used_numbers = []

        # combine forward and backward slice of the old revision, making a union between the two lists
        for line in for_slice_old:
            if line.line_number not in used_numbers:
                slice_old.append(line)
                used_numbers.append(line.line_number)
        for line in bck_slice_old:
            if line.line_number not in used_numbers:
                slice_old.append(line)
                used_numbers.append(line.line_number)

        # combine the slices of the new and old revision, making an intersection between the two lists
        return self.__combine_slices(slice_new, slice_old, change.diff)
