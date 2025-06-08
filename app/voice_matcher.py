from scipy.spatial.distance import cosine
import numpy as np
from app.audio_utils import extract_mfcc
from sklearn.preprocessing import StandardScaler

def is_voice_match(file_path: str, stored_mfcc: np.ndarray, threshold: float = 0.09) -> bool:
    try:
        uploaded_mfcc = extract_mfcc(file_path)
        uploaded_vector = uploaded_mfcc[:10].flatten()
        stored_vector = stored_mfcc[:10].flatten()

        scaler = StandardScaler()
        uploaded_vector = scaler.fit_transform(uploaded_vector.reshape(-1, 1)).flatten()
        stored_vector = scaler.fit_transform(stored_vector.reshape(-1, 1)).flatten()

        distance = cosine(uploaded_vector, stored_vector)
        print(f"Cosine distance: {distance}")
        return bool(distance < threshold)
    except Exception as e:
        print(f"Error in voice match: {e}")
        return False
