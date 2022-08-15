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

# Load the arguments



# Setup the GPU
if args.GPU >= 0:
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.GPU)

def initialize_model(args):

    # Create the deep learning model
    model = ContextAwareModel(weights=args.load_weights, input_size=args.num_features, num_classes=dataset_Test.num_classes, chunk_size=args.chunk_size*args.framerate, dim_capsule=args.dim_capsule, receptive_field=args.receptive_field*args.framerate, num_detections=dataset_Test.num_detections, framerate=args.framerate)
    if not args.CPU:
        model = model.cuda()
    
    # Load the best model and compute its performance
    checkpoint = torch.load(os.path.join("models", args.model_name, "model.pth.tar"))
    model.load_state_dict(checkpoint['state_dict'])
    return model

def run_test(args, model):
    dataset_Test = SoccerNetClipsTesting(path=args.video_path, features=args.features, framerate=args.framerate, chunk_size=args.chunk_size*args.framerate, receptive_field=args.receptive_field*args.framerate)
    test_loader = torch.utils.data.DataLoader(dataset_Test,
        batch_size=1, shuffle=False,
        num_workers=1, pin_memory=True)
    return test(test_loader, model=model, model_name=args.model_name, save_predictions=Trueh, cpu = args.CPU)




