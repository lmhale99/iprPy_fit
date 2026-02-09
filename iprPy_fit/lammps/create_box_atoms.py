from typing import Optional
from datetime import date

from . import version_date

def create_box_atoms(lmp,
                     units: str,
                     atom_style: str,
                     pbc: list,
                     natypes: int ,
                     region_params: list,
                     atype: list,
                     x: list,
                     v: Optional[list],
                     symbols: list,
                     masses: list,
                     pair_info: Optional[str],
                     potential = None):
    """
    Initial setup of a dynamic LAMMPS simulation using parameter extracted
    from an atomman System by dump_lammps_dynamic_parameters()
    """
    lammps_date = version_date(lmp)

    # Base settings
    lmp.cmd.clear()
    if lammps_date < date(2024, 1,1):  # This is only a version guess!!!!
        lmp.cmd.box('tilt', 'large')
    lmp.cmd.units(units)
    lmp.cmd.atom_style(atom_style)
    
    # Create box
    lmp.cmd.boundary(*pbc)
    lmp.cmd.region('box', 'prism', *region_params)
    lmp.cmd.create_box(natypes, 'box')

    # Create atoms
    lmp.create_atoms(len(atype), atomid=None, atype=atype, x=x, v=v)

    # Define potential
    if potential is not None:
        pair_info = potential.pair_info(symbols=symbols,  masses=masses)
    lmp.commands_string(pair_info)
