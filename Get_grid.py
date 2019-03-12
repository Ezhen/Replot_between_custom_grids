import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import pyproj
from Class_grid import Class_grid

def Get_any_standard_grid(grdfile):
	nc = Dataset(grdfile, 'r')
	variables = list(nc.variables.keys())
	if 'lon' in variables and 'lat' in variables:
		lon = nc.variables['lon'][:]
		lat = nc.variables['lat'][:]
	elif 'longitude' in variables and 'latitude' in variables:
		lon = nc.variables['longitude'][:]
		lat = nc.variables['latitude'][:]
	else:
		 raise NameError('No conditional latitude and longitude found')

	for i in variables:

		if nc.variables[i][:].ndim == 3:
			var = nc.variables[i][0]; break
		elif nc.variables[i][:].ndim == 4:
			var = nc.variables[i][0,0]; break
		else:
			pass
	nc.close()
	try:
		lon,lat = np.meshgrid(lon,lat)
		lon_t,lat_t = lon,lat

		lon_vert = 0.5 * (lon[:,1:] + lon[:,:-1])
		lon_vert = 0.5 * (lon_vert[1:,:] + lon_vert[:-1,:])
		lat_vert = 0.5 * (lat[1:,:] + lat[:-1,:])
		lat_vert = 0.5 * (lat_vert[:,1:] + lat_vert[:,:-1])

		a=np.ones((len(var),len(var.T)))
		a[var.mask==True]=0
		mask_t=a

		z_t = 1; h=1
		geod = pyproj.Geod(ellps='WGS84')
		az_forward, az_back, dx = geod.inv(lon_vert[:,:-1], lat_vert[:,:-1], lon_vert[:,1:], lat_vert[:,1:])
		angle = 0.5 * (az_forward[1:,:] + az_forward[:-1,:])
		angle = (90 - angle) * np.pi/180.

		name = grdfile.split('/')[-1].split('_')[0].split('.')[0]
		return Class_grid(lon_t, lat_t, lon_vert, lat_vert, mask_t, z_t, h, angle, name)
	except:
		raise NameError('No variables are found')



