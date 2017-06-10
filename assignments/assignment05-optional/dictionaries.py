##### H:
def h_printer():
    superbowls = {'joe montana': 4, 'tom brady': 3, 'joe flacco': 0}
    print(superbowls['tom brady'])
    # Prints: 3

    superbowls['peyton manning'] = 1
    print(superbowls)
    # Prints: {'peyton manning': 1, 'tom brady': 3, 'joe flacco': 0, 'joe montana': 4}

    superbowls['joe flacco'] = 1
    print(superbowls)
    # Prints:{'peyton manning': 1, 'tom brady': 3, 'joe flacco': 1, 'joe montana': 4}
    # end example work

    print('colin kaepernick' in superbowls)
    # Prints: false

    print(len(superbowls))
    Prints: 4

    print(superbowls['peyton manning'] == superbowls['joe montana'])
    # Prints: false

    superbowls[('eli manning', 'giants')] = 2
    print(superbowls)
    # Prints: {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1, ('eli manning', 'giants'): 2}

    superbowls[3] = 'cat'
    print(superbowls)
    # Prints: {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1,
    # ('eli manning', 'giants'): 2, 3: 'cat'}

    superbowls[('eli manning', 'giants')] = superbowls['joe montana'] + superbowls['peyton manning']
    print(superbowls)
    # Prints: {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1,
    # ('eli manning', 'giants'): 5, 3: 'cat'}

    superbowls[['steelers', '49ers']] = 11
    print(superbowls)
    # Prints: errors lists are not hashable


##### I:
def replace_all(d, x, y):
    """Replaces all values of x with y.
    Given: d = {1: {2:3, 3:4}, 2:{4:4, 5:3}}
    Usage: replace_all(d,3,1)
    Results: {1: {2: 1, 3: 4}, 2: {4: 4, 5: 1}}
    """
    for key, val in d.items():
        if type(val) == dict:
            replace_all(val, x, y)
        elif val == x:
            d[key] = y
    return d


###### J:
def rm(d, x):
    """Removes all pairs with value x.
    Given:  d = {1:2, 2:3, 3:2, 4:3}
    Usage:  rm(d,2)
    Results: {2:3, 4:3}
    """

    # for key in list(d.keys()):
    #     if d[key] == x:
    #         d.pop(key)

    # or

    for key in list(d.items()):
        if key[1] == x:
            d.pop(key[0])
    # or

    # keys = []
    # for key, val in d.items():
    #     if val == x:
    #         keys.append(key)
    # for key in keys:
    #     d.pop(key)

    return d


if __name__ == '__main__':
    d = {1: {2: 3, 3: 4}, 2: {4: 4, 5: 3}}
    print(replace_all(d,3,1))
    d = {1: 2, 2: 3, 3: 2, 4: 3}
    print(rm(d,2))