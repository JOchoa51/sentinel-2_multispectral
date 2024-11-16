from functions import simple
from functions import indices
import os
from time import perf_counter
import rasterio as rs
from rasterio.enums import Resampling
import numpy as np

GREEN = "\u001B[32m"
RED = "\u001B[31m"
BLUE = "\u001B[34m"
YELLOW = "\u001B[33m"
RESET = "\u001B[0m"


def read(start: int, end: int, path: str):
    '''
    Description
    -----------
    Reads the files of a directory and check if they are in TIF file to select them, read them 
    using rasterio and add them to a dictionary containing the corresponding band name.
    It creates a range of numbers given the start and end, so that all images in between are taken
    into account.

    Once the images are saved in the dictionary, it takes the largest height of the images and the
    largest width for the followin interpolation. The images are passed through the read() function
    of rasterio and an out_shape is defined as follows:

    >>> height = len(images["B2"][0]) # height in pixels of the highest-resolution image
    >>> width = len(images["B2"][1]) # width in pixels of the highest-resolution image
    >>> out_shape=(height, width)

    Then a cubic resampling method is used to interpolate the images and make them all have the same
    spatial resolution.

    Parameters 
    ----------- 
    start: int
        Starting number of the range of bands you wish to read.
    end: int
        Ending number of the range of bands you wish to read.
    path: str
        Full path of the directory in which the images are to be found.
        
    Returns      
    -------
    resampled: dict
        Dictionary containing the resampled images to the highest resolution available.

    '''

    print(F"{RED}\nReading...")
    images = dict()
    for file in os.listdir(path):
        if file.endswith("tif"):
            for i in range(start, end+1):
                file_path = f"{path}\{file}"
                ds = rs.open(file_path)
                images[f"B{file[-6:-4]}"] = ds.read(1)
    print("Resampling...")
    start = perf_counter()
    resampled = dict()
    # Altura de la matriz de máxima dimensión
    height = len(images["B02"][0])
    # Anchura de la matriz de máxima dimensión
    width = len(images["B02"][1])
    for file in os.listdir(path):
        if file.endswith(".tif"):
            with rs.open(f"{path}\{file}") as src:
                imagen_resampled = src.read(out_shape=(height, width), # out_shape=(rows, columns)
                                    resampling=Resampling.cubic) 
            # Normalización de los valores de la matriz
            imagen_resampled = imagen_resampled / np.amax(imagen_resampled)
            # Almacenamiento en un diccionario
            resampled[f"B{file[-6:-4]}"] = imagen_resampled
    end = perf_counter()
    print(f"{GREEN}Resampling time: {round(end-start, 4)} s {RESET}")
    return resampled

def menu():
    '''
    Description
    -----------
    Prints the menu of the compositions available.
        
    '''
    print(f"{YELLOW}\n## SIMPLE COMPOSITIONS ## {RESET}  \
            \n1. Natural. \
            \n2. Infrared \
            \n3. Short wave infrared \
            \n4. Agriculture \
            \n5. Geology \
            \n6. Bathymetric \
            \n\n{YELLOW}## BAND INDICES ## {RESET}\
            \n7. Normalized Difference Vegetation Index (NDVI) \
            \n8. Normalized Difference Moisture Index (NDMI) \
            \n9. Green Normalized Difference Vegetation Index (GNDVI) \
            \n10. Enhanced Vegetation Index (EVI) \
            \n11. Advanced Vegetation Index (AVI) \
            \n12. Soil Adjusted Vegetation Index (SAVI) \
            \n13. Water Stress Index (WSI) \
            \n14. Green Coverage Index (GCI) \
            \n15. Normalized Burned Ratio Index (NBRI) \
            \n16. Bare Soil Index (BSI) \
            \n17. Normalized Differential Water Index (NDWI) \
            \n18. Normalized Differential Snow Index (NDSI) \
            \n19. Normalized Differential Glacier Index (NDGI) \
            \n20. Atmospherically Resistant Vegetation Index (ARVI) \
            \n21. Structure Insensitive Pigmentation Index (SIPI) \
            \n22. Built-up Normalized Difference Index")

def save_simple(path: str, title: str):
    '''
    Description
    -----------
    This function is only called if the user decides to save the image through a command prompt.
    It saves the image to the directory "compositions".

    Parameters 
    ----------- 
    path: str
        Full path to the folder that contains the images.
    title: str
        Name of the composition.
   
    Notes
    -----
    This function saves the image of a simple composition, i.e., it does not include a colorbar.
    '''
    save = input("Save image? (Y/N): ")
    if save == 'Y' or save == 'Y'.lower():
        simple.create(comp, title, save=True, path=path)
        print(f"{GREEN}Image saved!{RESET}")
    else: 
        simple.create(comp, title)

