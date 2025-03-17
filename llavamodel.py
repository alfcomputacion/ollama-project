import ollama
import base64
import os
from PIL import Image
from PIL.ExifTags import TAGS
from geopy.geocoders import Nominatim

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# folder_path = './images'
folder_path = './test/Destroyed'
all_images = []


def getResponse():
    # Encode the image
    base64_image = encode_image(image_path)

    # Send request to Ollama
    response = ollama.chat(
        model="llava:latest",
        messages=[
            {
                'role': 'user',
                'content': 'tell me in 3 or four words if this structure is damaged, and how bad if it is? and what part of the building is damaged?',
                'images': [base64_image]
            }
        ]
    )

    # Print the response
    print(response['message']['content'])

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref =='W' :
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def convert_to_degrees(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format.

    Args:
        value (tuple): The GPS coordinate as a tuple (degrees, minutes, seconds)

    Returns:
        float: The coordinate in degrees
    """
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0) 

for root, _, files in os.walk(folder_path):
    for file in files:
        # Path to your image
        image_path = os.path.join(root, file)
        pic = Image.open(image_path)
        exifdata = pic.getexif()
        
        for tagid in exifdata:
            # getting the tag name instead of tag id
            tagname = TAGS.get(tagid, tagid)
        
            # passing the tagid to get its respective value
            value = exifdata.get(tagid)
        
            # printing the final result
            # print(f"{tagname:25}: {value}") 
        # print('For image: ', file)

        xif = {TAGS[k] : v
               for k, v in pic._getexif().items()
               if k in TAGS
               }
        # print(xif)
        if xif:
            try:
                north = xif['GPSInfo'][2]
                east = xif['GPSInfo'][4]

                
                # lat = (((north[0] * 60) + north[1]*60)+ north[2])/ 60 / 60
                # long = (((east[0] * 60) + east[1]*60)+ east[2])/ 60 / 60

                lat = convert_to_degrees(xif['GPSInfo'][2])
                long = convert_to_degrees(xif['GPSInfo'][4])

                # print('Latitude: ', float(lat))
                # print('Longitude: ', float(long))
                
                lat_ref = xif['GPSInfo'][1]
                lon_ref = xif['GPSInfo'][3]

                # Adjust the sign of the coordinates based on the reference (N/S, E/W)
                if lat_ref != "N":
                    lat = -lat
                if lon_ref != "E":
                    long = -long

                # Format the GPS coordinates into a human-readable string
                geo_coordinate = "{0}° {1}, {2}° {3}".format(lat, lat_ref, long, lon_ref)
                # print(geo_coordinate)

                # FOR ADDRESSES GEOPY
                # geolocator = Nominatim(user_agent="llavamodel")
                # location = geolocator.reverse(lat, long)
                # print(location)

                # Create a Google Maps link
                google_maps_link = f"https://www.google.com/maps?q={lat},{long}"
                print(f"Google Maps link: {google_maps_link}")
            except:
                print('no GPS info.')
        print('___________________________________________________________________________')      
        # img = Image.open(image_path)
        # img.show()
        getResponse()
        # print("este:::::",xif[0])

