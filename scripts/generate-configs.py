#!/usr/bin/env python3

import re
import subprocess
import sys
from pathlib import Path


# Store generated files in the same directory as this script.
OUTPUT_DIR = Path(__file__).resolve().parent

CALIBRATION_FILE = OUTPUT_DIR / "calibration.cfg"
VIRTUAL_DEVICE_FILE = OUTPUT_DIR / "virtual_dev.cfg"


CAMERA_CONFIG_CONTENT = """DEPTH,640,480,30,Z16,0
COLOR,640,360,30,RGB8,0
#INFRARED,640,480,30,Y8,1
"""


VIRTUAL_DEVICE_CONTENT = """depth_width=960
depth_height=320
depth_fov_x=120
depth_fov_y=60

color_width=720
color_height=240
color_fov_x=120
color_fov_y=40
"""


def get_realsense_serial_numbers() -> list[str]:
    """Get RealSense device serial numbers, excluding ASIC serial numbers."""
    try:
        result = subprocess.run(
            ["rs-enumerate-devices"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print(
            "Error: rs-enumerate-devices was not found.",
            file=sys.stderr,
        )
        print(
            "Make sure the librealsense tools are installed and available in PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as error:
        print(
            "Error: rs-enumerate-devices failed.",
            file=sys.stderr,
        )

        if error.stderr:
            print(error.stderr, file=sys.stderr)

        sys.exit(1)

    serial_pattern = re.compile(
        r"^\s*Serial Number\s*:\s*(\S+)\s*$"
    )

    serial_numbers: list[str] = []

    for line in result.stdout.splitlines():
        match = serial_pattern.match(line)

        if match:
            serial_numbers.append(match.group(1))

    # Remove duplicates while preserving enumeration order.
    return list(dict.fromkeys(serial_numbers))


def create_camera_config_files(serial_numbers: list[str]) -> None:
    """Create one camera configuration file per serial number."""
    for serial_number in serial_numbers:
        config_file = OUTPUT_DIR / f"{serial_number}.cfg"

        config_file.write_text(
            CAMERA_CONFIG_CONTENT,
            encoding="utf-8",
        )

        print(f"Created {config_file.name}")


def create_calibration_file(
    camera_1: str,
    camera_2: str,
) -> None:
    """
    Create the camera calibration configuration.

    camera_1 is connected to virtual_dev.
    camera_2 is connected to camera_1.
    """
    calibration_content = (
        f"{camera_2}, {camera_1}, "
        "0.8660254, 0, -0.5, 0,1,0, "
        "0.5, 0., 0.8660254, 0,0,0\n"
        f"{camera_1}, virtual_dev, "
        "0.96592583, 0, 0.25881905, 0,1,0, "
        "-0.25881905, 0., 0.96592583, 0,0,0\n"
    )

    CALIBRATION_FILE.write_text(
        calibration_content,
        encoding="utf-8",
    )

    print(f"Created {CALIBRATION_FILE.name}")


def create_virtual_device_file() -> None:
    """Create the virtual device configuration file."""
    VIRTUAL_DEVICE_FILE.write_text(
        VIRTUAL_DEVICE_CONTENT,
        encoding="utf-8",
    )

    print(f"Created {VIRTUAL_DEVICE_FILE.name}")


def main() -> None:
    serial_numbers = get_realsense_serial_numbers()

    if len(serial_numbers) != 2:
        print(
            f"Error: expected 2 RealSense cameras, "
            f"but found {len(serial_numbers)}.",
            file=sys.stderr,
        )

        if serial_numbers:
            print(
                "Detected serial numbers:",
                file=sys.stderr,
            )

            for serial_number in serial_numbers:
                print(
                    f"  {serial_number}",
                    file=sys.stderr,
                )

        sys.exit(1)

    camera_1, camera_2 = serial_numbers

    print("Detected cameras:")
    print(f"  Camera 1: {camera_1}")
    print(f"  Camera 2: {camera_2}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    create_camera_config_files(serial_numbers)
    create_calibration_file(camera_1, camera_2)
    create_virtual_device_file()

    print()
    print("Configuration generation complete.")


if __name__ == "__main__":
    main()
