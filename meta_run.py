#!/usr/bin/env python3
import os, sys, datetime

def qsub(script_name, out_dir, script_params={}):
    """
    Submit a job to the cluster using qsub.
    :param script_name: Name of the script to run
    :param out_dir: Directory to run the script in
    :param qsub_args: Arguments to pass to qsub
    :return: Output from qsub -- job ID
    """
    os.makedirs(out_dir, exist_ok=True)
    script_params = ','.join([f"{k}=\"{v}\"" for k, v in script_params.items()])
    cmd = f"cd {out_dir}; qsub { '-v ' + script_params if script_params else ''} {script_name}"
    print(cmd)
    stream = os.popen(cmd)
    output = stream.read()
    return output

metarunner_dir = "~/metalogs"
outdir = f"{metarunner_dir}/{datetime.now().strftime('%y-%m-%d/%H-%M')}"

if len(sys.argv) < 4:
    print("Usage: python3 meta_run.py <script> <book_path> <lang>")
    sys.exit(1)

script_name = sys.argv[1]       # will be used later, once there's script for coquiAI
script_name = "meta_script.sh"
params = {
    "BOOK": sys.argv[2],
    "LANG": sys.argv[3],
    "HOME": os.environ["HOME"]
}

print(qsub(script_name, outdir, params))
