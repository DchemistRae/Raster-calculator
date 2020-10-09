#====================================================================================#
#====================================================================================#
                     #Project 03: Raster Calculator 
                           #Group Members: 
                              #Raymond Asimhi
                              #Sara Doumi
                              #Marica Bazzanella
#====================================================================================#
#====================================================================================#


#Import libraries
import gdal
import numpy as np
import osr
from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *

#The Raster Calculator function
#Note!! No need to enter the inputs as a string. Just type the demanded and the script
#will convert it to string format automatically

input1 = input("Please enter the path of a Raster image (Format .tif) here: ")
input2 = input("Do you want to add another image? If yes,enter path;\
                   if not, enter 0: ")
expression = input("Please enter the operation to apply on the image here: ")

def RasterCalculator(input1,input2,expression,outPath=0):
    if input2 != '0':
        #Open datasets 
        img_data1 = gdal.Open(str(input1))
        img_data2 = gdal.Open(str(input2))
        print("\n The Projection of the first image is:\n ",
              img_data1.GetProjectionRef())
        print("\n The Projection of the second image is: \n ",
              img_data2.GetProjectionRef())
        print('\n In process! Please wait ......')
        band1= img_data1.RasterCount
        band2=img_data2.RasterCount
        band_img1 = img_data1.GetRasterBand(band1)
        band_img2 = img_data2.GetRasterBand(band2)
        gt= img_data1.GetGeoTransform()
        #Read the input data into a numpy array
        array_1 = band_img1.ReadAsArray()
        array_2 = band_img2.ReadAsArray()
        #Perform the calculations 
        try :
            if str(expression) == '+' :
                dataOut = array_1 + array_2
            elif str(expression) == '-':
                dataOut = array_1 - array_2
            elif str(expression) == '*': 
                dataOut = array_1 * array_2
            elif str(expression) == '/':
                dataOut = array_1 / array_2
            elif str(expression) == '**': 
                dataOut = array_1 ** array_2
            else:
                print("Invalid expression!")
        except ValueError as DimensionError:
            print("Oops! \n Images provided do not have the same dimensions. \
                      Please try again with compatible images.")
        outPath = input("Please enter a path to save your output here.\
                        The path should include a choosen name \
                        for the output and format (.tif): ")
        print('In process! Please wait ......')
        #Write out the final raster file
        driver = gdal.GetDriverByName("GTiff")
        outfile_data = driver.Create(str(outPath), img_data1.RasterXSize,
                                img_data1.RasterYSize,band1, band_img1.DataType)
        outfile_data.SetGeoTransform(gt)
        CopyDatasetInfo(img_data1,outfile_data)
        bandOut=outfile_data.GetRasterBand(band1)
        BandWriteArray(bandOut, dataOut)
        dsOutSRS= osr.SpatialReference()
        dsOutSRS.ImportFromWkt(img_data1.GetProjectionRef())
        dsOutSRS.SetProjection(dsOutSRS.ExportToWkt())
        #Close datasets
        band_img1 = None
        band_img2 = None
        img_data1 = None
        img_data2 = None
        bandOut = None
        outfile_data = None
        print("The process has finished, please check your output file.")
            #break
    else: 
        img_data1 = gdal.Open(str(input1))
        print("\n The Projection of the provided image is:\n" ,
                  img_data1.GetProjectionRef())
        print('\n In process! Please wait ......')
        #Read the data into numpy arrays
        band1=img_data1.RasterCount
        band_img1 = img_data1.GetRasterBand(band1)
        gt= img_data1.GetGeoTransform()
        array_1 = band_img1.ReadAsArray()
        #The actual calculation
        if str(expression) == 'cos':
            dataOut=np.cos((array_1))
        elif str(expression) == 'sin':
            dataOut = np.sin((array_1))
        elif str(expression)== 'tan':
            dataOut = np.tan((array_1))
        elif str(expression) == 'log':
            dataOut = np.log((array_1))
        elif str(expression) == 'log10':
            dataOut= np.log10((array_1))
        else:
            print("Invalid expression!")
        outPath = input("Please enter a path to save your output here.\
                        The path should include a choosen name \
                        for the output and format (.tif): ")
        print('In process! Please wait ......')
        driver = gdal.GetDriverByName("GTiff")
        outfile_data = driver.Create(str(outPath), img_data1.RasterXSize,
                                img_data1.RasterYSize,band1, band_img1.DataType)
        outfile_data.SetGeoTransform(gt)
        CopyDatasetInfo(img_data1,outfile_data)
        bandOut=outfile_data.GetRasterBand(band1)
        BandWriteArray(bandOut, dataOut)
        dsOutSRS= osr.SpatialReference()
        dsOutSRS.ImportFromWkt(img_data1.GetProjectionRef())
        dsOutSRS.SetProjection(dsOutSRS.ExportToWkt())
        band_img1 = None
        img_data1 = None
        bandOut = None
        outfile_data = None
        print("The process has finished, please check your output file.")

RasterCalculator(input1,input2,expression,outPath=0)
