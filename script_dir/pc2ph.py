# import laspy.file
# import laspy.header

import rasterio as rio
from rasterio.warp import transform
import subprocess
import json
import sys
import logging
LOG_FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=LOG_FORMAT)



def pc2ph(file_path, grid_size, WORKING_DIR):


	# get the crs from the las file
	# the same crs will be used for the output raster
	crs_las = {'init': 'EPSG:3945'}


	pipeline_max = [
		file_path,
		{
			"type":"writers.gdal",
			"filename":str(WORKING_DIR/"max.tif"),
			"output_type":"max",
			"gdaldriver":"GTiff",
			"window_size":3,
			"resolution":grid_size
		}
	]

	pipeline_min = [
		file_path,
		{
			"type":"writers.gdal",
			"filename":str(WORKING_DIR/"min.tif"),
			"output_type":"min",
			"gdaldriver":"GTiff",
			"window_size":3,
			"resolution":grid_size
		}
	]

	with open(WORKING_DIR / 'pipeline_max.json', 'w') as outfile:
		json.dump(pipeline_max, outfile)
	with open(WORKING_DIR / 'pipeline_min.json', 'w') as outfile:
		json.dump(pipeline_min, outfile)

	logging.debug('Generating min and max rasters...')
	#generate 2 rasters: max and min (description of pipelines in .json files)
	subprocess.run('pdal pipeline '+str(WORKING_DIR/'pipeline_max.json'), shell=True)
	subprocess.run('pdal pipeline '+str(WORKING_DIR/'pipeline_min.json'), shell=True)
	# subprocess.run('pdal pipeline '+json.dumps(pipeline_max), shell=True)
	# subprocess.run('pdal pipeline '+json.dumps(pipeline_min), shell=True)


	logging.debug('Generating diff raster...')

	dataset_max = rio.open(WORKING_DIR/'max.tif')
	dataset_min = rio.open(WORKING_DIR/'min.tif')

	new_dataset = rio.open(WORKING_DIR/'output.tif', 'w',
									driver = dataset_max.driver,
									nodata = dataset_max.nodata,
									height=dataset_max.height, width=dataset_max.width,
									count=dataset_max.count, dtype=rio.float64,
									crs=crs_las, transform=dataset_max.transform)

	band_max = dataset_max.read(1)
	band_min = dataset_min.read(1)

	band = band_max - band_min

	new_dataset.write(band, 1)

	logging.debug('All done')


if __name__ == "__main__":

	pc2ph('input.las', 0.2)