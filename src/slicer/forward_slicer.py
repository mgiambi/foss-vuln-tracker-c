from src.slicer.parent_slicer import ParentSlicer
from src.change.line import Line
from typing import List


class ForwardSlicer(ParentSlicer):

    def __init__(self):
        ParentSlicer.__init__(self)

    def _forward_slice(self, lines: List[Line], seeds: List[Line]) -> List[Line]:
        final_slice = []
        current_method = ""

        for line in lines:
            current_method = line.method_name

            if line.line_number in [seed.line_number for seed in seeds] and line.line_def:
                line.line_rel.extend(line.line_def)
                # Point 2a
                line.line_rel.extend(line.line_ref)

            # Point 1b
            for prev_line in final_slice:
                if self._is_predicate_of(prev_line, line, lines) or \
                        self._intersection(prev_line.line_rel, line.line_ref):
                    if not line.line_rel and prev_line.method_name == current_method:
                        line.line_rel.extend(line.line_def)
                        # Point 2b
                        if self._intersection(prev_line.line_rel, line.line_ref):
                            line.line_rel.extend(line.line_ref)

            if line.line_rel:
                final_slice.append(line)

        return final_slice
