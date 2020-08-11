import os
from tqdm import tqdm
from utils.functional import flac2pcm

def preprocess(src_path, leave_trail):
    print("LibriSpeech dataset preprocessing initiated...")

    for speaker in tqdm(os.listdir(src_path)):
        if os.path.isdir(src_path + speaker):
            for sublevel in os.listdir(src_path + speaker):
                if os.path.isdir(src_path + speaker+ '/' + sublevel):
                    for file in os.listdir(src_path + speaker + '/' + sublevel):
                        if file.endswith('.trans.txt'):

                            # todo : split each sentence on trans.txt and make ground truth files

                            pass
                        if file.endswith('.flac'):
                            flac2pcm(src_path, file[:-5], leave_trail)


def create_labels(src_path, label_dest_path):
    print("Creating labels...")

    pass


def create_script(final_dest, script_name):
    print("Creating scripts...")

    pass


def collect(src_path, final_dest, script_name, collect_trail):
    print("Collecting preprocessed audio, ground truth, and script files...")

    pass