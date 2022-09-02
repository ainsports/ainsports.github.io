import os
import logging
from datetime import datetime
import time
import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import torch

from dataset import SoccerNetClipsTesting
from model import ContextAwareModel
from train import test

# Fixing seeds for reproducibility
torch.manual_seed(0)
np.random.seed(0)

def initialize_model(args):
    # dataset_Test = SoccerNetClipsTesting(path=args.video_path, features=args.features, framerate=args.framerate, chunk_size=args.chunk_size*args.framerate, receptive_field=args.receptive_field*args.framerate)
    # Create the deep learning model
    model = ContextAwareModel(weights=args.load_weights, input_size=args.num_features, 
        num_classes=17, chunk_size=args.chunk_size*args.framerate, dim_capsule=args.dim_capsule, 
        receptive_field=args.receptive_field*args.framerate, 
        num_detections=15, framerate=args.framerate)
    if not args.CPU:
        model = model.cuda()
    
    # Load the best model and compute its performance
    if args.CPU:
        checkpoint = torch.load(os.path.join("models", args.model_name, "model.pth.tar"), map_location=torch.device('cpu'))
    else:
        checkpoint = torch.load(os.path.join("models", args.model_name, "model.pth.tar"))
    model.load_state_dict(checkpoint['state_dict'])
    return model

def run_test(args, model, video_path):
    dataset_Test = SoccerNetClipsTesting(path=video_path, features=args.features, 
        framerate=args.framerate, chunk_size=args.chunk_size*args.framerate, 
        receptive_field=args.receptive_field*args.framerate)
    test_loader = torch.utils.data.DataLoader(dataset_Test,
        batch_size=1, shuffle=False,
        num_workers=1, pin_memory=True)
    return test(test_loader, video_path, model=model, cpu = args.CPU)




