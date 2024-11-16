import numpy as np
import matplotlib.pyplot as plt
import os

# BAND INDICES
# see
# https://acolita.com/lista-de-indices-espectrales-en-sentinel-2-y-landsat/

def create(array: any, title: str, cmap="viridis", save=False, path=None):
    '''
    Display the image in a matplotlib subplot with its respective colorbar.

    Parameters 
    ----------- 
    array: ndarray
        2D array containing the image data.
    title: str
        Name of the composition.
    save: bool
        Wether the user wants to save the image or not.
    path: str
        Path where the folder "Compositions" will be created.
        Default is the same path where the images are saved.

    Notes
    -----
    The array can have both a (3,N,M) or a (N,M) shape, where the first is an image with 3 bands.

    Examples
    --------
    >>> import rasterio as rs
    >>> from functions import simple
    >>> image = rs.open('ndvi.png')
    >>> image = image.read(1)
    >>> indices.create(image, 'NDVI', cmap='viridis', save=False, path=None)
    '''
    cmap = input("Which colormap would you like to use? Or press Enter to use default: ")
    if cmap == "":
        # cmap = 'viridis'
        plt.imshow(array)
    else:
        plt.imshow(array, cmap=cmap)
    plt.title(title)
    plt.colorbar()
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    if save == True and path != None:
        plt.savefig(f"{path}\Compositions\{title}.png", dpi=400)
        display = input("Display image? (Y/N): ")
        if display == 'Y' or display == 'Y'.lower():
            plt.show()
    else: 
        plt.show()
        
def ndvi(dictionary):
    '''
    Description
    -----------
    The Normalized Difference Vegetation Index (NDVI) is a numerical indicator that uses 
    the red and near-infrared spectral bands. The NDVI is highly associated with the 
    vegetation content. High NDVI values correspond to areas that reflect more in the near 
    infrared spectrum. Higher near-infrared reflectance corresponds to denser and healthier 
    vegetation (GU, 2019).

    Formula
    -------
    (NIR - RED) / (NIR + RED)   \n
    Sentinel-2: (B8 - B4) / (B8 + B4)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the NDVI index.
    
    References
    --------
    https://www.geo.university/pages/blog?p=spectral-indices-with-multispectral-satellite-data

    '''

    b8 = dictionary["B08"] / np.amax(dictionary["B08"])
    b4 = dictionary["B04"] / np.amax(dictionary["B04"])
    index = (b8-b4) / (b8+b4)
    index = index / np.amax(index)
    return index[0]

def ndmi(dictionary):
    '''
    Description
    -----------
    The Normalized Difference Moisture Index (NDMI) is used to determine the water content 
    of vegetation. It is calculated as a ratio between the NIR and SWIR values in the 
    traditional way (USGS, 2019).

    Formula
    -------
    (NIR - SWIR) / (NIR + SWIR)   \n
    Sentinel-2: (B8 - B11) / (B8 + B11)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the NDMI index.
    
    References
    --------
    https://www.usgs.gov/landsat-missions/normalized-difference-moisture-index

    '''
    b8a = dictionary["B8A"] / np.amax(dictionary["B8A"])
    b11 = dictionary["B11"] / np.amax(dictionary["B11"])
    index = (b8a-b11) / (b8a+b11)
    index = index / np.amax(index)
    return index[0]

def gndvi(dictionary):
    '''
    Description
    -----------
    The Green Normalized Difference Vegetation Index (GNDVI) is a modified version of the NDVI 
    to be more sensitive to variation in crop chlorophyll content. «The highest values of 
    correlation with the content of the N and DM leaf were obtained with the GNDVI index in all 
    periods of data acquisition and in both experimental phases. …GNDVI was more sensible than 
    NDVI in identifying different concentration rates of chlorophyll, which is highly correlated 
    with nitrogen, in two plant species” ( Gitelson et al. 1996 ) .

    Formula
    -------
    (NIR - GREEN) / (NIR + GREEN)   \n
    Sentinel-2: (B8 - B3) / (B8 + B3)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the GNDVI index.
    
    References
    --------
    https://www.researchgate.net/profile/Anatoly-Gitelson

    '''

    b8 = dictionary["B08"] / np.amax(dictionary["B08"])
    b3 = dictionary["B03"] / np.amax(dictionary["B03"])
    index = (b8-b3) / (b8+b3)
    index = index / np.amax(index)
    return index[0]

