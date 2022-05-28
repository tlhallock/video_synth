# https://hub.docker.com/r/cwaffles/openpose
FROM nvidia/cuda:11.6.0-devel-ubuntu18.04

# get deps
RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
python3-dev python3-pip git g++ wget make libprotobuf-dev protobuf-compiler libopencv-dev \
libgoogle-glog-dev libboost-all-dev libcaffe-cuda-dev libhdf5-dev libatlas-base-dev libopenblas-dev
# libculbas9.1

RUN apt search blas

RUN pip3 install -U pip
RUN pip3 install -U setuptools

#for python api
RUN pip3 install numpy opencv-python

#replace cmake as old version has CUDA variable bugs (3.12.1 doesn't find CUA_cublas_device_LIBRARY)

# Maybe not needed anymore?
# RUN apt-get install -y cmake

RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.0/cmake-3.16.0-Linux-x86_64.tar.gz
RUN tar xzf cmake-3.16.0-Linux-x86_64.tar.gz -C /opt
# RUN rm cmake-3.16.0-Linux-x86_64.tar.gz
ENV PATH="/opt/cmake-3.16.0-Linux-x86_64/bin:${PATH}"


RUN export CUDNN_URL="http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/cudnn-8.0-linux-x64-v5.1.tgz" && \
  echo "wget -c ${CUDNN_URL} ${WGET_VERBOSE}" && \
  wget -c ${CUDNN_URL} ${WGET_VERBOSE} && \
  tar -xzf cudnn-8.0-linux-x64-v5.1.tgz -C /usr/local && \
  rm cudnn-8.0-linux-x64-v5.1.tgz && ldconfig

#get openpose
WORKDIR /openpose
RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git .

#build it
WORKDIR /openpose/build
# RUN sed -i 's/\# ---\[ BLAS/set\(BLAS \"Open\"\)/' $(find /openpose -name Dependencies.cmake)
# sed -i 's?\#\#\# OS-DEPENDENT FLAGS?set\(CUDA_cublas_device_LIBRARY \"/usr/local/cuda-11.6/targets/x86_64-linux/lib/libcublas.so\"\)?' ../CMakeLists.txt
RUN cmake -DBUILD_PYTHON=ON ..
RUN make -j `nproc`
RUN make install
WORKDIR /openpose

