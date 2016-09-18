import tensor4

class VarSeries:
    def __init__(self, tensors):
        self.tensors = tensors

    def derive(self, old_index, new_index):
        new_tensors = []
        for i in self.tensors:
            new_tensors.append( tensor.derive[new_index,old_index] * i)
        return VarSeries(new_tensors)

    def solve1d(self, inits, old_index, new_index):
        
        size = tensor4.Tensor.default_size
        solution = inits[::] + [None]*(size-len(inits))
        tensor = self.tensors[0]
        series = self.tensors[1]
        
        for i in range(size):
            non_zeroes = []
            undetermined = []
            for j in range(size):
                kwarg = {old_index: i, new_index: j}
                if tensor(**kwarg) != 0:
                    if solution[j] is not None:
                        non_zeroes.append(j)
                    else:
                        undetermined.append(j)
            if len(undetermined) > 1:
                raise IndexError("too many undetermined")

            for j in undetermined:
                kwarg = {old_index: i, new_index: j}
                sol = -series(**{old_index: i})
                for root in non_zeroes:
                    new_kwarg = {old_index: i, new_index: root}
                    print(solution[root], tensor(**kwarg))
                    sol = sol - solution[root]*tensor(**new_kwarg)
                
                solution[j] = sol / (tensor(**kwarg))
        print(solution)
        return tensor4.Tensor(solution)

    def solve(self): pass

    def __str__(self):
        string = ""
        for i in self.tensors:
            string += str(i) + '\n'
        return string
