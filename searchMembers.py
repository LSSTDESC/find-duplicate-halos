import GCRCatalogs
import numpy as np
import sys

pix = sys.argv[1]

badHalos = np.load(f'./duplicateHalos_pix/{pix}.npy').astype(int)

if len(badHalos) == 0 :
	print('No bad halos in this pixel.')
	sys.exit()

print('LOADING CATALOGS', end='.....')
dc2 = GCRCatalogs.load_catalog('cosmoDC2_v1.1.4')
cluster_data = dc2.get_quantities(['halo_id', 'galaxy_id'], filters=[(lambda x: np.isin(x,badHalos), 'halo_id')], native_filters=[f'healpix_pixel == {pix}'])
print('DONE')

print(len(cluster_data['galaxy_id']))

scr = __file__.replace(os.path.basename(__file__), '')

np.save(f'{scr}duplicateMembers_pix/{pix}.npy', np.array(cluster_data['galaxy_id']).astype(int))
