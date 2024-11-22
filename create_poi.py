# ##########################################################################################
# Hans Straßgütl
#       Pulls data from Openstreetmaps using the OverpassTurbo API.
#       Build Point of Interest in 2 KML formats: OruxMaps and OrganicMaps
#       
#       Uses a commandline paramater AND a JSON file. See readme-licence for details
#           
# ------------------------------------------------------------------------------------------
# Version:
#	2024 02 		Initial start of coding
#	2024 11 		Now includes: GPX, GPI, KML, KML for Organic Maps
#
# ##########################################################################################

import sys
import argparse
import ast  # Module for safely evaluating strings containing Python expressions
import requests
import shutil
import simplekml
import os
import subprocess
import xml.etree.ElementTree as ET

# ...................................................
# Where do I find my utils to be imported? Set your path here!
sys.path.append("C:\\SynologyDrive\\Python\\00_import_h_utils")
try:
    import h_utils                              # type: ignore
except Exception as e:
    print(f"Error importing utils: {e}")

# ------------------------------------------------------------------------------------------
#  _____ _ _          _                     _ _ _             
# |  ___(_) | ___    | |__   __ _ _ __   __| | (_)_ __   __ _ 
# | |_  | | |/ _ \   | '_ \ / _` | '_ \ / _` | | | '_ \ / _` |
# |  _| | | |  __/   | | | | (_| | | | | (_| | | | | | | (_| |
# |_|   |_|_|\___|___|_| |_|\__,_|_| |_|\__,_|_|_|_| |_|\__, |
#               |_____|                                 |___/ 
# ------------------------------------------------------------------------------------------
def mycopy_to_folder(c_path: str, root_path: str, items_in_scope: str, land: str , tag: str ) -> None:
    '''
    Create Folder depending on country and tag. 
    copy file from root to new folder
    '''
    lodging = ['hotel', 'motel', 'hostel', 'guest_house', 'apartment', 'camp_site', 'alpine_hut', 'caravan_site']
    if not os.path.exists(".\\"+root_path+"\\"): os.mkdir(".\\"+root_path+"\\")
    if not os.path.exists(".\\"+root_path+"\\"+items_in_scope): os.mkdir(".\\"+root_path+"\\"+items_in_scope)
    if not os.path.exists(".\\"+root_path+"\\"+items_in_scope+"\\"+land): os.mkdir(".\\"+root_path+"\\"+items_in_scope+"\\"+land)
    copypath = ".\\"+root_path+"\\"+items_in_scope+"\\"+land+"\\"
    if tag in lodging:
        copypath = copypath + "lodging"
        if not os.path.exists(copypath): os.mkdir(copypath)
        copypath = copypath + "\\"
    
    if tag.lower() == "motorcycle":
        copypath = copypath + "moto-dealer"
        if not os.path.exists(copypath): os.mkdir(copypath)
        copypath = copypath + "\\"
    
    copypath = copypath+c_path
    
    if os.path.isfile(copypath):                                # wenn die datei schon besteht, lösche sie weg 
        os.remove(copypath)                                     # !!! Remove remark after Test
    
    if os.path.exists(".\\"+ c_path): shutil.copy2(".\\"+ c_path , copypath)

# ------------------------------------------------------------------------------------------
#   ____      _       ___                                     
#  / ___| ___| |_    / _ \__   _____ _ __ _ __   __ _ ___ ___ 
# | |  _ / _ \ __|  | | | \ \ / / _ \ '__| '_ \ / _` / __/ __|
# | |_| |  __/ |_   | |_| |\ V /  __/ |  | |_) | (_| \__ \__ \
#  \____|\___|\__|___\___/  \_/ \___|_|  | .__/ \__,_|___/___/
#               |_____|                  |_|                  
# ------------------------------------------------------------------------------------------
'''
    Send Query to Overpass and download data
    Return JSON
'''
def download_data(query: str):
    overpass_url = "http://overpass-api.de/api/interpreter"
    # print(query)
    response = requests.get(overpass_url, params={"data": query})
    # print(response.json)
    return response.json()

