import numpy as np
from utils import slurm_submit
from tqdm import tqdm
import sys

items = sys.argv[1]	# halos or members

pixels = np.load('cosmodc2_pixels.npy')

[slurm_submit(items, pix, gap=False) for pix in tqdm(pixels)]

