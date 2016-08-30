import tens

class VarSeries:
    def __init__(self, tensors):
        self.tensors = tensors

    def derive(self, old_index, new_index):
        new_tensors = []
        for i in self.tensors:
            new_tensors.append( tens.derive[new_index,old_index] * i)
        return VarSeries(new_tensors)

    def __str__(self):
        string = ""
        for i in self.tensors:
            string += str(i) + '\n'
        return string
