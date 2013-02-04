# THIS CODE IS A SIMPLE HACK (A MESS) TO GET THE JOB DONE - USE WITH CARE

# Average the data sets and calculate the standard deviation for each set
# In order to run the script you will need Python 2.7.3, Numpy and Matplotlib

from pylab import *

def get_data(prefix, nr_tests):
	tmp = []

	for i in range(nr_tests):
		fname = "data/" + prefix + "_" + str(i) + ".txt"
		tmp.append(np.loadtxt(fname))

	data = np.mean(tmp, 0)
	std = np.std(tmp, 0)
	return(data, std)
	    
def gen_figure(cpu_data1, cpu_std1,cpu_data12, cpu_std12,nvcc_data, nvcc_std, fig_title,fig_name):
	figure(1)
	plot(cpu_data1[:,0],cpu_data1[:,1], color="blue", linewidth=2.5, label = "CPU 1 thread")
	plot(cpu_data12[:,0],cpu_data12[:,1], color="red", linewidth=2.5, label = "CPU 12 threads")
	plot(nvcc_data[:,0],nvcc_data[:,1], color="green", linewidth=2.5, label = "GPU")

	xlabel('Number of elements')
	ylabel('Time [ms]')
	title(fig_title)
	legend(loc='upper left')
	grid()

	errorbar(cpu_data1[:,0],cpu_data1[:,1], cpu_std1[:,1], color="blue")
	errorbar(cpu_data12[:,0],cpu_data12[:,1], cpu_std12[:,1], color="red")
	errorbar(nvcc_data[:,0],nvcc_data[:,1], nvcc_std[:,1], color="green")

	savefig(fig_name, dpi=72)

	close()

def gen_figure_norm(cpu_data1, cpu_data12, fig_title,fig_name):
	figure(1)
	plot(cpu_data1[:,0],cpu_data1[:,1], color="blue", linewidth=2.5, label = "CPU-1/GPU")
	plot(cpu_data12[:,0],cpu_data12[:,1], color="red", linewidth=2.5, label = "CPU-12/GPU")

	xlabel('Number of elements')
	ylabel('Speedup')
	title(fig_title)
	legend(loc='upper left')
	grid()

	savefig(fig_name, dpi=72)

	close()

def gen_figure_norm_cpu(cpu_data1, fig_title,fig_name):
	figure(1)
	plot(cpu_data1[:,0],cpu_data1[:,1], color="blue", linewidth=2.5, label = "CPU-1/CPU-12")

	xlabel('Number of elements')
	ylabel('Speedup')
	title(fig_title)
	legend(loc='upper left')
	grid()

	savefig(fig_name, dpi=72)

	close()

def gen_plot(gcc47_prefix1, gcc47_prefix12, nvcc_prefix,  nr_tests, descr):	
	gcc47_data1, gcc47_std1 = get_data(gcc47_prefix1, nr_tests)

	gcc47_data12, gcc47_std12 = get_data(gcc47_prefix12, nr_tests)
	
	nvcc_data, nvcc_std = get_data(nvcc_prefix, nr_tests)

	gen_figure(gcc47_data1, gcc47_std1,gcc47_data12, gcc47_std12,nvcc_data, nvcc_std, "GCC-4.7.2 CPU vs GPU", "GCC472_all.png")

	gcc47_norm1 = gcc47_data1
	gcc47_norm1[:,1] = gcc47_data1[:,1]/nvcc_data[:,1]

	gcc47_norm12 = gcc47_data12
	gcc47_norm12[:,1] = gcc47_data12[:,1]/nvcc_data[:,1]

	gen_figure_norm(gcc47_norm1, gcc47_norm12, "GCC-4.7.2 CPU normalized with GPU","GCC472_normalized.png")
	
	gcc47_norm1cpu = gcc47_data1
	gcc47_norm1cpu[:,1] = gcc47_data1[:,1]/gcc47_data12[:,1]
	
	gen_figure_norm_cpu(gcc47_norm1cpu, "GCC-4.7.2 CPU normalized","GCC472_normalized_cpu.png")
	
nr_tests = 20
gen_plot("gcc_472_data_1", "gcc_472_data_12", "nvcc_data", nr_tests, "")