def evi(dictionary):
    '''
    Description
    -----------
    The Enhanced Vegetation Index (EVI) is similar to the NDVI and can be used to quantify the 
    greenness of vegetation. However, EVI corrects for some atmospheric conditions and canopy 
    background noise and is more sensitive in areas with dense vegetation. It incorporates an 
    "L" value to adjust the bottom of the awning, "C" values as coefficients of atmospheric 
    resistance and values of the blue band (B). These enhancements allow the calculation of 
    indices as a ratio between R and NIR values, while reducing background noise, atmospheric 
    noise, and clipping in most cases ( USGS, 2019 ).

    Formula
    -------
    G * ((NIR - RED) / (NIR + C1 * RED - C2 * BLUE + L)))   \n
    Sentinel-2: 2.5 * ((B8 - B4) / (B8 + 6 * B4 - 7.5 * B2 + 1))

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the EVI index.
    
    References
    --------
    https://www.usgs.gov/landsat-missions/landsat-enhanced-vegetation-index?qt-science_support_page_related_con=0#qt-science_support_page_related_con

    '''
    # BUG: It does not work
    
    b8 = dictionary["B08"] / np.amax(dictionary["B08"])
    b4 = dictionary["B04"] / np.amax(dictionary["B04"])
    b2 = dictionary["B02"] / np.amax(dictionary["B02"])
    C1 = 6 / 9
    C2 = 7.5 / 9
    L = 1 / 9
    G = 2.5 / 9
    index = G * ((b8 - b4) / (b8 + C1 * b4 - C2 * b2 + L))
    index = index / np.amax(index)
    return index[0]

def avi(dictionary):
    '''
    Description
    -----------
     The Advanced Vegetation Index (AVI) is a numerical indicator, similar to NDVI, that uses 
    the red and near-infrared spectral bands. Like the NDVI, the AVI is used in vegetation 
    studies to monitor crop and forest variations over time. Through the multitemporal combination 
    of AVI and NDVI, users can discriminate different types of vegetation and extract phenological 
    characteristics/parameters ( GU, 2019 ).

    Formula
    -------
    [NIR * (1 - RED) * (NIR - RED)] ^ 1/3   \n
    Sentinel-2: [B8 * (1 - B4)*(B8 - B4)] ^ 1/3

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the AVI index.
    
    References
    --------
    https://www.geo.university/pages/blog?p=spectral-indices-with-multispectral-satellite-data

    '''
   
    b8 = dictionary["B08"] / np.amax(dictionary["B08"])
    b4 = dictionary["B04"] / np.amax(dictionary["B04"])
    index = abs((b8 * (1 - b4)*(b8 - b4)))**(1/3)
    index = index / np.amax(index)
    return index[0]

def savi(dictionary):
    '''
    Description
    -----------
    The Soil Adjusted Vegetation Index (SAVI) is used to correct the NDVI for the influence 
    of soil brightness in areas where vegetative cover is low. The SAVI derived from Landsat 
    surface reflectance is calculated as a ratio of RED and NIR values with a ground luminosity 
    (L) correction factor set to 0.5 to accommodate most land cover types ( USGS, 2019 ).

    Formula
    -------
    ((NIR - RED) / (NIR + RED + L)) * (1 + L)   \n
    Sentinel-2: (B8 - B4) / (B8 + B4 + 0.428) * (1.428)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the SAVI index.
    
    References
    --------
    https://www.usgs.gov/landsat-missions/landsat-soil-adjusted-vegetation-index

    '''

    b8 = dictionary["B08"] / np.amax(dictionary["B08"])
    b4 = dictionary["B04"] / np.amax(dictionary["B04"])
    index = abs(((b8 - b4) / (b8 + b4 + 0.428))) * (1.428)
    index = index / np.amax(index)
    return index[0]

def wsi(dictionary):
    '''
    Description
    -----------
    The Water Stress Index is used for canopy stress analysis, productivity prediction, 
    and biophysical modelling. The interpretation of the MSI is reversed relative to other 
    aquatic vegetation indices; therefore, the highest values of the index indicate a 
    greater water stress of the plants and, in inference, a lower moisture content of the soil. 
    The values of this index range from 0 to more than 3, with the common range for green 
    vegetation being 0.2 to 2 ( Welikhe et al., 2017 ).

    Formula
    -------
    MidIR / NIR   \n
    Sentinel-2: B11 / B8

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the WSI index.
    
    References
    --------
    https://www.omicsgroup.org/journals/estimation-of-soil-moisture-percentage-using-landsatbased-moisturestress-index-2469-4134-1000200.php?aid=90942

    '''

    b8 = dictionary["B08"] / np.amax(dictionary["B08"])
    b11 = dictionary["B11"] / np.amax(dictionary["B11"])
    index = (b11/b8) * 1.25
    index = index / np.amax(index)
    return index[0]

