Инструкция по загрузке и отработке веб-приложения в стримлайте:

В гугл диске по этой ссылке  https://drive.google.com/drive/folders/1K60Sfuzm4ZqPfjt-tUPIKiCs5dLvpucw?usp=drive_link, можно найти файл model.pth. Его необходимо скачать вместе с другими файлами из папки web.
Все файлы нужно объединить в одну папку и запустить командную строку(для Windows) с запросом " cd 'путь к папке web'.
Затем нужно выполнить команду pip install -r requirements.txt.
И, наконец, streamlit run app.py

Убедитесь, что у вас скачан ffmpeg, иначе загрузка видео не совершиться.

Для Windows:
Скачайте FFmpeg с официального сайта (выберите Windows builds from gyan.dev).

Распакуйте архив в удобную папку (например, C:\ffmpeg).

Добавьте путь к FFmpeg в переменные среды PATH:

Откройте Параметры → Система → О системе → Дополнительные параметры системы → Переменные среды.

В разделе "Системные переменные" найдите Path, нажмите Изменить → Создать и добавьте путь к папке bin из распакованного FFmpeg (например, C:\ffmpeg\bin).

Сохраните и перезапустите терминал.

macOS (Homebrew):
brew install ffmpeg
Linux (Ubuntu/Debian):
sudo apt update && sudo apt install ffmpeg -y


