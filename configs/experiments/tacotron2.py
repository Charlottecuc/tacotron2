from tacotron2.text import symbols
global symbols
import json
import numpy as np


class Config:
    # Audio params
    sampling_rate = 22050                        # Sampling rate
    filter_length = 1024                         # Filter length
    hop_length = 256                             # Hop (stride) length
    win_length = 1024                            # Window length
    mel_fmin = 0.0                               # Minimum mel frequency
    mel_fmax = 8000.0                            # Maximum mel frequency
    n_mel_channels = 80                          # Number of bins in mel-spectrograms
    max_wav_value = 32768.0                      # Maximum audiowave value

    ### Tacotron Params
    # Symbols
    n_symbols = len(symbols)                     # Number of symbols in dictionary
    symbols_embedding_dim = 512                  # Text input embedding dimension

    # Speakers
    n_speakers = 128                             # Number of speakers
    speakers_embedding_dim = 16                  # Speaker embedding dimension
    try:
        speaker_coefficients = json.load(open('train/speaker_coefficients.json'))  # Dict with speaker coefficients
    except IOError:
        print("Speaker coefficients dict is not available")
        speaker_coefficients = None

    # Emotions
    use_emotions = True                          # Use emotions
    n_emotions = 8                               # N emotions
    emotions_embedding_dim = 8                   # Emotion embedding dimension
    try:
        emotion_coefficients = json.load(open('train/emotion_coefficients.json'))  # Dict with emotion coefficients
    except IOError:
        print("Emotion coefficients dict is not available")
        emotion_coefficients = None

    # Encoder
    encoder_kernel_size = 5                      # Encoder kernel size
    encoder_n_convolutions = 3                   # Number of encoder convolutions
    encoder_embedding_dim = 512                  # Encoder embedding dimension

    # Attention
    attention_rnn_dim = 1024                     # Number of units in attention LSTM
    attention_dim = 128                          # Dimension of attention hidden representation

    # Attention location
    attention_location_n_filters = 32            # Number of filters for location-sensitive attention
    attention_location_kernel_size = 31          # Kernel size for location-sensitive attention

    # Decoder
    n_frames_per_step = 2                        # Number of frames processed per step
    decoder_rnn_dim = 1024                       # Number of units in decoder LSTM
    prenet_dim = 256                             # Number of ReLU units in prenet layers
    max_decoder_steps = 2000                     # Maximum number of output mel spectrograms
    gate_threshold = 0.5                         # Probability threshold for stop token
    p_attention_dropout = 0.1                    # Dropout probability for attention LSTM
    p_decoder_dropout = 0.1                      # Dropout probability for decoder LSTM
    decoder_no_early_stopping = False            # Stop decoding once all samples are finished

    # Postnet
    postnet_embedding_dim = 512                  # Postnet embedding dimension
    postnet_kernel_size = 5                      # Postnet kernel size
    postnet_n_convolutions = 5                   # Number of postnet convolutions

    # Optimization
    mask_padding = False                         # Use mask padding
    use_loss_coefficients = True                 # Use balancing coefficients
    # Loss scale for coefficients
    if emotion_coefficients is not None and speaker_coefficients is not None:
        loss_scale = 1.5 / (np.mean(list(speaker_coefficients.values())) * np.mean(list(emotion_coefficients.values())))
    else:
        loss_scale = None

    ### Waveglow params
    n_flows = 12                                 # Number of steps of flow
    n_group = 8                                  # Number of samples in a group processed by the steps of flow
    n_early_every = 4                            # Determines how often (i.e., after how many coupling layers) a number of channels (defined by --early-size parameter) are output to the loss function
    n_early_size = 2                             # Number of channels output to the loss function
    wg_sigma = 1.0                               # Standard deviation used for sampling from Gaussian
    segment_length = 4000                        # Segment length (audio samples) processed per iteration
    wn_config = dict(
        n_layers=8,                              # Number of layers in WN
        kernel_size=3,                           # Kernel size for dialted convolution in the affine coupling layer (WN)
        n_channels=512                           # Number of channels in WN
    )

    ### Audio postprocessing params
    snst = 0.00005                               # filter sensitivity
    wdth = 1000                                  # width of filter

    ### Script args
    model_name = "Tacotron2"
    output_directory = "logs"                    # Directory to save checkpoints
    log_file = "nvlog.json"                      # Filename for logging

    anneal_steps = [500, 1000, 1500]             # Epochs after which decrease learning rate
    anneal_factor = 0.1                          # Factor for annealing learning rate

    tacotron2_checkpoint = 'data/pretrained/t2_fp32_torch'    # Path to pre-trained Tacotron2 checkpoint for sample generation
    waveglow_checkpoint = 'data/pretrained/wg_fp32_torch'     # Path to pre-trained WaveGlow checkpoint for sample generation
    restore_from = ''                                         # Checkpoint path to restore from

    # Training params
    epochs = 300                                 # Number of total epochs to run
    epochs_per_checkpoint = 20                   # Number of epochs per checkpoint
    seed = 1234                                  # Seed for PyTorch random number generators
    dynamic_loss_scaling = True                  # Enable dynamic loss scaling
    amp_run = False                              # Enable AMP (FP16) # TODO: Make it work
    cudnn_enabled = True                         # Enable cudnn
    cudnn_benchmark = False                      # Run cudnn benchmark

    # Optimization params
    use_saved_learning_rate = False
    learning_rate = 1e-3                         # Learning rate
    weight_decay = 1e-6                          # Weight decay
    grad_clip_thresh = 1                         # Clip threshold for gradients
    batch_size = 64                              # Batch size per GPU

    # Dataset
    load_mel_from_dist = False                   # Loads mel spectrograms from disk instead of computing them on the fly
    text_cleaners = ['english_cleaners']         # Type of text cleaners for input text
    training_files = 'train/train.txt'           # Path to training filelist
    validation_files = 'train/val.txt'           # Path to validation filelist

    dist_url = 'tcp://localhost:23456'           # Url used to set up distributed training
    group_name = "group_name"                    # Distributed group name
    dist_backend = "nccl"                        # Distributed run backend

    # Sample phrases
    phrases = {
        'speaker_ids': [0, 1],
        'texts': [
            'Hello, how are you doing today?',
            'I would like to eat a Hamburger.',
            'Hi.',
            'I would like to eat a Hamburger. Would you like to join me?',
            'Do you have any hobbies?'
        ]
    }


