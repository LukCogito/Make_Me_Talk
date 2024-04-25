#!/usr/bin/python3
import os, sys
from datetime import datetime

def qsub(script_path, out_dir, script_params={}, dry_run=False):
    """
    Submit a job to the cluster using qsub.
    :param script_name: Name of the script to run
    :param out_dir: Directory to run the script in
    :param qsub_args: Arguments to pass to qsub
    :param dry_run: If True, return the command instead of running it
    :return: Output from qsub -- job ID
    """
    script_params = ','.join([f"{k}=\"{v}\"" for k, v in script_params.items()])
    script_params = f"-v {script_params}" if script_params else ''
    cmd = f"cd {out_dir}; qsub { script_params } {script_path}"

    if dry_run:
        return cmd
    
    print(cmd)
    os.makedirs(out_dir, exist_ok=True)
    stream = os.popen(cmd)
    output = stream.read()
    return output

if len(sys.argv) < 4:
    print("Usage: python3 meta_run.py <script> <book_path> <lang> [<dry_run>=False|True]")
    sys.exit(1)

home_dir = os.path.expanduser("~")
metarunner_dir = home_dir + "/metalogs"
outdir = f"{metarunner_dir}/{datetime.now().strftime('%y-%m-%d/%H-%M')}"

script_name = sys.argv[1]       # will be used later, once there's script for coquiAI
script_name = f"{os.path.dirname(os.path.abspath(__file__))}/meta_job_script.sh"
params = {
    "BOOK": sys.argv[2],
    "LANG": sys.argv[3],
    "HOMEDIR": home_dir
}
dry_run = False if len(sys.argv) < 5 else (sys.argv[4].lower() == "true")

script_name = os.path.abspath(script_name)
params["BOOK"] = os.path.abspath(params["BOOK"])

if not os.path.exists(params["BOOK"]):
    print(f"Error: File '{params['BOOK']}' not found.", file=sys.stderr)
    sys.exit(1)

if params["LANG"] not in ["en", "cs"]:
    print(f"Error: Invalid language '{params['LANG']}'; language must be 'en' or 'cs'.", file=sys.stderr)
    sys.exit(1)

if not os.path.exists(script_name):
    print(f"Error: File '{script_name}' not found.", file=sys.stderr)
    sys.exit(1)

try:
    print(qsub(script_name, outdir, params, dry_run=dry_run))
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
