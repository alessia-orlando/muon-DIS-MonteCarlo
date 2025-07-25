# muon-DIS-MonteCarlo

In this project, we will analyse the data from the MonteCarlo simulation of muons Deep Inelastic Scattering (DIS) in the SND@LHC detector. These kind of events represent one of the main backgrounds in the search of neutrinos arising from the decay of particles produced in the proton-proton collisions at LHC. In particular, we will focus on the events in the SciFi system of the detector, which consists of five scintillating fibre stations. The stations are alternated with Emulsion Cloud Chambers walls, and together they represent the tracking system of the detector. For the analysis of the simulated data, sndsw will be used (https://github.com/SND-LHC/sndsw).

<img width="699" height="394" alt="layout" src="https://github.com/user-attachments/assets/00667ad3-056f-4600-807f-31729420a492" />

The final goal is to use a Random Forest Classifier to predict the SciFi station in which a simulated muon track starts based on some features which will be discussed in detail. 

## The Data
### Data exploration
The MC data are generated in a two-step process involving Pythia 6 (physics process) and Geant4 (detector response) and stored in a ROOT TTree file. The branches of the TTree used in this project are:
- MCTrack: branch containing informations about the simulated muon track (MonteCarlo truth).
- Digi_ScifiHits: branch containing digitized hits in the SciFi detector.

In muonDIS_scifi.py we select events with at least one hit in the SciFi tracker; after this requirement we have 888 muon events. From the MCTrack we can obtain the starting coordinates of the event; in particular, taking the starting Z coordinate (along the beam axis) we can associate it to one of the five SciFi stations using SndlhcGeo and the geofile, in which informations about the geometry of the detector are stored. A track starts in a given station {i} if its starting Z coordinate is between the stations {i} and {i-1}. As for the first SciFi station, since there is only a wall in front of it and no other station, a track starts there if its starting Z coordinate is between the first station and the 10 cm before it. Values for the starting station can be:
- 1 if the track starts in station 1;
- 2 if the track starts in station 2;
- 3 if the track starts in station 3;
- 4 if the track starts in station 4;
- 5 if the track starts in station 5;
- -1 if the track does not start in the SciFi system.
  
The features of the digitized data which will be used to predict the starting station of the muons are:
- Number of hits per station;
- QDC/hit per station (QDC measures the integrated charge of the analog signal produced by the SiPM);
- Horizontal shower width L_x per station;
- Vertical shower width L_y per station.

As an example, the plot below shows the distribution of the starting station of the muon tracks.

<img width="995" height="602" alt="Schermata del 2025-07-25 20-03-59" src="https://github.com/user-attachments/assets/e7b07fdf-83df-43f0-a346-456a81d35472" />

### Data preparation and Dataset exploration
In order to be used in the Random Forest Classifier, data must be converted in a .csv format. Looping over the selected events as it was done previously, the data.py file writes the starting station of each event (target) and the features mentioned above as columns and stores them inside the data.csv file.

In the plots.ipynb notebook we explore the characteristics of the dataset. After checking the most important informations, such as shape, data types and missing values, we can also plot the distributions for each column and the relationship between the features via a correlation matrix.

## Random Forest Classifier
After preparing and checking the data, it is possible to classify the events and predict if the muon track started in the SciFi target and, if so, in which station. For this we use Random Forest, i.e. a machine learning model that builds multiple decision trees, trains them on a random subset of the data, and combines their predictions. To build and train the Random Forest in random_forest.ipynb, we use the `RandomForestClassifier` from the scikit-learn library.

The data is split in the training and test sets:
- Training set: this portion of the data (80%) is used to train the model;
- Test set: this portion of the data (20%) is not used during the training, but it is used to evaluate the performance of the model after the training.

The classifier provides: 
- `.fit(X_train, y_train)` to train the model on the data. It builds all the decision trees using the features and the target;
- `.predict(X_test)` to make predictions using the trained model. It passes each input sample down every tree in the forest and uses a majority vote to assign a prediction.

At the end, starting from the features, the model will be able to predict where the muon interaction takes place. In this case, the accuracy of the predictions is about 88%. 

In the random_forest.ipynb notebook we preprocess the data, defining the feature columns X and the target column y, and split it into training and test sets. Using the scikit-learn class RandomizedSearchCV, we can find the best hyperparameters for the model within a given range and fit the best model to our data.

## Run instructions
### Setup, data exploration and preparation (on lxplus)
1. Log into lxplus
    ```
   ssh username@lxplus.cern.ch
    ```
2. Clone this repository
    ```
   git clone https://github.com/alessia-orlando/muon-DIS-MonteCarlo
   cd muon-DIS-MonteCarlo
    ```
3. Setup the source environment to use sndsw
   ```
   source //eos/experiment/sndlhc/users/gpsndlhc/setup_for_box.sh
   ```
4. Data exploration
   ```
   python muonDIS_scifi.py
   ```
A ROOT file muonDIS_scifi_plots.py will be created; all the histograms are contained there.

5. Data preparation
   ```
   python data.py
   ```
   The file data.csv will be created.

### Dataset exploration and Random Forest Classifier (locally)
1. Clone the repository locally
   ```
   git clone https://github.com/alessia-orlando/muon-DIS-MonteCarlo
   cd muon-DIS-MonteCarlo
   ```
2. Create a virtual environment
   ```
   python -m venv venv
   ```
3. Activate the virtual environment
   - Windows:
     ```
     source venv/Scripts/activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```
4. Install the needed packages (if not already available)
   ```
   pip install numpy pandas scikit-learn matplotlib graphviz
   ```
5. To use graphviz
   - Linux:
     ```
     sudo apt-get install graphviz
     ```
   - macOS:
     ```
     brew install graphviz
     ```
   - Windows:
     Download from https://graphviz.org/download/ and install
6. Launch Jupyter Notebook
   ```
   jupyter notebook
   ```
7. Navigate to the files


   
   
