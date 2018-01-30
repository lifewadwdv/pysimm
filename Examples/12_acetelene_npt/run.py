import os
from pysimm import system, cassandra, lmps

# Setup the box with acetelene molecules on the regular grid
sst = system.System()

bx_size = 30
sst.dim = system.Dimension(dx=bx_size, dy=bx_size, dz=bx_size, center=[bx_size / 2, bx_size / 2, bx_size / 2])
sst.forcefield = 'trappe/amber'

molec = system.read_lammps('c2h4.lmps')
molec.forcefield = 'trappe/amber'

# Creating system of 1000 molecules for NPT calculations
# displ = 3
# for i in range(10):
#     for j in range(10):
#         for k in range(10):
#             sst.add(molec.copy(dx=displ*i, dy=displ*j, dz=displ*k), change_dim=False)
#
# lmps.check_lmps_attr(sst)
# sst.write_lammps('init_conf.lmps')

cs = cassandra.Cassandra(sst)
npt_props = cs.read_input('props.inp')
npt_props['Pressure_Info'] = 25  # Simulated pressure in bars
npt_props['Start_Type'] = {'start_type': 'make_config', 'species': 1000}

cs.add_npt_mc(species=molec, is_rigid=True, out_folder='results', **npt_props)

cs.run()

lmps.check_lmps_attr(cs.system)
cs.system.write_lammps('final_conf.lmps')