def save_index(path: str, title: str):
    '''
    Description
    -----------
    This function is only called if the user decides to save the image through a command prompt.
    It saves the image to the directory "compositions".

    Parameters 
    ----------- 
    path: str
        Full path to the folder that contains the images.
    title: str
        Name of the composition.
   
    Notes
    -----
    The image saved by this function includes a colorbar.
    '''
    save = input("Save image? (Y/N): ")
    if save == 'Y' or save == 'Y'.lower():
        indices.create(comp, title, save=True, path=path)
        print(f"{GREEN}Image saved!{RESET}")
    else: 
        indices.create(comp, title) 

def run_again():
    '''
    Description
    -----------
    Determines whether the user wants to run again the program from the menu in order to let
    them choose another composition.

    Returns
    -------
    again, option: str, int
        Tuple containing both the decision of executing again and the new option to be selected.
    '''
    again = input(f"{YELLOW}\nWould you like to crete another composition? (Y/N): {RESET}")
    if again == "Y" or again == "Y".lower():
        menu()
        option = int(input(f"{YELLOW}\n\nWhich composition would you like to create? Please specify the number: {RESET}"))
    elif again == "N" or again == "n".lower():
        print(f"{BLUE}\nThanks, see you!\n{RESET}")
        exit()
    return (again, option)

if __name__ == "__main__":

    print(GREEN,"\nWELCOME TO THE REMOTE SENSING PROCESSING PROGRAM\n",RESET)
    print("This program crates composition and indices of images obtained with Sentinel-2 satellite.\n")
    print(f"{BLUE}Please select the path in which your images are located\n{RESET}")

    path = input(f"\tFull path of the folder that contains the images: ")
    images = read(1,12, path)

    menu()
    option = int(input(f"{YELLOW}\n\nWhich composition would you like to create? Please specify the number: {RESET}"))

    while True:
    # Simples
        if option == 1:
            comp = simple.natural_color(images)
            save_simple(path, "Natural color")
            again, option = run_again()
        elif option == 2:
            comp = simple.infrared(images)
            save_simple(path, "False infrared")
            again, option = run_again()
        elif option == 3:
            comp = simple.shortwave_ir(images)
            save_simple(path, "Short wave infrared")
            again, option = run_again()
        elif option == 4:
            comp = simple.agriculture(images)
            save_simple(path, "Agriculture")
            again, option = run_again()
        elif option == 5:
            comp = simple.geology(images)
            save_simple(path, "Geology")
            again, option = run_again()
        elif option == 6:
            comp = simple.bathymetric(images)
            save_simple(path, "Bathymetric")
            again, option = run_again()
    # Indices
        elif option == 7:
            comp = indices.ndvi(images)
            save_index(path, "Normalized Difference Vegetation Index")
            again, option = run_again()
        elif option == 8:
            comp = indices.ndmi(images)
            save_index(path, "Normalized Difference Moisture Index")
            again, option = run_again()
        elif option == 9:
            comp = indices.gndvi(images)
            save_index(path, "Green Normalized Difference Vegetation Index")
            again, option = run_again()
        elif option == 10:
            comp = indices.evi(images)
            save_index(path, "Enhanced Vegetation Index")
            again, option = run_again()
        elif option == 11:
            comp = indices.avi(images)
            save_index(path, "Advanced Vegetation Index")
            again, option = run_again()
        elif option == 12:
            comp = indices.savi(images)
            save_index(path, "Soil Adjusted Vegetation Index")
            again, option = run_again()
        elif option == 13:
            comp = indices.wsi(images)
            save_index(path, "Water Stress Index")
            again, option = run_again()
        elif option == 14:
            comp = indices.gci(images)
            save_index(path, "Green Coverage Index")
            again, option = run_again()
        elif option == 15:
            comp = indices.nbri(images)
            save_index(path, "Normalized Burned Ratio Index")
            again, option = run_again()
        elif option == 16:
            comp = indices.bsi(images)
            save_index(path, "Bare Soil Index")
            again, option = run_again()
        elif option == 17:
            comp = indices.ndwi(images)
            save_index(path, "Normalized Differential Water Index")
            again, option = run_again()
        elif option == 18:
            comp = indices.ndsi(images)
            save_index(path, "Normalized Differential Snow Index")
            again, option = run_again()
        elif option == 19:
            comp = indices.ndgi(images)
            save_index(path, "Normalized Differential Glacier Index")
            again, option = run_again()
        elif option == 20:
            comp = indices.arvi(images)
            save_index(path, "Atmospherically Resistant Vegetation Index")
            again, option = run_again()
        elif option == 21:
            comp = indices.sipi(images)
            save_index(path, "Structure Insensitive Pigmentation Index")
            again, option = run_again()
        elif option == 22:
            comp = indices.bndi(images)
            save_index(path, "Built-up Normalized Difference Index")
            again, option = run_again()
        if option < 1 or option >22:
            print("Wrong option. Select again.\n")
            option = int(input(f"{YELLOW}\n\nWhich composition would you like to create? Please specify the number: {RESET}")) 
    

