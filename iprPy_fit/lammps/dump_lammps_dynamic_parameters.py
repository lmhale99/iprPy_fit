from typing import Optional

def dump_lammps_dynamic_parameters(
    system,
    atom_style: Optional[str] = None,
    units: Optional[str] = None,
    natypes: Optional[int] = None, 
    potential = None,
    return_pair_info: bool = False,
    include_velocities: bool = False) -> dict:
    """
    Extracts data stored in an atomman System and optionally a PotentialLAMMPS
    and transforms it into simple terms that can be used to easily create a box
    and atoms inside a dynamic LAMMPS simulation.
    
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
    return_pair_info : bool, optional
        Indicates if the LAMMPS command lines associated with setting mass,
        pair_style and pair_coeff are built and returned as a string.  If True,
        potential must be given.  Default value is False.
    include_velocities : bool, optional
        Indicates if velocity information in the system (if present) is to
        be extracted and included in the returned outputs.  Default value is
        False.
    
    Returns
    -------
    params : dict
        Dict containing the following by name.
    units : str
        The units option style to use.
    atom_style : str
        The atom_style option to use.
    pbc : list
        Tuple of three bool indicating which directions are periodic.
    region_params : list
        The LAMMPS parameters to define the box shape and position:
        (xlo, xhi, ylo, yhi, zlo, zhi, xy, xz, yz). These can then be directly
        passed to a "region box prism" command.
    atype : list
        The atype of each atom.
    x : list
        The flattened array of atom coordinates.
    v : list or None
        The flattened array of atom velocities. Will be None if
        include_velocities is False.
    symbols : list
        The list of element model symbols found in the system.
    masses : list
        The list of element masses associated with the symbols.
    pair_info : str or None
        Generated LAMMPS commands for reading in a potential.  Only
        built if return_pair_info is True.
    """
    # Test that box parameters are compatible with LAMMPS
    if not system.box.is_lammps_norm():
        raise ValueError('System not normalized for LAMMPS compatibility')
    
    region_params = [
        float(system.box.xlo), float(system.box.xhi),
        float(system.box.ylo), float(system.box.yhi),
        float(system.box.zlo), float(system.box.zhi),
        float(system.box.xy), float(system.box.xz), float(system.box.yz)]
    pbc = []
    for flag in system.pbc:
        if flag:
            pbc.append('p')
        else:
            pbc.append('m')
    
    
    # Extract potential-based parameters
    if potential is not None:
        if units is None:
            units = potential.units
        if atom_style is None:
            atom_style = potential.atom_style
        if natypes is None:
            natypes = len(potential.normalize_symbols(system.symbols))
    
    # Set default parameter values
    else:
        if units is None:
            units = 'metal'
        if atom_style is None:
            atom_style = 'atomic'
        if natypes is None:
            natypes = system.natypes
    
    atype = system.atoms.atype.tolist()
    x = system.atoms.pos.flatten().tolist()

    if include_velocities and 'velocity' in system.atoms.prop():
        v = system.atoms.velocity.flatten().tolist()
    else:
        v = None

    symbols = system.symbols
    masses = system.masses
    if potential is not None and return_pair_info:
        pair_info = potential.pair_info(symbols=system.symbols,
                                        masses=system.masses)
    else:
        pair_info = None
        
    return dict(
        units = units,
        atom_style = atom_style,
        pbc = pbc,
        natypes = natypes,
        region_params = region_params,
        atype = atype,
        x = x,
        v = v,
        symbols = symbols,
        masses = masses,
        pair_info = pair_info
    )