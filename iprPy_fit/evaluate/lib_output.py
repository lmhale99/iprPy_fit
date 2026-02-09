
import atomman as am
import atomman.unitconvert as uc

def lib_output(lmp) -> dict:
    """
    This extracts the energy, force and pressure values from an interactive
    LAMMPS run.
    
    Parameters
    ----------
    lmp : lammps.lammps
        The LAMMPS library object to interact with.
    natoms : int
        The number of atoms in the system.
    units : str
        The LAMMPS units option allowing for the conversion of the outputs
        to atomman working units.
    """
    # Get lammps units
    lammps_units = am.lammps.style.unit(lmp.extract_global('units'))
    
    # Get natoms
    natoms = lmp.get_natoms()

    # Get results
    results = {}
    results['E_pot_total'] = uc.set_in_units(lmp.get_thermo('pe'), lammps_units['energy'])
    results['E_pot_atom'] =  uc.set_in_units(lmp.get_thermo('pe') / natoms, lammps_units['energy'])
    results['P_xx'] = uc.set_in_units(lmp.get_thermo('pxx'), lammps_units['pressure'])
    results['P_yy'] = uc.set_in_units(lmp.get_thermo('pyy'), lammps_units['pressure'])
    results['P_zz'] = uc.set_in_units(lmp.get_thermo('pzz'), lammps_units['pressure'])
    results['F'] = uc.set_in_units(lmp.numpy.extract_atom('f', nelem=natoms, dim=3), lammps_units['force'])

    return results