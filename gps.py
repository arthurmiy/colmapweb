from pathlib import Path
import glob
##teste2
import os
from exif import Image
from sys import argv

def parse_argv(args):
    commands = {}
    for i, arg in enumerate(args):
        if "-" in arg:
            commands[arg[1:]] = args[i+1]
    return commands

def check_commands(commands, required_commands):
    for required_comm in required_commands:
        if not required_comm in commands.keys():
            return required_comm
    return None

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref =='W' :
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def image_coordinates(image_path):
    print(image_path)
    pathSplit = image_path.split('/')
    fileName = (pathSplit[len(pathSplit)-1])
    with open(image_path, 'rb') as src:
        img = Image(src)
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (decimal_coords(img.gps_latitude,
                      img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
            
        except AttributeError:
            print ('No Coordinates')
    else:
        print ('The Image has no EXIF information')
        
    return(fileName + " " + str(coords[0]) + " " + str(coords[1]) + " "+ str(img.gps_altitude))

def run(import_folder, save_file):
  files_list = (glob.glob(import_folder+ f"/*"))
  for file in files_list:
    try:
      tmp = image_coordinates(file)
      file1 = open(save_file, "a")  # append mode
      file1.write(tmp+"\n")
      file1.close()
    except ValueError:
      print('noexif')

##start
commands = parse_argv(argv)
missing_comm = check_commands(commands, ["i", "p"])

if not missing_comm is None:
    print(f"-{missing_comm} flag is missing" )

else:
    import_folder = str(Path(commands["i"]).resolve())
    save_path = str(Path(commands["p"]).resolve())
    save_file = save_path+"/gps.txt"
    f = open(save_file, "w")
    f.write("")
    f.close()
    run (import_folder, save_file)

    
# #     run(import_folder)

