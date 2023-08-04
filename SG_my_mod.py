def set_frequency(f_0, f_1, step):
	global f, f0, f1, df
	df = step
	f0 = f_0
	f1 = f_1
	f = f_0 - step
	return f_0

def set_receiver_serial_number(sf_1, sf_2, sf_id):
	global serial_number
	if sf_id == 1:
		serial_number = sf_1
	elif sf_id == 2:
		serial_number = sf_2
	return serial_number

def set_filenames(full_path, aux_name, result_name):
	global filename, result_filename
	filename = full_path + aux_name
	result_filename = full_path + result_name	
	return "Done"

def sweeper(prob_lvl):
	global f, f1, df, f0

	read_receptor(f)
	if prob_lvl:
		f += df
	
	if f >= f1:
		f = f0
		
	return f
	
def read_receptor(f):
	global serial_number
	import os

	low_frequency = int(f/1e6) - 10
	high_frequency = int(f/1e6) + 10
	number_of_sweeps = 3

	file_name = "/home/diego/Downloads/hack_aut/hack_both/test.txt"
	command = f'hackrf_sweep -f {low_frequency}:{high_frequency} -N {number_of_sweeps} -d {serial_number} -r {file_name}' 

	os.system(command)

	margin = 3e6
	analyzer_file = open("/home/diego/Downloads/hack_aut/hack_both/test.txt", "r")
	results = analyzer_file.readlines()

	result_file = open("/home/diego/Downloads/hack_aut/hack_both/result.txt", "a")
	for line in results:
		line = line.split(', ')
		lf = int(line[2])
		df = int(float(line[4]))

		for i in range(5):
			result_file.write(str(lf + i*df) + ", " + str(float(line[6 + i])) + "\n")
























	
