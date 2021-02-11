#**************************************************************************************************************************************
#                                                           Hot Spots Analalysis
#**************************************************************************************************************************************


import arcpy
import os

arcpy.CheckOutExtension("spatial")

# Get inputput values
calls = arcpy.GetParameterAsText(0)
raster = arcpy.GetParameterAsText(1)
distance_method = arcpy.GetParameterAsText(2)


# Run CollectEvents
ce_outfc = os.path.join("in_memory","weighted_calls")
weightedcalls, result_field, z_max_value = arcpy.stats.CollectEvents(Input_Incident_Features = calls,
                                                    Output_Weighted_Point_Feature_Class = ce_outfc)

# Run HotSpots Analalysis
hotspot_outfc = os.path.join("in_memory","weighted_calls_hotspot")
arcpy.stats.HotSpots(Input_Feature_Class = weightedcalls,
                     Input_Field=result_field,
                     Output_Feature_Class = hotspot_outfc,
                     Conceptualization_of_Spatial_Relationships = "ZONE_OF_INDIFFERENCE",
                     Distance_Method = distance_method,
                     Standardization = "NONE",
                     Distance_Band_or_Threshold_Distance = 2960,
                     Self_Potential_Field = "",
                     Weights_Matrix_File = "",
                     Apply_False_Discovery_Rate__FDR__Correction = "NO_FDR",
                     number_of_neighbors = None)


# Run NaturalNeighbor Analysis
natual_neighbor = arcpy.sa.NaturalNeighbor(in_point_features = hotspot_outfc,
                         z_field="GiZScore",
                         cell_size = raster)

# Reclassify Raster
Hotspot_Raster = arcpy.sa.Reclassify(in_raster = natual_neighbor,
                                     reclass_field = "value",
                                     remap="""-100 -2.580000 -5;-2.580000 -1.960000 -4;
                                        -1.960000 -1.650000 -3;-1.650000 -1.300000 -2;
                                        -1.300000 -1 -1;-1 1 0;1 1.300000 1;1.300000 1.650000 2;
                                        1.650000 1.960000 3;1.960000 2.580000 4;2.580000 100 5""",
                                     missing_values="DATA")


# Convert Raster output to Feature
outputfeature = os.path.join("%scratchfolder%", "outputPolygon1.shp")
arcpy.RasterToPolygon_conversion(Hotspot_Raster, outputfeature,"SIMPLIFY")

outputpolygon = arcpy.SetParameterAsText(3, outputfeature)

