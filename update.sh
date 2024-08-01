#!/bin/bash
# ----------------------------------------
# SCORE Project - GeoNode explorer updater
# Giacomo Roversi
# CNR-ISAC Rome (IT)
# 31 July 2024
# ----------------------------------------

#SBATCH -n 1
#SBATCH --mem=2G
#SBATCH --time 2:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=g.roversi@isac.cnr.it
#SBATCH --output=/work/users/roversi/logs/%j_%x.log

export DISPLAY=:0

cd "$HOME/geonode-explorer/"

# Activate the conda environment for the crontab shell
source "$HOME/anaconda3/etc/profile.d/conda.sh"
conda activate

# Execute the notebook with extended timeout (10 min)
jupyter nbconvert --ExecutePreprocessor.timeout=600 --to notebook --execute --inplace notebook.ipynb

# Upload the changes
git commit -am "Monthly automatic update"
git push

cd ~

# Done.


