import numpy as np
import sys, os

items = sys.argv[1]

pixels = np.load('cosmodc2_pixels.npy')

if items == 'halos' :
	results_list = [np.load(f'./duplicateHalos_pix/{pix}.npy') for pix in pixels]
	results = np.concatenate(results_list)
	np.save('./duplicateHalos.npy', results)
elif items == 'members' :
	results_list = [np.load(f'./duplicateMembers_pix/{pix}.npy') for pix in pixels if os.path.exists(f'./duplicateMembers_pix/{pix}.npy')]
	results = np.concatenate(results_list)
	np.save('./duplicateMembers.npy', results)


