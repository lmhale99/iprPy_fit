from yabadaba.record import Record

import numpy as np

class ReferenceStructure(Record):
    """
    Class for representing reference_structure records that provide structure,
    energies, forces, and stress information from DFT to be used in fitting.
    """

    ########################## Basic metadata fields ##########################

    @property
    def style(self) -> str:
        """str: The record style"""
        return 'reference_structure'

    @property
    def modelroot(self) -> str:
        """str: The root element of the content"""
        return 'reference-structure'
    
    ####################### Define Values and attributes #######################

    def _init_values(self):
        """
        Method that defines the value objects for the Record.  This should
        call the super of this method, then use self._add_value to create new Value objects.
        Note that the order values are defined matters
        when build_model is called!!!
        """
        self._add_value('strlist', 'symbols', valuerequired=True,
                        modelpath='system-info.symbol')
        self._add_value('str', 'composition', valuerequired=True,
                        modelpath='system-info.composition')
        self._add_value('int', 'natypes', valuerequired=True,
                        modelpath='system-info.cell.natypes')
        self._add_value('system_model', 'system', valuerequired=True,
                        modelpath="atomic-system", prop_unit={'pos': 'angstrom', 'force': 'eV/angstrom'})
        self._add_value('float', 'E_pot_total', unit='eV', metadatakey='E_pot_total (eV)',
                        modelpath='reference_values.E_pot_total')
        self._add_value('float', 'E_pot_atom', unit='eV', metadatakey='E_pot_atom (eV)',
                        modelpath='reference_values.E_pot_atom')
        self._add_value('float', 'P_xx', unit='GPa', metadatakey='P_xx (GPa)',
                        modelpath='reference_values.P_xx')
        self._add_value('float', 'P_yy', unit='GPa', metadatakey='P_yy (GPa)',
                        modelpath='reference_values.P_yy')
        self._add_value('float', 'P_zz', unit='GPa', metadatakey='P_zz (GPa)',
                        modelpath='reference_values.P_zz')
       
    def set_system_attributes(self):
        """
        auto sets the symbols, composition and natypes class attributes based
        on the current system.
        """
        self.symbols = self.system.symbols
        self.composition = self.system.composition
        self.natypes = self.system.natypes

    def reference_dict(self):
        """
        Method to return a dictionary of the reference values for this structure.
        """
        ref_dict = {}
        ref_dict['E_pot_total'] = self.E_pot_total
        ref_dict['E_pot_atom'] = self.E_pot_atom
        if 'force' in self.system.atoms.prop():
            ref_dict['F'] = self.system.atoms.force
        else:
            ref_dict['F'] = None
        ref_dict['P_xx'] = self.P_xx
        ref_dict['P_yy'] = self.P_yy
        ref_dict['P_zz'] = self.P_zz
        return ref_dict
    