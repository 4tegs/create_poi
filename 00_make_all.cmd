@echo off
@REM goto dealer
cls
@REM -----------------------------------------------------------
@REM  _              _       _             
@REM | |    ___   __| | __ _(_)_ __   __ _ 
@REM | |   / _ \ / _` |/ _` | | '_ \ / _` |
@REM | |__| (_) | (_| | (_| | | | | | (_| |
@REM |_____\___/ \__,_|\__, |_|_| |_|\__, |
@REM                    |___/         |___/ 
@REM -----------------------------------------------------------
:lodging
create_poi.exe --dictionary "{'key':'tourism', 'tag':'alpine_hut',    'clear_name':'Alpine_Hut',      'icon':'Alpinehut.svg',   'garmin_icon':'Lodge' ,  'icon_color':'placemark-brown',      'brand':'false', 'brand_name':'',        'second_key':'', 'second_tag':'' }"
create_poi.exe --dictionary "{'key':'tourism', 'tag':'apartment',     'clear_name':'Apartment',       'icon':'Apartment.svg',   'garmin_icon':'Lodging' ,  'icon_color':'placemark-teal',       'brand':'false', 'brand_name':'',        'second_key':'', 'second_tag':'' }"
create_poi.exe --dictionary "{'key':'tourism', 'tag':'camp_site',     'clear_name':'Camping',         'icon':'Camping-16.svg',  'garmin_icon':'Campground' ,  'icon_color':'placemark-purple',     'brand':'false', 'brand_name':'',        'second_key':'', 'second_tag':'' }"
create_poi.exe --dictionary "{'key':'tourism', 'tag':'caravan_site',  'clear_name':'Camper_Car_Site', 'icon':'Caravan-16.svg',  'garmin_icon':'RV Park' ,  'icon_color':'placemark-deeppurple', 'brand':'false', 'brand_name':'',        'second_key':'', 'second_tag':'' }"
create_poi.exe --dictionary "{'key':'tourism', 'tag':'guest_house',   'clear_name':'Guesthouse',      'icon':'guest_house.svg', 'garmin_icon':'Lodging' ,  'icon_color':'placemark-teal',       'brand':'false', 'brand_name':'',        'second_key':'', 'second_tag':'' }"
create_poi.exe --dictionary "{'key':'tourism', 'tag':'hostel',        'clear_name':'Hostel',          'icon':'Hostel-16.svg',   'garmin_icon':'Lodge' ,  'icon_color':'placemark-teal',       'brand':'false', 'brand_name':'',        'second_key':'', 'second_tag':'' }"
create_poi.exe --dictionary "{'key':'tourism', 'tag':'hotel',         'clear_name':'Hotel',           'icon':'Hotel-16.svg',    'garmin_icon':'Lodging' ,  'icon_color':'placemark-teal',       'brand':'false', 'brand_name':'',        'second_key':'', 'second_tag':'' }"
create_poi.exe --dictionary "{'key':'tourism', 'tag':'motel',         'clear_name':'Motel',           'icon':'Motel-16.svg',    'garmin_icon':'Lodging' ,  'icon_color':'placemark-teal',       'brand':'false', 'brand_name':'',        'second_key':'', 'second_tag':'' }"
@REM goto end
@REM -----------------------------------------------------------
@REM  _____           _ 
@REM |  ___|   _  ___| |
@REM | |_ | | | |/ _ \ |
@REM |  _|| |_| |  __/ |
@REM |_|   \__,_|\___|_|
@REM -----------------------------------------------------------
:fuel 
create_poi.exe --dictionary "{'key':'amenity', 'tag':'fuel',          'clear_name':'Gas_Station',     'icon':'Fuel.png', 		'garmin_icon':'Gas Station' ,  'icon_color':'placemark-bluegray',   'brand':'false', 'brand_name':'',       'second_key':'',            'second_tag':'' }"
create_poi.exe --dictionary "{'key':'amenity', 'tag':'fuel',          'clear_name':'LPG_Gas_Station', 'icon':'gas-station.png', 'garmin_icon':'Gas Station' ,  'icon_color':'placemark-pink',  		'brand':'false', 'brand_name':'',       'second_key':'fuel:lpg',    'second_tag':'yes' }"
    
@REM -----------------------------------------------------------
@REM  ____             _           
@REM |  _ \  ___  __ _| | ___ _ __ 
@REM | | | |/ _ \/ _` | |/ _ \ '__|
@REM | |_| |  __/ (_| | |  __/ |   
@REM |____/ \___|\__,_|_|\___|_| 
@REM -----------------------------------------------------------
@REM Make sure, all icon used here are bmp format 24*24 8 bit 256 color as, beside KML for Oruxmaps icons, these icons will be used to be displayed as Garmin POI icons
@REM True only for tag = motorcycle
@REM Use Motorcycle-Generic if you want to find any Motorcycle shops not related to a specific brand. Can be gear, helmets aso.
:dealer
create_poi.exe --dictionary "{'key':'shop', 'tag':'motorcycle',     'clear_name':'Motorcycle-Generic',  'icon':'bmp_4_oruxmaps/moto.bmp'        , 'garmin_icon':'ATV' ,  'icon_color':'placemark-orange',	'brand':'false','brand_name':'',            'second_key':'', 'second_tag':''}"
create_poi.exe --dictionary "{'key':'shop', 'tag':'motorcycle',     'clear_name':'BMW-Dealer',          'icon':'bmp_4_oruxmaps/BMW.bmp'         , 'garmin_icon':'ATV' ,  'icon_color':'placemark-orange',	'brand':'true', 'brand_name':'BMW',         'second_key':'', 'second_tag':''}"
create_poi.exe --dictionary "{'key':'shop', 'tag':'motorcycle',     'clear_name':'CFMoto-Dealer',       'icon':'bmp_4_oruxmaps/CFMOTO.bmp'      , 'garmin_icon':'ATV' ,  'icon_color':'placemark-orange',	'brand':'true', 'brand_name':'CFMOTO',      'second_key':'', 'second_tag':''}"
create_poi.exe --dictionary "{'key':'shop', 'tag':'motorcycle',     'clear_name':'GasGas-Dealer',       'icon':'bmp_4_oruxmaps/GasGas.bmp'      , 'garmin_icon':'ATV' ,  'icon_color':'placemark-orange',	'brand':'true', 'brand_name':'GasGas',      'second_key':'', 'second_tag':''}"
create_poi.exe --dictionary "{'key':'shop', 'tag':'motorcycle',     'clear_name':'Honda-Dealer',        'icon':'bmp_4_oruxmaps/Honda.bmp'       , 'garmin_icon':'ATV' ,  'icon_color':'placemark-orange',	'brand':'true', 'brand_name':'Honda',       'second_key':'', 'second_tag':''}"
create_poi.exe --dictionary "{'key':'shop', 'tag':'motorcycle',     'clear_name':'Husqvarna-Dealer',    'icon':'bmp_4_oruxmaps/Husqvarna.bmp'   , 'garmin_icon':'ATV' ,  'icon_color':'placemark-orange',	'brand':'true', 'brand_name':'Husqvarna',   'second_key':'', 'second_tag':''}"
create_poi.exe --dictionary "{'key':'shop', 'tag':'motorcycle',     'clear_name':'KTM-Dealer',          'icon':'bmp_4_oruxmaps/KTM.bmp'         , 'garmin_icon':'ATV' ,  'icon_color':'placemark-orange',	'brand':'true', 'brand_name':'KTM',         'second_key':'', 'second_tag':''}"
create_poi.exe --dictionary "{'key':'shop', 'tag':'motorcycle',     'clear_name':'Suzuki-Dealer',       'icon':'bmp_4_oruxmaps/Suzuki.bmp'      , 'garmin_icon':'ATV' ,  'icon_color':'placemark-orange',	'brand':'true', 'brand_name':'Suzuki',      'second_key':'', 'second_tag':''}"
create_poi.exe --dictionary "{'key':'shop', 'tag':'motorcycle',     'clear_name':'Yamaha-Dealer',       'icon':'bmp_4_oruxmaps/Yamaha.bmp'      , 'garmin_icon':'ATV' ,  'icon_color':'placemark-orange',	'brand':'true', 'brand_name':'Yamaha',      'second_key':'', 'second_tag':''}"
:end
@REM create_poi.exe --dictionary "{'key':'amenity', 'tag':'biergarten',  'clear_name':'Biergarten',          'icon':'beergarden.png', 'garmin_icon':'ATV' ,  'icon_color':'placemark-purple', 'brand':'false','brand_name':'',            'second_key':'', 'second_tag':''}"