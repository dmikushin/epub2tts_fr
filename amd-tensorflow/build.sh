# Docker container for building ROCm TensorFlow from source.
# Based on: https://gist.github.com/briansp2020/1e8c3e5735087398ebfd9514f26a0007
set -e
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export PYTORCH_ROCM_ARCH="gfx1100"
export HIP_VISIBLE_DEVICES=0
export ROCM_PATH=/opt/rocm
export DEVICE_LIB_PATH=/opt/rocm/amdgcn/bitcode
export HIP_DEVICE_LIB_PATH=/opt/rocm/amdgcn/bitcode

# Build Tensorflow 2.14
cd /tensorflow
if [ ! -d tensorflow-upstream ]; then
    git clone --depth 1 -b r2.14-rocm-enhanced https://github.com/ROCmSoftwarePlatform/tensorflow-upstream.git
fi
cd tensorflow-upstream
#sed -i 's/5.7.0/5.7.1/g' build_rocm_python3
sed -i 's/"gfx1030" /"gfx1030",/g' tensorflow/compiler/xla/stream_executor/device_description.h
./build_rocm_python3
