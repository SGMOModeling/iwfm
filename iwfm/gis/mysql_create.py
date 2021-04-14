# mysql_create.py
# Create a mysql database
# Copyright (C) 2020-2021 Hydrolytics LLC
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


def mysql_create(dbname, host='localhost', port=3306, user='root', passwd='', verbose=False):
    ''' mysql_create() - Create a mysql database 
        DEMO - how to do it
    
    Parameters
    ----------
    dbname : str
        database file base name 
    
    host : str, default='localhost'
        host
    
    port : int, default=3306
        port number

    user : str, default='root'
        user name
    
    passwd : str, default=''
        password

    verbose : bool, default=False
        True = command line update on
    
    Returns
    -------
    nothing

    '''
    import pymysql

    # establish a database connection on local machine as root database user
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db='mysql')
    # conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='mysql')

    if verbose:
        print(f'  PyMySQL connected to {dbname}')

    # get the database cursor needed to change the database
    cur = conn.cursor()

    # check if database exists, and drop it if it does
    cur.execute('DROP DATABASE IF EXISTS ' + dbname)
    cur.execute('CREATE DATABASE ' + dbname)

    # Close cursor and connection
    cur.close()
    conn.close()
    return
