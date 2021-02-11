#**************************************************************************************************************************************
#                                                           Consume GP Service
#**************************************************************************************************************************************

import arcpy
import config
import os
import sys
import time


arcpy.env.overwriteOutput = True
ws = arcpy.env.workspace = config.workspace
hs_output = os.path.join(config.scratchworkspace, 'hotspotoutput')

try:
    # Import toolbox
    arcpy.ImportToolbox('https://{0}/server/services;hotspotgpservice2;{1};{2}'.format(config.standaloneserver, config.sausername, config.sapassword))
    
    # Run the tool and get the job ID
    inputCalls = arcpy.MakeFeatureLayer_management('https://{}/server/rest/services/Hosted/callsFS/FeatureServer/0'.format(config.fedservername))
    result = arcpy.hotspotgpservice2.hotspotscript(calls = inputCalls, rastersize = 'outRlayer1')
    
    while result.status != 4:
        time.sleep(0.2)
    
    # Save the result at disk space    
    routput = result.getOutput(0)
    arcpy.CopyFeatures_management(routput, hs_output)
    
    print("Consume gp service successfully. gp service = {} ".format(result))
except:
    print("Unexpected error during consuming web tool: ", sys.exc_info())
