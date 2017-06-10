
########### A:
def a_printer():
    a = [1,5,4,2,3]
    print(a[0],a[-1])
#this will print a[0] in this case 1 and then will print the last element starting in reverse order a[0] - one position
#prints 1 3

########### B:
def remove_all(el, lst):
    """Removes all instances of el from lst.
    Given: x = [3, 1, 2, 1, 5, 1, 1, 7]
    Usage: remove_all(1, x)
    Would result in: [3, 2, 5, 7]
    """
    # a non pythonic solution
    #for element in lst:
    #    if element == el:
    #        lst.remove(el)

    # a more pythonic solution using list comp
    lst = [element for element in lst if element != el]

    # the first solution is similar to any C solution loop through and delete. lst.remove actually removes the first
    # occurance of the element not really the one that is found.
    # solution number two re-assigns the list lst to itself by selecting only the elements that are not el


########### C:
def add_this_many(x, y, lst):
    """ Adds y to the end of lst the number of times x occurs in lst.
    Given: lst = [1, 2, 4, 2, 1]
    Usage: add_this_many(1, 5, lst)
    Results in: [1, 2, 4, 2, 1, 5, 5]
    """
    # a
    for element in lst:
        if element == x:
            lst.append(y)

    # b
    b = [element for element in lst if element != x]
    for foo in range(len(b)):
        lst.append(y)


############ D:
def d_printer():
    a = [3, 1, 4, 2, 5, 3]
    print(a[:4])
    # Prints: 3 1 4 2

    print(a)
    # Prints: 3 1 4 2 5 3

    print(a[1::2])
    # Prints: 1 2 3  gets every other item ::2 starting with the second element 1

    print(a[:])
    # Prints: 3 1 4 2 5 3 gets every element between nothing and nothing

    print(a[4:2])
    # Prints: nothing there are no elements starting at 4 going to 2

    print(a[1:-2])
    # Prints: 1 4 2 prints the second element 1: then starting from the end go to the third element :-2

    print(a[::-1])
    # Prints: 3 5 2 4 1 3 prints reverse order :: extended splice mixed with -1 starting at ending element


######### E:
# in place saves memory
def reverse(lst):
    """ Reverses lst in place.
    Given: x = [3, 2, 4, 5, 1]
    Usage: reverse(x)
    Results: [1, 5, 4, 2, 3]
    """
    lst = lst[::-1]


########### F:
def rotate(lst, k):
    """ Return a new list, with the same elements of lst, rotated to the right k.
    Given: x = [1, 2, 3, 4, 5]
    Usage: rotate(x, 3)
    Results: [3, 4, 5, 1, 2]
    """

    # collect list starting from element k
    newList = lst[k:]
    # add list ending at element k
    newList.extend(lst[:k])
    return newList
