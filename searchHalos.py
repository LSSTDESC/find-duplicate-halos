import GCRCatalogs
import numpy as np
import sys

np.bool = bool


pix = sys.argv[1]

print('LOADING CATALOGS', end='.....')
gc_cdc2 = GCRCatalogs.load_catalog('cosmoDC2_v1.1.4')
gc_sky = GCRCatalogs.load_catalog('skysim5000_v1.1.2')

cluster_data = gc_cdc2.get_quantities(['x', 'y', 'z', 'redshift', 'halo_mass', 'halo_id', 'baseDC2/target_halo_fof_halo_id',
                                       'lightcone_replication', 'step'],
                                      filters=['is_central'], native_filters=[f'healpix_pixel == {pix}'])

cluster_data_sky = gc_sky.get_quantities(['x', 'y', 'z', 'redshift', 'halo_mass', 'halo_id', 'baseDC2/target_halo_fof_halo_id',
                                          'lightcone_replication', 'step'],
                                      filters=['is_central'], native_filters=[f'healpix_pixel == {pix}'])
print('DONE')

bad_ids = np.array([])
bad_reps = np.array([])
bad_steps =  np.array([])

replication_list = np.unique(cluster_data['lightcone_replication'])
step_list = np.unique(cluster_data['step'])

mask_bad = []
bad_ids = []
bad_reps = []
bad_steps = []
print('GETTING POSSIBLE BAD IDs', end='......')
for rep in replication_list:
    lc_mask = (cluster_data['lightcone_replication']==rep)
    lc_mask_sky = (cluster_data_sky['lightcone_replication']==rep)
    for step in step_list:
        mask_sample = lc_mask & (cluster_data['step']==step)
        mask_sample_sky = lc_mask_sky & (cluster_data_sky['step']==step)
        fof_tags = cluster_data['baseDC2/target_halo_fof_halo_id'][mask_sample]
        fof_tags_sky = cluster_data_sky['baseDC2/target_halo_fof_halo_id'][mask_sample_sky]

        mask_bad = np.logical_not(np.isin(fof_tags,fof_tags_sky))
        bad_ids.append(fof_tags[mask_bad])
        bad_reps.append(np.ones(np.sum(mask_bad),dtype='int')*rep)
        bad_steps.append(np.ones(np.sum(mask_bad),dtype='int')*step)

bad_ids = np.concatenate(bad_ids)
bad_reps = np.concatenate(bad_reps)
bad_steps = np.concatenate(bad_steps)
print('DONE')

print("Number of candidate duplicates: ", len(bad_ids))
duplicates=0

duplicate_masses = []
duplicate_halo_id = []
bad_ids_true=[]
bad_reps_true=[]
bad_steps_true=[]
dists=[]

print('MATCHING TRUE BAD IDs', end='......')
for obj in range(len(bad_ids)):
    #find the halo
    idx = np.where((cluster_data['baseDC2/target_halo_fof_halo_id']==bad_ids[obj])&(cluster_data['lightcone_replication']==bad_reps[obj])&(cluster_data['step']==bad_steps[obj]))[0][0]
    # get a comparison sample of objects with the same replication number and step
    mask_comparison = (cluster_data_sky['lightcone_replication']==bad_reps[obj])&(cluster_data_sky['step']==bad_steps[obj])
    # calculate distance of halo sample to halo 
    dist_halos = np.sqrt((cluster_data_sky['x'][mask_comparison] - cluster_data['x'][idx])**2 + (cluster_data_sky['y'][mask_comparison] - cluster_data['y'][idx])**2 + (cluster_data_sky['z'][mask_comparison] - cluster_data['z'][idx])**2)
    # calculate whether mass and distance are both close (exact mass and dist<200kpc)
    mask_dup = (cluster_data_sky['halo_mass'][mask_comparison]==cluster_data['halo_mass'][idx])&(dist_halos<0.7)
    if np.sum(mask_dup)>0:
        # we should have one duplicate exactly (matching to itself), so duplicate means >1
        bad_ids_true.append(bad_ids[obj])
        bad_reps_true.append(bad_reps[obj])
        bad_steps_true.append(bad_steps[obj])
        duplicate_masses.append(cluster_data['halo_mass'][idx])
        duplicate_halo_id.append(cluster_data['halo_id'][idx])
        dists.append(dist_halos[mask_dup][dist_halos[mask_dup]>0])
        duplicates+=1
print('DONE')


print("Number of duplicates found in skysim: ", duplicates)
print("Halo ids of duplicate halos: ", duplicate_halo_id)

np.save(f"./duplicateHalos_pix/{pix}.npy", np.array(duplicate_halo_id).astype(int))

