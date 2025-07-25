import ROOT
import shipLHC_conf as sndDet_conf
import SndlhcGeo
from os.path import exists

geo = SndlhcGeo.GeoInterface("/eos/experiment/sndlhc/users/fmei/muons_with_box/geant4_output/geofile_full.muonDIS-TGeant4-muonDis_0.root")
scifi = geo.snd_geo.Scifi  # SciFi geometry
nscifi = scifi.nscifi  # number of SciFi stations
file_path = "/eos/experiment/sndlhc/users/fmei/muons_with_box/geant4_output/sndLHC.muonDIS-TGeant4-muonDis_"
cbmsim = ROOT.TChain("cbmsim")  # chain TTrees from different files

n_files_to_read = 5
for i in range (n_files_to_read):
    file_name = file_path+str(i)+"_dig.root"
    if not exists(file_name):
        continue
    this_read = cbmsim.Add(file_name)

# Detector coordinates
x_min, x_max = -80, 5
y_min, y_max = 5, 75
z_min, z_max = 270, 580
x_range = x_max - x_min
y_range = y_max - y_min
z_range = z_max - z_min

# X, Y, Z STARTING POSITIONS
h_incoming_x = ROOT.TH1D("h_incoming_x", "Incoming muon x;x[cm]", x_range, x_min, x_max)
h_incoming_y = ROOT.TH1D("h_incoming_y", "Incoming muon y;y[cm]", y_range, y_min, y_max)
h_incoming_z = ROOT.TH1D("h_incoming_z", "Incoming muon z;z[cm]", z_range, z_min, z_max)
h_scifi_starting_station = ROOT.TH1D("h_scifi_starting_station", "Starting SciFi station; SciFi station", 6, 0, 6)

# NUMBER OF HITS
h_scifi_hits = ROOT.TH1D("h_scifi_hits", "Number of Scifi hits; # hits", 30, 0, 30)
h_scifi_hits_stations = ROOT.TH1D("h_scifi_hits_stations", "Scifi hits per station; SciFi Station", 6, 0, 6)

# QDC
h_scifi_qdc = ROOT.TH1D("h_scifi_qdc", "SciFi signal; QDC", 200, -2, 20)


for i_event, event in enumerate(cbmsim):  # loop over events
    if len(cbmsim.MCTrack) == 0: continue
    n_scifi_hits = len(event.Digi_ScifiHits)
    if n_scifi_hits >= 1:  # select events with at least one hit in SciFi
        incoming_mu = event.MCTrack[0]  # incoming muon track

        # coordinates of the MCTrack start
        start_x = incoming_mu.GetStartX()
        start_y = incoming_mu.GetStartY()
        start_z = incoming_mu.GetStartZ()

        # starting stations
        starting_station = -1
        for i in range(nscifi):
            z_pos = getattr(scifi, f"Ypos{i}")
            if i == 0:  # first SciFi station
                if z_pos - 10 < start_z < z_pos:
                    starting_station = i + 1
                    break
            else:
                z_pos_prev = getattr(scifi, f"Ypos{i - 1}")
                if z_pos_prev + scifi.zdim < start_z < z_pos:
                    starting_station = i + 1
                    break
        if starting_station != -1:
            h_scifi_starting_station.Fill(starting_station)
        
        for scifihit in event.Digi_ScifiHits:  # loop over digitized hits
            station = scifihit.GetStation()
            h_scifi_hits_stations.Fill(station)
            if scifihit.GetSignal() > -999:  # hit SiPM
                h_scifi_qdc.Fill(scifihit.GetSignal())

        h_incoming_x.Fill(incoming_mu.GetStartX())        
        h_incoming_y.Fill(incoming_mu.GetStartY())
        h_incoming_z.Fill(incoming_mu.GetStartZ())

        h_scifi_hits.Fill(n_scifi_hits)


c_incoming_x = ROOT.TCanvas("c_incoming_x")
h_incoming_x.Draw()
c_incoming_x.Draw()

c_incoming_y = ROOT.TCanvas("c_incoming_y")
h_incoming_y.Draw()
c_incoming_y.Draw()

c_incoming_z = ROOT.TCanvas("c_incoming_z")
h_incoming_z.Draw()
c_incoming_z.Draw()

c_scifi_starting_station = ROOT.TCanvas("c_scifi_starting_station")
h_scifi_starting_station.Draw()
c_scifi_starting_station.Draw()

c_scifi_hits = ROOT.TCanvas("c_scifi_hits")
h_scifi_hits.Draw()
c_scifi_hits.Draw()

c_scifi_hits_stations = ROOT.TCanvas("c_scifi_hits_stations")
h_scifi_hits_stations.Draw()
c_scifi_hits_stations.Draw()

c_scifi_qdc = ROOT.TCanvas("c_scifi_qdc")
h_scifi_qdc.Draw()
c_scifi_qdc.Draw()

output = ROOT.TFile("muonDIS_scifi_plots.root", "RECREATE")

h_incoming_x.Write()
h_incoming_y.Write()
h_incoming_z.Write()
h_scifi_starting_station.Write()

h_scifi_hits.Write()
h_scifi_hits_stations.Write()
h_scifi_qdc.Write()

output.Close()
