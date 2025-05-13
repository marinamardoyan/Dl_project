
import cv2
from torchvision import transforms
from PIL import Image
import torch
import numpy as np
from pydub import AudioSegment

def extract_video_tensor_cv2(video_path, target_frames=16):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_count < 1:
        raise ValueError("Видео не содержит кадров или повреждено.")

    indices = np.linspace(0, frame_count - 1, num=target_frames).astype(int)

    transform = transforms.Compose([
        transforms.Resize((112, 112)),
        transforms.ToTensor()
    ])

    frames = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        tensor = transform(image)
        frames.append(tensor)

    cap.release()

    if len(frames) == 0:
        raise ValueError("Не удалось извлечь кадры из видео.")

    video_tensor = torch.stack(frames, dim=1)  # [C, T, H, W]
    return video_tensor.unsqueeze(0)  # [1, C, T, H, W]

def extract_audio_tensor(video_path):
    audio = AudioSegment.from_file(video_path).set_frame_rate(16000).set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
    return torch.tensor(samples).unsqueeze(0)  # [1, time]
