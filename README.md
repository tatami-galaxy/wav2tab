wav2tab
==============================

music to tab generation

# Demucs installation #
# from https://github.com/facebookresearch/demucs

git clone https://github.com/facebookresearch/demucs.git
cd demucs
conda env update -f environment-cpu.yml  # if you don't have GPUs
conda env update -f environment-cuda.yml # if you have GPUs
conda activate demucs
pip install -e .

brew install sound-touch  # mac
sudo apt-get install soundstretch  # ubuntu

# for ffmpeg error
conda uninstall ffmpeg
conda install -c conda-forge ffmpeg

# basic pitch installation #
# from https://github.com/spotify/basic-pitch

pip install basic-pitch --upgrade

# project structure
/data -> datasets
/models -> trained models

