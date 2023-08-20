import sys
import subprocess
import os
import json


def updateProject(name, attribute, value):
     with open('./projects/'+name+'/project.json') as jsonFile:
        data = json.load(jsonFile)

     data[attribute] = value

     with open('./projects/'+name+'/project.json', "w") as jsonFile:
        json.dump(data, jsonFile)

# total arguments
n = len(sys.argv)
DATASET_PATH = './projects/'+sys.argv[n-1]
os.chdir (os.getcwd())


subprocess.run('''colmap database_creator --database_path '''+DATASET_PATH+'''/database.db''',shell=True)

updateProject(sys.argv[n-1],'feature_extractor','running')
subprocess.run('''colmap feature_extractor \
   --database_path '''+DATASET_PATH+'''/database.db \
   --image_path '''+DATASET_PATH+'''/images''',shell=True)
updateProject(sys.argv[n-1],'feature_extractor','done')

updateProject(sys.argv[n-1],'exhaustive_matcher','running')
subprocess.run('''colmap exhaustive_matcher \
   --database_path '''+DATASET_PATH+'''/database.db''',shell=True)
updateProject(sys.argv[n-1],'exhaustive_matcher','done')


subprocess.run('''mkdir '''+DATASET_PATH+'''/sparse''',shell=True)

updateProject(sys.argv[n-1],'mapper','running')
subprocess.run('''colmap mapper \
    --database_path '''+DATASET_PATH+'''/database.db \
    --image_path '''+DATASET_PATH+'''/images \
    --output_path '''+DATASET_PATH+'''/sparse''',shell=True)
updateProject(sys.argv[n-1],'mapper','done')

subprocess.run('''mkdir '''+DATASET_PATH+'''/dense''',shell=True)

updateProject(sys.argv[n-1],'image_undistorter','running')
subprocess.run('''colmap image_undistorter \
    --image_path '''+DATASET_PATH+'''/images \
    --input_path '''+DATASET_PATH+'''/sparse/0 \
    --output_path '''+DATASET_PATH+'''/dense \
    --output_type COLMAP \
    --max_image_size 2000''',shell=True)
updateProject(sys.argv[n-1],'image_undistorter','done')


updateProject(sys.argv[n-1],'patch_match_stereo','running')
subprocess.run('''colmap patch_match_stereo \
    --workspace_path '''+DATASET_PATH+'''/dense \
    --workspace_format COLMAP \
    --PatchMatchStereo.geom_consistency true''',shell=True)
updateProject(sys.argv[n-1],'patch_match_stereo','done')


updateProject(sys.argv[n-1],'stereo_fusion','running')
subprocess.run('''colmap stereo_fusion \
    --workspace_path '''+DATASET_PATH+'''/dense \
    --workspace_format COLMAP \
    --input_type geometric \
    --output_path '''+DATASET_PATH+'''/dense/fused.ply''',shell=True)
updateProject(sys.argv[n-1],'stereo_fusion','done')


#convert to LAS
subprocess.run('''pdal translate '''+DATASET_PATH+'''/dense/fused.ply '''+DATASET_PATH+'''/dense/tmp.las''',shell=True)
#correct LAS
subprocess.run('''pdal translate '''+DATASET_PATH+'''/dense/tmp.las '''+DATASET_PATH+'''/dense/'''+sys.argv[n-1]+'''.las''',shell=True)


#generate potree page
subprocess.run('''./PotreeConverter_linux_x64/PotreeConverter '''+DATASET_PATH+'''/dense/'''+sys.argv[n-1]+'''.las -o ./htdocs/p --generate-page '''+sys.argv[n-1],shell=True)

## update potreeaddress
#open text file in read mode
text_file = open("./baseaddress", "r")
#read whole file to a string
data = text_file.read()
#close file
text_file.close()
potreeAddress = data+'/p/'+sys.argv[n-1]+'.html'
updateProject(sys.argv[n-1],'dense_pointcloud_address',potreeAddress)




updateProject(sys.argv[n-1],'poisson_mesher','running')
subprocess.run('''colmap poisson_mesher \
    --input_path '''+DATASET_PATH+'''/dense/fused.ply \
    --output_path '''+DATASET_PATH+'''/dense/'''+sys.argv[n-1]+'''.ply''',shell=True)
updateProject(sys.argv[n-1],'poisson_mesher','done')




#generate glb model in correct folder
subprocess.run('''python converter.py -it ply -et glb -if '''+DATASET_PATH+'''/dense/'''+sys.argv[n-1]+'''.ply -ef ./htdocs/models/''',shell=True)

#move las file to download folder
subprocess.run('mv '+DATASET_PATH+'/dense/'+sys.argv[n-1]+'.las ./htdocs/las/',shell=True)

poisson_mesh_address=data+'''/models/'''+sys.argv[n-1]+'.glb'
updateProject(sys.argv[n-1],'poisson_mesh_address',poisson_mesh_address)
updateProject(sys.argv[n-1],'delaunay_mesh_address',data)