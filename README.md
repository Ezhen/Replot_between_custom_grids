# Replot_between_custom_grids
Scripts to replot variables from one custom conventional grid to another.

Required libraries:
Pyroms3 - https://github.com/ESMG/pyroms
netCDF4
some other more-less standard libraries

Content:
* EDIT_and_EXECUTE_ME.py - main script, where we define grid we replot FROM and ON and varaibles for replotting
* Get_grid.py - reads the grid (credits to Kate Heldstrom)
* make_remap_any_other_grid_file.py - slight modification of Kate's initial script, which was made for ROMS only
* Class_grid.py - class grid

Folder RESULTS contains replotted 2 resulting netCDF files with replotted variables from one grid to another and in reverse.

! Three territorial snapshots of COPERNICUS files (Odyssea & Mercator) are here as for the demonstration purpose only and will be removed immediately by request !

All credits to Kate Heldstrom, https://github.com/ESMG/pyroms/commits?author=kshedstrom
She built the core to prepare files for ROMS; I adopted it for my purposes.
