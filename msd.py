# Kuntal Ghosh
# Code for computing mean squared displacement

import numpy as np

def read_lammpstrj(filename):
    """Generator to read LAMMPS trajectory frames."""
    with open(filename) as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith('ITEM: TIMESTEP'):
                timestep = int(f.readline())
                timestep *= 0.001
                f.readline()  # Skip 'ITEM: NUMBER OF ATOMS'
                n_atoms = int(f.readline())
                f.readline()  # Skip 'ITEM: BOX BOUNDS'
                box = []
                for _ in range(3):
                    lo, hi = map(float, f.readline().split()[:2])
                    box.append(hi - lo)
                box = np.array(box)
                header = f.readline().split()[2:]
                colmap = {name: i for i, name in enumerate(header)}
                atoms = {}
                for _ in range(n_atoms):
                    parts = f.readline().split()
                    atom_id = int(parts[colmap['id']])
                    pos = np.array([
                        float(parts[colmap['x']]),
                        float(parts[colmap['y']]),
                        float(parts[colmap['z']])
                    ])
                    atoms[atom_id] = pos
                yield timestep, box, atoms

traj_file = '../mapping/com.lammpstrj'
ref_pos = None
id_to_idx = {}
msd_list = []
time_list = []

for frame_idx, (timestep, box, atoms) in enumerate(read_lammpstrj(traj_file)):
    if frame_idx == 0:
        atom_ids = sorted(atoms.keys())
        ref_pos = np.zeros((len(atom_ids), 3))
        for idx, aid in enumerate(atom_ids):
            id_to_idx[aid] = idx
            ref_pos[idx] = atoms[aid]
        t0 = timestep
    else:
        current_pos = np.zeros_like(ref_pos)
        for aid, pos in atoms.items():
            if aid in id_to_idx:
                current_pos[id_to_idx[aid]] = pos
        disp = current_pos - ref_pos
        disp -= box * np.round(disp / box)  # Apply PBC correction
        msd = np.mean(np.sum(disp**2, axis=1))
        msd_list.append(msd)
        time_list.append(timestep - t0)

# Save to file
with open('msd_deep_mbpol.dat', 'w') as fout:
    fout.write('# Time MSD\n')
    fout.write('0 0.0\n')
    for t, m in zip(time_list, msd_list):
        fout.write(f'{t} {m}\n')

