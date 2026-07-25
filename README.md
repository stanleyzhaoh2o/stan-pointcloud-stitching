This is a project for two realsense camera stitching.
Refer to: https://github.com/realsenseai/librealsense/blob/master/doc/installation.md for the RealSense SDK installation.
1. rs-enumerate-devices, make sure there are two connected devices 
2. mkdir build && cd build
3. cmake ../ && make
4. cd ../
5. ./scripts/generate-configs.sh or python3 scripts/generate-configs.py
6. cp scripts/*.cfg build/Release/. && cd build/Release
7. ./stan-pointcloud-stitching $PWD calibration.cfg