def gci(dictionary):
    '''
    Description
    -----------
    In remote sensing, the Green Coverage Index (GCI), or Chlorophyll Index is used to estimate 
    the chlorophyll content in the leaves of various plant species. The chlorophyll content 
    reflects the physiological state of the vegetation; it decreases in stressed plants and 
    can therefore be used as a measure of plant health ( EOS, 2019 ).

    Formula
    -------
    (NIR) / (GREEN) - 1   \n
    Sentinel-2: (B9 / B3) - 1

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the GCI index.
    
    References
    --------
    https://eos.com/blog/vegetation-indices/

    '''

    b9 = dictionary["B09"] / np.amax(dictionary["B09"])
    b3 = dictionary["B03"] / np.amax(dictionary["B03"])
    index = (b9 / b3) - 1
    index = index / np.amax(index)
    return index[0]

def nbri(dictionary):
    '''
    Description
    -----------
    Forest fires are a natural or man-made phenomenon that destroys natural resources, 
    live livestock, unbalances the local environment, releases a large amount of greenhouse 
    gases, etc. The Normalized Burned Ratio Index (NBRI) takes advantage of the near-infrared 
    and shortwave infrared spectral bands, which are sensitive to changes in vegetation, 
    to detect burned areas and monitor ecosystem recovery ( GU, 2019 ).

    Formula
    -------
    (NIR - SWIR) / (NIR + SWIR)   \n
    Sentinel-2: (B8 - B12) / (B8 + B12)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the NBRI index.
    
    References
    --------
    https://www.geo.university/pages/blog?p=spectral-indices-with-multispectral-satellite-data

    '''

    b8 = dictionary["B08"] / np.amax(dictionary["B08"])
    b12 = dictionary["B12"] / np.amax(dictionary["B12"])
    index = (b8 - b12) / (b8 + b12)
    index = index / np.amax(index)
    return index[0]

def bsi(dictionary):
    '''
    Description
    -----------
    The Bare Soil Index (BSI) is a numerical indicator that combines blue, red, near 
    infrared, and shortwave infrared spectral bands to capture soil variations. These 
    spectral bands are used in a standardized manner. The shortwave infrared bands and 
    the red spectral bands are used to quantify the mineral composition of the soil, 
    while the blue bands and the near-infrared spectral bands are used to enhance the 
    presence of vegetation ( GU, 2019 ).

    Formula
    -------
    ((RED+SWIR) - (NIR+BLUE)) / ((RED+SWIR) + (NIR+BLUE))   \n
    Sentinel-2: (B11 + B4) - (B8 + B2) / (B11 + B4) + (B8 + B2)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the BSI index.
    
    References
    --------
    https://www.geo.university/pages/blog?p=spectral-indices-with-multispectral-satellite-data

    '''

    b2 = dictionary["B02"] / np.amax(dictionary["B02"])
    b4 = dictionary["B04"] / np.amax(dictionary["B04"])
    b8 = dictionary["B08"] / np.amax(dictionary["B08"])
    b11 = dictionary["B11"] / np.amax(dictionary["B11"])
    index = ((b11 + b4) - (b8 + b2)) / ((b11 + b4) + (b8 + b2))
    index = index / np.amax(index)
    return index[0]

def ndwi(dictionary):
    '''
    Description
    -----------
    The Normalized Differential Water Index (NDWI) is used for the analysis of water masses. 
    The index uses green and near-infrared bands from remotely sensed imagery. The NDWI can 
    improve water information efficiently in most cases. It is sensitive to land accumulation 
    and results in the overestimation of water bodies. NDWI products can be used in conjunction 
    with NDVI change products to assess the context of areas of apparent change ( Bahadur, 2018 ).

    Formula
    -------
    (GREEN - NIR) / (GREEN + NIR)   \n
    Sentinel-2: (B3 - B8) / (B3 + B8)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the NDWI index.
    
    References
    --------
    https://www.linkedin.com/pulse/ndvi-ndbi-ndwi-calculation-using-landsat-7-8-tek-bahadur-kshetri/

    '''

    b3 = dictionary["B03"] / np.amax(dictionary["B03"])
    b8 = dictionary["B08"] / np.amax(dictionary["B08"])
    index = (b3 - b8) / (b3 + b8)
    index = index / np.amax(index)
    return index[0]

