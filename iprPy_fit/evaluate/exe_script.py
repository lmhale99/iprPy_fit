import atomman as am
import atomman.unitconvert as uc
import numpy as np

def exe_script(lammps_command, script, units='metal'):
    """
    Evaluates the energies of all ref_systems using a LAMMPS script
    and a LAMMPS executable. (Forces not currently supported)

    Parameters
    ----------
    lammps_command : str
        The LAMMPS executable to use.
    script : str
        The full LAMMPS script to use.
    units : str, optional.
        The LAMMPS units the simulation is running in.  Used to convert
        output values to atomman working units.  Default value is 'metal'.

    Returns
    -------
    values : DataModelDict
        The computed values for the reference systems.
    """
    # Get lammps units
    lammps_units = am.lammps.style.unit(units)
    
    # Run LAMMPS
    log = am.lammps.run(lammps_command, script=script, logfile=None)

    # Initialize results dict
    nsims = len(log.simulations)
    results = {}
    results['E_pot_total'] = np.empty(nsims)
    results['E_pot_atom'] = np.empty(nsims)
    results['P_xx'] = np.empty(nsims)
    results['P_yy'] = np.empty(nsims)
    results['P_zz'] = np.empty(nsims)

    # Extract values from the simulation
    for i, simulation in enumerate(log.simulations):
        results['E_pot_total'][i] = simulation.thermo.PotEng.values[-1]
        results['E_pot_atom'][i] = simulation.thermo.v_peatom.values[-1]
        results['P_xx'][i] = simulation.thermo.Pxx.values[-1]
        results['P_yy'][i] = simulation.thermo.Pyy.values[-1]
        results['P_zz'][i] = simulation.thermo.Pzz.values[-1]

    # Convert values to working units
    results['E_pot_total'] = uc.set_in_units(results['E_pot_total'], lammps_units['energy'])
    results['E_pot_atom'] = uc.set_in_units(results['E_pot_atom'], lammps_units['energy'])
    results['P_xx'] = uc.set_in_units(results['P_xx'], lammps_units['pressure'])
    results['P_yy'] = uc.set_in_units(results['P_yy'], lammps_units['pressure'])
    results['P_zz'] = uc.set_in_units(results['P_zz'], lammps_units['pressure'])
    
    return results