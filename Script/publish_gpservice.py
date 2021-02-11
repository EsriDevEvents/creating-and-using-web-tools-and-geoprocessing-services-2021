#**************************************************************************************************************************************
#                                                           Publish GP Service
#**************************************************************************************************************************************



import arcpy
import os
import config
import sys

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

# Set workspace and scratch folder
ws = arcpy.env.workspace = config.workspace
sc = arcpy.env.scratchworkspace = config.scratchworkspace

# Set connection file
servername = config.standaloneserver
connectionFile = os.path.join(ws, r"Connection\{}.ags".format(servername))
    
# Set input and output data then run the script tool
try:
    intbx = 'hotspot.tbx'
    inputfc = os.path.join(ws, 'HotSpotData.gdb', 'calls')
    inputRaster = arcpy.management.MakeRasterLayer(os.path.join(ws,'stowe_elev.tif'), 'outRlayer1')
    distance_method = 'Manhattan'
    outputdata = os.path.join('Scratch', 'outputPolygon')

    arcpy.ImportToolbox(intbx)
    history_item = arcpy.hotspotscript_hotspot(inputfc, inputRaster, distance_method)
    print("Tool runs successfully")
except:
    print("Making layer or running tool error:", sys.exc_info()[0])   
    
    
# Add Data Store 
try:
    arcpy.AddDataStoreItem(connection_file = connectionFile, 
                           datastore_type = "FOLDER", 
                           connection_name = "HSRef", 
                           server_path = config.uncpath, 
                           client_path = ws)
    print("Add data store")
except:
    print("Adding data store error:", sys.exc_info()[0])      


# Publish a gp service
try:
    # Create a service definition draft
    draft_file = os.path.join(sc,'gpservice.sddraft')
    draft_file_return = arcpy.CreateGPSDDraft(result = history_item,
                                          out_sddraft = draft_file,
                                          service_name ='hotspotgpservice2',
                                          server_type = "ARCGIS_SERVER", 
                                          connection_file_path = connectionFile,
                                          copy_data_to_server = False,
                                          showMessages = "Info", 
                                          constantValues = ['hotspotscript.distancem'])
    print("Service Definition Draft is ready.")

    # Analyze the return from creating the service definition draft
    if (draft_file_return['errors']):
        print("error message = " + (draft_file_return['errors'] or 'None'))
    else:
        print("warning message = " + (draft_file_return['warnings'] or 'None'))
    
        # Stage the service
        definition_file = os.path.join(sc, 'gpservice1.sd')
        arcpy.StageService_server(draft_file, definition_file)
        print("Service staged.")

        # Upload service definition
        arcpy.UploadServiceDefinition_server(definition_file, connectionFile)
        print("Service published.")
except:
    print("Publishing error:", sys.exc_info()[0])    
    
try:
    arcpy.RemoveDataStoreItem(connection_file = connectionFile, 
                          datastore_type = "FOLDER", 
                          connection_name = "HSRef")    
    print("Remove data store")
except:
    print("Removing data store error:", sys.exc_info()[0])   