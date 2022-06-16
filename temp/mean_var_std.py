import numpy as np
from pandas import array

# import pprint

# pp = pprint.PrettyPrinter()

d = {
    'mean': [],
    'variance': [],
    'standard deviation': [],
    'max': [],
    'min': [],
    'sum': []
}


def calculate() -> dict:
    # try-except for length of list as well
    try:

        list_input = input("Enter 9 digits: ")
        matrix_list = [int(i) for i in list_input]

        np_array = np.asarray(matrix_list)
        a = np.reshape(np_array, (3, 3))

        mean = [(np.mean(a, axis=0)), (np.mean(a, axis=1)), np.mean(a)]
        [d['mean'].append(i.tolist()) for i in mean]

        variance = [(np.var(a, axis=0)), (np.var(a, axis=1)), np.var(a)]
        [d['variance'].append(i.tolist()) for i in variance]

        std = [(np.std(a, axis=0)), (np.std(a, axis=1)), np.std(a)]
        [d['standard deviation'].append(i.tolist()) for i in std]

        max = [(np.max(a, axis=0)), (np.max(a, axis=1)), np.max(a)]
        [d['max'].append(i.tolist()) for i in max]

        min = [(np.min(a, axis=0)), (np.min(a, axis=1)), np.min(a)]
        [d['min'].append(i.tolist()) for i in min]

        sum = [(np.sum(a, axis=0)), (np.sum(a, axis=1)), np.sum(a)]
        [d['sum'].append(i.tolist()) for i in sum]

        print(d)





    except ValueError:
        print("List must contain nine numbers.")


calculate()

# def avg():
#     mean = [(np.mean(a, axis=0)), (np.mean(a, axis=1)), np.mean(a)]
#     m = [d['mean'].append(i.tolist()) for i in mean]

#     variance = [(np.var(a, axis=0)), (np.var(a, axis=1)), np.var(a)]
#     v = [d['variance'].append(i.tolist()) for i in variance]

#     std = [(np.std(a, axis=0)), (np.std(a, axis=1)), np.std(a)]
#     s = [d['standard deviation'].append(i.tolist()) for i in std]

#     max = [(np.max(a, axis=0)), (np.max(a, axis=1)), np.max(a)]
#     mx = [d['max'].append(i.tolist()) for i in max]

#     min = [(np.min(a, axis=0)), (np.min(a, axis=1)), np.min(a)]
#     mn = [d['min'].append(i.tolist()) for i in min]

#     sum = [(np.sum(a, axis=0)), (np.sum(a, axis=1)), np.sum(a)]
#     sm = [d['sum'].append(i.tolist()) for i in sum]

#     pp.pprint(d)

# avg()
