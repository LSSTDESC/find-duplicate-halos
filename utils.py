import os, sys, yaml, subprocess, time
import glob, struct
import numpy as np
import matplotlib.pyplot as plt


def create_slurm_script(items, pixel) :

    scr = __file__.replace('utils.py', '')

    logPath = os.path.join(scr, 'slurm_logs')
    scriptPath = os.path.join(scr, 'slurm_scripts')

    logFile = os.path.join(logPath, f"{items}_{pixel}.out")
    script = os.path.join(scriptPath, f"{items}_{pixel}.sh")

    if not os.path.exists(logPath) :
        os.makedirs(logPath)
    if not os.path.exists(scriptPath) :
        os.makedirs(scriptPath)

    f = open(f"{script}", "w")
    f.write("#!/bin/sh\n")
    f.write(f"#SBATCH --nodes=1\n")
    f.write(f"#SBATCH --job-name=search_{pixel}\n")
    f.write(f"#SBATCH --time=5:00:00\n")
    f.write(f"#SBATCH --partition=lsst,htc\n")
    f.write(f"#SBATCH --ntasks=4\n")
    f.write(f"#SBATCH --output={logFile}\n")
    f.write(f"#SBATCH --mem=8GB\n")
    if items == 'halos' :
    	f.write(f"python -u {scr}searchHalos.py {pixel}\n")
    elif items == 'members' :
    	f.write(f"python -u {scr}searchMembers.py {pixel}\n")
    f.close()
    return script


def slurm_submit(items, pixel, dep=None, gap=True) :

    if (dep is not None) and (gap == True) :
        time.sleep(3)

    script = create_slurm_script(items, pixel)
    if dep is not None:
        cmd = f"sbatch --depend=afterok:{dep} {script}"
    else:
        cmd = f"sbatch {script}"

    res = subprocess.run(cmd, shell=True, capture_output=True)
    job_id = str(res.stdout).split("Submitted batch job ")[1].split("\\")[0]
    return job_id

