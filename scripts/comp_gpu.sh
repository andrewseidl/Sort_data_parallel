g++ -c -O3 -std=c++11 utils.cpp
nvcc -O3 -arch=sm_35 utils.o parallel_sort_GPU.cu -o nvcc_test

