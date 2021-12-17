# import laspy.file
# import laspy.header

import rasterio as rio
from rasterio.warp import transform
import matplotlib.pyplot as plt





def main():


	crs_wgs84 = {'init': 'EPSG:4326'} #LonLat WGS84...
	crs_las = {'init': 'EPSG:3945'}




	output = 'PlantHeight_020.tif'
	# raster_name_min = 'rast_cc2alteia_min_020.tif'

	dataset = rio.open('./raster_full_cc_020.tif')
	dataset_min = rio.open('./raster_full_cc_min_020.tif')

	new_dataset = rio.open('./'+output, 'w',
									driver = dataset.driver,
									nodata = dataset.nodata,
									height=dataset.height, width=dataset.width,
									count=dataset.count, dtype=rio.float64,
									crs=crs_las, transform=dataset.transform)

	band = dataset.read(1)
	band_min = dataset_min.read(1)

	band = band - band_min

	plt.imshow(band)
	plt.show()

	new_dataset.write(band, 1)


#exec avec KDtree et ball select : 209s 
#exec avec select : 209s 

if __name__ == "__main__":

	main()