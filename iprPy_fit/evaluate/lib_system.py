from typing import Optional

from ..lammps import dump_lammps_dynamic
from . import lib_run0, lib_output

def lib_system(lmp,
               system,
               potential,
               atom_style: Optional[str] = None,
               units: Optional[str] = None,
               natypes: Optional[int] = None,
               include_velocities: bool = False
               ) -> dict:
    """
    Evaluate the energy, forces, and pressures on an atomman system using a
    dynamic LAMMPS interaction.

    Parameters
    ----------
    lmp : lammps.lammps
        The LAMMPS interactive object to use.
    system : atomman.System 
        The system that LAMMPS will replicate.
    potential : atomman.lammps.Potential
        Potential-specific values of atom_style, units, and natypes can be
        extracted from a Potential object.  If both potential and any of the
        individual values are given, the individual values will be used.
    atom_style : str, optional
        The LAMMPS atom_style option associated with the data file.  If neither
        atom_style or potential is given, will set atom_style to 'atomic'.
    units : str, optional
        The LAMMPS units option associated with the data file.  If neither
        units or potential is given, will set units 'metal'.
    natypes : int, optional
        Allows the natypes value to be manually changed.  This is needed if
        natypes needs to be greater than the current number of atypes.  If
        neither natypes or potential is given, will use system.natypes.
    include_velocities : bool, optional
        Indicates if velocity information in the system (if present) is to
        be extracted and included in the returned outputs.  Default value is
        False.
    
    Returns
    -------
    dict
        Dict containing energy, forces and system pressure values.
    """
    # Set basic parameters, box, atoms and potential based on system and potential objects
    dump_lammps_dynamic(system, lmp, potential, atom_style=atom_style,
                        units=units, natypes=natypes,
                        include_velocities=include_velocities)
    
    # Perform a run 0
    lib_run0(lmp)

    # Extract results
    results = lib_output(lmp)
    
    return results