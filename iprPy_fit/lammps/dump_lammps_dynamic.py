from typing import Optional


from . import dump_lammps_dynamic_parameters
from . import create_box_atoms

def dump_lammps_dynamic(
    system,
    lmp,
    potential,
    atom_style: Optional[str] = None,
    units: Optional[str] = None,
    natypes: Optional[int] = None, 
    include_velocities: bool = False):
    """
    Extracts data stored in an atomman System and passes it to a dynamic
    LAMMPS object to define basic settings, box, atoms, and potential
    information.
    
    Parameters
    ----------
    system : atomman.System 
        The system that LAMMPS will replicate.
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
    potential : atomman.lammps.Potential, optional
        Potential-specific values of atom_style, units, and natypes can be
        extracted from a Potential object.  If both potential and any of the
        individual values are given, the individual values will be used.
    include_velocities : bool, optional
        Indicates if velocity information in the system (if present) is to
        be extracted and included in the returned outputs.  Default value is
        False.
    
    """
    lammps_params = dump_lammps_dynamic_parameters(system, atom_style=atom_style,
                                                   units=units, natypes=natypes,
                                                   potential=potential,
                                                   return_pair_info=True,
                                                   include_velocities=include_velocities)
    create_box_atoms(lmp, **lammps_params)