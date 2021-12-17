# import laspy.file
# import laspy.header

import rasterio as rio
from rasterio.warp import transform
# import matplotlib.pyplot as plt
import subprocess



def main():


	crs_wgs84 = {'init': 'EPSG:4326'} #LonLat WGS84...
	crs_las = {'init': 'EPSG:3945'}

	#generate 2 rasters: max and min (description of pipelines in .json files)
	subprocess.run('pdal pipeline pipeline_max.json', shell=True)
	subprocess.run('pdal pipeline pipeline_min.json', shell=True)

	dataset_max = rio.open('./max.tif')
	dataset_min = rio.open('./min.tif')

	new_dataset = rio.open('./output.tif', 'w',
									driver = dataset_max.driver,
									nodata = dataset_max.nodata,
									height=dataset_max.height, width=dataset_max.width,
									count=dataset_max.count, dtype=rio.float64,
									crs=crs_las, transform=dataset_max.transform)

	band_max = dataset_max.read(1)
	band_min = dataset_min.read(1)

	band = band_max - band_min

	# plt.imshow(band)
	# plt.show()

	new_dataset.write(band, 1)





if __name__ == "__main__":

	main()