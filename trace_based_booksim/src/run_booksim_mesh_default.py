#!/usr/bin/python
# python run_booksim.py <directory to injection file>


import os, re, glob, sys, math
import numpy as np

# Extract command line arguments
trace_file_dir = sys.argv[1] #directory name

os.chdir(trace_file_dir)
#mesh_sizes_per_layer = pd.readcsv('mesh_sizes_per_layer.csv')
mesh_size = np.loadtxt('mesh_sizes.csv')
mesh_size = int(mesh_size[0])
num_packets_per_layer = np.loadtxt('num_packets_per_layer.csv')
os.chdir('..')

num_layers = len(num_packets_per_layer)

# Initialize dictionary to hold latency values
# latency_dict = dict()

# Get a list of all files in directory
files = glob.glob(trace_file_dir + '/*txt')

# Initialize file counter
file_counter = 0

# Create directory to store config files
os.system('mkdir -p ./logs/configs')

#latency = np.zeros(num_layers)
latency_outfile = open('./logs/latency_mesh_default.csv', 'a')

# Iterate over all files
for layer_idx in range(0, num_layers):
#for file in files :


    # Open read file handle of config file
    fp = open('./mesh_config_trace_based', 'r')

    # Set path to config file
    config_file = './logs/configs/layer_' + str(layer_idx) + '_mesh_config'

    # Open write file handle for config file
    outfile = open(config_file, 'w')

    # Iterate over file and set size of mesh in config file
    for line in fp :
        
        line = line.strip()
        
        # Search for pattern
        matchobj = re.match(r'^k=', line)

        # Set size of mesh if line in file corresponds to mesh size
        if matchobj :
            line = 'k=' + str(mesh_size) + ';'

        # Write config to file
        outfile.write(line + '\n')

    # Close file handles
    fp.close()
    outfile.close()

    # trace file
    file_name = 'trace_file_' + str(layer_idx) + '.txt'

    if (os.path.isfile(trace_file_dir + '/' + file_name)):
        
        # Copy trace file
        os.system('cp ' + trace_file_dir + '/' + file_name + ' ./trace_file.txt')

        # Set path to log file for trace files
        log_file = './logs/layer_' + str(layer_idx) + '.log'

        # Run Booksim with config file and save log
        booksim_command = './booksim ' + config_file + ' > ' + log_file
        os.system(booksim_command)

        # Grep for packet latency average from log file
        layer_latency = os.popen('grep "Trace is finished in" ' + log_file + ' | tail -1 | awk \'{print $5}\'').read().strip()

        #if (type(layer_latency) == str):
        #latency[layer_idx] = int(layer_latency)
        #outfile = open('./logs/latency_mesh_default.csv', 'w')
        latency_outfile.write(layer_latency + '\n')
        #outfile.close()
    
    else:
        layer_latency = num_packets_per_layer[layer_idx]
        latency_outfile.write(str(layer_latency) + '\n')
        #outfile.close()
        
    print('[ INFO] Latency: ' + str(layer_latency) +'\n')

latency_outfile.close()
#np.savetxt('logs/latency_mesh_default.csv', latency, fmt='%i', delimiter=' ')
