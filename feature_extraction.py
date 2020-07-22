#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: winstonlin
"""
import os
import numpy as np
from scipy.io import savemat
import subprocess


def SmileExtract(input_path, out_path, feature_type, opensmile_root):
    ERROR_record = ''
    for dirPath, dirNames, fileNames in os.walk(input_path):
        fileNames = np.sort(fileNames)
        for i in range(len(fileNames)):
            if '.wav' in fileNames[i]:
                input_file = input_path + fileNames[i]
                output_file = out_path + fileNames[i].replace('.wav','.arff')
                if feature_type == 'eGeMAPS':
                    # eGeMAPS: LLDs
                    cmd = opensmile_root+'opensmile-2.3.0/SMILExtract -C '+opensmile_root+'opensmile-2.3.0/config_lld/eGeMAPSv01a.conf -I ' + input_file + ' -O ' + output_file
                elif feature_type == 'IS13ComParE':
                    # IS13ComParE: LLDs
                    cmd = opensmile_root+'opensmile-2.3.0/SMILExtract -C '+opensmile_root+'opensmile-2.3.0/config_lld/IS13_ComParE.conf -I ' + input_file + ' -O ' + output_file
                else:
                    raise ValueError('Unsupport Feature Type!')
                try:
                    subprocess.call(cmd, shell=True)
                except:
                    ERROR_record += 'Error: '+fileNames[i]+'\n'
            else:
                ERROR_record += 'Source not WAV file: ' +fileNames[i]+'\n'
    
    if feature_type == 'eGeMAPS':
        record_file = open("ErrorRecord_smile_eGeMAPS.txt","w") 
    elif feature_type == 'IS13ComParE':
        record_file = open("ErrorRecord_smile_IS13ComParE.txt","w")
    record_file.write(ERROR_record)
    record_file.close()
    
# parsing .arff file to .mat
def TryToFloat(single_data):
    try:
        return float(single_data)
    except:
        return None

def LoadFeature(filename):
    content = open(filename, 'r').read()
    data = content.split('@data\n')[1].split('\n')
    data = filter(None, data)
    feature = [[TryToFloat(data_split) for data_split in d.split(',') \
                if TryToFloat(data_split)!=None] for d in data]
    return feature

def ArfftoMat(input_path, out_path):
    ERROR_record = ''
    for dirPath, dirNames, fileNames in os.walk(input_path):
        fileNames = np.sort(fileNames)
        for i in range(len(fileNames)):
            if '.arff' in fileNames[i]:
                input_file = input_path + fileNames[i]
                output_file = out_path + fileNames[i].replace('.arff','.mat')
                try:
                    data = LoadFeature(input_file)
                    data = np.array(data)
                    savemat(output_file, {'Audio_data':data})
                except:
                    ERROR_record += 'Error: '+fileNames[i]+'\n'
            else:
                ERROR_record += 'Source not ARFF file: ' +fileNames[i]+'\n'
    print(ERROR_record)

###############################################################################
###############################################################################



if __name__=='__main__':
    """
    Args:
                     OpenSmile Root (str): installed opensmile-2.3.0 folder path 
                              Input (str): source folder path that contains .wav files
                   Default .wav file spec: [mono, 16k]
    Default LLDs window size and hop size: [32ms, 16ms] 
    (i.e., window size contains 512 sample points with 256 points (50%) overlaps 
           under 16k sampling rate wav file.)
    """
    # Parameters
    opensmile_root = '/media/winston/UTD-MSP/'
    input_audio_folder_path = './test_wav/'
    feature_type ='IS13ComParE'               # 'IS13ComParE' or 'eGeMAPS' are currently supported 
    
    # create output directory and folders
    os.mkdir(input_audio_folder_path.replace('wav',feature_type+'_llds'))
    os.mkdir(input_audio_folder_path.replace('wav',feature_type+'_llds')+'/feat_arff/')
    os.mkdir(input_audio_folder_path.replace('wav',feature_type+'_llds')+'/feat_mat/')
    
    ####################### Extracting LLDs ####################
    # Part 1: OpenSmile => Arff File
    output_arff_folder_path = input_audio_folder_path.replace('wav',feature_type+'_llds')+'/feat_arff/'
    SmileExtract(input_audio_folder_path, output_arff_folder_path, feature_type=feature_type, opensmile_root=opensmile_root)
    # Part 2: Arff File => Mat File
    output_mat_folder_path = output_arff_folder_path.replace('feat_arff','feat_mat')
    ArfftoMat(output_arff_folder_path, output_mat_folder_path)
    ############################################################

