from tensor4 import *

def empty_mat(sizes):
    if len(sizes) == 0:
        return None
    lis = []
    for i in range(sizes[0]):
        lis.append(empty_mat(sizes[1:]))
    return lis

def set_item(lis, index, item):
    if len(index) == 1:
        lis[index[0]] = item
    else:
        set_item(lis[index[0]], index[1:], item)

def get_item(lis, index):
    if len(index) == 0:
        return lis
    else:
        return get_item(lis[index[0]], index[1:])

class VarSeries:
    def __init__(self, tensors):
        self.tensors = tensors

    def derive(self, old_index, new_index):
        new_tensors = []
        for i in self.tensors:
            new_tensors.append( tensor.derive[new_index,old_index] * i)
        return VarSeries(new_tensors)

    def solve1d(self, inits, old_index, new_index):
        
        size = Tensor.default_size
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
                    sol = sol - solution[root]*tensor(**new_kwarg)
                
                solution[j] = sol / (tensor(**kwarg))
        return Tensor(solution, old_index)

    def solve(self, inits, old_index, new_index):
        
        size = Tensor.default_size
        tensor = self.tensors[0]
        #series = self.tensors[1]

        solution = []
        for i in range(Tensor.default_size):
            if i < len(inits):
                solution.append(inits[i].to_list())
            else:
                solution.append(empty_mat([Tensor.default_size]*(len(new_index)-1)))

        
        for i in itertools.product(range(size),repeat=len(old_index)):
            non_zeroes = []
            undetermined = []
            for j in itertools.product(range(size),repeat=len(new_index)):
                kwarg = dict(zip(old_index, i))
                kwarg.update(dict(zip(new_index, j)))
                if tensor(**kwarg) != 0:
                    if get_item(solution , j) is not None:
                        non_zeroes.append(j)
                    else:
                        undetermined.append(j)
            #print(non_zeroes,undetermined, i)
            if len(undetermined) > 1:
                #print(solution)
                #raise IndexError("too many undetermined")
                continue

            for j in undetermined:
                kwarg = dict(zip(old_index, i))
                kwarg.update(dict(zip(new_index, j)))
                
                #sol = -series(**{old_index: i})
                sol = 0
                
                for root in non_zeroes:
                    new_kwarg = dict(zip(old_index, i))
                    new_kwarg.update(dict(zip(new_index, root)))
                    
                    sol = sol - get_item(solution , root)*tensor(**new_kwarg)
                
                set_item( solution , j , sol / (tensor(**kwarg)) )
        #print(solution)
        return Tensor(solution, *new_index)

    
    def __str__(self):
        string = ""
        for i in self.tensors:
            string += str(i) + '\n'
        return string

Tensor.default_size = 8
matr = derive['i','j']*derive['j','k'] + delta['i','k']
B = VarSeries([matr , Tensor(lambda i: 0, 'i')])
sin = B.solve1d([0,1],'i','k')


Q = VarSeries([laplace2d])
W = Q.solve([Tensor(lambda i:1 , 'i'),Tensor(lambda i:2 , 'i')] , ('x1','y1') , ('x2','y2') )





