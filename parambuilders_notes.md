# parambuilders

## Interfacing with iprPy_fit

I think the mandatory components that ParamBuilders need for interfacing with iprPy_fit are 

- "tempdir" attribute that is a auto-picked temporary directory for any temporary parameter files during the fitting process.
- "tempfiles" attribute that is a list? dict? of the file paths for any temporary parameter files during the fitting process.
- "update_potential()" method that takes kwargs as inputs, updates only the associated parameter values in the class, updates the "tempfiles", and returns an updated PotentialLAMMPS object.

I also see some class-specific components for supporting the required components

- "paramfile_name", etc. that allow for specification of what to call the parameter file(s). Defaults to something like "TEMPPOT.style".
- Separate out the mapping of kwargs->parameters in update_potential() into a separate method. Multiple different mapping methods could then be defined in the class and selected with some name, or alternatively a user-defined mapping function could be passed in. (see next section for reasoning).

## General categories of ParamBuilders

I see three general categories of ParamBuilders: Pair, Parameter, and Table.

### Pair

The Pair category is for the "true" pair_styles in LAMMPS that define all parameter values in the pair_style and pair_coeff lines (i.e. no parameter files).  For these, update_potential() would map the given kwargs to the parameters in the PotentialLAMMPS object, then return the updated PotentialLAMMPS.  It would be busywork, but builders could be constructed for any single such pair_style.  Hybrids would require custom classes based on what they contain.

### Parameter

The Parameter category is for the potentials that use parameter files that contain specific parameter values, like tersoff, sw, and meam.  The full set of parameters is clearly established and a default kwargs->parameters mapping method would allow for any to all to be individually set.  However, different publications often use simplified parameter sets rather than the full set where many of the terms are coupled to the same or related values.  This would not require new builders if different kwargs->parameters methods are allowed.

### Table

The Table category is for the potentials that use tabulated functions, such as the eam styles.  With these styles, the basic builders generate the tabular format from user-defined functions and parameter sets.  This could possibly be made generic?


## Adding more builders

I have related parameter file builders for EAM styles in potentials.paramfile. I think meam, reaxff and sw have been done in some fashion before as well.

