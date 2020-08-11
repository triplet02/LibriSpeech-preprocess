import argparse
from utils.functional import ParameterError
from utils.preprocess import preprocess, create_labels, create_script, collect

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LibriSpeech Dataset Preprocessor')
    parser.add_argument('--src_path', type=str, default="Check YOUR PATH for LibriSpeech Dataset\
                                                        ex) 'C:/LibriSpeech/train_clean_100/'")
    parser.add_argument('--final_dest', type=str, default="Set YOUR PATH for all preprocessed audio and script files")
    parser.add_argument('--label_dest_path', type=str, default="Set YOUR PATH to save labeled csv file")
    parser.add_argument('--script_name', type=str, default="Set script file name")
    parser.add_argument('--leave_trail', action='store_true', default=False,
                        help="Preprocessor will convert flac file to wav file first,\
                             then delete it and convert it to pcm file.\
                             If this option is used, preprocessor will not delete wav file.")
    parser.add_argument('--collect_trail', action='store_true', default=False,
                        help="If this option is used, preprocessor will collect wav files to 'final_dest'\
                             as like pcm files. If not, wav files will be remained at 'src_path.'\
                             Therefore, DO NOT use this option when 'leave_trail' option is False.")

    options = parser.parse_args()
    if options.leave_trail is False and options.collect_trail is True:
        raise ParameterError("'leave_trail' is False, but 'collect_trail' is True.\
                              To use 'collect_trail', set 'leave_trail' True first.")

    preprocess(options.src_path, options.leave_trail)
    create_labels(options.src_path, options.label_dest_path)
    create_script(options.label_dest_path, options.final_dest, options.script_name)
    collect(options.src_path, options.final_dest, options.script_name, options.collect_trail)