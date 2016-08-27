import itertools

def product(iterable):
    p = 1
    for i in iterable:
        p *= i
    return p

class Tensor:
    default_size = 3
    def __init__(self, f=None):
        self.func = f
        self.argcount = 0 if f is None else f.__code__.co_argcount

    def __getitem__(self, index):
        return IndexedTensor(self, index)

    def __setitem__(self, index, expr):
        def new_func(*args):
            return expr.evaluate(tuple(index), args)
        self.func = new_func
        self.argcount = len(index)

    def string(self, default_size = None, sizes = None):
        sizes = [] if sizes is None else sizes
        default_size = self.default_size if default_size is None else default_size
        while len(sizes) < self.argcount:
            sizes.append(default_size)
            
        sizes = sizes[:self.argcount]
        print(sizes,self.argcount)

        strings = []
        breakpoints = []
        for i in itertools.product(*(range(i) for i in sizes)):
            hor_index = sum(val*default_size**(pos//2) for pos,val in enumerate(reversed(i)) if pos % 2 == 0)
            vert_index = sum(val*default_size**(pos//2) for pos,val in enumerate(reversed(i)) if pos % 2 == 1)
            #print(i, hor_index, vert_index)
            try:
                strings[vert_index] += ("\t" if i[-1] == 0 else " ") + str(self.func(*i))
            except IndexError:
                if i[-2] == default_size-1:
                    breakpoints += [vert_index]
                strings.append(str(self.func(*i)))
            #string.append(str(self.func(*i)))
        return "\n".join((val+"\n") if pos in breakpoints else val for pos,val in enumerate(strings))

    def __str__(self):
        return self.string()


class IndexedTensor:
    def __init__(self, tensor, index):
        if len(index) != tensor.argcount:
            raise IndexError('must have correct no. indices')
        
        self.tensor = tensor
        self.index = index

    def __mul__(self, other):
        return TensorTerm([self, other])

    def __add__(self, other):
        return TensorTerm([self]) + TensorTerm([other])

    def evaluate(self, index, args, sum_index, sum_args):
        total_index = index + sum_index
        total_args = args + sum_args
        
        ind_dict = {} # easy access to the position of an index
        for pos,val in enumerate(total_index):
            ind_dict[val] = pos

        pos_list = []
        for i in self.index:
            pos_list.append(ind_dict[i])
            
        return self.tensor.func(*(total_args[i] for i in pos_list))

class TensorTerm:
    def __init__(self, tensors):
        self.tensors = tensors
        ind_dict = {}
        for ten in tensors:
            for i in ten.index:
                try:
                    ind_dict[i] += 1
                except KeyError:
                    ind_dict[i] = 1
                    
        self.index = []
        self.sum_index = []
        for key in ind_dict:
            if ind_dict[key] > 2:
                raise IndexError('more than 2 occurencanse of one index')
            elif ind_dict[key] == 2:
                self.sum_index.append(key)
            elif ind_dict[key] == 1:
                self.index.append(key)

    def __mul__(self, other):
        return TensorTerm(self.tensors + other.tensors)

    def __add__(self, other):
        return TensorExpr([self, other])

    def evaluate(self, index, args):
        summ = []
        for i in itertools.product(range(Tensor.default_size), repeat=len(self.sum_index) ):
            factors = []
            for tensor in self.tensors:
                factors.append( tensor.evaluate(index, args, tuple(self.sum_index), i) )
            prod = product(factors)
            summ.append(prod)
        return sum(summ)
        
        

class TensorExpr:
    def __init__(self, terms):
        test_index = set(terms[0].index)
        for i in terms:
            if set(i.index) != test_index:
                raise IndexError('terms must have same indices')

        self.terms = terms
        

    def __add__(self, other):
        return TensorExpr(self.terms + other.terms)

    def evaluate(self, index, args):
        summ = []
        for i in self.terms:
            summ.append( i.evaluate(index, args) )
        return sum(summ)



eps = Tensor(lambda i,j,k:(1 if (k-j)%3==1 else -1)*(1 if set((i,j,k)) == set((0,1,2)) else 0))
delta = Tensor(lambda i,j: int(i==j))









            
