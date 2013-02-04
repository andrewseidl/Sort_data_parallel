#undef _GLIBCXX_ATOMIC_BUILTINS
#undef _GLIBCXX_USE_INT128

#include <iostream>
#include <vector>
#include <ctime>

#include <thrust/device_vector.h>
#include <thrust/sort.h>

#include "utils.h"


int main() {
    std::vector<double> V;
    thrust::device_vector<double> d_V;
    
    //use the system time to create a random seed
    unsigned int seed = (unsigned int) time(NULL);
    
    size_t step = 10;
    size_t mem = 10000000;

    for(size_t i = 16; i <= mem; i = 2 * step, step *= 1.1) {
	    cudaEvent_t start, stop, startcopy, stopcopy;
	    cudaEventCreate(&startcopy);
	    cudaEventCreate(&start);
	    cudaEventCreate(&stop);
	    cudaEventCreate(&stopcopy);

		//Fill V with random numbers in the range [0,1]:
        V.resize(i);
        rnd_fill(V, 0.0, 1.0, seed);
		cudaEventRecord(startcopy,0);
        d_V = V;

	    //Start recording
	    cudaEventRecord(start,0);
        
        thrust::stable_sort(d_V.begin(), d_V.end());
        
	    //Stop recording
	    cudaEventRecord(stop,0);

		//Copy data back to CPU
		thrust::copy(d_V.begin(), d_V.end(), V.begin());
		cudaEventRecord(stopcopy,0);

	    cudaEventSynchronize(stopcopy);
	    float inclusiveTime, exclusiveTime;
	    cudaEventElapsedTime(&exclusiveTime, start, stop);
	    cudaEventElapsedTime(&inclusiveTime, startcopy, stopcopy);

	    cudaEventDestroy(startcopy);
	    cudaEventDestroy(start);
	    cudaEventDestroy(stop);
	    cudaEventDestroy(stopcopy);

	    std::cout << i << "\t" << exclusiveTime << "\t" << inclusiveTime<< std::endl;
    }
    
    return 0;
}