def ndsi(dictionary):
    '''
    Description
    -----------
    The Normalized Differential Snow Index (NDSI) is a numerical indicator that shows snow 
    cover over land areas. The shortwave and green infrared (SWIR) spectral bands are used 
    within this formula to map snow cover. Since snow absorbs most of the incident radiation 
    in the SWIR while clouds do not, this allows NDSI to distinguish snow from clouds. This 
    formula is commonly used in snow and ice cover mapping applications, as well as glacier 
    monitoring ( Bluemarblegeo, 2019 ).

    Formula
    -------
    (GREEEN - SWIR) / (GREEEN + SWIR))   \n
    Sentinel-2: (B3 - B11) / (B3 + B11)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the NDSI index.
    
    References
    --------
    https://www.bluemarblegeo.com/knowledgebase/global-mapper-19/Raster_Calculator.htm

    '''
 
    b3 = dictionary["B03"] / np.amax(dictionary["B03"])
    b11 = dictionary["B11"] / np.amax(dictionary["B11"])
    index = (b3 - b11) / (b3 + b11)
    index = index / np.amax(index)
    return index[0]

def ndgi(dictionary):
    '''
    Description
    -----------
    The Normalized Differential Glacier Index (NDGI) is used to help detect and monitor 
    glaciers using the green and red spectral bands. This equation is commonly used in 
    glacier detection and glacier monitoring applications ( Bluemarblegeo, 2019 ).

    Formula
    -------
    (NIR - GEEN) / (NIR + GEEN)   \n
    Sentinel-2: (B3 - B4) / (B3 + B4)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the NDGI index.
    
    References
    --------
    https://www.bluemarblegeo.com/knowledgebase/global-mapper-19/Raster_Calculator.htm

    '''

    b3 = dictionary["B03"] / np.amax(dictionary["B03"])
    b4 = dictionary["B04"] / np.amax(dictionary["B04"])
    index = (b3 - b4) / (b3 + b4)
    index = index / np.amax(index)
    return index[0]

def arvi(dictionary):
    '''
    Description
    -----------
    As its name suggests, the Atmospherically Resistant Vegetation Index (ARVI) is the first 
    vegetation index, which is relatively prone to atmospheric factors (such as aerosol). 
    The ARVI index formula invented by Kaufman and Tanré is basically NDVI corrected for 
    atmospheric scattering effects in the red reflectance spectrum using the measurements at 
    blue wavelengths ( EOS, 2019 ).

    Formula
    -------
    (NIR - (2 * RED) + BLUE) / (NIR + (2 * RED) + Blue)   \n
    Sentinel-2: (B8 - (2 * B4) + B2) / (B8 + (2 * B4) + B2)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the ARVI index.
    
    References
    --------
    https://eos.com/blog/vegetation-indices/

    '''
 
    b2 = dictionary["B02"] / np.amax(dictionary["B02"]) # Blue
    b4 = dictionary["B04"] / np.amax(dictionary["B04"]) # Red
    b8 = dictionary["B08"] / np.amax(dictionary["B08"]) # NIR
    index = (b8 - (2 * b4) + b2) / (b8 + (2 * b4) + b2)
    index = index / np.amax(index)
    return index[0]

def sipi(dictionary):
    '''
    Description
    -----------
    The Structure Insensitive Pigmentation Index (SIPI) is good for the analysis of vegetation 
    with variable canopy structure. Estimate the relationship between carotenoids and chlorophyll: 
    the increase in the value of the signals of stressed vegetation ( EOS, 2019 ).

    Formula
    -------
    (NIR - BLUE) / (NIR - RED)   \n
    Sentinel-2: (B8 - B2) / (B8 - B4)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the SIPI index.
    
    References
    --------
    https://eos.com/blog/vegetation-indices/

    '''

    b2 = dictionary["B02"] / np.amax(dictionary["B02"]) # Blue
    b4 = dictionary["B04"] / np.amax(dictionary["B04"]) # Red
    b8 = dictionary["B08"] / np.amax(dictionary["B08"]) # NIR
    index = ((b8 - b2) / (b8 - b4)) * 1E+6
    index = index / np.amax(index)
    return index[0]

def bndi(dictionary):
    '''
    Description
    -----------
    The NDBI or Built-up Normalized Difference Index allows estimating areas with built-up 
    surfaces or under construction compared to the usual naturalized areas with vegetation 
    or bare. The NDBI index, together with others such as the NDVI index and the UI index, 
    are a way of territorial analysis in urban studies, infrastructures and the comparison 
    of the evolution of cities over time.

    Formula
    -------
    (SWIR - NIR)/ (SWIR + NIR)   \n
    Sentinel-2: (B11 - B8) / (B11 + B8)

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
        
    Returns      
    -------
    index: ndarray
        Array containing the values of the BNDI index.
    
    References
    --------
    http://www.gisandbeers.com/calculo-indice-ndbi-analisis-urbanisticos/

    '''

    b11 = dictionary["B11"] / np.amax(dictionary["B11"]) # SWIR
    b8 = dictionary["B08"] / np.amax(dictionary["B08"]) # NIR
    index = (b11 - b8) / (b11 + b8)
    index = index / np.amax(index)
    return index[0]