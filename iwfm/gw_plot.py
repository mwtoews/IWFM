# gw_plot.py
# Assemble groundwater hydrograph info and call fns to draw individual plots
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


def gw_plot(obs_file, gwhyd_info_file, gwhyd_files, gwhyd_names, yaxis_width, titlewords):
    ''' gw_plot() - Assemble groundwater hydrograph info and call fns to 
        write individual plots to PDF files

    Parameters
    ----------
    obs_file : str
        name of PEST smp file with observed values 
        (or 'none' if no observations)
    
    gwhyd_info_file : int
        IWFM groundwater.dat file name
    
    gwhyd_files : list
        list of IWFM hydrograph file names
    
    gwhyd_names : list
        list of legend entries
    
    yaxis_width : int
        minimum y-axis width, -1 for automatic
    
    title_words : str
        plot title words
    
    Return
    ------
    count : int
        number of hydrographs processed
    
    '''
    
    import iwfm as iwfm 

    well_dict, well_list = iwfm.read_sim_wells(gwhyd_info_file)  

    gwhyd_sim = iwfm.read_sim_hyds(len(gwhyd_files), gwhyd_files)  

    if obs_file.lower() != 'none':  # have observed values
      obs = iwfm.read_obs_smp(obs_file)
      count = iwfm.gw_plot_obs(well_list,len(gwhyd_files),obs,gwhyd_sim,gwhyd_names,well_dict,titlewords,yaxis_width)
    else:                           # no observed values
      count = iwfm.gw_plot_noobs(well_list,len(gwhyd_files),gwhyd_sim,gwhyd_names,well_dict,titlewords,yaxis_width)
    return count

if __name__ == '__main__':
    ' Run gw_plot() from command line '
    import sys
    import iwfm as iwfm
    import iwfm.debug as idb

    # read arguments from command line
    gwhyd_files = []
    gwhyd_names = []

    if len(sys.argv) > 1:  # arguments are listed on the command line
        titlewords = sys.argv[1]        # graph title
        obs_file = sys.argv[2]          # PEST-style smp file with observed values
        gwhyd_info_file = sys.argv[3]   # IWFM Groundwater.data file
        yaxis_width = int(sys.argv[4])  # y-axis minimum size
        no_hyds = int(sys.argv[5])      # No of simulated hydrograpns
        for i in range(0, no_hyds):
            gwhyd_files.append(sys.argv[6 + i * 2])  # IWFM groundwater hydrograph file
            gwhyd_names.append(
                sys.argv[6 + i * 2 + 1]
            )  # Legend name for this hydrograph

    else:  # get everything form the command line
        titlewords      = input('Graph title: ')
        obs_file        = input('Observed values file name (smp format) or \'none\'): ')
        gwhyd_info_file = input('IWFM Groundwater.dat file name: ')
        yaxis_width     = input('Minimum y-axis scale (-1 to autoscale): ')
        no_hyds         = int(input('Number of hydrographs to plot: '))
        for i in range(0, no_hyds):
            filename    = input(f'  IWFM Groundwater Hydrograph {i+1} file name: ')
            gwhyd_files.append(filename)
            legendname  = input(f'  Graph legend for {filename}: ')
            gwhyd_names.append(legendname)

    # test that the input files exist
    if obs_file.lower() != 'none':
      iwfm.file_test(obs_file)
    iwfm.file_test(gwhyd_info_file)
    for i in range(0, no_hyds):
        iwfm.file_test(gwhyd_files[i])

    idb.exe_time()  # initialize timer
    count = gw_plot(obs_file, gwhyd_info_file, gwhyd_files, gwhyd_names, yaxis_width, titlewords)
    print(f'  Created {count} PDF hydrograph files')  # update cli
    idb.exe_time()  # print elapsed time
