#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 11:29:01 2022

@author: trivizakis
"""
import os
import numpy as np
import pandas as pd
import SimpleITK as sitk
import pickle as pkl

def resample_volume(volume, interpolator = sitk.sitkLinear, new_spacing = [0.39, 0.39, 0.55]):
    # volume = sitk.ReadImage(volume_path, sitk.sitkFloat32) # read and cast to float32
    original_spacing = volume.GetSpacing()
    original_size = volume.GetSize()
    new_size = [int(round(osz*ospc/nspc)) for osz,ospc,nspc in zip(original_size, original_spacing, new_spacing)]
    return sitk.Resample(volume, new_size, sitk.Transform(), interpolator,
                         volume.GetOrigin(), new_spacing, volume.GetDirection(), 0,
                         volume.GetPixelID())

dataset_path = "/mnt/wwn-0x5000c500cc141236/manifest-1654812109500/Duke-Breast-Cancer-MRI/"
annotation_path = "dataset/"
bbxls = "Annotation_Boxes.xls"
clinicalxls = "Clinical_and_Other_Features.xls"

bounding_boxes = pd.read_excel(annotation_path+bbxls, index_col=0)
clinical_data = pd.read_excel(annotation_path+clinicalxls, index_col=0, header=0)

#pre-dwi
examinations_t1 = {}
for _,patients,_ in os.walk(dataset_path):
    for patient in patients:
        if "Breast_MRI" in patient:
            # print(patient)
            for root, examinations ,_ in os.walk(dataset_path+patient+"/"):
                index=0
                for examination in examinations:
                    if "t1" in examination:
                        examinations_t1[patient]=root+"/"+examination
                    elif "T1" in examination:
                        examinations_t1[patient]=root+"/"+examination
                    elif "pre" in examination:
                        examinations_t1[patient]=root+"/"+examination
                        
#first time point of dwi
examinations_dyn1 = {}
for _,patients,_ in os.walk(dataset_path):
    for patient in patients:
        if "Breast_MRI" in patient:
            # print(patient)
            for root, examinations ,_ in os.walk(dataset_path+patient+"/"):
                index=0
                for examination in examinations:
                    if "1st" in examination:
                        examinations_dyn1[patient]=root+"/"+examination
                    elif "Ph1" in examination:
                        examinations_dyn1[patient]=root+"/"+examination

pkl.dump(examinations_dyn1,open("dataset/examinations_dyn1.pkl","wb"))
                        
print("Didn't find:")
for pid in list(bounding_boxes.index):
    if not pid in list(examinations_dyn1.keys()):
        print(pid)
