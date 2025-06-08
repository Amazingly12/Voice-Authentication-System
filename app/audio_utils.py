import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import librosa
import numpy as np

def extract_mfcc(file_path: str, n_mfcc: int = 13) -> np.ndarray:
    y, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc.T
