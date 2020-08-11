import os
import shutil
import pandas as pd
from tqdm import tqdm
from utils.functional import flac2pcm, load_label, sentence_to_label

def preprocess(src_path, leave_trail):
    print("LibriSpeech dataset preprocessing initiated...")

    for speaker in tqdm(os.listdir(src_path)):
        if os.path.isdir(src_path + speaker):
            for sub_level in os.listdir(src_path + speaker):
                if os.path.isdir(src_path + speaker + '/' +sub_level):
                    for file in os.listdir(src_path + speaker + '/' +sub_level):
                        if file.endswith('.trans.txt'):
                            with open(src_path + speaker + '/' + sub_level + '/' + file, 'r') as f:
                                while True:
                                    text = f.readline()
                                    if not text: break
                                    text_file, sentence = text.lower().replace('\n', '').split(' ', 1)
                                    with open(src_path + speaker + '/' + sub_level + '/' + text_file + '.txt', 'w') as t:
                                        t.write(sentence)

                        if file.endswith('.flac'):
                            flac2pcm(src_path + speaker + '/' + sub_level, file[:-5], leave_trail)


def create_labels(src_path, label_dest_path):
    print("Creating labels...")

    label_list = list()
    label_freq = list()

    for speaker in tqdm(os.listdir(src_path)):
        if os.path.isdir(src_path + speaker):
            for sub_level in os.listdir(src_path + speaker):
                if os.path.isdir(src_path + speaker + '/' + sub_level):
                    for file in os.listdir(src_path + speaker + '/' + sub_level):
                        if '.trans.txt' in file: continue
                        if file.endswith('.txt'):
                            with open(src_path + speaker + '/' + sub_level + '/' + file, "r") as f:
                                sentence = f.read()

                                for ch in sentence:
                                    if ch not in label_list:
                                        label_list.append(ch)
                                        label_freq.append(1)
                                    else:
                                        label_freq[label_list.index(ch)] += 1
                        else:
                            continue

    # sort together Using zip
    label_freq, label_list = zip(*sorted(zip(label_freq, label_list), reverse=True))
    label = {'id': [0, 1, 2], 'char': ['<pad>', '<sos>', '<eos>'], 'freq': [0, 0, 0]}

    for idx, (ch, freq) in enumerate(zip(label_list, label_freq)):
        label['id'].append(idx + 3)
        label['char'].append(ch)
        label['freq'].append(freq)

    # save to csv
    label_df = pd.DataFrame(label)
    label_df.to_csv(label_dest_path + "LibriSpeech_labels.csv", encoding="utf-8", index=False)


def create_script(label_dest_path, src_path, script_prefix):
    print("Creating scripts...")

    char2id, id2char = load_label(label_dest_path + 'LibriSpeech_labels.csv')

    for speaker in tqdm(os.listdir(src_path)):
        if os.path.isdir(src_path + speaker):
            for sub_level in os.listdir(src_path + speaker):
                if os.path.isdir(src_path + speaker + '/' + sub_level):
                    for file in os.listdir(src_path + speaker + '/' + sub_level):
                        if ".trans.txt" in file: continue
                        if file.endswith('.txt'):
                            sentence, labeled = None, None

                            with open(src_path + speaker + '/' + sub_level + '/' + file, "r") as f:
                                sentence = f.read()

                            with open(src_path + speaker + '/' + sub_level + '/' + script_prefix + file[:-4] + '.txt', "w") as f:
                                labeled = sentence_to_label(sentence, char2id)
                                f.write(labeled)


def collect(src_path, final_dest, collect_trail):
    print("Collecting preprocessed audio, ground truth, and script files...")

    for speaker in tqdm(os.listdir(src_path)):
        if os.path.isdir(src_path + speaker):
            for sub_level in os.listdir(src_path + speaker):
                if os.path.isdir(src_path + speaker + '/' + sub_level):
                    for file in os.listdir(src_path + speaker + '/' + sub_level):
                        if ".trans.txt" in file: continue
                        if file.endswith('.pcm') or file.endswith('.txt') or (file.endswith('.wav') and collect_trail):
                            shutil.move(src_path + speaker + '/' + sub_level + '/' + file, final_dest)
