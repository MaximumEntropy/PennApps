from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import numpy as np
from sklearn.cluster import KMeans
import nltk
import subprocess
import os
import json
from app.models import *

# Create your views here.

# Content - Recorded notes
def listResultsView(request):
	query_results = DialogueBlock.objects.all()
	context = {'query_results': query_results}
	return render(request, 'app/index.html', context)

# Analytics
def speakerMax(request):
    #

def speakerLeast(request):
    #

def moreConfident(request):
    #

def meetingAgenda(request):
    #



def fbank_feature_extractor(wav_file_path):
    '''
    Extracts mfcc features for the wav file
    '''

    # Extracts mfcc features every 1/200th of a second.
    (rate, sig) = wav.read(wav_file_path)
    fbank_feat = logfbank(sig, rate)

    return fbank_feat


def mfcc_feature_extractor(wav_file_path):
    '''
    Extracts mfcc features for the wav file
    '''

    # Extracts mfcc features every 1/200th of a second.
    (rate, sig) = wav.read(wav_file_path)
    mfcc_feat = mfcc(sig, rate)

    return mfcc_feat


def speaker_identification(features, num_cluster=2):
    '''
    Clusters the mfcc features into a pre-set number of clusters
    '''

    RESOLUTION_SIZE = 200

    # Initialized and train GMM

    kmeans = KMeans(n_clusters=num_cluster)
    kmeans.fit(features)
    labels = kmeans.labels_
    speaker_labels = []
    prev_i = 0

    # Assign speaker labels
    for i in range(0, len(features), RESOLUTION_SIZE):
        labels_in_window = labels[prev_i:i]
        speaker_labels.append(sorted(nltk.FreqDist(labels_in_window).items(), key=lambda x:x[1], reverse=True)[0][0])
        prev_i = i

    del speaker_labels[0]  # Hack!

    for ind, speaker in enumerate(speaker_labels[5:]):
        prev_5 = sorted(nltk.FreqDist(speaker_labels[max(0, ind):ind + 5]).items(), key=lambda x:x[1], reverse=True)[0][0]
        next_5 = sorted(nltk.FreqDist(speaker_labels[ind + 5:ind + 10]).items(), key=lambda x:x[1], reverse=True)[0][0]
        if speaker != prev_5 and speaker != next_5:
            speaker_labels[ind + 5] = prev_5
    
    return speaker_labels[1:]


def get_asr_transcript(file_path):
    '''
    Get the asr transcripts from the IBM APIs
    '''

    file_path = '@' + file_path
    file_pointer = os.popen('curl -k -u 8ba36e4f-b5dd-45a7-8e67-8a59a5eca217:Dr2uog1CcnIv -X POST --limit-rate 40000 --header "Content-Type: audio/flac" --header "Transfer-Encoding: chunked" --data-binary ' +  file_path + ' "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?continuous=true&timestamps=true&max_alternatives=1"')
    contents = file_pointer.read()
    transcript = json.loads(contents)
    
    return transcript


def construct_speaker_dialogue_mapping(transcript, speaker_labels):
    '''
    Map text-blocks to speakers
    '''

    speaker_transcript_blocks = []

    speaker_labels = {ind: 'Speaker' + val for ind, val in enumerate(speaker_labels)}

    current_speaker = speaker_labels[0]
    current_transcript = ''
    current_timestamp = 0
    
    for result in transcript['results']:
        transcript = result['alternatives'][0]['transcript']
        timestamps = result['alternatives'][0]['timestamps']
        for timestamp in timestamps:
            if int(timestamp[1]) > current_timestamp:
                if speaker_labels[int(timestamp[1])] != current_speaker:
                    speaker_transcript_blocks.append([current_speaker, current_transcript])
                    current_speaker = speaker_labels[int(timestamp[1])]
                    current_transcript = timestamp[0]
                else:
                    current_transcript += " " + timestamp[0]

    return speaker_transcript_blocks


def get_trump_example(request):
    '''
    Get the donald trump video example
    '''
    wav_file_path = '/home/trump_megyn.wav'
    flac_file_path = '/home/trump_megyn.flac'
    mfcc_features = mfcc_feature_extractor(wav_file_path)
    speaker_labels = speaker_identification(mfcc_features, 2)
    asr_transcript = get_asr_transcript(flac_file_path)
    conversation_blocks = construct_speaker_dialogue_mapping(asr_transcript, speaker_labels)
    
