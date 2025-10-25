import os
import fiona
import rasterio
from rasterio.crs import CRS
from fiona.crs import from_epsg, from_string


def get_shapefile_crs(shapefile_path):
    """Obtém o CRS de um arquivo shapefile"""
    with fiona.open(shapefile_path) as src:
        return src.crs


def get_raster_crs(raster_path):
    """Obtém o CRS de um arquivo raster"""
    with rasterio.open(raster_path) as src:
        return src.crs


def compare_crs(crs1, crs2):
    """Compara dois CRS, retorna True se forem equivalentes"""
    try:
        # Tenta comparar diretamente
        if crs1 == crs2:
            return True

        # Converte para objeto CRS do rasterio se necessário
        crs1_obj = CRS.from_user_input(crs1) if not isinstance(crs1, CRS) else crs1
        crs2_obj = CRS.from_user_input(crs2) if not isinstance(crs2, CRS) else crs2

        return crs1_obj == crs2_obj
    except:
        return False


def check_crs_compatibility(shp_folder, tif_folder):
    """Verifica se todos os SHP e TIF têm o mesmo CRS"""
    # Coletar todos os arquivos SHP
    shp_files = [f for f in os.listdir(shp_folder) if f.endswith('.shp')]
    if not shp_files:
        print("Nenhum arquivo .shp encontrado na pasta especificada.")
        return

    # Coletar todos os arquivos TIF
    tif_files = [f for f in os.listdir(tif_folder) if f.endswith('.tif')]
    if not tif_files:
        print("Nenhum arquivo .tif encontrado na pasta especificada.")
        return

    # Obter CRS do primeiro SHP como referência
    try:
        reference_shp_crs = get_shapefile_crs(os.path.join(shp_folder, shp_files[0]))
        print(f"CRS de referência (primeiro SHP): {reference_shp_crs}")
    except Exception as e:
        print(f"Erro ao ler o arquivo SHP {shp_files[0]}: {e}")
        return

    # Verificar todos os SHPs
    shp_errors = []
    for shp in shp_files[1:]:
        try:
            crs = get_shapefile_crs(os.path.join(shp_folder, shp))
            if not compare_crs(reference_shp_crs, crs):
                shp_errors.append(f"{shp}: {crs}")
        except Exception as e:
            shp_errors.append(f"{shp}: ERRO - {str(e)}")

    # Verificar todos os TIFs
    tif_errors = []
    for tif in tif_files:
        try:
            crs = get_raster_crs(os.path.join(tif_folder, tif))
            if not compare_crs(reference_shp_crs, crs):
                tif_errors.append(f"{tif}: {crs}")
        except Exception as e:
            tif_errors.append(f"{tif}: ERRO - {str(e)}")

    # Exibir resultados
    if not shp_errors and not tif_errors:
        print("✅ Todos os arquivos SHP e TIF possuem o mesmo CRS.")
        print(f"CRS comum: {reference_shp_crs}")
    else:
        if shp_errors:
            print("\n❌ Arquivos SHP com CRS diferente:")
            for error in shp_errors:
                print(f"  - {error}")

        if tif_errors:
            print("\n❌ Arquivos TIF com CRS diferente:")
            for error in tif_errors:
                print(f"  - {error}")


if __name__ == "__main__":
    # Configuração dos diretórios
    shp_folder = r"D:\01-TESE\03-Capitulo_IV\09-ortomosaicos\07-camadas_raster_120m\shps"
    tif_folder = r"D:\01-TESE\03-Capitulo_IV\09-ortomosaicos\07-camadas_raster_120m"

    # Verifica existência das pastas
    if not os.path.isdir(shp_folder):
        print(f"Pasta não encontrada: {shp_folder}")
    elif not os.path.isdir(tif_folder):
        print(f"Pasta não encontrada: {tif_folder}")
    else:
        check_crs_compatibility(shp_folder, tif_folder)
