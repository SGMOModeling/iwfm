# rmse_calc.py
# calculate root mean square error between two lists of values
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


def rmse_calc(predictions, targets):
    """ rmse_calc() - Return the RMSE between measured (targets)
        and simulated (predictions) values

    Parameters:
      predictions     (list):  Model values
      targets         (list):  Observed values

    Returns:
      Numpy array of RMSE values for each set of values
    """
    import numpy as np

    return np.sqrt(np.mean((np.array(predictions) - np.array(targets)) ** 2))
