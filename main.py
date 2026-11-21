"""The Passport Page of a Country That Isn't There — writes entry.png to /output."""

import os
import shutil


def main() -> None:
    os.makedirs("/output", exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    shutil.copyfile(src, "/output/entry.png")


if __name__ == "__main__":
    main()
