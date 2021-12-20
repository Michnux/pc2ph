# import laspy.file
# import laspy.header

import rasterio as rio
from rasterio.warp import transform
import subprocess
import json


def pc2ph(file_path, grid_size):


	# get the crs from the las file
	# the same crs will be used for the output raster
	crs_las = {'init': 'EPSG:3945'}


	pipeline_max = [
		"/home/work_dir/input.las",
		{
			"type":"writers.gdal",
			"filename":"max.tif",
			"output_type":"max",
			"gdaldriver":"GTiff",
			"window_size":3,
			"resolution":grid_size
		}
	]

	pipeline_min = [
		"/home/work_dir/input.las",
		{
			"type":"writers.gdal",
			"filename":"min.tif",
			"output_type":"min",
			"gdaldriver":"GTiff",
			"window_size":3,
			"resolution":grid_size
		}
	]

	with open('pipeline_max.json', 'w') as outfile:
		json.dump(pipeline_max, outfile)
	with open('pipeline_min.json', 'w') as outfile:
		json.dump(pipeline_min, outfile)

	#generate 2 rasters: max and min (description of pipelines in .json files)
	subprocess.run('pdal pipeline pipeline_max.json', shell=True)
	subprocess.run('pdal pipeline pipeline_min.json', shell=True)
	# subprocess.run('pdal pipeline '+json.dumps(pipeline_max), shell=True)
	# subprocess.run('pdal pipeline '+json.dumps(pipeline_min), shell=True)

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

	new_dataset.write(band, 1)



if __name__ == "__main__":

	pc2ph('input.las', 0.2)