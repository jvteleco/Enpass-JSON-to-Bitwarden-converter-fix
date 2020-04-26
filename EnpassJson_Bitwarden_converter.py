# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------
# EnpassJson_Bitwarden_converter.py
# AUTHOR: JVTELECO
# v1.0 26/04/2020
#-----------------------------------------------------------------------

"""
This EnpassJson_Bitwarden_converter.py script allows to fix the hidden fields of 
the Bitwarden Json file after importing an Enpass JSON.
"""



import traceback
import json


EnpassFileName="Enpass_vault.json"
BitwardenFileName="Bitwarden_exported.json"

items_processed = 0
items_processed_changed = 0

print("Opening Enpass file")
with open(EnpassFileName, encoding="utf8") as f:
    json_data_enpass = json.load(f)
  
##print(json_data)  
#print(json.dumps(json_data_enpass, indent = 2))
##print(json.dumps(json_data, indent = 2, sort_keys=True))

print("Opening Bitwarden file")
with open(BitwardenFileName,encoding="utf8") as f_bt:
    json_data_bitwarden = json.load(f_bt)
  

  
fixed_file= open('Fixed_DELETE.txt', 'w')
  
##print(json_data)  
#print(json.dumps(json_data_bitwarden, indent = 2))
##print(json.dumps(json_data, indent = 2, sort_keys=True))




long_json_data_enpass_items = len(json_data_enpass["items"])
long_json_data_bitwarden_items = len(json_data_bitwarden["items"])
print("Enpass number items:", long_json_data_enpass_items )
print("Bitwarden number items:", long_json_data_bitwarden_items)

print("\n\n Starting comparison...\n\n")

for i in range(0, long_json_data_enpass_items):

    item_enpass = json_data_enpass["items"][i]
    item_enpass_title = item_enpass["title"]
#    print("\nENPASS:\t\t", item_enpass_title)
    
    for j in range(0, long_json_data_bitwarden_items):
        item_bitwarden = json_data_bitwarden["items"][j]
        item_bitwarden_name = item_bitwarden["name"]
        if item_enpass_title == item_bitwarden_name:
#            print("Bitwarden:\t", item_bitwarden_name)
            #Now check for sensitive items
            #print(json.dumps(item_enpass, indent = 2))
            #print(json.dumps(item_bitwarden, indent = 2))
            
            #we now only the items in the fields that are the custom fields
            try:
#            if (1):
                for k in range(0, len(item_bitwarden["fields"])):
                    field_bitwarden=item_bitwarden["fields"][k]
                    #print(field_bitwarden)
                    
                    
                    #we now check the name against the Enpass item
                    #when there is a match, need to check the sensitive value
                    #if it is '1', need to change the bitwarden item type to '1' so it is hidden
                    for m in range(0, len(item_enpass["fields"])):
                        field_enpass=item_enpass["fields"][m]
                        if field_bitwarden["name"] == field_enpass["label"]:
#                            print("MATCH")
#                            print(field_bitwarden)
#                            print(field_enpass)
                            #print(type(field_enpass["sensitive"]))
                            #print(type(field_bitwarden["type"]))
                            if field_enpass["sensitive"] == 1:
                                field_bitwarden["type"] = 1
                                items_processed_changed = items_processed_changed + 1
                                #print("CHANGED:\t", field_bitwarden)
                                fixed_file.write(str(item_bitwarden_name))
                                fixed_file.write("\t")
                                fixed_file.write(str(field_bitwarden))
                                fixed_file.write("\n")
                
                
                
                
                
                items_processed=items_processed+1
                #end clause of: if item_enpass_title == item_bitwarden_name:
            except Exception as e:
                #probably if a bitwarden does not have custom fields, will throw an exception of "fields" KeyError, does not exist
                ##print(e)
#                print("ERROR Bitwarden:\t", item_bitwarden_name)
#                print(traceback.format_exc())
                pass
                
                
print("\n\n Finised comparison.\n\n")



print("Enpass number items:", long_json_data_enpass_items )
print("Bitwarden number items:", long_json_data_bitwarden_items)
print("Number of items processed with custom fields", items_processed)
print("Number of fields fixed to hidden", items_processed_changed)




with open('Bitwarden_fixed.json', 'w') as json_file:
    json.dump(json_data_bitwarden, json_file, indent = 2)
  
  
fixed_file.close()
