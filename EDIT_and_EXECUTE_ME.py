import pyroms
from Get_grid import Get_any_standard_grid
from make_remap_any_other_grid_file import make_remap_any_other_grid_file
from netCDF4 import Dataset
import numpy as np

# DEFINE file names

file_from = '/home/ulg/mast/eivanov/Validation/Ultimate_remapping/Odyssea_satellite.nc'		# File contains the grid we replot FROM
file_on = '/home/ulg/mast/eivanov/Validation/Ultimate_remapping/Mercator_ocean.nc'			# File contains the grid ON which we replot


# DEFINE variables to replot - put them one by one inside a list

#variables = ['analysed_sst']
variables = []



# ---------------------------------------------------------------------------------------------#
# SCRIPT EXECUTION # SCRIPT EXECUTION # SCRIPT EXECUTION # SCRIPT EXECUTION # SCRIPT EXECUTION #
# ---------------------------------------------------------------------------------------------#

grid_from = Get_any_standard_grid(file_from)
grid_on = Get_any_standard_grid(file_on)

make_remap_any_other_grid_file(grid_from)
make_remap_any_other_grid_file(grid_on)


# compute remap weights input namelist variables for bilinear remapping at rho points

grid1_file = 'remap_grid_%s_t.nc' %(grid_from.name)
grid2_file = 'remap_grid_%s_t.nc' %(grid_on.name)

interp_file_from = 'remap_weights_%s_to_%s_bilinear_t_to_t.nc' %(grid_from.name,grid_on.name)
interp_file_on = 'remap_weights_%s_to_%s_bilinear_t_to_t.nc' %(grid_on.name,grid_from.name)


map1_name = '%s to %s Bilinear Mapping' %(grid_from.name,grid_on.name)
map2_name = '%s to %s Bilinear Mapping' %(grid_on.name,grid_from.name)

pyroms.remapping.compute_remap_weights(grid1_file, grid2_file, interp_file_from, interp_file_on, map1_name, map2_name, 1, 'bilinear')

nc1 = Dataset(file_from.split('/')[-1][:-3]+'_remapped.nc', 'w', format='NETCDF4')
nc2 = Dataset(file_on, 'r', format='NETCDF4')
nc3 = Dataset(file_from, 'r', format='NETCDF4')
allvar = list(nc2.variables.keys())

if 'lon' in allvar and 'lat' in allvar:
	lon = nc2.variables['lon'][:]
	lat = nc2.variables['lat'][:]
elif 'longitude' in allvar and 'latitude' in allvar:
	lon = nc2.variables['longitude'][:]
	lat = nc2.variables['latitude'][:]
nc1.createDimension('lat', len(lat))
nc1.createDimension('lon', len(lon))
nc1.createVariable('lat', 'f4', 'lat')
nc1.createVariable('lon', 'f4', 'lon')
nc1.variables['lat'][:] = lat
nc1.variables['lon'][:] = lon

allvar = list(nc3.variables.keys())
for var in allvar:
	if 'time' in var:
		time = nc3.variables[var][:]
nc1.createDimension('time', len(time))
nc1.createVariable('time', 'int32', 'time')
try:
	nc1.variables['time'].units = nc3.variables['time'].units
except:
	pass
nc1.variables['time'][:] = time

if len(variables) == 0:
	for var in allvar:
		if nc3.variables[var][:].ndim > 2:
			variables.append(var)

for var in variables:
	dimensions = ('time', 'lat', 'lon')
	spval= -32767
	nc1.createVariable(var, 'f8', dimensions, fill_value = spval)
	try:
		nc1.variables[var].long_name = nc3.variables[var].longname
	except:
		pass
	try:
		nc1.variables[var].units = nc3.variables[var].units
	except:
		pass
	try:
		nc1.variables[var].field = nc3.variables[var].field
	except:
		pass
	ndim = nc3.variables[var][:].ndim
	for i in range(len(time)):
		if ndim == 4:
			src_var = nc3.variables[var][i,0,:,:]
		elif ndim == 3:
			src_var = nc3.variables[var][i,:,:]
		dst_var = pyroms.remapping.remap(src_var, interp_file_from, spval=spval)
		dst_var = np.ma.masked_where(grid_on.mask_t==0,dst_var)
		dst_var = np.ma.masked_where(dst_var<-999,dst_var)		# interpolation is not perfect
		dst_var = np.ma.masked_where(grid_from.lat_t.max() < grid_on.lat_t,dst_var)
		dst_var = np.ma.masked_where(grid_from.lon_t.max() < grid_on.lon_t,dst_var)
		dst_var = np.ma.masked_where(grid_from.lat_t.min() > grid_on.lat_t,dst_var)
		dst_var = np.ma.masked_where(grid_from.lon_t.min() > grid_on.lon_t,dst_var)
		dst_var = np.ma.masked_where(dst_var < (np.nanmean(dst_var) - np.nanstd(dst_var)),dst_var) 		# interpolation is not perfect
		nc1.variables[var][i] = dst_var

	print('variable %s is written into the file' %(var))
nc1.close()
nc2.close()
nc3.close()
