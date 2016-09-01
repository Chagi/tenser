import itertools

class Tensor:
    default_size = 3
    def __init__(self, func, *index):
        if isinstance(func, (list,tuple)):
            def new_func(*args):
                if len(args) == 1:
                    return func[args[0]]
                else:
                    return new_func(*args[:-1])[args[-1]]
            self.func = new_func
        else:
            if f.__code__.co_argcount != len(index):
                raise IndexError('no. indiices must match f args')
            self.func = func
        self.index = index
        self.argcount = len(index)

    def __getitem__(self,index):
        return Tensor(self.func, *index)

    def __add__(self, other):
        if not set(self.index) == set(other.index):
            raise IndexError('bad index')
        ind_dict = {val: pos for pos,val in enumerate(self.index)}
        def new_func(*args):
            a = self.func(*(args[ind_dict[i]] for i in self.index))
            b = other.func(*(args[ind_dict[i]] for i in self.index))
            return a+b

        return Tensor(new_func, *self.index)

    def __mul__(self, other):
        total_index = {}
        for i in self.index + other.index:
            try:
                total_index[i] += 1
            except KeyError:
                total_index[i] = 1
                
        new_index = []
        sum_index = []
        for key in total_index:
            if total_index[key] > 2:
                raise IndexError('more than 2 occurencanse of one index')
            elif total_index[key] == 2:
                sum_index.append(key)
            elif total_index[key] == 1:
                new_index.append(key)

        ind_dict = {val: pos for pos,val in enumerate(new_index+sum_index)}

        def new_func(*args):
            s = 0
            for i in itertools.product(range(Tensor.default_size),repeat=len(sum_index)):
                tot_args = args + i
                tot_index = new_index + sum_index
                a = self.func(*(tot_args[ind_dict[i]] for i in self.index))
                b = other.func(*(tot_args[ind_dict[i]] for i in other.index))
                s += a*b
            return s
        return Tensor(new_func, *new_index)
        
            

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
                if len(i) > 1 and i[-2] == default_size-1:
                    breakpoints += [vert_index]
                strings.append(str(self.func(*i)))
            #string.append(str(self.func(*i)))
        return "\n".join((val+"\n") if pos in breakpoints else val for pos,val in enumerate(strings))

    def __str__(self):
        return self.string()


def product(iterable):
    p = 1
    for i in iterable:
        p *= i
    return p

eps = Tensor(lambda i,j,k:(1 if (k-j)%3==1 else -1)*(1 if set((i,j,k)) == set((0,1,2)) else 0),'i','j','k')
delta = Tensor(lambda i,j: int(i==j),'i','j')

derive = Tensor(lambda i,j: j if i+1 == j else 0 , 'i','j')
exp = Tensor(lambda i: 1/product(range(1,i+1)) , 'i')



