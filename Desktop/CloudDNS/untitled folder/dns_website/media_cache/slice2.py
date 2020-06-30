# given an array of tuples: (x, y)
import geopandas as gpd
import os
import gdal
import pandas as pd

image_path = "C:\\Users\\michael\\Google Drive\\Data_SESYNC_earthengine3\\LT5_L1T_32DAY_TOA_20020101_30_1_gee_08142017.tif"

def get_coordinate_pairs(tuple_array)
	lat_scale = 1 / 111133.25 * 12
	lon_scale = 1 / 96560.6 * 12

	c_pair_list = []

	x1_list = []
	x2_list = []
	y1_list = []
	y2_list = []
	for (x, y) in tuple_array:
		x1 = x - lat_scale
		x2 = x + lat_scale
		y1 = y - lon_scale
		y2 = y + lon_scale

		c_pair = ((x1, y1), (x2, y2))
		c_pair_list.append(c_pair)

		x1_list.append(x1)
		x2_list.append(x2)
		y1_list.append(y1)
		y2_list.append(y2)

	df = pd.DataFrame(data={'x1':x1_list, 'y1':y1_list, 'x2':x2_list, 'y2':y2_list})
	df.to_csv('../output_coordinates.csv')
	return c_pair_list, df

src = gdal.Open(image_path)
if src is None:
    print ('Unable to open ', image_path)
    sys.exit(1)
cols = src.RasterXSize
rows = src.RasterYSize
    
ds_crs = wkt2epsg(src.GetProjectionRef())

transform = src.GetGeoTransform()
x_origin = transform[0]
y_origin = transform[3]
pixel_width = transform[1]
pixel_height = -transform[5]

