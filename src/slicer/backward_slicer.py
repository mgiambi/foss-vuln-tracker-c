from src.slicer.parent_slicer import ParentSlicer
from src.change.line import Line
from typing import List


class BackwardSlicer(ParentSlicer):

    def __init__(self):
        ParentSlicer.__init__(self)

    def __reverse_list(self, list_: list) -> list:
        ret_list = []

        for element in list_:
            ret_list.insert(0, element)

        return ret_list

    def _backward_slice(self, lines: List[Line], seeds: List[Line], light: bool) -> List[Line]:
        final_slice = []
        current_method = ""

        for line in self.__reverse_list(lines):
            current_method = line.method_name

            # Point 1
            for seed in seeds:
                if line.line_number == seed.line_number:
                    line.line_rel.extend(line.line_ref)
                    break

            # Point 2
            for succ_line in final_slice:
                if self._intersection(succ_line.line_rel, line.line_def) and not line.line_rel and succ_line.method_name == current_method:
                    line.line_rel.extend(line.line_ref)
                    break

            # Point 3 (NOT IMPLEMENTED)
            # if not light:
                # Todo => implement conservative slicing

            # Point 4
            for succ_line in final_slice:
                if self._is_predicate_of(line, succ_line, lines) \
                        and succ_line.line_rel and not line.line_rel and succ_line.method_name == current_method:
                    line.line_rel.extend(line.line_ref)
                    break

            if line.line_rel:
                final_slice.append(line)

        return final_slice
