module add conda-modules
cenv=Make_Me_Talk_venv
if conda activate $cenv; then
	echo CONDA ACTIVE
else
	conda init
	conda env remove -n $cenv
	conda create python -n $cenv  --no-default-packages
	conda activate $cenv
	pip install -r requirements.txt
	echo CONDA ACTIVE
fi

echo NOT INSTALLING TTS OR MIMIC3 -- USE DOCKER CONTAINERS!!
