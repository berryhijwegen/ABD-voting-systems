""" Helper methods. """

def flatten(lst):
    """ Helper method to flatten a list with sublists. """
    output_lst = []
    for sublst in lst:
        if not isinstance(sublst, list):
            output_lst.append(sublst)
        else:
            for element in sublst:
                output_lst.append(element)
    return output_lst
