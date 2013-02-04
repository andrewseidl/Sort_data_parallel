#clang++ -O3 -std=c++11 -stdlib=libc++ utils.cpp parallel_sort_CPU.cpp -o clang_test
#g++ -O3 -std=c++0x utils.cpp parallel_sort_CPU.cpp -o gcc_463_test
g++ -O3 -std=c++11 utils.cpp parallel_sort_CPU.cpp -lpthread -o gcc_472_test

