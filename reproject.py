import geopandas as gpd

# caminho pro SHP que tá em 4326
shp_path = r"D:\01-TESE\03-Capitulo_IV\09-ortomosaicos\07-camadas_raster_120m\shps\estressadas.shp"

gdf = gpd.read_file(shp_path)
gdf = gdf.to_crs("EPSG:32721")
gdf.to_file(shp_path, driver="ESRI Shapefile")
print("Reprojeção concluída.")
