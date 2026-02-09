from ..lammps import create_box_atoms

from . import lib_run0, lib_output

def lib_params(lmp, **kwargs) -> dict:
    """
    Evaluate the energy, forces, and pressures on an atomman system using a
    dynamic LAMMPS interaction using system information extracted by
    dump_lammps_dynamic_parameters.

    Parameters
    ----------
    lmp : lammps.lammps
        The LAMMPS interactive object to use.
    **kwargs : any
        The output from dump_lammps_dynamic_parameters().
    
    Returns
    -------
    dict
        Dict containing energy, forces and system pressure values.
    """
    # Set basic parameters, box, atoms and potential based on kwargs
    create_box_atoms(lmp, **kwargs)

    # Perform a run 0
    lib_run0(lmp)

    # Extract results
    results = lib_output(lmp)
    
    return results