# ------------------------------------------------------------------------------------------
#  _  ____  __ _         ___                        _      
# | |/ /  \/  | |       / _ \ _ __ __ _  __ _ _ __ (_) ___ 
# | ' /| |\/| | |      | | | | '__/ _` |/ _` | '_ \| |/ __|
# | . \| |  | | |___   | |_| | | | (_| | (_| | | | | | (__ 
# |_|\_\_|  |_|_____|___\___/|_|  \__, |\__,_|_| |_|_|\___|
#                  |_____|        |___/                    
# ------------------------------------------------------------------------------------------
def rework_kml_for_organic(kml_path, icon_color):
    kml_file_name, kml_tmp_file_name = h_utils.make_short_name(kml_path, 'kml')
    kml_tmp = open(kml_tmp_file_name, "w", encoding='utf-8')                # Open a Tempfile. Will be deleted later

    with open(kml_file_name, "r", encoding='utf-8') as kml_file:
        data = kml_file.readlines()                                         # read data line by line   
    
    # rework kml file as Textfile. remove all leading blanks and attach a new line command.
    for x in data:
        x = x.strip()
        x = x + '\n'
        kml_tmp.writelines(x)
    kml_tmp.close()
    kml_file.close()

    # Get the reworked file
    with open(kml_tmp_file_name, "r", encoding='utf-8') as kml_file:
        data = kml_file.readlines()                                         # read data line by line 
    kml_file.close()

    # Now delete the initial KML file and write out the new one into it
    kml_final = open(kml_file_name, "w", encoding='utf-8')
    is_placemark = False
    for x in data:
        kml_final.writelines(x)
        if x.find('<Placemark')  != -1 : is_placemark = True
        if x.find('</Placemark') != -1 : is_placemark = False
        if is_placemark :
            if x.find('<name>') != -1 :
                kml_final.writelines('<Snippet maxLines="0"/>\n')
                kml_final.writelines('<styleUrl>#' + icon_color + '</styleUrl>\n')
    kml_final.close()
    os.remove(kml_tmp_file_name)                                           

# ------------------------------------------------------------------------------------------
#  __  __       _       
# |  \/  | __ _(_)_ __  
# | |\/| |/ _` | | '_ \ 
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|
# ------------------------------------------------------------------------------------------
def main(args):
    # Check if the --dictionary argument is provided
    if args.dictionary is None:
        # args.dictionary = "{'key':'amenity', 'tag':'fuel', 'clear_name':'LPG_Gas_Station', 'icon':'gas-station.png' , 'icon_color':'placemark-bluegray', 'brand':'false', 'brand_name':'', 'second_key':'fuel:lpg', 'second_tag':'yes' }"
        # param_json = ast.literal_eval(args.dictionary)
        h_utils.error_message("dict_01", True)
        return
    try:
        # Convert the string representation of the dictionary to a dictionary
        param_json = ast.literal_eval(args.dictionary)
    except (SyntaxError, ValueError) as e:
        h_utils.error_message("dict_02", True)
    return param_json

