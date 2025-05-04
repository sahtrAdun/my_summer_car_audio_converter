# Audio Converter to OGG =RUS=

Программа для автоматической конвертации аудиофайлов из папки `input` в формат `.ogg` с параметрами:  
- Частота дискретизации: 44.1 кГц  
- Каналы: моно  
- Битность: 16 бит  

Имена выходных файлов генерируются как `track1.ogg`, `track2.ogg` и т.д.

---

## 🔧 Особенности

- ✅ Автоматическая установка FFmpeg (с прогресс-баром)
- ✅ Поддержка множества входных форматов (MP3, WAV, FLAC, M4A и др.)
- ✅ Очистка папки `output` при каждом запуске
- ✅ Возможность очистки папки `input` после обработки

## 📦 Использование через main.py

1. Убедитесь, что установлен Python 3.12 или выше.
2. Установите зависимости:
 ```bash
 pip install pydub tqdm
```
3. Запустите: python main.py


# Audio Converter to OGG =ENG=

This program automatically converts audio files from the input folder into .ogg format with the following parameters:   
 - Sample rate: 44.1 kHz
 - Channels: mono
 - Bit depth: 16 bit
  
Output file names are generated as track1.ogg, track2.ogg, etc. 

---

⚙️ Features 
 - ✅ Automatic FFmpeg installation (with progress bar)
 - ✅ Support for multiple input formats (MP3, WAV, FLAC, M4A, and more)
 - ✅ Clears the output folder on each run
 - ✅ Option to clear the input folder after conversion

## 📦 Usage via main.py

1. Make sure you have Python 3.12 or newer installed.
2. Install dependencies:
```bash
pip install pydub tqdm
```
3. Run: python main.py
