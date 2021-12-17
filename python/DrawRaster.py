# from utils import *
# from graphUtils import *
import rasterio as rio
import rasterio.features
import rasterio.warp
from rasterio.warp import transform
from matplotlib import pyplot
from rasterio.plot import show

import numpy as np
import math

from matplotlib import cm

# from parse import *
# import geojson
# from os import listdir

import time

import matplotlib.pyplot as plt
from tqdm import tqdm


DSM_like = False


def drawPoint(pu, pv, im, color, radius):
#dessine un point sur l'im


	U = range(-radius, radius)
	V = range(-radius, radius)

	for i in U:
		for j in V:
			if(i**2+j**2<=radius**2):
				if pu+i < im.shape[0] and pu+i >= 0 and pv+j < im.shape[1] and pv+j >= 0:
					im[pu+i, pv+j]=color




def LonLat2uv(Lon, Lat, dataset):


	# #coord map
	# x, y = transform({'init': 'EPSG:4326'}, dataset.crs,  [Lon] , [Lat])
	# #coord image
	pixel_y, pixel_x = ~dataset.transform*(x[0], y[0]) #le transpose ici n'est pas super clean
	# pixel_y, pixel_x = ~dataset.transform*(Lon, Lat) #le transpose ici n'est pas super clean

	return pixel_x, pixel_y


def scatter_geotiff(raster_name, Lon, Lat, val):
#draw a geotiff scatter of a value C [0,1]

	# west, south, east, north = rio.transform.array_bounds(ref_dataset.height, ref_dataset.width, ref_dataset.transform)
	# new_transform = rasterio.transform.from_bounds(west, south, east, north, new_ds_width, new_ds_height)

	#boundaries
	west = min(Lon)
	east = max(Lon)
	south = min(Lat)
	north = max(Lat)

	resolution = 0.5 #m
	new_ds_width = (east-west)*111120*math.cos((north+south)/2/180*math.pi)/resolution
	new_ds_height = (north-south)*111120/resolution


	print('new_ds_width = ', new_ds_width)
	print('new_ds_height = ', new_ds_height)


	LonLat2pix = rasterio.transform.from_bounds(west, south, east, north, new_ds_width, new_ds_height)


	# x, y = transform({'init': 'EPSG:4326'}, {'init': 'EPSG:26749'},  [west, east] , [south, north])
	# west2 = x[0]
	# east2 = x[1]
	# south2 = y[0]
	# north2 = y[1]

	# print(west2, south2, east2, north2)

	# #shift
	# west2 += -220
	# east2 += -220
	# south2 += 0
	# north2 += 0

	# EPSG267492pix = rasterio.transform.from_bounds(west2, south2, east2, north2, new_ds_width, new_ds_height)


	crs = {'init': 'EPSG:4326'} #LonLat WGS84...
	# crs = {'init': 'EPSG:26749'}

	# exit()

	if DSM_like==False: 
		#4 colors rasters
		new_dataset = rasterio.open('./'+raster_name, 'w', driver='GTiff', compress="JPEG",
										height=new_ds_height, width=new_ds_width,
										count=4, dtype=rasterio.uint8,
										crs=crs, transform=LonLat2pix)
		image = np.zeros((new_dataset.height, new_dataset.width, 4), dtype=np.uint8)

		cmap = cm.get_cmap('RdYlGn', 12)

		for i in tqdm(range(len(val))):
			v, u = ~LonLat2pix*(Lon[i], Lat[i])
			u = int(round(u))
			v = int(round(v))
			c = cmap(val[i])
			drawPoint(u, v, image, [255*c[0], 255*c[1], 255*c[2], 255*c[3]], 4)

		# plt.imshow(image)
		# plt.show()

		new_dataset.write(image[:,:, 0], 1)
		new_dataset.write(image[:,:, 1], 2)
		new_dataset.write(image[:,:, 2], 3)
		new_dataset.write(image[:,:, 3], 4)


	else:
		#DSM like raster
		new_dataset = rasterio.open('./'+raster_name, 'w', driver='GTiff',
										nodata = 0,
										height=new_ds_height, width=new_ds_width,
										count=1, dtype=rasterio.float32,
										crs=crs, transform=LonLat2pix)

		DSM = np.zeros((new_dataset.height, new_dataset.width, 1), dtype=np.float32)
		mask = np.zeros((new_dataset.height, new_dataset.width, 1), dtype=np.uint8)

		for i in tqdm(range(len(val))):
			v, u = ~LonLat2pix*(Lon[i], Lat[i])
			u = int(round(u))
			v = int(round(v))
			drawPoint(u, v, DSM, [val[i]*15.0], 4)
			drawPoint(u, v, mask, [255], 4)

		# plt.imshow(DSM)
		# plt.show()

		new_dataset.write_mask(mask[:,:,0])
		new_dataset.write(DSM[:,:,0], 1)




	new_dataset.close()


if __name__ == "__main__":

	image = np.zeros((200, 200, 4), dtype=np.uint8)

	image[100,100] = [255, 0, 0, 255]

	#drawPoint(100, 100, image, [255,0,0,255], 50)
	radius = 50
	U = range(-radius, radius)
	V = range(-radius, radius)

	print(U)

	pu = 100
	pv = 100

	for i in U:
		for j in V:
			if(i**2+j**2<=radius**2):
				# if pu+i < im.shape[0] and pu+i >= 0 and pv+j < im.shape[1] and pv+j >= 0:
				image[pu+i, pv+j]=[255, 0, 0, 255]

	plt.imshow(image)
	plt.show()