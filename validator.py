import os
import sys
import glob
from pathlib import Path


def get_root_dir() -> Path:
    if getattr(sys, "frozen", False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        print("Bundle detected!")
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent


def validate_installation() -> bool:
    root_dir = get_root_dir()

    tess_dir = root_dir / "deps" / "tessdata"
    adb_dir = root_dir / "deps" / "platform-tools"

    tessdata_present = False
    adb_present = False

    if os.path.exists(tess_dir):
        tessdata_present = True
        available_trainingdata = glob.glob(str(tess_dir / "*.traineddata"))
        if len(available_trainingdata) == 0:
            print("Tess dir found, but no training data is present")
            print(
                f"It is expected that you put the training files for tesseract in this folder: {tess_dir}"
            )
            tessdata_present = False
    else:
        print("Tess dir is missing")
        print(
            f"It is expected that you create the folder ({tess_dir}) and put the training files for tesseract in it."
        )
        tessdata_present = False

    if os.path.exists(adb_dir):
        adb_present = True
        if not os.path.isfile(adb_dir / "adb.exe"):
            print("Adb dir found, but adb.exe missing")
            print(
                f"It is expected that your adb.exe file is located in this folder: {adb_dir}"
            )
            adb_present = False
    else:
        print("Adb dir is missing")
        print(
            f"It is expected that you create the folder ({adb_dir}) and put extract the downloaded platform tools into it."
        )
        adb_present = False

    return tessdata_present and adb_present
