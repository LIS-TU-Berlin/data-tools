from data_tools import h5_helper
import numpy as np

def write_to_file():
    manifest = { 'info': 'This is a description of the data file - include anything here ', 'num_entries': 1 }
    dat = np.random.randn(2,3)
    x = np.array([1,2,3])

    print('=== writing z.h5 ===')
    h5 = h5_helper.H5Writer('z.h5')
    h5.write_dict('manifest', manifest)
    h5.write_list('list', [x, x], 'float64')
    h5.write('data1/X', dat, 'float64')

def print_file_info():
    h5 = h5_helper.H5Reader('z.h5')
    print('=== this is the same as calling ry_h5Info from command line ===')
    h5.print_info()
    print('===')

def read_from_file():
    h5 = h5_helper.H5Reader('z.h5')
    manifest = h5.read_dict('manifest')
    alist = h5.read('list')
    data = h5.read('data1/X')

    print('manifest:', manifest)
    print('alist:', alist[0], alist[1], type(alist), alist.shape, alist.dtype)
    print('data:', type(data), data.shape, data.dtype)
    print('===')


if __name__ == "__main__":
    write_to_file()
    print_file_info()
    read_from_file()
