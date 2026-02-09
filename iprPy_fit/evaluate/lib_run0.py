def lib_run0(lmp):
    """
    This performs the LAMMPS commands for a run 0.  Assumes basic settings,
    box, atoms and potential are already set.
    """
    # Setup a run 0
    lmp.cmd.thermo_style('custom', 'step', 'pxx', 'pyy', 'pzz', 'pe')
    lmp.cmd.thermo_modify('format', 'float', '%.13e')
    lmp.cmd.fix('nve', 'all', 'nve')
    lmp.cmd.run(0)