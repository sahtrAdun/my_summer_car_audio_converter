import os
import sys
import subprocess
import shutil
import zipfile
import tempfile
import urllib.request


def install_ffmpeg():
    print("[INFO] Checking for FFmpeg...")

    if ffmpeg_exists():
        print("[INFO] FFmpeg already installed.")
        ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
        ffmpeg_bin_dir = os.path.join(ffmpeg_dir, "bin")
        return ffmpeg_bin_dir

    print("[INFO] FFmpeg not found. Starting automatic installation...")

    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
    ffmpeg_bin_dir = os.path.join(ffmpeg_dir, "bin")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "ffmpeg.zip")

            print("[INFO] Downloading ffmpeg...")
            urllib.request.urlretrieve(ffmpeg_url, zip_path)

            print("[INFO] Unpacking ffmpeg...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            extracted_folder = None
            for folder in os.listdir(tmpdir):
                if folder.startswith("ffmpeg-") and os.path.isdir(os.path.join(tmpdir, folder)):
                    extracted_folder = os.path.join(tmpdir, folder)
                    break

            if not extracted_folder:
                raise Exception("Could not find the ffmpeg folder in the archive.")

            shutil.move(extracted_folder, ffmpeg_dir)

        if os.path.exists(ffmpeg_bin_dir):
            print("[INFO] FFmpeg installed successfully.")
            return ffmpeg_bin_dir
        else:
            raise Exception("Could not find ffmpeg after installation.")

    except Exception as e:
        print(f"[ERROR] Failed to install FFmpeg: {e}")
        return None


def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def ffmpeg_exists():
    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
    ffmpeg_bin_dir = os.path.join(ffmpeg_dir, "bin")
    ffmpeg_exe_path = os.path.join(ffmpeg_bin_dir, "ffmpeg.exe")
    return os.path.exists(ffmpeg_exe_path)

def setup_environment():
    if not check_ffmpeg():
        ffmpeg_bin_path = install_ffmpeg()
        if ffmpeg_bin_path:
            os.environ["PATH"] += os.pathsep + ffmpeg_bin_path
        else:
            print("[ERROR] FFmpeg is not installed. The program will not work correctly.")
            return False
    return True


# ============== MAIN ============== #
from pydub import AudioSegment

def convert_to_ogg(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
    audio.export(output_path, format="ogg")


def main():
    input_folder = "input"
    output_folder = "output"

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    print(f"[INFO] Found {len(files)} files in 'input' folder.")
    max_tracks = len(files)

    count = 0
    for filename in files:
        if count >= max_tracks:
            break

        input_path = os.path.join(input_folder, filename)
        output_name = f"track{count + 1}.ogg"
        output_path = os.path.join(output_folder, output_name)

        print(f"[{count + 1}] Converting {filename} to {output_name}")
        try:
            convert_to_ogg(input_path, output_path)
            count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"\nTotal tracks processed: {count}")


if __name__ == "__main__":
    if setup_environment():
        main()