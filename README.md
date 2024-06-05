# find-duplicate-halos
Get the IDs of duplicate halos and their member galaxies which you may want to remove from the cosmoDC2 and/or the DC2 galaxy catalogs, depending on your work.

# What are duplicate halos?
An order of a few hundred halos in the cosmoDC2 simulated catalog (and by extension, the DC2 catalog) share the same space (ra, dec, z) and mass as another halo. This was due to an understood technical issue in the cosmoDC2 simulation which should have chosen one of the halos and thrown away the other along with its members, but it didn't.

These duplicates may or may not affect your work. For example, in cluster finding algorithms the duplicates can have a serious effect since the cluster finder would see a very rich cluster (having the members of both halos) but the halo it would be matched to would have a mass reflecting roughly half of the members. This would skew the mass-richness relation. In addition, though the duplicates are a very small fraction of the catalog, they are mostly seen in high mass halos so they may have a larger effect when focusing on the high mass clusters/halos.

This was an issue realized after the DC2 images were built so it was decided to leave them in for consistency between the cosmoDC2 and DC2 catalogs. Thus, the duplicates will contribute to additional affects at the image level such as galaxy blending so how to deal with them is left to you.

These duplicates are not present in the skySim5000 simulation and as such it is advised, when possible to use skySim5000. But if you need to use cosmoDC2 and DC2 then this repo provides a way to collect the halo and galaxy IDs of the duplicates. Note, it only flags the halo to remove, leaving behind the other halo.

The base code was provide by Patricia Larsen (@patricialarsen) -- some extensions were made to run effeciently over the full cosmoDC2 catalog.

# To run:
Note, you don't need to run the code. The duplicate halos and members have been provided in duplicateHalos.npy and duplicateMembers.npy. But, for clarity, to run at CC-in2p3 you just need to say <br />
`python searchParty.py halos` <br />
After this is finished run <br />
`python searchParty.py members` <br />
This will search each healpix pixel in the cosmoDC2 catalog for duplicates. Now we just need to combine the results: <br />
`python combineResults.py halos` <br />
`python combineResults.py members` <br />

To run at NERSC you will need to modify the slurm options in `utils.py` to comply with NERSC requirements.
