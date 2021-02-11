#**************************************************************************************************************************************
#                                                           Consume Web Tool 
#**************************************************************************************************************************************


import arcpy
import config
import os
import sys
import time


arcpy.env.overwriteOutput = True
ws = arcpy.env.workspace = config.workspace

try:
    # Import toolbox
    arcpy.ImportToolbox('https://{0}/server/services;hotspotwebtool1;{1};{2}'.format(config.fedservername, config.username, config.password))
    
    # Run the tool and get output
    inputfc = os.path.join('HotSpotData.gdb', 'calls')
    result = arcpy.hotspotwebtool1.hotspotscript(calls = inputfc, rastersize = 'outRlayer1', esri_out_feature_service_name = config.outputFSName)
    
    while result.status != 4:
        time.sleep(0.2)    
        
    routput = result.getOutput(0)
    print("Consume web tool successfully. feature service = {} ".format(result))
except:
    print("Consume web tool error:", sys.exc_info()[0])  
