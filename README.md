# PCA_histogram
Generates a GIF showing how pairwise distance changes as dimensions are reduced using principal component analysis. While running, the program prints the curren dimension being worked on to the command line.

Requires ImageMagick to generate the gif.
Requires the following python libraries:
  numpy
  matplotlib
  sklearn
Command line arguments:
  input_file: The csv file to be analyzed. The data must be numbers only.
  --set_x_lim int: Sets the maximum x value shown on the histogram. Default is the maximum x value.
  --set_y_lim int: Sets the maximum y value shown on the histogram Default is the maxiimum y value.
  --ascending: Goes from lower dimensions to higher.
  --output_file_name string: Sets the name of the final GIF. Default is the name of the csv input file.
  --ignore_header: Ignores the first row of data.
  --ignore_row_names: Ignores the first column of data.
  --plot_name string: Sets the name of the plot on the histograms. Default is the name of the csv.
  --dim_floor int: Sets the lowest dimension the histogram will go to. Default is 0.
  --dim_ciel int: Sets the highest dimension the histogram will go to. Default is the dimension of the data set.
