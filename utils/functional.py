import soundfile as sf
import os
import pandas as pd


class ParameterError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class Wav2Pcm(object):
    """ Convert wav to pcm format """
    def __call__(self, src_path, file_name):
        sample_Rate, bit_rate, pcm_data = self.convert(src_path + file_name + '.wav')

        with open(src_path + file_name + '.pcm', 'wb') as pcm:
            pcm.write(pcm_data)

    def _get_field(self, wav, offset, lent):
        """
        Get values for filed. This is only working for fields with byteorder little
        Args :
          wav : the wave file
          offset : which position to start at.
          lent : length of field
        Return :
          Int of the desired field.
        """
        wav.seek(0)
        wav.seek(offset, 0)
        return int.from_bytes(wav.read(lent), byteorder='little')

    def convert(self, wav_in):
        """
        Get the sample rate, bit rate and PCM raw bytes from a wav.
        Args :
          wav_in : wave file, or string with path to wave file.
        Return :
          sample_rate : int representing the wave file sample rate
          bit_rate : int repesenting the wave file bit rate
          pcm : bytes representing the raw sound.
        """
        if type(wav_in) is str:
            wav_file = open(wav_in, 'rb')
        else:
            wav_file = wav_in
        header_size = self._get_field(wav_file, 16, 4)
        sample_rate = self._get_field(wav_file, 24, 4)
        bit_rate = self._get_field(wav_file, 34, 2)
        wav_file.seek(0)

        if header_size == 16:
            data = wav_file.read()[44:]

        elif header_size == 18:
            data = wav_file.read()[46:]

        else:
            print("WAV format unknown")
            exit(1)

        wav_file.close()
        return sample_rate, bit_rate, data


def load_label(filepath):
    char2id = dict()
    id2char = dict()
    ch_labels = pd.read_csv(filepath, encoding="cp949")
    id_list = ch_labels["id"]
    char_list = ch_labels["char"]
    freq_list = ch_labels["freq"]

    for (id_, char, freq) in zip(id_list, char_list, freq_list):
        char2id[char] = id_
        id2char[id_] = char
    return char2id, id2char


def flac2pcm(src_path, file_name, leave_trail):
    flac_data, sr = sf.read(src_path + file_name + '.flac')
    sf.write(src_path + file_name + '.wav', flac_data, sr, format='WAV', endian='LITTLE', subtype='PCM_16')

    wav2pcm = Wav2Pcm()
    wav2pcm(src_path, file_name)

    if not leave_trail:
        os.remove(src_path + file_name + '.wav')
