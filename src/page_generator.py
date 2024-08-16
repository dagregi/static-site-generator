import os
import shutil


def copy_contents(from_dir, to_dir):
    def copy(fro, to):
        for item in os.listdir(fro):
            print(f"Copying: {fro}/{item} to {to_dir}/{item}")
            if os.path.isfile(f"{fro}/{item}"):
                shutil.copy(f"{fro}/{item}", to)
            else:
                os.mkdir(f"{to}/{item}")
                copy(f"{fro}/{item}", f"{to}/{item}")

    if not os.path.exists(to_dir):
        print(f"Creating {to_dir} directory")
        os.mkdir(to_dir)
    if os.path.getsize(to_dir) != 0:
        for item in os.listdir(to_dir):
            print(f"Removing: {to_dir}/{item}")
            if os.path.isfile(f"{to_dir}/{item}"):
                os.remove(f"{to_dir}/{item}")
            else:
                shutil.rmtree(f"{to_dir}/{item}")
    copy(from_dir, to_dir)
