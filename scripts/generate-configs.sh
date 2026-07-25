#!/usr/bin/env bash

set -euo pipefail

OUTPUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CALIBRATION_FILE="${OUTPUT_DIR}/calibration.cfg"
VIRTUAL_DEVICE_FILE="${OUTPUT_DIR}/virtual_dev.cfg"

# Read only the normal device serial numbers.
# This excludes lines such as "ASIC Serial Number".
mapfile -t serials < <(
    rs-enumerate-devices |
    awk -F: '
        /^[[:space:]]*Serial Number[[:space:]]*:/ {
            serial = $2
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", serial)

            if (serial != "") {
                print serial
            }
        }
    ' |
    awk '!seen[$0]++'
)

if [[ ${#serials[@]} -ne 2 ]]; then
    echo "Error: expected exactly 2 RealSense cameras, but found ${#serials[@]}." >&2

    if [[ ${#serials[@]} -gt 0 ]]; then
        echo "Detected serial numbers:" >&2
        printf "  %s\n" "${serials[@]}" >&2
    fi

    exit 1
fi

CAMERA_1="${serials[0]}"
CAMERA_2="${serials[1]}"

echo "Found cameras:"
echo "  Camera 1: ${CAMERA_1}"
echo "  Camera 2: ${CAMERA_2}"
echo "Output directory: ${OUTPUT_DIR}"
echo

# Create one stream configuration file for each physical camera.
for camera in "$CAMERA_1" "$CAMERA_2"; do
    camera_config="${OUTPUT_DIR}/${camera}.cfg"

    cat > "$camera_config" <<'EOF'
DEPTH,640,480,30,Z16,0
COLOR,640,360,30,RGB8,0
#INFRARED,640,480,30,Y8,1
EOF

    echo "Created ${camera}.cfg"
done

# Create the calibration configuration using the detected camera order.
cat > "$CALIBRATION_FILE" <<EOF
${CAMERA_2}, ${CAMERA_1}, 0.8660254, 0, -0.5, 0,1,0, 0.5, 0., 0.8660254, 0,0,0
${CAMERA_1}, virtual_dev, 0.96592583, 0, 0.25881905, 0,1,0, -0.25881905, 0., 0.96592583, 0,0,0
EOF

echo "Created calibration.cfg"

# Create the virtual device configuration.
cat > "$VIRTUAL_DEVICE_FILE" <<'EOF'
depth_width=960
depth_height=320
depth_fov_x=120
depth_fov_y=60

color_width=720
color_height=240
color_fov_x=120
color_fov_y=40
EOF

echo "Created virtual_dev.cfg"

echo
echo "Configuration generation complete."
