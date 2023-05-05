wav2tab
==============================

music to tab generation

## ensure conda is installed

## Demucs installation #
### from https://github.com/facebookresearch/demucs

git clone https://github.com/facebookresearch/demucs.git <br />
cd demucs <br />
conda env update -f environment-cpu.yml  # if you don't have GPUs <br />
conda env update -f environment-cuda.yml # if you have GPUs <br />
conda activate demucs <br />
pip install -e . <br />

brew install sound-touch  # mac <br />
sudo apt-get install soundstretch  # ubuntu <br />

### for ffmpeg error 
conda uninstall ffmpeg <br />
conda install -c conda-forge ffmpeg<br />

## Basic Pitch installation #
### from https://github.com/spotify/basic-pitch

pip install basic-pitch --upgrade

### run this to setup directory structure in wav2tab repo
python repo_setup.py

## requirements
### make sure env is activated
pip install -r requirements
