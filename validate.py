#!/usr/bin/env python3

import json
import sys

if len(sys.argv) != 2:
    print("validate.py: test output correctness and extract performance for the UK-NNSS Grid benchmark.")
    print("Usage: validate.py <result_json_file>")
    sys.exit(1)


jsonfile = sys.argv[1]

with open(jsonfile, 'r') as file:
    data = json.load(file)

valid = True

print("\n# Grid benchmark validation\n")

# Get the MPI decomposition
mpi_decomp = data['geometry']['mpi']
mpi_decomp_s = '.'.join(str(x) for x in mpi_decomp)
print(f'   MPI Decomposition : {mpi_decomp_s}\n')
# Test for valid MPI decomposition
if (mpi_decomp[0] > mpi_decomp[1]) or (mpi_decomp[1] > mpi_decomp[2]) or (mpi_decomp[2] > mpi_decomp[3]):
    print(f'   Result invalid: MPI decompostion does not match X <= Y <= Z <= T')
    valid = False


lvals = [24, 32, 48]
perfvals = {}


flops_a = data['flops']['results']
for flops in flops_a:
    if flops['L'] in lvals:
        perfvals[flops['L']] = flops['Gflops_dwf4']

for lval in lvals:
    if lval not in perfvals.keys():
        print(f'   Result invalid: local volume {lval}^4 missing from results file')
        valid = False
    else:
        print(f'   {lval}^4 DWF4 Performance : {perfvals[lval]:.0f} Gflops/s/node')

print("\n   Validation:", ("PASSED" if valid else "FAILED") )

