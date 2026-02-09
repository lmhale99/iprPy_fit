import numpy as np

def errorfxn(values, ref_values, weights):
    """
    Error evaluation function
        sum( ((value - ref) / weight)^2 )

    Parameters
    ----------
    values : dict
        The property values computed during the evaluation stage
    ref_values : dict
        The reference property values to compare to
    weights : dict
        The weights to use for each property type
    """
    error = 0
    for key in weights:
        
        # Skip "empty" weight values
        weight = weights[key]

        if weight is None:
            continue
        if isinstance(weight, float) and (np.isnan(weight) or weight <= 0.0):
            continue
        
        value = values[key]
        ref_value = ref_values[key]
        
        # if weight is array, 
        #    check len(weight) matches value
        #    ignore nan and <= elements from arrays

        error += np.sum(((value - ref_value) / weight)**2)

    return error