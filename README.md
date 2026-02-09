# iprPy_fit

This repository serves as the working space for building potential fitting tools for LAMMPS potentials using components in the Python packages potentials, atomman and iprPy.  Pieces of the code here may get incorporated into those packages in the future, but some will likely remain. At the very least, example notebooks should still stay here!

Still to do:

- Integrate in mpi4py capabilities to speed up evaluations.
- Pick a good minimization algorithm and add callback method to show progress.
- Add force comparisons to the error function.  Note that each item will be of a different size.
- Make certain final potential after minimization is saved and updated somewhere.
- Create a base ParamBuilder class to define the common methods.
- Regenerate reference data to include forces and double-check all values and units.  I believe the structures were originally evaluated using the Purja Pun Si potential (Si.tersoff.modc in this repository).
- Define a yabadaba record for the reference data to give it a proper schema.


Quick code overview:

- parambuilder: potential parameter builders
    - TersoffModC: for tersoff.modc format
- lammps: LAMMPS-based methods
    - build_script: builds a LAMMPS run0 script based on run0.template for a system and potential. Only used for exe runs.
    - dump_lammps_commands: builds the LAMMPS command lines for the system and potential as used by build_script. Only used for exe runs.
    - version_date: converts the LAMMPS library version to a datetime.date.
    - dump_lammps_dynamic_parameters: converts system and potential objects into (hopefully) pickle-compatible parameters.
    - create_box_atoms: LAMMPS lib commands for creating the system and defining the potential based on dump_lammps_dynamic_parameters() output.
    - dump_lammps_dynamic: combines the previous two to convert a system and potential object directly into LAMMPS library commands.
- evaluate: evaluation methods that run LAMMPS and extract values.
    - evaluate: wrapper method for the options below.
    - exe_script: Uses a LAMMPS exe and takes pre-generated LAMMPS scripts.  DOES NOT SUPPORT FORCES AT THE MOMENT!
    - lib_script: Uses a LAMMPS lib and takes pre-generated LAMMPS scripts.
    - lib_system: Uses a LAMMPS lib and takes systems and potential as atomman objects.
    - lib_params: Uses a LAMMPS lib and takes dump_lammps_dynamic_parameters() sets.
    - lib_run0: LAMMPS lib commands for a run 0.  Used by lib_system and lib_params.
    - lib_output: LAMMPS lib commands for extracting energies, pressures and forces.  Used by lib_script, lib_systems, and lib_params.
- minimize: minimization components.
    - errorfxn: computes the error value based on current values, reference values and weights.
    - minfxn: The core minimization function: updates parameters, evaluates, and computes error.
    - minimize: Sets up and runs minimization using minfxn.