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

updateProject(sys.argv[n-1],'poisson_mesher','running')
subprocess.run('''colmap poisson_mesher \
    --input_path '''+DATASET_PATH+'''/dense/fused.ply \
    --output_path '''+DATASET_PATH+'''/dense/meshed-poisson.ply''',shell=True)
updateProject(sys.argv[n-1],'poisson_mesher','done')

updateProject(sys.argv[n-1],'delaunay_mesher','running')
subprocess.run('''colmap delaunay_mesher \
    --input_path '''+DATASET_PATH+'''/dense \
    --output_path '''+DATASET_PATH+'''/dense/meshed-delaunay.ply''',shell=True)
updateProject(sys.argv[n-1],'delaunay_mesher','done')


# subprocess.run('''colmap automatic_reconstructor --workspace_path ''' + DATASET_PATH + ''' --image_path '''+ DATASET_PATH + '''/images --use_gpu=0''')

