Инструкция по открытию приложения.

https://drive.google.com/drive/folders/1K60Sfuzm4ZqPfjt-tUPIKiCs5dLvpucw?usp=drive_link - ссылка на диск, где находится файл best_model.pth. Вам следует скачать содержимое папки web, а также файл best_model.pth. Все поместить в одну папку, открыть командную строку и задать путь до этой папки: cd 'Пользователь/../web'

Далее pip install -r requirements.txt, чтобы загрузить все библиотеки. Наконец, пропишите в командной строке "streamlit run app.py"

Примечание. Убедитесь, что у вас установлен ffmpeg.

Вот как это сделать:
Windows:
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
