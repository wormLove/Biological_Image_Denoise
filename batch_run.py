import os
import subprocess
import argparse
from tqdm import tqdm

def batch_process(data_dir, action, output_dir):

    os.makedirs(output_dir, exist_ok=True)
    tif_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.tif')])

    if not tif_files:
        print("No .tif files found in the directory!")
        return

    for tif_file in tqdm(tif_files, desc="Processing Files", unit="file"):
        input_path = os.path.join(data_dir, tif_file)
        log_file = os.path.join(output_dir, f"{os.path.splitext(tif_file)[0]}.log")

        cmd = [
            "python", 
            "denoise.py",
            "--FilePath", input_path,
            "--Action", action,
            "--OutDir", output_dir
        ]

        with open(log_file, "w") as log:
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)

        print(f"✔ {tif_file} processed, log saved in {log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch run denoise pipeline")
    parser.add_argument("--DataDir", type=str, required=True, help="Directory containing .tif files")
    parser.add_argument("--Action", type=str, default="d", help="Processing type: s, d, or sd")
    parser.add_argument("--OutDir", type=str, required=True, help="Directory for output files")

    args = parser.parse_args()
    batch_process(args.DataDir, args.Action, args.OutDir)









