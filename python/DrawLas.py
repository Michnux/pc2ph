import laspy.file
import laspy.header
import numpy as np

import rasterio as rio
import rasterio.features
import rasterio.warp
from rasterio.warp import transform

import matplotlib.pyplot as plt
import os
import math
from tqdm import tqdm





#convert raster to point cloud, using the DSM
def raster2pc(file_name, dsm):

	# f = laspy.read('./Point cloud.las') #cheat mode...
	dsm = rio.open(dsm)
	a = dsm.read(1)

	fm = rio.open(file_name)
	r = fm.read(1)
	g = fm.read(2)
	b = fm.read(3)
	al = fm.read(4)



	points = [] # np.zeros((4, new_dataset.height, new_dataset.width), 'uint8')
	for i in tqdm(range(0, al.shape[0], 2)):
		for j in range(0, al.shape[1], 2):
			if al[i,j]!=0: #alpha channel

				print('in alpha')
				# if r[i,j]+b[i,j]>30: #evite les effets de marges surements dus au jpg? was 3 for fuel maps
				x, y = fm.transform*(j,i)
				j2, i2 = ~dsm.transform*(x, y)
				if i2>=0 and i2<a.shape[0] and j2>=0 and j2<a.shape[1]:
					z = a[int(i2),int(j2)]
					points.append([x,y,z,r[i,j],g[i,j],b[i,j]])
					print([x,y,z,r[i,j],g[i,j],b[i,j]])

	# hdr = laspy.header.Header()

	scale = f.header.scale
	offset = f.header.offset

	dataset = np.vstack(points)

	dataset[:,0]=(dataset[:,0]-offset[0])/scale[0]
	dataset[:,1]=(dataset[:,1]-offset[1])/scale[1]
	dataset[:,2]=(dataset[:,2]-offset[2]+0.5)/scale[2] #ajout d'une petit offset en hauteur pour que les routes soient plus haut que le nuage de point original sur la représentation


	print("generate las...")
	outFile1 = laspy.file.File(file_name+'.las', mode = "w", header = f.header)
	outFile1.X = dataset[:,0];
	outFile1.Y = dataset[:,1];
	outFile1.Z = dataset[:,2];
	outFile1.red = dataset[:,3]
	outFile1.green = dataset[:,4]
	outFile1.blue = dataset[:,5]
	outFile1.close()



if __name__ == "__main__":
	raster2pc('speedmap_wgs84.tif', 'DSM.tif')





	# f = laspy.file.File('./TyreMap.las', mode='r')
	# print(f.header)
	# scale = f.header.scale
	# offset = f.header.offset


	# print(scale, offset)
	# print(scale[0]*offset[0], scale[1]*offset[1], scale[2]*offset[2])



	# headerformat = f.header.header_format
	# for spec in headerformat:
	#     print(spec.name)
	#     #, f.header[spec.name])

	# print(f.header.vlrs[0].__dict__)