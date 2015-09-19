import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.decomposition import PCA
import sys
import argparse
import subprocess
import os

def main():
    '''
        Converts data from a csv into a GIF of histograms of
        pairwise distances as dimensions are reduced
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--set_x_lim', type=int,\
        help='Set the maximum x value shown on the histograms')
    parser.add_argument('--set_y_lim', type=int,\
       help='Set the maximum y value shown on the histrogms')
    parser.add_argument('input_file',\
       help='Input file name. Must be a csv.')
    parser.add_argument('--ascending', action='store_true',\
        help='Final gif is in ascending order')
    parser.add_argument('--output_file_name', help='Set the output file name')
    parser.add_argument('--ignore_header', action='store_true',\
        help='Ignores the first row of the input file')
    parser.add_argument('--ignore_row_names', action='store_true',\
        help='Ignores the first column of the input file')
    parser.add_argument('--plot_name',\
        help='Set the name at the top of the plots')
    parser.add_argument('--dim_floor', type=int,\
        help='Set the lowest dimension the plot will go to')
    parser.add_argument('--dim_ciel', type=int,\
        help='Set the highest dimension the plot will go to')
    args = parser.parse_args()
    file_name = args.input_file
    file_in = open(file_name)
    if args.ignore_row_names:
        num_cols = len(file_in.readline().split(','))
        file_in.seek(0)
        if args.ignore_header:
            M_original = np.genfromtxt(file_in, usecols=range(2, num_cols),\
                delimiter=',', skip_header=1)
        else:
            M_original = np.genfromtxt(file_in, usecols=range(2, num_cols),\
                delimiter=',')
    else:
        if args.ignore_header:
            M_original = np.genfromtxt(file_in, delimiter=',', skip_header=1)
        else:
            M_original = np.genfromtxt(file_in, delimiter=',')
    dim = len(M_original[0])
    if args.set_x_lim == None or args.set_y_lim == None:
        y_lim, x_lim = 0, 0
        for i in {1, dim}:
            P = PCA(n_components=i)
            M_temp = np.copy(M_original)
            M_temp_reduced = P.fit_transform(M_temp)
            M_temp_reduced_dist_matrix = pairwise_distances(M_temp_reduced)
            M_temp_reduced_dist_list = M_temp_reduced_dist_matrix.flatten()
            if args.set_y_lim == None:
                y, _, _ = plt.hist(M_temp_reduced_dist_list,\
                    bins=100, color='b')
                y_lim = np.append(y, y_lim).max()
                plt.clf()
            else:
                y_lim = args.set_y_lim
            if args.set_x_lim == None:
                x_lim = M_temp_reduced_dist_list.max()
            else:
                x_lim = args.set_x_lim
    else:
       y_lim, x_lim = args.set_y_lim, args.set_x_lim 
    if args.output_file_name == None:
        out_file_name = file_name[:4] + '.gif'
    else:
        out_file_name = args.output_file_name
    if args.dim_floor == None:
        start_dim = 1
    else:
        start_dim = args.dim_floor
    if args.dim_ciel == None:
        end_dim = dim + 1
    else:
        end_dim = args.dim_ciel + 1
    if args.plot_name == None:
        plot_name = file_name[:-4]
    else:
        plot_name = args.plot_name
    for dim_counter in range(start_dim, end_dim):
        print dim_counter
        plt.xlim([0, x_lim])
        plt.ylim([0, y_lim])
        M_temp = np.copy(M_original)
        P = PCA(n_components=dim_counter)
        M_temp_reduced = P.fit_transform(M_temp)
        M_temp_reduced_dist_matrix = pairwise_distances(M_temp_reduced)
        M_temp_reduced_dist_list = M_temp_reduced_dist_matrix.flatten()
        plt.hist(M_temp_reduced_dist_list, bins=100, color='b')
        plt.title(plot_name)
        plt.xlabel('total dimensions:' + str(dim_counter))
        plt.savefig(file_name[:-4] + '_' + str(dim_counter).zfill(4) + '.png')
        plt.clf()
    
    if args.ascending:
        subprocess.call(['convert', '-delay', '20', '-loop', '0',\
            file_name[:-4] + '_*.png', out_file_name])
    else:
        subprocess.call(['convert', '-delay', '20', '-loop', '0', '-reverse',\
            file_name[:-4] + '_*.png', out_file_name])
    for i in range(start_dim, end_dim):
        os.remove(file_name[:-4] + '_' + str(i).zfill(4) + '.png')
if __name__ == '__main__':
    main()
