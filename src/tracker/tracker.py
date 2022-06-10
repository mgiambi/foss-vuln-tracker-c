class VulnerabilityTracker:

    def __init__(self):
        pass

    def find_evidence(self, revision, slice):
        evidence = []

        for slice_line in sorted(slice, key=lambda x: x.line_number):
            revision_line = [item for item in revision.diff.range if item[1] == str(slice_line.line_number)]

            if revision_line:
                line_to_append = slice_line
                line = revision_line[0]
                line_to_append.line_number = line[0]
                evidence.append(line_to_append)

        return sorted(evidence, key=lambda x: x.line_number)
