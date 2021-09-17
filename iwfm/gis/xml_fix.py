# xml_fix.py
# fix a broken XML file
# Copyright (C) 2020-2021 University of California
# -----------------------------------------------------------------------------
# This information is free; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This work is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# -----------------------------------------------------------------------------


def xml_fix(infile, outfile, verbose=False):
    ''' xml_fix() - Read a broken XML file and write repaired file
    

    Parameters
    ----------
    infile : str
        input XML file name
    
    outfile : str
        output XML file name

    Returns
    -------
    nothing
    
    '''
    from bs4 import BeautifulSoup

    data = open(infile)
    new_data = BeautifulSoup(data.read(), features='xml')
    fixed = open(outfile, 'w')
    fixed.write(new_data.prettify())
    fixed.close()
    if verbose:
        print(f'  Fixed file \'{infile}\' and wrote to \'{outfile}\' ')
    return
    