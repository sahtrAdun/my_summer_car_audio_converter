import os
import sys
import subprocess
import shutil
import zipfile
import tempfile
import urllib.request
from tqdm import tqdm

def download_progress_hook(count, block_size, total_size):
    tqdm.write(f"\rDownloading: {count * block_size / (1024 * 1024):.2f} MB of {total_size / (1024 * 1024):.2f} MB", end="")

def download_with_progress(url, output_path):
    print(f"[INFO] Starting download from {url}")
    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc="Downloading FFmpeg") as pbar:
        def reporthook(count, blocksize, totalsize):
            pbar.total = totalsize
            pbar.update(blocksize)

        urllib.request.urlretrieve(url, output_path, reporthook=reporthook)

def install_ffmpeg():
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

            download_with_progress(ffmpeg_url, zip_path)

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

    print(f"[INFO] Clearing '{output_folder}' folder...")
    for f in os.listdir(output_folder):
        file_path = os.path.join(output_folder, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print(f"[INFO] '{output_folder}' folder cleared.")

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

    try:
        response = input("All tracks have been converted. Do you want to clear the 'input' folder? [y/N]: ").strip().lower()
        if response in ('y', 'yes'):
            for f in os.listdir(input_folder):
                file_path = os.path.join(input_folder, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("[INFO] 'input' folder has been cleared.")
        else:
            print("[INFO] 'input' folder will not be cleared.")
    except Exception as e:
        print(f"[ERROR] Could not clear input folder: {e}")


if __name__ == "__main__":
    if setup_environment():
        main()