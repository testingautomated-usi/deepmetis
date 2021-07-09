import rasterization_tools


class Digit:
    def __init__(self, desc, label):
        self.xml_desc = desc
        self.expected_label = label
        self.purified = rasterization_tools.rasterize_in_memory(self.xml_desc)
        self.confidence = list()
        self.predicted_label = list()
        self.confidence_original = list()
        self.predicted_label_original = list()

    def clone(self):
        clone_digit = Digit(self.xml_desc, self.expected_label)
        return clone_digit
