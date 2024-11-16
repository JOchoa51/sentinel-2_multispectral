import matplotlib.pyplot as plt
import numpy as np

def create(array: any, title: str, save=False, path=None):
    '''
    Display the image in a matplotlib subplot.

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
    >>> simple.create(image, 'NDVI', cmap='viridis')
    '''

    plt.imshow(array)
    plt.title(title)
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    if save == True and path != None:
        plt.savefig(f"{path}\Compositions\{title}.png", dpi=400)
        display = input("Display image? (Y/N): ")
        if display == 'Y' or display == 'Y'.lower():
            plt.show()
    else: 
        plt.show()

def natural_color(dictionary, alpha=1.5):
    '''
    Description
    -----------
    The natural color band combination uses the red (B4), green (B3), and blue (B2) channels. 
    Its purpose is to display imagery the same way our eyes see the world. Just like how we 
    see, healthy vegetation is green. Next, urban features often appear white and grey. Finally, 
    water is a shade of dark blue depending on how clean it is.
    https://gisgeography.com/sentinel-2-bands-combinations/

    Formula
    -------
    RED, GREEN, BLUE    \n
    Sentinel-2: B4, B3, B2

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
    alpha: float, optional
        Parameter that changes the brightness of the image. Lower is darker, higher is brighter.
        Default is 1.5.
        
    Returns      
    -------
    rgb: ndarray
        Array containing the values of the natural color composite.
    
    References
    --------
    https://gisgeography.com/sentinel-2-bands-combinations/

    Examples
    --------

    '''
    
    rgb = np.stack([dictionary["B04"], dictionary["B03"], dictionary["B02"]], axis=-1)
    return rgb[0]*alpha

def infrared(dictionary, alpha=1.5):
    '''
    Description
    -----------
    The color infrared band combination is meant to emphasize healthy and unhealthy vegetation. 
    By using the near-infrared (B8) band, it's especially good at reflecting chlorophyll. 
    This is why in a color infrared image, denser vegetation is red. But urban areas are white.

    Formula
    -------
    NIR, RED, GREEN \n
    Sentinel-2: B8, B4, B3

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
    alpha: float, optional
        Parameter that changes the brightness of the image. Lower is darker, higher is brighter.
        Default is 1.5.
        
    Returns      
    -------
    ir: ndarray
        Array containing the values of the infrared composite.

    References
    ----------
    https://gisgeography.com/sentinel-2-bands-combinations/
    '''

    ir = np.stack([dictionary["B08"], dictionary["B04"], dictionary["B03"]], axis=-1)
    return ir[0]*alpha

def shortwave_ir(dictionary, alpha=1.5):
    '''
    Description
    -----------
    The short-wave infrared band combination uses SWIR (B12), NIR (B8A), and red (B4). 
    This composite shows vegetation in various shades of green. In general, darker shades 
    of green indicate denser vegetation. But brown is indicative of bare soil and built-up areas.

    Formula
    -------
    SWIR, NIR, RED \n
    Sentinel-2: B12, B8A, B4

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
    alpha: float, optional
        Parameter that changes the brightness of the image. Lower is darker, higher is brighter.
        Default is 1.5.
        
    Returns      
    -------
    ir: ndarray
        Array containing the values of the short-wave infrared composite.

    References
    ----------
    https://gisgeography.com/sentinel-2-bands-combinations/
    '''
    
    swir = np.stack([dictionary["B12"], dictionary["B8A"], dictionary["B04"]], axis=-1)
    return swir[0]*alpha

def agriculture(dictionary, alpha=1.5):
    '''
    Description
    -----------
    The agriculture band combination uses SWIR-1 (B11), near-infrared (B8), and blue (B2). 
    It's mostly used to monitor the health of crops because of how it uses short-wave and 
    near-infrared. Both these bands are particularly good at highlighting dense vegetation 
    that appears as dark green.

    Formula
    -------
    SWIR-1, NIR, BLUE \n
    Sentinel-2: B11, B8, B2

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
    alpha: float, optional
        Parameter that changes the brightness of the image. Lower is darker, higher is brighter.
        Default is 1.5.
        
    Returns      
    -------
    agr: ndarray
        Array containing the values of the agriculture composite.

    References
    ----------
    https://gisgeography.com/sentinel-2-bands-combinations/
    '''

    agr = np.stack([dictionary["B11"], dictionary["B08"], dictionary["B02"]], axis=-1)
    return agr[0]*alpha

def geology(dictionary, alpha=1.5):
    '''
    Description
    -----------
    The geology band combination is a neat application for finding geological features. 
    This includes faults, lithology, and geological formations. By leveraging the SWIR-2 (B12), 
    SWIR-1 (B11), and blue (B2) bands, geologists tend to use this Sentinel band combination 
    for their analysis.

    Formula
    -------
    SWIR-2, SWIR-1, BLUE \n
    Sentinel-2: B12, B11, B2

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
    alpha: float, optional
        Parameter that changes the brightness of the image. Lower is darker, higher is brighter.
        Default is 1.5.
        
    Returns      
    -------
    geo: ndarray
        Array containing the values of the geology composite.

    References
    ----------
    https://gisgeography.com/sentinel-2-bands-combinations/
    '''
    geo = np.stack([dictionary["B12"], dictionary["B11"], dictionary["B02"]], axis=-1)
    return geo[0]*alpha

def bathymetric(dictionary, alpha=1.5):
    '''
    Description
    -----------
    As the name implies, the bathymetric band combination is good for coastal studies. 
    The bathymetric band combination uses the red (B4), green (B3), and coastal band (B1). 
    Using the coastal aerosol band is good for estimating suspended sediment in the water.

    Parameters 
    ----------- 
    dictionary: dict
        Dictionary that contains the bands.
    alpha: float, optional
        Parameter that changes the brightness of the image. Lower is darker, higher is brighter.
        Default is 1.5.
    
    Formula
    -------
    RED, GREEN, COASTAL \n
    Sentinel-2: B4, B3, B1

    Returns      
    -------
    bath: ndarray
        Array containing the values of the bathymetric composite.
    '''
    
    bath = np.stack([dictionary["B04"], dictionary["B03"], dictionary["B01"]], axis=-1)
    return bath[0]*alpha
