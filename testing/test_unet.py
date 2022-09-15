import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import torch
from lib.modules.segmentation import *

h,w,d,c = 128,128,32,1

depths = [[16,32,64],[16,32,64,128]]
spatial_dims = [2,3]

def unet_base(D,sd,conv_type):
    K = [3 for _ in D]
    S = [2 for _ in D]
    if sd == 2:
        i = torch.rand(size=[1,c,h,w])
        output_size = [1,1,h,w]
    elif sd == 3:
        i = torch.rand(size=[1,c,h,w,d])
        output_size = [1,1,h,w,d]
    a = UNet(sd,depth=D,upscale_type="transpose",padding=1,
            strides=S,kernel_sizes=K,conv_type=conv_type)
    o,bb = a(i)
    assert list(o.shape) == output_size

def unet_skip(D,sd,conv_type):
    K = [3 for _ in D]
    S = [2 for _ in D]
    if sd == 2:
        i = torch.rand(size=[1,c,h,w])
        i_skip = torch.rand(size=[1,c,h,w])
        output_size = [1,1,h,w]
    elif sd == 3:
        i = torch.rand(size=[1,c,h,w,d])
        i_skip = torch.rand(size=[1,c,h,w,d])
        output_size = [1,1,h,w,d]
    a = UNet(sd,depth=D,upscale_type="transpose",padding=1,
            strides=S,kernel_sizes=K,skip_conditioning=1,
            link_type="conv",conv_type=conv_type)
    o,bb = a(i,X_skip_layer=i_skip)
    assert list(o.shape) == output_size

def unet_skip_feature(D,sd,conv_type):
    n_features = 4
    K = [3 for _ in D]
    S = [2 for _ in D]
    if sd == 2:
        i = torch.rand(size=[2,c,h,w])
        i_skip = torch.rand(size=[2,1,h,w])
        i_feat = torch.rand(size=[2,n_features])
        output_size = [2,1,h,w]
    elif sd == 3:
        i = torch.rand(size=[2,c,h,w,d])
        i_skip = torch.rand(size=[2,1,h,w,d])
        i_feat = torch.rand(size=[2,n_features])
        output_size = [2,1,h,w,d]
    a = UNet(sd,depth=D,upscale_type="transpose",padding=1,
            strides=S,kernel_sizes=K,feature_conditioning=n_features,
            skip_conditioning=1,
            feature_conditioning_params={
            "mean":torch.zeros_like(i_feat),
            "std":torch.ones_like(i_feat)},
            link_type="conv")
    o,bb = a(i,X_feature_conditioning=i_feat,X_skip_layer=i_skip)
    assert list(o.shape) == output_size

def test_unet_2d():
    for D in depths:
        for conv_type in ["regular","resnet"]:
            unet_base(D,2,conv_type)

def test_unet_3d():
    for D in depths:
        for conv_type in ["regular","resnet"]:
            unet_base(D,3,conv_type)

def test_unet_2d_skip():
    for D in depths:
        for conv_type in ["regular","resnet"]:
            unet_skip(D,2,conv_type)

def test_unet_3d_skip():
    for D in depths:
        for conv_type in ["regular","resnet"]:
            unet_skip(D,3,conv_type)

def test_unet_2d_skip_feature():
    for D in depths:
        for conv_type in ["regular","resnet"]:
            unet_skip_feature(D,2,conv_type)

def test_unet_3d_skip_feature():
    for D in depths:
        for conv_type in ["regular","resnet"]:
            unet_skip_feature(D,3,conv_type)