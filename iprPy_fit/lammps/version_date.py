from datetime import date

def version_date(lmp):
    """
    Read the lammps version and return it as a datetime.date
    """
    return date.fromisoformat(str(lmp.version()))