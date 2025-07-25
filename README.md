# muon-DIS-MonteCarlo

In this project, we will analyse the data from the MonteCarlo simulation of muons Deep Inelastic Scattering (DIS) in the SND@LHC detector. These kind of events represent one of the main backgrounds in the search of neutrinos arising from the decay of particles produced in the proton-proton collisions at LHC. In particular, we will focus on the events in the SciFi system of the detector. The system represents the electronic part of the tracker and consists of five scintillating fibre stations. For the analysis of the simulated data, sndsw will be used (https://github.com/SND-LHC/sndsw).

The aim is to use a Random Forest Classifier to predict the starting SciFi station of a simulated muon based on some features which will be discussed in detail. 

## Setup
To setup this repository and run the code:
1. Log into lxplus
    ```
   ssh yourusername@lxplus.cern.ch
    ```
2. Clone this repository
    ```
   git clone https://github.com/alessia-orlando/muon-DIS-MonteCarlo
   cd muon-DIS-MonteCarlo
    ```
3. Setup the source environment to use sndsw (an SND@LHC computing account is needed)
   ```
   source //eos/experiment/sndlhc/users/gpsndlhc/setup_for_box.sh
   ```
## The Data
### Data exploration
The MC data are generated in a two-step process involving Pythia6 and Geant4 and stored in a ROOT TTree file. The branches of the TTree used in this project are:
- MCTrack: branch containing informations about the simulated muon track (MonteCarlo truth).
- Digi_ScifiHits: branch containing digitized hits in the SciFi detector.

In `muonDIS_scifi.py` we select events with at least one hit in the SciFi tracker; after this requirement we have 888 muon events. In particular, we will consider the starting station of each track and other features. The starting station is derived from MCTrack, taking the starting Z coordinate (along the beam axis) and assigning it to one of the stations using `SndlhcGeo` and the geofile, in which informations about the geometry of the detector are stored. Values for the starting station can be:
- 1 if the track starts in station 1;
- 2 if the track starts in station 2;
- 3 if the track starts in station 3;
- 4 if the track starts in station 4;
- 5 if the track starts in station 5;
- -1 if the track does not start in the SciFi system.
  
The features which will be used to predict the starting station of the muons are:
- Number of hits in each station;
- QDC/hit in each station;
- Horizontal shower width L_x in each station;
- Vertical shower width L_y in each station.

### Data preparation and Dataset exploration
In order to be used in the Random Forest Classifier, data must be converted in a `.csv` format. Looping over the selected event as it was done previously, the `data.py` file writes the starting station of each event (target) and the features mentioned above as columns and stores them inside the `data.csv` file.

The dataset can now be explored using python libraries `pandas` and `matplotlib`. From now on, sndsw will no longer be needed. The characteristics of our data can be directly visualized in the Jupyter Notebook `plots.ipynb`.

## Random Forest Classifier

