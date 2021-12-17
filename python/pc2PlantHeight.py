#will run in this docker containing cloudcompare
#https://github.com/tyson-swetnam/cloudcompare-docker
# cc command line man mage
#https://www.cloudcompare.org/doc/wiki/index.php?title=Command_line_mode

import rasterio as rio
from rasterio.warp import transform
import matplotlib.pyplot as plt
import subprocess

# docker commands
# docker run -d -it -v C:\Users\michael.delagarde\Documents\DEV\jill:/home/host/ --name  tswetnam/xpra-cc:cudagl-18.04





def main(file_name):



	
	cmd1 = "CloudCompare -O "+file_name+" -RASTERIZE -GRID_STEP 0.2 -VERT_DIR 2 -PROJ MAX -SF_PROJ AVG -EMPTY_FILL INTERP -OUTPUT_RASTER_Z"
	cmd2 = "CloudCompare -O "+file_name+" -RASTERIZE -GRID_STEP 0.2 -VERT_DIR 2 -PROJ MIN -SF_PROJ AVG -EMPTY_FILL INTERP -OUTPUT_RASTER_Z"

	subprocess.run(cmd1, shell=True)
	subprocess.run(cmd2, shell=True)

	files = os.listdir('./')
	files = [x for x in files if file_name in x]


	# crs_wgs84 = {'init': 'EPSG:4326'} #LonLat WGS84...
	crs_las = {'init': 'EPSG:3945'}


	output = 'PlantHeight_020.tif'
	# raster_name_min = 'rast_cc2alteia_min_020.tif'

	dataset = rio.open(files[0])
	dataset_min = rio.open(files[1])

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




if __name__ == "__main__":

	file_name = "210323_Vol_6_Lidar.las"
	main(file_name)