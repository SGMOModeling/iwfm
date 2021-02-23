# sub_pp_file.py
# Copies the old preprocessor input file, replaces the file names with
# those of the new submodel, and writes out the new file
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


def sub_pp_file(in_pp_file, pre_dict, pre_dict_new, has_lake=False):
    """sub_pp_file() copies the old preprocessor input file,
        replaces the file names with those of the new model,
        and writes out the new file

    Parameters:
      in_pp_file     (str):   Name of existing preprocessor main input file
      pre_dict       (dict):  Dictionary of existing model preprocessor file names
      pre_dict_new   (dict):  Dictionary of submodel preprocessor file names
      has_lake       (bool):  Does the submodel have a lake file?

    Returns:
      nothing

    """
    import iwfm as iwfm

    # -- read the preprocessor file into array pre_lines
    pre_lines = open(in_pp_file).read().splitlines()  # open and read input file

    line_index = iwfm.skip_ahead(0, pre_lines, 3)  # skip comments
    # -- preproc output file
    pre_lines[line_index] = iwfm.pad_both(pre_dict_new['preout'], f=4, b=53) + ' '.join(
        pre_lines[line_index].split()[1:]
    )

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    # -- element file
    pre_lines[line_index] = iwfm.pad_both(
        pre_dict_new['elem_file'], f=4, b=53
    ) + ' '.join(pre_lines[line_index].split()[1:])

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    # -- node file
    pre_lines[line_index] = iwfm.pad_both(
        pre_dict_new['node_file'], f=4, b=53
    ) + ' '.join(pre_lines[line_index].split()[1:])

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    # -- stratigraphy file
    pre_lines[line_index] = iwfm.pad_both(
        pre_dict_new['strat_file'], f=4, b=53
    ) + ' '.join(pre_lines[line_index].split()[1:])

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    # -- stream file
    pre_lines[line_index] = iwfm.pad_both(
        pre_dict_new['stream_file'], f=4, b=53
    ) + ' '.join(pre_lines[line_index].split()[1:])

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    # -- lake file
    if len(pre_dict['lake_file']) > 1 and has_lake:
        pre_lines[line_index] = iwfm.pad_both(
            pre_dict_new['lake_file'], f=4, b=53
        ) + ' '.join(pre_lines[line_index].split()[1:])
    else:
        pre_lines[line_index] = (
            iwfm.pad_both(' ', f=4, b=53)
            + '/ '
            + ' '.join(pre_lines[line_index].split()[1:])
        )

    pre_lines.append('')
    # -- write new preprocessor input file
    with open(pre_dict_new['prename'], 'w') as outfile:
        outfile.write('\n'.join(pre_lines))

    return