class PreprocessingConfig:
    cpus = 42                                    # Amount of cpus for parallelization
    sr = 22050                                   # sampling ratio for audio processing
    top_db = 40                                  # level to trim audio
    limit_by = 'linda_johnson'                   # speaker to measure text_limit, dur_limit
    minimum_viable_dur = 0.05                    # min duration of audio
    text_limit = None                            # max text length (used by default)
    dur_limit = None                             # max audio duration (used by default)
    n = 300000                                   # max size of training dataset per speaker
    start_from_preprocessed = False               # load data.csv - should be in output_directory

    output_directory = 'train'
    data = [
        # {
        #     'path': 'data/raw-data/linda_johnson',
        #     'speaker_id': 0,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # }
        # {
        #     'path': 'data/raw-data/melissa',
        #     'speaker_id': 1,
        #     'metadata_file': 'metadata_8_emo.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/blizzard_2013',
        #     'speaker_id': 2,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/blizzard_2012',
        #     'speaker_id': 3,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        {
            'path': 'data/raw-data/degrasse',
            'speaker_id': 4,
            'metadata_file': 'metadata_e4.csv',
            'process_audio': True,
            'emotion_present': True
        },
        # {
        #     'path': 'data/raw-data/mcadams',
        #     'speaker_id': 5,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/scarjo_gcp',
        #     'speaker_id': 6,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/scarjo_her',
        #     'speaker_id': 7,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/scarjo_nikita',
        #     'speaker_id': 8,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/scarjo_the_dive_descript_grouped_50mil',
        #     'speaker_id': 9,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/scarjo_the_dive_descript_ungrouped',
        #     'speaker_id': 10,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/winslet',
        #     'speaker_id': 11,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/en_UK/by_book/female/elizabeth_klett/',
        #     'speaker_id': 12,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/en_US/by_book/female/judy_bieber/',
        #     'speaker_id': 13,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/en_US/by_book/female/mary_ann/',
        #     'speaker_id': 14,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
        # {
        #     'path': 'data/raw-data/en_US/by_book/male/elliot_miller/',
        #     'speaker_id': 15,
        #     'metadata_file': 'metadata_e4.csv',
        #     'process_audio': True,
        #     'emotion_present': True
        # },
    ]

    emo_id_map = {
        'sad': int(0),
        'happy': int(1),
        'angry': int(2),
        'fearful': int(3),
        'disgust': int(4),
        'surprised': int(5),
        'neutral': int(6),
        'calm': int(7)}
