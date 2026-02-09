import datetime


from potentials.record.PotentialLAMMPS import PotentialLAMMPS
from atomman import System
from atomman.tools import filltemplate
from iprPy.tools import read_calc_file


from . import dump_lammps_commands



def build_script(potential: PotentialLAMMPS,
                 system: System,
                 lammps_date: datetime.date) -> str:
    """
    Builds the LAMMPS input script to evaluate a single reference system.

    Parameters
    ----------
    potential : PotentialLAMMPS
        The potential object to use for generating the associated LAMMPS
        command lines.
    system : atomman.System
        The reference atomic system to evaluate.

    Returns
    -------
    script : str
        The LAMMPS script as a str.
    """
    # Define lammps variables
    lammps_variables = {}
    system_info = dump_lammps_commands(system, potential=potential,
                                       return_pair_info=True)
    lammps_variables['atomman_system_pair_info'] = system_info
    
    if lammps_date < datetime.date(2022, 12, 22):
        lammps_variables['box_tilt_large'] = 'box tilt large'
    else:
        lammps_variables['box_tilt_large'] = ''

    template = read_calc_file('iprPy_fit.lammps', 'run0.template')
    script = filltemplate(template, lammps_variables, '<', '>')

    return script


def build_combined_script(potential: PotentialLAMMPS,
                          systems: list,
                          lammps_date: datetime.date) -> str:
    """
    Builds the LAMMPS input script to evaluate all reference systems.

    Parameters
    ----------
    potential : PotentialLAMMPS
        The potential object to use for generating the associated LAMMPS
        command lines.
    systems : list of atomman.System
        The reference atomic systems to evaluate.

    Returns
    -------
    script : str
        The LAMMPS script as a str.
    """
    script = ''
    for system in systems:
        script += build_script(potential, system, lammps_date)

    return script