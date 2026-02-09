from pathlib import Path

from functools import partial

import scipy.optimize

from . import minfxn


def minimize(parambuilder,
             paramfilename: Path,
             params,
             ref_values,
             weights,

             lmp = None,
             scripts = None,
             systems = None,
             potential = None,
             paramsets = None,
             include_velocities: bool = False,
             units: str = 'metal',

             min_method='Nelder-Mead',
             min_options=None,
             ):
    """
    
    Parameters
    ----------
    parambuilder
        A iprPy_fit parambuilder object
    paramfilename : Path
        The location where the parameter file is to be found.
    params : list or dict
        The names of the parameters to fit.  If dict, then keys are the names
        and values are the fitting bounds.
    ref_values : dict
        reference values to compare to.
    weights : dict
        Weights to use for error calculation.
    lmp : 
        The LAMMPS executable or library object to use.
    
    scripts
        The LAMMPS script to run.
    systems
    potential
    paramsets
    include_velocities
    units
    
    """
    # split params and bounds if needed
    if isinstance(params, list):
        paramnames = params
        bounds = None
    elif isinstance(params, dict):
        paramnames = list(params.keys())
        bounds = list(params.values())
    else:
        raise TypeError('params must be list or dict')
    
    # Get initial parameter values associated with paramnames
    init_params = parambuilder.get_parameter_values(paramnames)

    # Define partial function for minimization to set kwargs
    constant_kwargs = dict(
        paramnames = paramnames,
        parambuilder = parambuilder,
        paramfilename = paramfilename,
        ref_values = ref_values,
        weights = weights,

        lmp = lmp,
        scripts = scripts,
        systems = systems,
        potential = potential,
        paramsets = paramsets,
        include_velocities = include_velocities,
        units = units)
    partialminfxn = partial(minfxn, **constant_kwargs)

    # Initial run to check error
    init_error = partialminfxn(init_params)
    print('Initial error is', init_error) 

    # Run minimization
    results = scipy.optimize.minimize(partialminfxn, init_params, method=min_method, 
                                      options=min_options, bounds=bounds)

    print('Final error is', results.fun)

    # Check final values
    final_params = {}
    for key, value in zip(paramnames, results.x):
        final_params[key] = float(value)
    
    return final_params