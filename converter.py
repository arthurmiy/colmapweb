from sys import argv
from enum import Enum

import bpy
import bmesh
import glob
from pathlib import Path
from subprocess import call

"""
opinionated script to triangulate and convert meshes using Blender
to run: have Blender in path variables
replaces the paths in the variable below
and run Blender --background --python batch_mesh_converter.py -- -it <import_type> -et <export_type> -t (to_tringulate) -if <source_meshe_dir> -ef <export_dir>
can import:
dae, fbx, obj
can export:
obj, glb, fbx
"""

# PARSING FUNCTIONS

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


# BLENDER FUNCTIONS

def clearScene():
    # dont use this when running in blender it will also clear your script
    bpy.ops.wm.read_homefile(use_empty=True)


def triangulate_object(obj):
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)

    bmesh.ops.triangulate(bm, faces=bm.faces[:])

    bm.to_mesh(me)
    bm.free()

# IMPORT
def ply_import_mesh(filepath):
    bpy.ops.import_mesh.ply(
        filepath=str(Path(filepath).resolve()))
    

def dae_import_mesh(filepath):
    bpy.ops.wm.collada_import(
        filepath=str(Path(filepath).resolve()))


def obj_import_mesh(filepath):
    bpy.ops.import_scene.obj(
        filepath=str(Path(filepath).resolve()))


def fbx_import_mesh(filepath):
    bpy.ops.import_scene.fbx(
        filepath=str(Path(filepath).resolve()),
        axis_forward="-Z",
        axis_up="Y",)

# EXPORT

def obj_export_scene(filepath):
    bpy.ops.export_scene.obj(
        filepath=str(Path(filepath).resolve()) + ".obj",
        use_materials=True,
        axis_forward="-Z",
        axis_up="Y")


def glb_export_scene(filepath):
    bpy.ops.export_scene.gltf(export_format='GLB', export_colors=True, 
        export_yup=False, 
        filepath=str(Path(filepath).resolve()))


def fbx_export_scene(filepath):
    bpy.ops.export_scene.fbx(
        filepath=str(Path(filepath).resolve()) + ".fbx",
        mesh_smooth_type="FACE", # For Unreal FACE or EDGE otherwise leave out
        axis_forward="-Z",
        axis_up="Y")

# EXECUTION

class ImportFun(Enum):
    OBJ = {"suffix": "obj", "function": obj_import_mesh}
    FBX = {"suffix": "fbx", "function": fbx_import_mesh}
    DAE = {"suffix": "dae", "function": dae_import_mesh}
    PLY = {"suffix": "ply", "function": ply_import_mesh}


class ExportFun(Enum):
    OBJ = {"suffix": "obj", "function": obj_export_scene}
    FBX = {"suffix": "fbx", "function": fbx_export_scene}
    GLB = {"suffix": "glb", "function": glb_export_scene}
    GLTF = {"suffix": "gltf", "function": glb_export_scene}


def run(import_type, import_function, export_function, import_folder, export_folder, triangulate):
    for file in glob.glob(import_folder + f"/*.{import_type}"):
        clearScene()
        export_file = Path(export_folder).joinpath(Path(file).stem)
        import_function(file)
        
        for obj in bpy.data.objects:
            if obj.type == "MESH":
                # more function could be added here
                if triangulate:
                    triangulate_object(obj)
                
        export_function(export_file)


commands = parse_argv(argv)
missing_comm = check_commands(commands, ["it", "et", "if", "ef"])

if not missing_comm is None:
    print(f"-{missing_comm} flag is missing" )

else:
    # more functions could be added here
    traingulate = "t" in commands.keys()

    import_type = commands["it"]

    # get import function based on import type
    for modelFormat in list(ImportFun):
        if import_type == modelFormat.value["suffix"]:
            import_function = modelFormat.value["function"]

    # get export function based on export type
    export_type = commands["et"]

    for modelFormat in list(ExportFun):
        if export_type == modelFormat.value["suffix"]:
            export_function = modelFormat.value["function"]


    import_mesh_folder = str(Path(commands["if"]).resolve())
    export_mesh_folder = str(Path(commands["ef"]).resolve())
    
    run(import_type, import_function, export_function, import_mesh_folder, export_mesh_folder, traingulate)