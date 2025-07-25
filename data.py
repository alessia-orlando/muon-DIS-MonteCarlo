import ROOT
import shipLHC_conf as sndDet_conf
import SndlhcGeo
from os.path import exists
import csv

geo = SndlhcGeo.GeoInterface("/eos/experiment/sndlhc/users/fmei/muons_with_box/geant4_output/geofile_full.muonDIS-TGeant4-muonDis_0.root")
scifi = geo.snd_geo.Scifi  # SciFi geometry
scifi_mod = geo.modules['Scifi']
nscifi = scifi.nscifi  # number of SciFi stations
file_path = "/eos/experiment/sndlhc/users/fmei/muons_with_box/geant4_output/sndLHC.muonDIS-TGeant4-muonDis_"
cbmsim = ROOT.TChain("cbmsim")  # chain TTrees from different files

n_files_to_read = 5
for i in range (n_files_to_read):
    file_name = file_path+str(i)+"_dig.root"
    if not exists(file_name):
        continue
    this_read = cbmsim.Add(file_name)

# create the .csv file
with open("data.csv", mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    column_names = []
    column_names.append('Starting station')
    for i in range(nscifi):
        column_names.append(f'hits in station {i+1}')
        column_names.append(f'QDC/hits in station {i+1}')
        column_names.append(f'L_x in station {i+1}')
        column_names.append(f'L_y in station {i+1}')
    writer.writerow(column_names)

    A, B = ROOT.TVector3(), ROOT.TVector3()
    
    for i_event, event in enumerate(cbmsim):  # loop over events
        if len(cbmsim.MCTrack) == 0: continue
        n_scifi_hits = len(event.Digi_ScifiHits)

        if n_scifi_hits >= 1:  # select events with at least one hit in SciFi
            
            hits_per_station = {}
            qdc_per_station = {}
            min_per_station = {}  # minimum hit position in a station
            max_per_station = {}  # maximum hit position in a station
            l = {}

            incoming_mu = event.MCTrack[0]
            start_z = incoming_mu.GetStartZ()
            starting_station = -1
            for i in range(nscifi):
                z_pos = getattr(scifi, f"Ypos{i}")
                if i == 0:
                    if z_pos - 10 < start_z < z_pos:
                        starting_station = i + 1
                        break
                else:
                    z_pos_prev = getattr(scifi, f"Ypos{i - 1}")
                    if z_pos_prev + scifi.zdim < start_z < z_pos:
                        starting_station = i + 1
                        break

            for i in range(nscifi):
                        hits_per_station[f"scifi_{i+1}_x"] = 0
                        hits_per_station[f"scifi_{i+1}_y"] = 0
                        qdc_per_station[f"scifi_{i+1}_x"] = 0
                        qdc_per_station[f"scifi_{i+1}_y"] = 0
                        min_per_station[f"scifi_{i+1}_x"] = float("inf")
                        min_per_station[f"scifi_{i+1}_y"] = float("inf")
                        max_per_station[f"scifi_{i+1}_x"] = float("-inf")
                        max_per_station[f"scifi_{i+1}_y"] = float("-inf")
                        l[f"scifi_{i+1}_x"] = 0
                        l[f"scifi_{i+1}_y"] = 0
                
            for scifihit in event.Digi_ScifiHits:  # loop over hits
                station = scifihit.GetStation()
                qdc = scifihit.GetSignal()

                if scifihit.isVertical():  # vertical: features on the x direction
                    hits_per_station[f"scifi_{station}_x"] += 1
                    scifi_mod.GetSiPMPosition(scifihit.GetDetectorID(), A, B)
                    if A.X() > max_per_station[f"scifi_{station}_x"]:
                        max_per_station[f"scifi_{station}_x"] = A.X()
                    if A.X() < min_per_station[f"scifi_{station}_x"]:
                        min_per_station[f"scifi_{station}_x"] = A.X()
                    if qdc > -999: # hit SiPM
                        qdc_per_station[f"scifi_{station}_x"] += qdc
                else:  # horizontal: features on the y direction
                    hits_per_station[f"scifi_{station}_y"] += 1
                    scifi_mod.GetSiPMPosition(scifihit.GetDetectorID(), A, B)
                    if A.Y() > max_per_station[f"scifi_{station}_y"]:
                        max_per_station[f"scifi_{station}_y"] = A.Y()
                    if A.Y() < min_per_station[f"scifi_{station}_y"]:
                        min_per_station[f"scifi_{station}_y"] = A.Y()
                    if scifihit.GetSignal() > -999: # hit SiPM
                        qdc_per_station[f"scifi_{station}_y"] += qdc
            
                    for i in range(nscifi):
                        diff_x = max_per_station[f"scifi_{i+1}_x"] - min_per_station[f"scifi_{i+1}_x"] 
                        if diff_x != float("-inf") and diff_x != float("inf"):
                            l[f"scifi_{i+1}_x"] = diff_x  # shower width in x direction
                        else:
                            l[f"scifi_{i+1}_x"] = 0
                        diff_y = max_per_station[f"scifi_{i+1}_y"] - min_per_station[f"scifi_{i+1}_y"]
                        if diff_y != float("-inf") and diff_y != float("inf"):
                            l[f"scifi_{i+1}_y"] = diff_y  # shower width in y direction
                        else:
                            l[f"scifi_{i+1}_y"] = 0
        
            row = []
            row.append(starting_station)
            for i in range(nscifi):
                tot_hits = hits_per_station[f"scifi_{i+1}_x"] + hits_per_station[f"scifi_{i+1}_y"]
                row.append(tot_hits)
                if tot_hits > 0:
                    row.append(qdc_per_station[f"scifi_{i+1}_x"]/tot_hits + qdc_per_station[f"scifi_{i+1}_y"]/tot_hits)
                else:
                    row.append(0)
                row.append(l[f"scifi_{i+1}_x"])
                row.append(l[f"scifi_{i+1}_y"])
    
            writer.writerow(row)