if __name__ == "__main__":
    global json_file_name
    # ....................................................
    # Erhalte die Übergabeparameter. Erstelle dazu den 
    # default GPX Entry - sofern übergeben.
    # Ansonsten setze Default Pfad auf den Pfad der Exe
    # 
    #  Der Übergabe Paramater MUSS so aussehen: 
    # --dictionary "{'key':'tourism', 'tag':'alpine_hut', 'clear_name':'Alpine_Hut', 'icon':'Alpinehut.svg', 'icon_color':'placemark-brown','brand':'false', 'brand_name':'', 'second_key':'', 'second_tag':'' }"
    # ....................................................
    os.system('cls') 
    my_script = h_utils.IchSelbst()
    my_name = sys.argv[0]                       # the first argument is the script itself
    file_paths = sys.argv[1:]                   # the first argument (0) is the script itself. 1: heisst, wir haben nun in der file_paths alle anderen Argumente
    # ....................................................
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        print("\n\tOverpass_2_KML - Pull data from Overpass Turbo and convert it to a KML for OruxMaps\n\t\tVersion v2 dated 11/2024\n\t\tWritten by Hans Strassguetl - https://gravelmaps.de \n\t\tLicenced under https://creativecommons.org/licenses/by-sa/4.0/ \n\t\tIcons used are licensed under: Map Icons Collection - Creative Commons 3.0 BY-SA\n\t\tAuthor: Nicolas Mollet - https://mapicons.mapsmarker.com\n\t\tor https://creativecommons.org/publicdomain/zero/1.0/deed.en\n\n")
    # ....................................................
    # Lets get the dictionary passed via command line
    # ....................................................
    parser = argparse.ArgumentParser(description="Process a dictionary from the command line.")
    parser.add_argument("--dictionary", type=str, help="A string representation of a dictionary.\n\n Example: ""{'key1': 'value1', 'key2': 'value2'}"" ")
    args = parser.parse_args()
    param_json = main(args)

    if 'key' in param_json: key = param_json["key"] # type: ignore
    else: h_utils.error_message("dict_03", True)
    if 'tag' in param_json: tag = param_json["tag"] # type: ignore
    else: h_utils.error_message("dict_03", True)
    if 'clear_name' in param_json: clear_name = param_json["clear_name"]  # type: ignore
    else: h_utils.error_message("dict_03", True)
    if 'brand' in param_json: brand = param_json["brand"]  # type: ignore
    else: h_utils.error_message("dict_03", True)
    if brand.lower() == "true": 
        brand = True
    else:
        brand = False
    if 'brand_name' in param_json: brand_name = param_json["brand_name"]   # type: ignore
    else: h_utils.error_message("dict_03", True)
    
    garmin_icon = 'ATV'
    if 'garmin_icon' in param_json: garmin_icon = param_json["garmin_icon"]  # type: ignore
    else: h_utils.error_message("dict_03", True)

    if 'icon' in param_json: my_icon = param_json["icon"]  # type: ignore
    else: h_utils.error_message("dict_03", True)
    if 'icon_color' in param_json: icon_color = param_json["icon_color"]  # type: ignore
    else: h_utils.error_message("dict_03", True)
    second_key = ""
    if 'second_key' in param_json:   # type: ignore
        second_key = param_json["second_key"]   # type: ignore
        second_tag = ""
        if 'second_tag' in param_json: second_tag = param_json["second_tag"]   # type: ignore
        else: h_utils.error_message("dict_03", True)
    
    # ....................................................
    # Lets get the JSON
    # ....................................................
    json_file_name = my_script.path_name_without_suffix+".json"
    my_json = h_utils.load_json(json_file_name)

    if '7z_exe' in my_json: z_exe = my_json["7z_exe"]
    else: h_utils.error_message("dict_03", True)
    if not os.path.exists(z_exe): h_utils.error_message("7z_01", True)
    
    GPSBabel = ""
    if 'GPSBabel' in my_json: GPSBabel = my_json["GPSBabel"]
    else: h_utils.error_message("dict_03", True)
    if not os.path.exists(GPSBabel): h_utils.error_message("GPSBabel", True)

    if 'in_scope' in my_json: in_scope = my_json["in_scope"]
    else: h_utils.error_message("dict_03", True)
    print("Fetch \t\t: "+ clear_name)
    all_zip_files = ""
    all_zip_files_organic = ""
    all_zip_files_gpx = ""
    all_zip_files_gpi = ""
    for items_in_scope in in_scope:
        zip_kml_files = ""
        zip_kml_files_organic = ""
        zip_gpx_files = ""
        zip_gpi_files = ""
        my_countries = my_json["maps_geo"][items_in_scope]
        print("Working on \t: " + items_in_scope)
        for land in my_countries:
            count = 0
            if land in my_json["iso_code"]: iso =  my_json["iso_code"][land]
            else: h_utils.error_message("dict_04", True)
            # .......................................................................
            # Start of overpass query 
            # .......................................................................
            print("\tQuery\t: " + land.ljust(15," ") + " - " + iso)
            overpass_query = "[out:json][timeout:2400];\n// gather results\n"
            overpass_query = overpass_query+"area['ISO3166-1'='"+iso+"']->.a;\n(\n"
            if brand is False and second_key == "" :
                overpass_query = overpass_query + "node['"+key+"'='"+tag+"'](area.a);\n"
                overpass_query = overpass_query + "way['"+key+"'='"+tag+"'](area.a);\n"
                overpass_query = overpass_query + "relation['"+key+"'='"+tag+"'](area.a);\n"
            if brand == False and second_key != "" :
                overpass_query = overpass_query + "node['"+key+"'='"+tag+"'] ['"+second_key+"'='"+second_tag+"'](area.a);\n"
                overpass_query = overpass_query + "way['"+key+"'='"+tag+"'] ['"+second_key+"'='"+second_tag+"'](area.a);\n"
                overpass_query = overpass_query + "relation['"+key+"'='"+tag+"'] ['"+second_key+"'='"+second_tag+"'](area.a);\n"
            if brand == True:
                overpass_query = overpass_query + "node['"+key+"'='"+tag+"'] ['brand'~'.*"+brand_name+".*',i] (area.a);\n"
                overpass_query = overpass_query + "way['"+key+"'='"+tag+"'] ['brand'~'.*"+brand_name+".*',i] (area.a);\n"
                overpass_query = overpass_query + "relation['"+key+"'='"+tag+"'] ['brand'~'.*"+brand_name+".*',i] (area.a);\n"
            overpass_query = overpass_query+");\n// print results;\n// out body;\nout center;\n>;\nout skel qt;"
            # .......................................................................
            # End of overpass query 
            # .......................................................................
            # Perform the Overpass query and convert to GeoDataFrame
            data = download_data(overpass_query)

            # Collect coords into list
            coords = []
            for element in data['elements']:
                count += 1
                if element['type'] == 'node':
                    lon = element['lon']
                    lat = element['lat']
                elif 'center' in element:
                    lon = element['center']['lon']
                    lat = element['center']['lat']
                if 'tags' in element:
                    if 'opening_hours' in element['tags']:
                        descript = 'Opening Hours: ' + (element['tags']['opening_hours'])
                    else:
                        descript = ''

                    if 'name' in element['tags']:
                        name = (element['tags']['name'])
                    else:
                        name = "NoName"
                else:
                    name = "NoName"
                if name != "NoName":
                    new_waypoint = {"name": name, "description": descript, "lat": lat, "lon": lon}
                    coords.append(new_waypoint)
            
            # Some basic definitions
            kml_path            = clear_name+"-"+land+".kml"                            # type: ignore
            kml_path_organic    = clear_name+"-o-"+land+".kml"                          # type: ignore
            gpx_path            = clear_name+"-"+land+".gpx"                            # type: ignore
            gpi_path            = clear_name+"-"+land+".gpi"                            # type: ignore

            # Convert GeoDataFrame to GPX
            h_utils.create_gpx_with_symbols(coords, "tmp.gpx", garmin_icon )

            # Create a POI file
            if tag == "motorcycle":
                shutil.copy2("moto.bmp"       , "tmp.bmp") 
                if clear_name == "Motorcycle-Generic" :   shutil.copy2("moto.bmp"       , "tmp.bmp") 
                if clear_name == "BMW-Dealer"         :   shutil.copy2("BMW.bmp"        , "tmp.bmp")           
                if clear_name == "CFMoto-Dealer"      :   shutil.copy2("cfmoto.bmp"     , "tmp.bmp") 
                if clear_name == "Honda-Dealer"       :   shutil.copy2("honda.bmp"      , "tmp.bmp") 
                if clear_name == "Husqvarna-Dealer"   :   shutil.copy2("moto.bmp"       , "tmp.bmp") 
                if clear_name == "KTM-Dealer"         :   shutil.copy2("KTM.bmp"        , "tmp.bmp") 
                if clear_name == "Suzuki-Dealer"      :   shutil.copy2("moto.bmp"       , "tmp.bmp") 
                if clear_name == "Yamaha-Dealer"      :   shutil.copy2("Yamaha.bmp"     , "tmp.bmp") 
            if os.path.exists("tmp.bmp"): 
                rc = subprocess.run(GPSBabel + " -w -i gpx -f tmp.gpx -o garmin_gpi,bitmap=tmp.bmp,unique=1 -F Poi.gpi",  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)         # output is Poi.gpi in the same folder as we operate
                if os.path.exists("tmp.bmp"): os.remove("tmp.bmp")                                         
            else:
                rc = subprocess.run(GPSBabel + " -w -i gpx -f tmp.gpx -o garmin_gpi,unique=1 -F Poi.gpi",  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)         # output is Poi.gpi in the same folder as we operate        
            # ----------------------------------------------------------------
            # All for GPC and GPI here            
            # ----------------------------------------------------------------            
            # at this point there is a tmp.gpx and a Poi.gpi. 
            # Need to give it the right names now
            shutil.copy2("tmp.gpx"       , gpx_path) 
            shutil.copy2("Poi.gpi"       , gpi_path) 
            mycopy_to_folder(gpx_path, "GPX", items_in_scope , land, tag )              # copy the files into a folder hierarchy
            mycopy_to_folder(gpi_path, "GPI", items_in_scope , land, tag )              # copy the files into a folder hierarchy
            zip_gpx_files           = zip_gpx_files + gpx_path + " "                    # This is a list of names
            zip_gpi_files           = zip_gpi_files + gpi_path + " "                    # This is a list of names

            # ----------------------------------------------------------------            
            # All KML here
            # Convert GeoDataFrame to KML using simplekml
            # ----------------------------------------------------------------            
            kml = simplekml.Kml(name="<![CDATA["+clear_name+"-"+land+"]]>", visibility = "1" , open ="1", atomauthor = "Hans Straßgütl" , atomlink = "https://gravelmaps.de"  )  
            for element in coords:
                pt2 = kml.newpoint(name='<![CDATA[' + element["name"] + ']]>',coords=[(element["lon"], element["lat"])], description = element["description"])

            if count != 0: 
                kml.save(kml_path)                                                      # Now the standard KML is saved.
                shutil.copy2(kml_path, kml_path_organic)                                # Making sure that the standard KML isn't touched while reworking for Organic Maps

            mycopy_to_folder(kml_path, "POI", items_in_scope , land, tag )              # copy the files into a folder hierarchy
            zip_kml_files           = zip_kml_files + kml_path + " "                    # This is a list of names of KML Files that will be used by 7z later to create e.g. Gas_Station-germany.zip

            if count != 0: 
                rework_kml_for_organic(kml_path_organic, icon_color)                    # Now there should be 2 KML files 
                                                                                        # Standard: clear_name-land.kml (Gas_Station-germany.kml) 
                                                                                        # Organic Maps : clear_name-land_organic.kml (Gas_Station-germany_organic.kml) 
            mycopy_to_folder(kml_path_organic, "POI_organic", items_in_scope , land, tag )
            zip_kml_files_organic   = zip_kml_files_organic + kml_path_organic + " " 

        all_zip_files_gpx = all_zip_files_gpx + clear_name +"-gpx-"+items_in_scope + ".zip "  # a list of Zip file names that will be used to compress all of the zip files into one large e.g. Gas_Station-ALL.zip
        if zip_gpx_files != "": rc = subprocess.run(z_exe + "  a -mx7 -spe -sdel -tzip " + clear_name+"-gpx-"+items_in_scope + " " + zip_gpx_files ,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False) # type: ignore

        all_zip_files_gpi = all_zip_files_gpi + clear_name +"-gpi-"+items_in_scope + ".zip "  # a list of Zip file names that will be used to compress all of the zip files into one large e.g. Gas_Station-ALL.zip
        if zip_gpi_files != "": rc = subprocess.run(z_exe + "  a -mx7 -spe -sdel -tzip " + clear_name+"-gpi-"+items_in_scope + " " + zip_gpi_files ,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False) # type: ignore

        all_zip_files = all_zip_files + clear_name+"-"+items_in_scope + ".zip "         # a list of Zip file names that will be used to compress all of the zip files into one large e.g. Gas_Station-ALL.zip
        if zip_kml_files != "": rc = subprocess.run(z_exe + "  a -mx7 -spe -sdel -tzip " + clear_name+"-"+items_in_scope + " " + zip_kml_files ,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False) # type: ignore
        
        all_zip_files_organic = all_zip_files_organic + clear_name +"-o-"+items_in_scope + ".zip "  # a list of Zip file names that will be used to compress all of the zip files into one large e.g. Gas_Station-ALL.zip
        if zip_kml_files_organic != "": rc = subprocess.run(z_exe + "  a -mx7 -spe -sdel -tzip " + clear_name+"-o-"+items_in_scope + " " + zip_kml_files_organic ,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False) # type: ignore

    rc = subprocess.run(z_exe + "  a -mx7 -spe -sdel -tzip " + clear_name+"-ALL " + all_zip_files ,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)         # type: ignore
    if os.path.exists(clear_name+"-ALL.zip"):                                           # type: ignore
        shutil.copy2(clear_name + "-ALL.zip" , ".\\POI")                                # type: ignore
        os.remove(clear_name + "-ALL.zip")                                              # type: ignore

    rc = subprocess.run(z_exe + "  a -mx7 -spe -sdel -tzip " + clear_name+"-o-ALL " + all_zip_files_organic ,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False) # type: ignore
    if os.path.exists(clear_name+"-o-ALL.zip"):                                         # type: ignore
        shutil.copy2(clear_name + "-o-ALL.zip" , ".\\POI_organic")                      # type: ignore
        os.remove(clear_name + "-o-ALL.zip")                                            # type: ignore

    rc = subprocess.run(z_exe + "  a -mx7 -spe -sdel -tzip " + clear_name+"-gpx-ALL " + all_zip_files_gpx ,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False) # type: ignore
    if os.path.exists(clear_name+"-gpx-ALL.zip"):                                       # type: ignore
        shutil.copy2(clear_name + "-gpx-ALL.zip" , ".\\GPX")                            # type: ignore
        os.remove(clear_name + "-gpx-ALL.zip")                                          # type: ignore

    rc = subprocess.run(z_exe + "  a -mx7 -spe -sdel -tzip " + clear_name+"-gpi-ALL " + all_zip_files_gpi ,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False) # type: ignore
    if os.path.exists(clear_name+"-gpi-ALL.zip"):                                       # type: ignore
        shutil.copy2(clear_name + "-gpi-ALL.zip" , ".\\GPI")                            # type: ignore
        os.remove(clear_name + "-gpi-ALL.zip")                                          # type: ignore
    
    if os.path.exists("tmp.gpx"): os.remove("tmp.gpx")                                         
    if os.path.exists("Poi.gpi"): os.remove("Poi.gpi")                                         
    if os.path.exists("tmp.bmp"): os.remove("tmp.bmp")                                         

    print("Finished!")
