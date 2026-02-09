from pathlib import Path
from typing import Optional
from copy import deepcopy

import numpy as np

import atomman as am
import atomman.unitconvert as uc

try:
    from lammps import lammps as lammpsobj
except:
    has_lammps_lib = False
else:
    has_lammps_lib = True

from ..lammps import build_combined_script
from . import lib_system, lib_script, lib_params, exe_script

def evaluate(lmp = None,
             scripts = None,
             systems = None,
             potential = None,
             paramsets = None,
             include_velocities: bool = False,
             units: str = 'metal') -> dict:
    """
    Evaluates a set of reference systems using an interatomic potential
    and returns a dict of energies, pressures, and forces for comparison.

    Parameters
    ----------
    lmp : lammps.lammps, str, Path or None
        A LAMMPS interactive object or path to a LAMMPS executable.  If None,
        will attempt to import lammps and create a new lammps.lammps object.
    scripts : list or None
    """

    # Create a lammps interactive object if needed
    if lmp is None:
        if has_lammps_lib:
            lmp = lammpsobj(cmdargs=['-log', 'none', '-screen', 'none'])
        else:
            raise ValueError('lammps package not found!')

    # Interactive variations
    if isinstance(lmp, lammpsobj):
        
        rawresults = []

        # Run using prepared scripts
        if scripts is not None:
            assert systems is None, 'scripts and systems cannot both be given'
            assert potential is None, 'potential object can only be used with systems'
            assert paramsets is None, 'scripts and paramsets cannot both be given'

            for script in scripts:
                rawresults.append(lib_script(lmp, script))

        # Run using system and potential objects
        elif systems is not None:
            assert potential is not None, 'potential must be given with systems'
            assert paramsets is None, 'systems and paramsets cannot both be given'
            for system in systems:
                rawresults.append(lib_system(lmp, system, potential,
                                             include_velocities=include_velocities))
        
        # Run using extracted parameters (should be pickle-safe)
        elif paramsets is not None:
            assert potential is None, 'potential object can only be used with systems'
            for params in paramsets:
                rawresults.append(lib_params(lmp, **params))

        else:
            raise ValueError('scripts, systems + potential or paramsets must be given')

        # Initialize results dict
        nsims = len(rawresults)
        results = {}
        results['E_pot_total'] = np.empty(nsims)
        results['E_pot_atom'] = np.empty(nsims)
        results['P_xx'] = np.empty(nsims)
        results['P_yy'] = np.empty(nsims)
        results['P_zz'] = np.empty(nsims)
        results['F'] = []

        # Extract values from the simulation
        for i, raw in enumerate(rawresults):
            results['E_pot_total'][i] = raw['E_pot_total']
            results['E_pot_atom'][i] = raw['E_pot_atom']
            results['P_xx'][i] = raw['P_xx']
            results['P_yy'][i] = raw['P_yy']
            results['P_zz'][i] = raw['P_zz']
            results['F'].append(raw['F'])


    # Non-interactive variations
    elif isinstance(lmp, (str, Path)):
        # Get lammps version date
        lammps_date = am.lammps.checkversion(lmp)['date']
        
        if paramsets is not None:
            raise ValueError('paramsets not currently supported with lammps executable')

        if systems is not None:
            assert scripts is None, 'scripts and systems cannot both be given'
            assert potential is not None, 'potential must be given with systems'
            script = build_combined_script(potential, systems, lammps_date)
            units = potential.units
        
        elif scripts is not None:
            if hasattr(scripts, '__iter__'):
                script = '\n'.join(scripts)
            else:
                script = scripts
        
        else:
            raise ValueError('scripts, systems + potential or paramsets must be given')
        
        results = exe_script(lmp, script, units)
    
    return results
