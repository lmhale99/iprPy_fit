import io
import itertools
from pathlib import Path

from typing import Union, Optional
from yabadaba.record import Record
from yabadaba.tools import aslist
from potentials.record.PotentialLAMMPS import PotentialLAMMPS

from DataModelDict import DataModelDict as DM
from DataModelDict import uber_open_rmode

class TersoffModCInteraction(Record):
    """
    Record subclass representing the parameters of a single three symbol
    interaction for a tersoff.modc potential parameter file.
    """
    def __init__(self,
                 model: Union[str, io.IOBase, DM, None] = None,
                 name: Optional[str] = None,
                 database = None,
                 noname: bool = True,
                 paramlines: Optional[list] = None,
                 **kwargs):
        
        if paramlines is not None:
            assert model is None, 'paramline and model cannot both be given'
            assert len(kwargs) == 0, 'paramline cannot be given with parameter kwargs'

        super().__init__(model=model, name=name, database=database,
                         noname=noname, **kwargs)
        
        if paramlines is not None:
            self.load_paramlines(paramlines=paramlines)

    ########################## Basic metadata fields ##########################

    @property
    def style(self):
        """str: The record style"""
        return 'tersoff-modc-interaction'

    @property
    def modelroot(self):
        """str: The root element of the content"""
        return 'interaction'
    
    ############################# Define Values  ##############################

    def _init_values(self):
        """
        Method that defines the value objects for the Record.  This should
        call the super of this method, then use self._add_value to create new Value objects.
        Note that the order values are defined matters
        when build_model is called!!!
        """

        self._add_value('str', 'symbol1',valuerequired=True,
                        description='The center atom in a 3-body interaction')
        self._add_value('str', 'symbol2',
                        description='The atom bonded to the center atom')
        self._add_value('str', 'symbol3',
                        description='The atom influencing the 1-2 bond in a bond-order sense')
        
        self._add_value('float', 'beta', defaultvalue=3.0,
                        description='3-body exponential power term')
        self._add_value('float', 'alpha', defaultvalue=0.0,
                        description='3-body exponential scalar term')
        self._add_value('float', 'h', defaultvalue=0.0,
                        description='3-body reference angle: cos(theta0)')
        self._add_value('float', 'eta', defaultvalue=0.0,
                        description='bond order function power term')
        
        self._add_value('int', 'beta_ters', defaultvalue=1,
                        description='dummy parameter')
        self._add_value('float', 'lambda2', defaultvalue=0.0,
                        description='2-body attractive Morse distance term')
        self._add_value('float', 'B', defaultvalue=0.0,
                        description='2-body attractive Morse energy term')
        self._add_value('float', 'R', defaultvalue=0.0,
                        description='cutoff center')
        self._add_value('float', 'D', defaultvalue=0.0,
                        description='cutoff halfwidth')
        self._add_value('float', 'lambda1', defaultvalue=0.0,
                        description='2-body repulsive Morse distance term')
        self._add_value('float', 'A', defaultvalue=0.0,
                        description='2-body repulsive Morse energy term')
        
        self._add_value('float', 'n', defaultvalue=0.0,
                        description='bond order function power term')
        self._add_value('float', 'c1', defaultvalue=0.0,
                        description='3-body function coefficient')
        self._add_value('float', 'c2', defaultvalue=0.0,
                        description='3-body function coefficient')
        self._add_value('float', 'c3', defaultvalue=0.0,
                        description='3-body function coefficient')
        self._add_value('float', 'c4', defaultvalue=0.0,
                        description='3-body function coefficient')
        self._add_value('float', 'c5', defaultvalue=0.0,
                        description='3-body function coefficient')
        self._add_value('float', 'c0', defaultvalue=0.0,
                        description='Constant energy term')

    def load_paramlines(self, paramlines):
        """
        Read parameters in from a set of parameter lines
        """
        assert len(paramlines) == 3
        terms = paramlines[0].split() + paramlines[1].split() + paramlines[2].split()
        assert len(terms) == 21

        # Set terms
        for term, valobj in zip(terms, self.value_objects):
            valobj.value = term

    def build_paramlines(self):
        """
        Build parameter lines for the current parameters
        """
        lines = ['', '', '']
        
        # Set terms
        for i, valobj in enumerate(self.value_objects):
            style = type(valobj).__name__
            if style == 'FloatValue':
                lines[i // 7] += f'{valobj.value:.8f} '
            elif style == 'StrValue':
                lines[i // 7] += f'{valobj.value:2} '
            else:
                lines[i // 7] += f'{valobj.value} '

        for i in range(3):
            lines[i] = lines[i].strip()
        return lines

class TersoffModC(Record):
    """
    Record for reading and generating a tersoff.modc potential parameter file.
    """
    def __init__(self,
                 model: Union[str, io.IOBase, DM, None] = None,
                 name: Optional[str] = None,
                 database = None,
                 noname: bool = False,
                 symbols: Union[str, list, None] = None,
                 paramfile: Union[str, io.IOBase, None] = None,
                 **kwargs):
        """
        Init for TersoffModC.  Note that the first parameters are associated
        with database interactions and only the latter ones are important for
        common use.

        Parameters
        ----------
        model : str, file-like-object, DataModelDict or None, optional
            A record model for a TersoffModC parameter file to load.
            Cannot be given with paramfile or symbols.
        name : str or None, optional
            A name to associate with the record.
        database : yabadaba.database.Database, optional
            A database associated with the record. Automatically set if
            the record is retrieved from such a database.
        noname : bool, optional
            Indicates if the name field is ignored or needed.  Default value is
            False (a name is expected for database record interactions).
        symbols : str, list or None, optional
            One or more element symbols to automatically build all interaction
            combinations for.  Useful for new potential creation and saves the
            user from repeatedly calling add_interaction(). Cannot be given with
            model or paramfile
        paramfile : str, file-like-object, or None, optional
            An existing Tersoff/modc parameter file to read in.  Cannot be given
            with model or symbols.
        header : str, optional
            Optional file header comments to include at the top of any generated parameter
            file.
        """
        
        if paramfile is not None:
            assert model is None, 'paramfile and model cannot both be given'
            assert symbols is None, 'paramfile and symbols cannot both be given'
            assert len(kwargs) == 0, 'paramfile cannot be given with parameter kwargs'
        elif symbols is not None:
            assert model is None, 'symbols and model cannot both be given'

        super().__init__(model=model, name=name, database=database,
                         noname=noname, **kwargs)
        
        if paramfile is not None:
            self.load_paramfile(paramfile=paramfile)

        if symbols is not None:
            self.add_all_interactions(symbols)

    ########################## Basic metadata fields ##########################

    @property
    def style(self):
        """str: The record style"""
        return 'tersoff-modc'

    @property
    def modelroot(self):
        """str: The root element of the content"""
        return 'tersoff-modc'
    
    ############################# Define Values  ##############################

    def _init_values(self):
        """
        Method that defines the value objects for the Record.  This should
        call the super of this method, then use self._add_value to create new Value objects.
        Note that the order values are defined matters
        when build_model is called!!!
        """

        self._add_value('longstr', 'header', defaultvalue='',
                        description='Header line for the parameter file')
        self._add_value('record', 'interactions', recordclass=TersoffModCInteraction,
                        description='Interaction parameter sets')

    def add_interaction(self, **kwargs):
        """Creates a new interaction parameter set and adds it to the interaction list"""
        # Create new interaction object
        newinteraction = TersoffModCInteraction(**kwargs)
        
        # Verify that the new interaction's symbols are different than the old interactions
        for interaction in self.interactions:
            if ((interaction.symbol1 == newinteraction.symbol1) and
                (interaction.symbol2 == newinteraction.symbol2) and
                (interaction.symbol3 == newinteraction.symbol3)):
                raise ValueError(f'Interaction parameters already exist for {newinteraction.symbol1}-{newinteraction.symbol2}-{newinteraction.symbol3}')

        self.interactions.append(newinteraction)

    def add_all_interactions(self, symbols):
        """Auto creates empty interaction lines based on unique elemental symbols"""
        for symbol1, symbol2, symbol3 in itertools.product(aslist(symbols), repeat=3):
            self.add_interaction(symbol1=symbol1, symbol2=symbol2, symbol3=symbol3)

    def get_interaction(self, symbol1, symbol2, symbol3):
        """Return the interaction parameter set for the given model symbols"""
        for interaction in self.interactions:
            if ((interaction.symbol1 == symbol1) and
                (interaction.symbol2 == symbol2) and
                (interaction.symbol3 == symbol3)):
                return interaction
            
        raise ValueError(f'No interaction parameters found for {symbol1}-{symbol2}-{symbol3}')
        
    def load_paramfile(self, paramfile):
        """
        Read in a parameter file.
        """
        with uber_open_rmode(paramfile) as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].decode('UTF-8')

        # Read header
        self.header = lines[0].strip('# \r\n')

        # Read in parameter lines
        i = 1
        while i < len(lines):
            
            # Ignore comment and empty lines
            if lines[i].strip().startswith('#') or lines[i].strip() == '':
                i += 1
                continue

            self.add_interaction(paramlines=lines[i:i+3])
            i += 3

    def build_paramfile(self):
        """
        Build a parameter file.
        """
        lines = [
            f'# {self.header}',
            '#',
            '# Format:',
            '# element1 element2 element3 beta alpha h eta',
            '# beta_ters lambda2 B R D lambda1 A',
            '# n c1 c2 c3 c4 c5 c0',
        ]
        for interaction in self.interactions:
            lines.extend(interaction.build_paramlines())
        
        return '\n'.join(lines)
    
    def build_potential_object(self,
                               filename: Union[str, Path]) -> PotentialLAMMPS:
        """
        Creates a PotentialLAMMPS object allowing for direct integration of the
        parameter file into atomman.

        Parameters
        ----------
        filename : str or Path
            The filename/path where the parameter file is expected to be found.
        """
        # FOR LATER: set means of handling case where symbols != elements

        # Find the list of all unique symbols set as interactions.
        symbols = set()
        for interaction in self.interactions:
            symbols.update([interaction.symbol1, interaction.symbol2, interaction.symbol3])
        symbols = list(symbols)

        # Build potential object
        potential = PotentialLAMMPS.paramfile(filename, pair_style='tersoff/mod/c',
                                              elements=symbols, symbols=symbols)
        
        return potential

    def save_paramfile(self,
                       filename: Union[str, Path] = None,
                       return_potential: bool = False):
        """
        Builds and saves a parameter file

        Parameters
        ----------
        filename : str, Path or None, optional
            The filename/path where the parameter file will be saved.
            If None (default) will save to the local directory using the
            object's name, i.e. "name".tersoff.modc.
        return_potential : bool, optional
            Setting this to True will generate a PotentialLAMMPS object
            allowing for direct integration of the parameter file into
            atomman. Default value is None.

        Returns
        -------
        potentials.record.PotentialLAMMPS
            atomman-compatible PotentialLAMMPS object.  Returned if
            return_potential is True.
        """
        if filename is None:
            filename = f'{self.name}.tersoff.modc'
        with open(filename, 'w') as f:
            f.write(self.build_paramfile())

        if return_potential:
            return self.build_potential_object(filename)

    def update_parameter_values(self, **kwargs):
        """
        Convenience function for easily updating any of the parameter values.

        Parameters
        ----------
        **kwargs : float
            The names and values of any parameters to update.  The names
            combine the three symbol models and the parameter name
            delimited by underscores.  For example, 'Si_C_Si_beta' will alter
            the beta value of the Si-C-Si interaction.
        """
        for name, value in kwargs.items():
            terms = name.split('_')
            self.get_interaction(*terms[0:3]).set_values(**{'_'.join(terms[3:]): value})
            
    def get_parameter_value(self, name):
        """
        Convenience function for easily fetching any of the parameter values
        based on its long name.

        Parameters
        ----------
        name : str
            The long name of the parameter to get.  The name
            combines the three symbol models and the parameter name
            delimited by underscores.  For example, 'Si_C_Si_beta' will get
            the beta value of the Si-C-Si interaction.
        """
        terms = name.split('_')
        return getattr(self.get_interaction(*terms[0:3]), '_'.join(terms[3:]))
    
    def get_parameter_values(self, names):
        """
        Convenience function for easily fetching multiple parameter values
        based on their long names.

        Parameters
        ----------
        names : list
            The long name of the parameter to get.  The name
            combines the three symbol models and the parameter name
            delimited by underscores.  For example, 'Si_C_Si_beta' will get
            the beta value of the Si-C-Si interaction.
        """
        values = []
        for name in names:
            values.append(self.get_parameter_value(name))
        return values