from ..evaluate import evaluate
from . import errorfxn

def minfxn(params,
           paramnames,
           parambuilder,
           paramfilename,
           ref_values,
           weights,

           lmp = None,
           scripts = None,
           systems = None,
           potential = None,
           paramsets = None,
           include_velocities: bool = False,
           units: str = 'metal'

           ) -> float:
    """
    minimization function for potential fitting

    Parameters
    ----------
    params : list
        The values for the parameters being manipulated by the minimization.
    paramnames : list
        The names associated with the parameters.
    parambuilder
        The parameter file builder.
    paramfilename : str
        The path where the parameter file is saved.
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

    # Match variable parameters to parameter names
    kwargs = {}
    for p, n, in zip(params, paramnames):
        kwargs[n] = p

    # Update parameter file
    parambuilder.update_parameter_values(**kwargs)
    parambuilder.save_paramfile(paramfilename)
    
    # Build and run LAMMPS simulation to evaluate the current potential
    values = evaluate(lmp=lmp, scripts=scripts, systems=systems,
                      potential=potential, paramsets=paramsets,
                      include_velocities=include_velocities, units=units)

    # Evaluate the error
    error = errorfxn(values, ref_values, weights)

    return error