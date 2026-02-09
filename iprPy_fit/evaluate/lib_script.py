from . import lib_output

def lib_script(lmp,
               script) -> dict:
    """
    Evaluate the energy, forces, and pressures on an atomman system using a
    dynamic LAMMPS interaction and a full LAMMPS script.

    Parameters
    ----------
    lmp : lammps.lammps
        The LAMMPS interactive object to use.
    script : str
        The LAMMPS script to use.
    
    Returns
    -------
    dict
        Dict containing energy, forces and system pressure values.
    """
    # Run the script
    lmp.commands_string(script)

    # Extract results
    results = lib_output(lmp)
    
    return results