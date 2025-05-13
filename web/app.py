
import streamlit as st
import os
import torch
from model import RandomFrameClassifier
from utils import extract_audio_tensor, extract_video_tensor_cv2
import tempfile
import yt_dlp
import traceback
from pathlib import Path

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@st.cache_resource
def load_model(checkpoint_path="checkpoint_epoch_5.pth"):
    st.write("📦 Загрузка модели...")
    model = RandomFrameClassifier(num_classes=4)
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()
    st.success("✅ Модель загружена!")
    return model

model = load_model()

st.title("🎬 Определение виральности трейлера по ссылке YouTube")

url = st.text_input("Введите ссылку на видео (YouTube):")

if url:
    with st.spinner("⬇️ Скачиваем видео..."):
        tempdir = tempfile.TemporaryDirectory()
        output_template = os.path.join(tempdir.name, "video.%(ext)s")

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'quiet': True,
            'noplaylist': True
        }

        try:
            st.write("🔗 Скачивание началось...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.download([url])

            # Ищем получившийся файл
            downloaded_files = list(Path(tempdir.name).glob("video.*"))
            if not downloaded_files:
                st.error("❌ Видео не было корректно загружено.")
                st.stop()

            final_video_path = str(downloaded_files[0])

            if os.path.getsize(final_video_path) < 100_000:
                st.error("❌ Видео слишком маленькое или повреждено.")
                st.stop()

            st.success("✅ Видео успешно скачано!")
            st.video(final_video_path)

            with st.spinner("📊 Анализируем..."):
                st.write("🖼️ Извлечение кадров...")
                video_tensor = extract_video_tensor_cv2(final_video_path).to(device)

                st.write("🔊 Извлечение аудио...")
                audio_tensor = extract_audio_tensor(final_video_path).to(device)

                st.write("🤖 Предсказание...")
                with torch.no_grad():
                    output = model(video_tensor, audio_tensor)
                    predicted_class = torch.argmax(output, dim=1).item() + 1

                st.success(f"🎯 Предсказанный уровень виральности: **{predicted_class}** (от 1 до 4)")
        except Exception as e:
            st.error("❌ Ошибка при обработке видео:")
            st.code(traceback.format_exc())
        finally:
            tempdir.cleanup()
