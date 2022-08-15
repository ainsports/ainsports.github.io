from flask import Flask, redirect, url_for, request
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from run import initialize_model, run_test
import os 

app = Flask(__name__)
parser = ArgumentParser(description='context aware loss function', formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument('--video_path',   required=False, type=str, default="video.mp4", help='Path to the video dataset folder' )
parser.add_argument('--features',   required=False, type=str,   default="ResNET_PCA512.npy",     help='Video features' )
parser.add_argument('--max_epochs',   required=False, type=int,   default=1000,     help='Maximum number of epochs' )
parser.add_argument('--load_weights',   required=False, type=str,   default=None,     help='weights to load' )
parser.add_argument('--model_name',   required=False, type=str,   default="CALF_benchmark",     help='named of the model to load' )
parser.add_argument('--test_only',   required=False, action='store_true',  help='Perform testing only' )
parser.add_argument('--challenge',   required=False, action='store_true',  help='Perform evaluations on the challenge set to produce json files' )

parser.add_argument('--num_features', required=False, type=int,   default=512,     help='Number of input features' )
parser.add_argument('--chunks_per_epoch', required=False, type=int,   default=18000,     help='Number of chunks per epoch' )
parser.add_argument('--evaluation_frequency', required=False, type=int,   default=20,     help='Number of chunks per epoch' )
parser.add_argument('--dim_capsule', required=False, type=int,   default=16,     help='Dimension of the capsule network' )
parser.add_argument('--framerate', required=False, type=int,   default=2,     help='Framerate of the input features' )
parser.add_argument('--chunk_size', required=False, type=int,   default=120,     help='Size of the chunk (in seconds)' )
parser.add_argument('--receptive_field', required=False, type=int,   default=40,     help='Temporal receptive field of the network (in seconds)' )
parser.add_argument("--lambda_coord", required=False, type=float, default=5.0, help="Weight of the coordinates of the event in the detection loss")
parser.add_argument("--lambda_noobj", required=False, type=float, default=0.5, help="Weight of the no object detection in the detection loss")
parser.add_argument("--loss_weight_segmentation", required=False, type=float, default=0.000367, help="Weight of the segmentation loss compared to the detection loss")
parser.add_argument("--loss_weight_detection", required=False, type=float, default=1.0, help="Weight of the detection loss")

parser.add_argument('--batch_size', required=False, type=int,   default=32,     help='Batch size' )
parser.add_argument('--LR',       required=False, type=float,   default=1e-03, help='Learning Rate' )
parser.add_argument('--patience', required=False, type=int,   default=25,     help='Patience before reducing LR (ReduceLROnPlateau)' )

parser.add_argument('--GPU',        required=False, type=int,   default=-1,     help='ID of the GPU to use' )
parser.add_argument('--max_num_worker',   required=False, type=int,   default=4, help='number of worker to load data')
parser.add_argument('--CPU',   required=False, action='store_true',  help='Run on CPU only' )
parser.add_argument('--loglevel',   required=False, type=str,   default='INFO', help='logging level')

args, unknown = parser.parse_known_args()
model = None 

@app.route('/recieve', methods = ['GET', 'POST'])
def recieve():
    if request.method == 'POST':
        f = request.files['file']
        f.save('video.mp4')
        
        json_data = run_test(args, model)
        return json_data

print('loadding model ...')
model = initialize_model(args) 
app.run(debug = True)