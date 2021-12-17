# import laspy.file
# import laspy.header

import laspy
import numpy as np
from scipy import spatial
import rasterio as rio
from rasterio.warp import transform
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

import sys
sys.setrecursionlimit(10000)





def main():

	f = laspy.read('./210323_Vol_6_Lidar_50m.las')
	# f = laspy.read('./210323_Vol_6_Lidar.las')
	print(f.header.__dict__)
	scale = f.header.scale
	offset = f.header.offset
	mins = f.header.mins
	maxs = f.header.maxs


	print('scale', scale)
	print('offset', offset)

	print(f.header.vlrs)

	for i in range(len(f.header.vlrs)):
		print(f.header.vlrs[i].__dict__)


	# scaled_x = scaled_x_dimension(f)
	# scaled_y = scaled_y_dimension(f)
	# scaled_z = scaled_z_dimension(f)

	x = f.X * f.header.scales[0] + f.header.offsets[0]
	y = f.Y * f.header.scales[1] + f.header.offsets[1]
	z = f.Z * f.header.scales[2] + f.header.offsets[2]


	# min_x = mins[0]
	# min_y = mins[1]
	# max_x = maxs[0]
	# max_y = maxs[1]

	min_x = min(x)
	min_y = min(y)
	max_x = max(x)
	max_y = max(y)

	print('min_x, max_x, min_y, max_y')
	print(min_x, max_x, min_y, max_y)


	resolution = 2.5

	new_ds_width = (max_x - min_x)/resolution
	new_ds_height = (max_y - min_y)/resolution


	


	crs_wgs84 = {'init': 'EPSG:4326'} #LonLat WGS84...
	crs_las = {'init': 'EPSG:3945'}

	# x, y = transform(crs_las, crs_wgs84,  scaled_x[0:10] , scaled_y[0:10])
	# print(x, y)

	west, south, east, north = min_x, min_y, max_x, max_y
	EPSG39452pix = rio.transform.from_bounds(west, south, east, north, new_ds_width, new_ds_height)
	print('EPSG39452pix')
	print(EPSG39452pix)

	x = x - min_x
	y = y - min_y


	exit(1)

	# v, u = ~EPSG39452pix*(scaled_x.astype(np.float32), scaled_y.astype(np.float32))

	# print(u[0:100], v[0:100])

	if True:
		print('building KDTree')
		start = time.process_time()
		dataset = np.vstack([x.astype(np.float32), y.astype(np.float32)]).transpose()
		tree = spatial.KDTree(dataset, leafsize=20)
		print('KDTree built. time = '+str(time.process_time() - start))

	# print('dataset.size')
	# print(dataset.size)



	raster_name = 'rast.tif'

	if False:
		#4 colors rasters
		new_dataset = rio.open('./'+raster_name, 'w', driver='GTiff', compress="JPEG",
										height=new_ds_height, width=new_ds_width,
										count=4, dtype=rio.uint8,
										crs=crs_wgs84, transform=EPSG39452pix)
		image = np.zeros((new_dataset.height, new_dataset.width, 4), dtype=np.uint8)



		for i in range(new_dataset.width):
			print(str(i)+'/'+str(new_dataset.width))
			for j in range(new_dataset.height):
				select = (resolution*i < x) & (x < resolution*(i+1)) & (resolution*j < y) & (y < resolution*(j+1))
				image[j,i,0]= np.mean(f.red[select])
				image[j,i,1]= np.mean(f.green[select])
				image[j,i,2]= np.mean(f.blue[select])
				image[j,i,3]= 255

				# print(image[i,j,0], image[i,j,1], image[i,j,2], image[i,j,3])
				print(len(f.red[select]))


		plt.imshow(image)
		plt.show()

		new_dataset.write(image[:,:, 0], 1)
		new_dataset.write(image[:,:, 1], 2)
		new_dataset.write(image[:,:, 2], 3)
		new_dataset.write(image[:,:, 3], 4)
		new_dataset.close()

	else:

		new_dataset = rio.open('./'+raster_name, 'w', driver='GTiff',
										nodata = 0,
										height=new_ds_height, width=new_ds_width,
										count=1, dtype=rio.float32,
										crs=crs_las, transform=EPSG39452pix)

		DSM = np.zeros((new_dataset.width, new_dataset.height, 1), dtype=np.float32)
		# mask = np.zeros((new_dataset.height, new_dataset.width, 1), dtype=np.uint8)

		print('building raster')
		start = time.process_time()

		for i in range(new_dataset.height):
			# print(str(i)+'/'+str(new_dataset.height))
			for j in range(new_dataset.width):

				# start = time.process_time()
				# select = (resolution*i < x) & (x < resolution*(i+1)) & (resolution*(new_dataset.width-j-1) < y) & (y < resolution*(new_dataset.width-j))
				# if len(z[select])>0:
				# 	DSM[j,i,0] = np.max(z[select])
				# else:
				# 	DSM[j,i,0] = 0
				# print('1 pix select. time = '+str(time.process_time() - start))

				start = time.process_time()
				select = tree.query_ball_point([resolution*(i+0.5), resolution*(new_dataset.width-j-0.5)], resolution/2)
				if len(z[select])>0:
					DSM[j,i,0] = np.max(z[select])
				else:
					DSM[j,i,0] = 0
				print('1 pix kdtree. time = '+str(time.process_time() - start)+ '    ' + str(i*new_dataset.height+j) + '/' +str(new_dataset.height*new_dataset.width))


		plt.imshow(DSM)
		plt.show()

		# new_dataset.write_mask(mask[:,:,0])
		new_dataset.write(DSM[:,:,0], 1)


#exec avec KDtree et ball select : 209s 
#exec avec select : 209s 

if __name__ == "__main__":

	main()