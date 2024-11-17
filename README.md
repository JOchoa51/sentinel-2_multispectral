# Remote Sensing Image Processing Program

This project is a Python-based tool designed to process Sentinel-2 satellite imagery. It provides functionality for creating simple band compositions and calculating a variety of spectral indices, enabling detailed analysis of vegetation, water, soil, and geological features.

## Features

- **Simple Compositions**: Generate natural color, infrared, shortwave infrared, agriculture, geology, and bathymetric composites.
- **Spectral Indices**: Calculate indices such as NDVI, NDWI, NDMI, SAVI, and many others, using Sentinel-2 bands.
- **Customizable Outputs**: Save outputs with or without colorbars, and specify output paths.
- **Interactive Menu**: A simple terminal-based menu for choosing compositions and indices.

## Requirements

- Python 3.x
- Required Libraries:
  - `numpy`
  - `matplotlib`
  - `rasterio`

## Installation

1. Clone or download this repository.
2. Install the required libraries:
   $$$bash
   pip install numpy matplotlib rasterio
   $$$
3. Ensure your Sentinel-2 `.tif` images are placed in a specified folder.

## Usage

1. Run the program:
   $$$bash
   python main.py
   $$$
2. Follow the prompts:
   - Specify the path to the folder containing your `.tif` images.
   - Select a composition or spectral index from the menu.
   - Choose whether to save the output.

## Input Data Format

Input should consist of `.tif` files with Sentinel-2 band naming conventions (e.g., `B02`, `B04`, etc.). The program reads these files and performs necessary resampling for consistent resolutions.

## Outputs

- **Compositions**: RGB images representing different band combinations.
- **Indices**: Grayscale images representing calculated spectral indices.
- **File Saving**: Saved outputs include optional colorbars and are stored in the "Compositions" folder within the specified path.

## Example Workflow

1. **Start the Program**:
   $$$bash
   python main.py
   $$$
2. **Specify the Image Folder**:
   Provide the full path to the folder containing your Sentinel-2 `.tif` files.
3. **Choose an Option**:
   - For example, select "1" for a natural color composition.
4. **Save the Output**:
   Decide whether to save the composition or index with or without a colorbar.

## Supported Compositions and Indices

### Compositions:
- Natural Color (Bands 4, 3, 2)
- Infrared (Bands 8, 4, 3)
- Shortwave Infrared (Bands 12, 8A, 4)
- Agriculture (Bands 11, 8, 2)
- Geology (Bands 12, 11, 2)
- Bathymetric (Bands 4, 3, 1)

### Indices:
- NDVI: Normalized Difference Vegetation Index
- NDWI: Normalized Differential Water Index
- NDMI: Normalized Difference Moisture Index
- SAVI: Soil Adjusted Vegetation Index
- NDSI: Normalized Differential Snow Index
- And many more…

## Notes

- Ensure `.tif` files are named according to Sentinel-2 band conventions.
- Outputs are normalized for visualization.

## Contact

For questions or support, please contact:  
Jesús Ochoa Contreras  
ochoacontrerasjesus8@gmail.com
