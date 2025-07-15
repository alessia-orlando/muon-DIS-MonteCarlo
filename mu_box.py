import ROOT
import shipLHC_conf as sndDet_conf
import SndlhcGeo
from os.path import exists


file_path = "/eos/experiment/sndlhc/users/fmei/muons_with_box/geant4_output/sndLHC.muonDIS-TGeant4-muonDis_"
geo = SndlhcGeo.GeoInterface("/eos/experiment/sndlhc/users/fmei/muons_with_box/geant4_output/geofile_full.muonDIS-TGeant4-muonDis_0.root")
cbmsim = ROOT.TChain("cbmsim")

scifi = geo.snd_geo.Scifi


# READ FILES

n_files_to_read = 5
n_files_read = 0
for i in range (n_files_to_read):
    file_name = file_path+str(i)+"_dig.root"
    if not exists(file_name):
        continue
    this_read = cbmsim.Add(file_name)

    if this_read > 0:
        n_files_read += 1

print("Got {0} events from {1} files.".format(cbmsim.GetEntries(), n_files_read))

entries = cbmsim.GetEntries()
non_zero_count = 0

for i in range(entries):
    cbmsim.GetEvent(i)
    if len(cbmsim.MCTrack) != 0:
        non_zero_count += 1

print(f"Number of non-zero events: {non_zero_count}")

# X, Y, Z POSITION 
h_incoming_x = ROOT.TH1D("h_incoming_x", "Incoming muons x;x[cm]", 17, -80, 5)
h_incoming_y = ROOT.TH1D("h_incoming_y", "Incoming muons y;y[cm]", 14, 5, 75)
h_incoming_z = ROOT.TH1D("h_incoming_z", "Incoming muons z;z[cm]", 62, 270, 580)

h_incoming_xy = ROOT.TH2D("h_incoming_xy", "Incoming muons xy;x[cm];y[cm]", 17, -80, 5, 14, 5, 75)
h_incoming_zy = ROOT.TH2D("h_incoming_zy", "Incoming muons zy;z[cm];y[cm]", 62, 270, 580, 14, 5, 75)
h_incoming_zx = ROOT.TH2D("h_incoming_zx", "Incoming muons zx;z[cm];x[cm]", 62, 270, 580, 17, -80, 5)

# N_HITS
h_scifi_hits = ROOT.TH1D("h_scifi_hits", "Number of Scifi hits; # hits", 40, 0, 40)

h_mufilter_hits = ROOT.TH1D("h_mufilter_hits", "Number of MuFilter hits; # hits", 200, 0, 200)
h_mufilter_US_hits = ROOT.TH1D("h_mufilter_US_hits", "Number of US hits; # hits", 100, 0, 100)
h_mufilter_DS_hits = ROOT.TH1D("h_mufilter_DS_hits", "Number of DS hits; # hits", 100, 0, 100)
h_mufilter_veto_hits = ROOT.TH1D("h_mufilter_veto_hits", "Number of veto hits; #hits", 100, 0, 100)


# vedere num. di hit per piani scifi GetStation
# num. di hit per piani mufilter GetPlane
# separare x e y scifi isVertical()->true(x)
# mufilter: isShort (sipm piccolo/grande US), isVertical (come scifi)
# guardare i singoli sipm
# plot 2D x: coord. start y: # hit (sep. scifi e mufi)
# eventi 0 hit sia in scifi che in mufilter
# dist qdc
# solo grandi
# picco qdc mip scifi e us
# per stazione e totale
# scifi mufi points: GetEnergyLoss(), station() per scifi, per mufilter GetSystem fare a mano con GetDetectorID() // 10000
# per piano (GetDetectorID // 1000 % 10 ) parte da 0 


# SCIFI HITS
h_scifi_stations = ROOT.TH1D("h_scifi_stations", "Scifi hits per station; Scifi Station", 6, 0, 6)

# VETO HITS
h_veto_planes = ROOT.TH1D("h_veto_planes", "Veto hits per plane; Veto plane", 4, 0, 4)

# US HITS
h_us_planes = ROOT.TH1D("h_us_planes", "US hits per plane; US plane", 6, 0, 6)

# DS HITS
h_ds_planes = ROOT.TH1D("h_ds_planes", "DS hits per plane; DS plane", 5, 0, 5)

# ENERGY
h_energy = ROOT.TH1D("h_energy", "Muon energy; E[GeV]", 100, 0, 4000)

# VERTICAL/HORIZONTAL HITS
h_scifi_vertical = ROOT.TH1D("h_scifi_vertical", "Vertical Scifi hits; # vertical hits", 100, 0, 100)
h_scifi_horizontal = ROOT.TH1D("h_scifi_horizontal", "Horizontal Scifi hits; # horizontal hits", 100, 0, 100)

h_ds_vertical = ROOT.TH1D("h_ds_vertical", "Vertical DS hits; # vertical hits", 100, 0, 100)
h_ds_horizontal = ROOT.TH1D("h_ds_horizontal", "Horizontal DS hits; # horizontal hits", 100, 0, 100)

# HITS VS COORDINATES
h_x_hits = ROOT.TH2D("h_x_hits", "Hits vs starting x; x[cm]; # hits", 20, 3, 5, 100, 0, 100)
h_y_hits = ROOT.TH2D("h_y_hits", "Hits vs starting y; y[cm]; # hits", 50, 70, 75, 100, 0, 100)
h_z_hits = ROOT.TH2D("h_z_hits", "Hits vs starting z; z[cm]; # hits", 100, 353, 363, 100, 0, 100)

h_x_hits_scifi = ROOT.TH2D("h_x_hits_scifi", "Hits in scifi vs starting x; x[cm]; # scifi hits", 30, -80, 5, 100, 0, 100)
h_y_hits_scifi = ROOT.TH2D("h_y_hits_scifi", "Hits in scifi vs starting y; y[cm]; # scifi hits", 30, 5, 75, 100, 0, 100)
h_z_hits_scifi = ROOT.TH2D("h_z_hits_scifi", "Hits in scifi vs starting z; z[cm]; # scifi hits", 30, 270, 580, 100, 0, 100)

h_x_hits_mufilter = ROOT.TH2D("h_x_hits_mufilter", "Hits in mufilter vs starting x; x[cm]; # mufilter hits", 5, 0, 5, 100, 0, 100)
h_y_hits_mufilter = ROOT.TH2D("h_y_hits_mufilter", "Hits in mufilter vs starting y; y[cm]; # mufilter hits", 5, 70, 75, 100, 0, 100)
h_z_hits_mufilter = ROOT.TH2D("h_z_hits_mufilter", "Hits in mufilter vs starting z; z[cm]; # mufilter hits", 30, 350, 380, 100, 0, 100)

h_x_hits_veto = ROOT.TH2D("h_x_hits_veto", "Hits in veto vs starting x; x[cm]; # veto hits", 30, -80, 5, 30, 0, 100)
h_y_hits_veto = ROOT.TH2D("h_y_hits_veto", "Hits in veto vs starting y; y[cm]; # veto hits", 30, 5, 75, 30, 0, 100)
h_z_hits_veto = ROOT.TH2D("h_z_hits_veto", "Hits in veto vs starting z; z[cm]; # veto hits", 30, 270, 580, 30, 0, 100)

h_x_hits_us = ROOT.TH2D("h_x_hits_us", "Hits in us vs starting x; x[cm]; # us hits", 30, -80, 5, 30, 0, 100)
h_y_hits_us = ROOT.TH2D("h_y_hits_us", "Hits in us vs starting y; y[cm]; # us hits", 30, 5, 75, 30, 0, 100)
h_z_hits_us = ROOT.TH2D("h_z_hits_us", "Hits in us vs starting z; z[cm]; # us hits", 30, 270, 580, 30, 0, 100)

h_x_hits_ds = ROOT.TH2D("h_x_hits_ds", "Hits in ds vs starting x; x[cm]; # ds hits", 30, -80, 5, 30, 0, 100)
h_y_hits_ds = ROOT.TH2D("h_y_hits_ds", "Hits in ds vs starting y; y[cm]; # ds hits", 30, 5, 75, 30, 0, 100)
h_z_hits_ds = ROOT.TH2D("h_z_hits_ds", "Hits in ds vs starting z; z[cm]; # ds hits", 30, 270, 580, 30, 0, 100)

# SiPMs
h_us_sipm = ROOT.TH1D("h_us_sipm", "Number of fired US SiPMs", 17, 0, 17)
h_us_small = ROOT.TH1D("h_us_small", "Number of fired small US SiPMs", 17, 0, 17)

'''# ZERO HITS
h_incoming_x_zero = ROOT.TH1D("h_incoming_x_zero", "Incoming muons x (zero hits);x[cm]", 85, -80, 5)
h_incoming_y_zero = ROOT.TH1D("h_incoming_y_zero", "Incoming muons y (zero hits);y[cm]", 70, 5, 75)
h_incoming_z_zero = ROOT.TH1D("h_incoming_z_zero", "Incoming muons z (zero hits);z[cm]", 310, 270, 580)

h_incoming_xy_zero = ROOT.TH2D("h_incoming_xy_zero", "Incoming muons xy (zero hits);x[cm];y[cm]", 17, -80, 5, 14, 5, 75)
h_incoming_zy_zero = ROOT.TH2D("h_incoming_zy_zero", "Incoming muons zy (zero hits);z[cm];y[cm]", 62, 270, 580, 14, 5, 75)
h_incoming_zx_zero = ROOT.TH2D("h_incoming_zx_zero", "Incoming muons zx (zero hits);z[cm];x[cm]", 62, 270, 580, 17, -80, 5)
'''
# QDC
h_scifi_qdc = ROOT.TH1D("h_scifi_qdc", "SciFi signal; QDC", 200, -2, 20)
h_scifi_qdc_station = {}
for i in range(1, 6):
    h_scifi_qdc_station[i] = ROOT.TH1D(f"h_scifi_qdc_station{i}", f"QDC for SciFi station {i}", 200, 0, 20)

h_mufi_us_qdc = ROOT.TH1D("h_mufi_us_qdc", "US signal; QDC", 200, -2, 20)
h_mufi_us_qdc_plane = {}
for i in range(0, 5):
    h_mufi_us_qdc_plane[i] = ROOT.TH1D(f"h_mufi_us_qdc_plane{i}", f"QDC for US plane {i}", 200, 0, 20)

# scifi mufi points: GetEnergyLoss(), station() per scifi, per mufilter GetSystem fare a mano con GetDetectorID() // 10000
# per piano (GetDetectorID // 1000 % 10 ) parte da 0 
# totale


# SciFi POINTS
h_scifi_energy_loss = ROOT.TH1D("h_scifi_energy_loss", "Energy loss in SciFi; E[keV]", 100, 0, 100)
h_scifi_energy_loss_total = ROOT.TH1D("h_scifi_energy_loss_total", "Total energy loss in SciFi; E[MeV]", 200, 0, 20)
#h_scifi_energy_loss_station = {}
h_scifi_energy_loss_total_station = {}
for i in range(1, 6):
    #h_scifi_energy_loss_station[i] = ROOT.TH1D(f"h_scifi_energy_loss_station{i}", f"Energy loss in SciFi station {i}; E[keV]", 100, 0, 100)
    h_scifi_energy_loss_total_station[i] = ROOT.TH1D(f"h_scifi_energy_loss_total_station{i}", f"Total energy loss in SciFi station {i}; E[MeV]", 200, 0, 20)
h_z_scifi_energy_loss = ROOT.TH2D("h_z_scifi_energy_loss", "Total energy loss in scifi vs starting z; z[cm]; E[MeV]", 155, 270, 580, 200, 0, 20)

# MuFi POINTS
#h_mufi_energy_loss = ROOT.TH1D("h_mufi_energy_loss", "Energy loss in MuFilter; E[MeV]", 150, 0, 15)
#h_mufi_veto_energy_loss = ROOT.TH1D("h_mufi_veto_energy_loss", "Energy loss in veto; E [MeV]", 150, 0, 15)
h_mufi_us_energy_loss = ROOT.TH1D("h_mufi_us_energy_loss", "Energy loss in US; E[MeV]", 150, 0, 15)
h_mufi_us_energy_loss_total = ROOT.TH1D("h_mufi_us_energy_loss_total", "Total energy loss in US; E[MeV]", 1000, 0, 1000)
#h_mufi_ds_energy_loss = ROOT.TH1D("h_mufi_ds_energy_loss", "Energy loss in DS; E[MeV]", 150, 0, 15)
'''h_mufi_veto_energy_loss_plane = {}
for i in range(0, 3):
    h_mufi_veto_energy_loss_plane[i] = ROOT.TH1D(f"h_mufi_veto_energy_loss_plane{i}", f"Energy loss in veto plane {i}; E [MeV]", 150, 0, 15)
h_mufi_us_energy_loss_plane = {}'''
h_mufi_us_energy_loss_total_plane = {}
h_total_e_loss_scifi_us_plane = {}
for i in range(0, 5):
    #h_mufi_us_energy_loss_plane[i] = ROOT.TH1D(f"h_mufi_us_energy_loss_plane{i}", f"Energy loss in US plane {i}; E[MeV]", 150, 0, 15)
    h_mufi_us_energy_loss_total_plane[i] = ROOT.TH1D(f"h_mufi_us_energy_loss_total_plane{i}", f"Total energy loss in US plane {i}; E[MeV]", 150, 0, 150)
    h_total_e_loss_scifi_us_plane[i] = ROOT.TH2D(f"h_total_e_loss_scifi_us_plane{i}", f"Total energy loss in US plane {i} vs Scifi; SciFi E[MeV]; US E[MeV]", 10, 0, 10, 15, 0, 150)
'''h_mufi_ds_energy_loss_plane = {}
for i in range(0, 4):
    h_mufi_ds_energy_loss_plane[i] = ROOT.TH1D(f"h_mufi_ds_energy_loss_plane{i}", f"Energy loss in DS plane {i}; E[MeV]", 150, 0, 15)
'''
h_z_us_energy_loss = ROOT.TH2D("h_z_us_energy_loss", "Total energy loss in US vs starting z; z[cm]; E[MeV]", 155, 270, 580, 15, 0, 150)

h_scifi_us_energy_loss = ROOT.TH2D("h_scifi_us_energy_loss", "Total energy loss in SciFi vs total energy loss in US; US E[MeV]; Scifi E[MeV]", 50, 0, 100, 5, 0, 10)

#n_zero_scifi = 0
#n_non_zero_hits = 0
# LOOP OVER EVENTS

for i_event, event in enumerate(cbmsim):
    if len(cbmsim.MCTrack) == 0: continue
    incoming_mu = event.MCTrack[0]

    # Number of hits
    n_scifi_hits = len(event.Digi_ScifiHits)
    n_mufilter_hits = len(event.Digi_MuFilterHits)
    if n_scifi_hits >= 1:
        #non_zero_count += 1
        #n_non_zero_hits += 1
        n_mufilter_US_hits = 0
        n_mufilter_DS_hits = 0
        n_mufilter_veto_hits = 0

        if n_scifi_hits == 0:
            n_zero_scifi += 1
        
        #n_zero_hits = 0

        # hits per station/plane
        hits_per_station = set()
        hits_per_veto_plane = set()
        hits_per_us_plane = set()
        hits_per_ds_plane = set()
    
        # vertical/horizontal hits
        n_vertical_scifi_hits = 0
        n_horizontal_scifi_hits = 0
        
        n_vertical_ds_hits = 0
        n_horizontal_ds_hits = 0

        # loop on scifi hits
        for scifihit in event.Digi_ScifiHits:
            station = scifihit.GetStation()
            hits_per_station.add(station)
            if scifihit.isVertical():
                n_vertical_scifi_hits += 1
            else:
                n_horizontal_scifi_hits += 1
            if scifihit.GetSignal() > -999:
                h_scifi_qdc.Fill(scifihit.GetSignal())
                if 1 <= station <= 5:
                    h_scifi_qdc_station[station].Fill(scifihit.GetSignal())
            
        # loop on mufilter hits
        for mufilterhit in event.Digi_MuFilterHits:
                if mufilterhit.GetSystem() == 1 :
                    n_mufilter_veto_hits += 1
                    veto_plane = mufilterhit.GetPlane()
                    hits_per_veto_plane.add(veto_plane)
                    
                if mufilterhit.GetSystem() == 2 :
                    n_mufilter_US_hits += 1
                    us_plane = mufilterhit.GetPlane()
                    hits_per_us_plane.add(us_plane)
                    n_us_sipms = 0
                    n_us_small = 0
                    for s in range(16):
                        if mufilterhit.GetSignal(s) > -999:
                            #print(mufilterhit.GetSignal(j))
                            n_us_sipms += 1
                            if mufilterhit.isShort(s):
                                n_us_small += 1
                        if not mufilterhit.isShort(s): # big sipms only
                            h_mufi_us_qdc.Fill(mufilterhit.GetSignal(s))
                            if 0 <= us_plane <= 4:
                                h_mufi_us_qdc_plane[us_plane].Fill(mufilterhit.GetSignal(s))

                    h_us_small.Fill(n_us_small)
                    h_us_sipm.Fill(n_us_sipms)

                if mufilterhit.GetSystem() == 3 :
                    n_mufilter_DS_hits += 1
                    ds_plane = mufilterhit.GetPlane()
                    hits_per_ds_plane.add(ds_plane)
                    if mufilterhit.isVertical():
                        n_vertical_ds_hits += 1
                    else:
                        n_horizontal_ds_hits += 1
        
        total_scifi_energy_loss = 0
        total_scifi_energy_loss_station = {}
        for i in range(1, 6):
            total_scifi_energy_loss_station[i] = 0
        # Points
        for scifipoint in event.ScifiPoint:
            scifi_e_loss = scifipoint.GetEnergyLoss() * 1000000
            total_scifi_energy_loss += scifi_e_loss
            h_scifi_energy_loss.Fill(scifi_e_loss)
            station = scifipoint.station()
            if 1 <= station <= 5:
                # h_scifi_energy_loss_station[station].Fill(scifi_e_loss)
                # totale per stazione
                # funzione del punto di interazione
                total_scifi_energy_loss_station[station] += total_scifi_energy_loss

        total_us_energy_loss = 0
        total_us_energy_loss_plane = {}
        for i in range(0, 5):
            total_us_energy_loss_plane[i] = 0
        for mufilterpoint in event.MuFilterPoint:
            mufi_e_loss = mufilterpoint.GetEnergyLoss() * 1000
            total_us_energy_loss += mufi_e_loss
            #h_mufi_energy_loss.Fill(mufi_e_loss)
            system = mufilterpoint.GetDetectorID() // 10000
            plane = mufilterpoint.GetDetectorID() // 1000  % 10
            '''if system == 1:
                h_mufi_veto_energy_loss.Fill(mufi_e_loss)
                if 0 <= plane <= 2:
                    h_mufi_veto_energy_loss_plane[plane].Fill(mufi_e_loss)'''
            if system == 2:
                h_mufi_us_energy_loss.Fill(mufi_e_loss)
                if 0 <= plane <= 4:
                    #h_mufi_us_energy_loss_plane[plane].Fill(mufi_e_loss)
                    total_us_energy_loss_plane[plane] += total_us_energy_loss
            '''if system == 3:
                h_mufi_ds_energy_loss.Fill(mufi_e_loss)
                if 0 <= plane <= 3:
                    h_mufi_ds_energy_loss_plane[plane].Fill(mufi_e_loss)'''


        # Fill
        
        h_incoming_x.Fill(incoming_mu.GetStartX())        
        h_incoming_y.Fill(incoming_mu.GetStartY())
        h_incoming_z.Fill(incoming_mu.GetStartZ())
        h_incoming_xy.Fill(incoming_mu.GetStartX(), incoming_mu.GetStartY())
        h_incoming_zy.Fill(incoming_mu.GetStartZ(), incoming_mu.GetStartY())
        h_incoming_zx.Fill(incoming_mu.GetStartZ(), incoming_mu.GetStartX())

        h_scifi_hits.Fill(n_scifi_hits)
        h_mufilter_hits.Fill(n_mufilter_hits)
        h_mufilter_US_hits.Fill(n_mufilter_US_hits)
        h_mufilter_DS_hits.Fill(n_mufilter_DS_hits)
        h_mufilter_veto_hits.Fill(n_mufilter_veto_hits)

        for station in hits_per_station:
            h_scifi_stations.Fill(station)
        
        for veto_plane in hits_per_veto_plane:
            h_veto_planes.Fill(veto_plane)

        for us_plane in hits_per_us_plane:
            h_us_planes.Fill(us_plane)

        for ds_plane in hits_per_ds_plane:
            h_ds_planes.Fill(ds_plane)

        h_energy.Fill(incoming_mu.GetEnergy())
        
        h_scifi_vertical.Fill(n_vertical_scifi_hits)
        h_scifi_horizontal.Fill(n_horizontal_scifi_hits)
        
        h_ds_vertical.Fill(n_vertical_ds_hits)
        h_ds_horizontal.Fill(n_horizontal_ds_hits)

        h_x_hits.Fill(incoming_mu.GetStartX(), n_scifi_hits + n_mufilter_hits)
        h_y_hits.Fill(incoming_mu.GetStartY(), n_scifi_hits + n_mufilter_hits)
        h_z_hits.Fill(incoming_mu.GetStartZ(), n_scifi_hits + n_mufilter_hits)
        h_x_hits_scifi.Fill(incoming_mu.GetStartX(), n_scifi_hits)
        h_y_hits_scifi.Fill(incoming_mu.GetStartY(), n_scifi_hits)
        h_z_hits_scifi.Fill(incoming_mu.GetStartZ(), n_scifi_hits)
        h_x_hits_mufilter.Fill(incoming_mu.GetStartX(), n_mufilter_hits)
        h_y_hits_mufilter.Fill(incoming_mu.GetStartY(), n_mufilter_hits)
        h_z_hits_mufilter.Fill(incoming_mu.GetStartZ(), n_mufilter_hits)
        h_x_hits_veto.Fill(incoming_mu.GetStartX(), n_mufilter_veto_hits)
        h_y_hits_veto.Fill(incoming_mu.GetStartY(), n_mufilter_veto_hits)
        h_z_hits_veto.Fill(incoming_mu.GetStartZ(), n_mufilter_veto_hits)
        h_x_hits_us.Fill(incoming_mu.GetStartX(), n_mufilter_US_hits)
        h_y_hits_us.Fill(incoming_mu.GetStartY(), n_mufilter_US_hits)
        h_z_hits_us.Fill(incoming_mu.GetStartZ(), n_mufilter_US_hits)
        h_x_hits_ds.Fill(incoming_mu.GetStartX(), n_mufilter_DS_hits)
        h_y_hits_ds.Fill(incoming_mu.GetStartY(), n_mufilter_DS_hits)
        h_z_hits_ds.Fill(incoming_mu.GetStartZ(), n_mufilter_DS_hits)

        '''# Zero hits
        if n_mufilter_hits == 0 and n_scifi_hits == 0:
            h_incoming_x_zero.Fill(incoming_mu.GetStartX())
            h_incoming_y_zero.Fill(incoming_mu.GetStartY())
            h_incoming_z_zero.Fill(incoming_mu.GetStartZ())
            h_incoming_xy_zero.Fill(incoming_mu.GetStartX(), incoming_mu.GetStartY())
            h_incoming_zy_zero.Fill(incoming_mu.GetStartZ(), incoming_mu.GetStartY())
            h_incoming_zx_zero.Fill(incoming_mu.GetStartZ(), incoming_mu.GetStartX())'''

        #if n_mufilter_hits != 0 or n_scifi_hits != 0:
        h_scifi_energy_loss_total.Fill(total_scifi_energy_loss/1000)
        for i in range(1, 6):
            h_scifi_energy_loss_total_station[i].Fill(total_scifi_energy_loss_station[i]/1000)
        for i in range(0, 5):
            h_mufi_us_energy_loss_total_plane[i].Fill(total_us_energy_loss_plane[i])
            h_total_e_loss_scifi_us_plane[i].Fill(total_scifi_energy_loss/1000, total_us_energy_loss_plane[i])
        h_mufi_us_energy_loss_total.Fill(total_us_energy_loss)
        h_z_scifi_energy_loss.Fill(incoming_mu.GetStartZ(), total_scifi_energy_loss/1000)
        h_z_us_energy_loss.Fill(incoming_mu.GetStartZ(), total_us_energy_loss)
        h_scifi_us_energy_loss.Fill(total_us_energy_loss, total_scifi_energy_loss/1000)

#print(f"Number of events with hits in the detector: {n_non_zero_hits}")
#print(f"Number of events with hits in SciFi: {n_non_zero_hits - n_zero_scifi}")

c_incoming_xy = ROOT.TCanvas("c_incoming_xy")
h_incoming_xy.Draw("COLZ")
c_incoming_xy.Draw()

c_incoming_zy = ROOT.TCanvas("c_incoming_zy")
h_incoming_zy.Draw("COLZ")
c_incoming_zy.Draw()

c_incoming_zx = ROOT.TCanvas("c_incoming_zx")
h_incoming_zx.Draw("COLZ")
c_incoming_zx.Draw()

c_incoming_x = ROOT.TCanvas("c_incoming_x")
h_incoming_x.Draw()
c_incoming_x.Draw()

c_incoming_y = ROOT.TCanvas("c_incoming_y")
h_incoming_y.Draw()
c_incoming_y.Draw()

c_incoming_z = ROOT.TCanvas("c_incoming_z")
h_incoming_z.Draw()
c_incoming_z.Draw()

c_scifi_hits = ROOT.TCanvas("c_scifi_hits")
h_scifi_hits.Draw()
c_scifi_hits.Draw()

c_mufilter_hits = ROOT.TCanvas("c_mufilter_hits")
h_mufilter_hits.Draw()
c_mufilter_hits.Draw()

c_mufilter_US_hits = ROOT.TCanvas("c_mufilter_US_hits")
h_mufilter_US_hits.Draw()
c_mufilter_US_hits.Draw()

c_mufilter_DS_hits = ROOT.TCanvas("c_mufilter_DS_hits")
h_mufilter_DS_hits.Draw()
c_mufilter_DS_hits.Draw()

c_mufilter_veto_hits = ROOT.TCanvas("c_mufilter_veto_hits")
h_mufilter_veto_hits.Draw()
c_mufilter_veto_hits.Draw()

c_scifi_stations_hits = ROOT.TCanvas("c_scifi_stations_hits")
h_scifi_stations.Draw()
c_scifi_stations_hits.Draw()

c_veto_planes_hits = ROOT.TCanvas("c_veto_planes_hits")
h_veto_planes.Draw()
c_veto_planes_hits.Draw()

c_us_planes_hits = ROOT.TCanvas("c_us_planes_hits")
h_us_planes.Draw()
c_us_planes_hits.Draw()

c_ds_planes_hits = ROOT.TCanvas("c_ds_planes_hits")
h_ds_planes.Draw()
c_ds_planes_hits.Draw()

c_energy = ROOT.TCanvas("c_energy")
h_energy.Draw()
c_energy.Draw()

c_scifi_vertical = ROOT.TCanvas("c_scifi_vertical")
h_scifi_vertical.Draw()
c_scifi_vertical.Draw()

c_scifi_horizontal = ROOT.TCanvas("c_scifi_horizontal")
h_scifi_horizontal.Draw()
c_scifi_horizontal.Draw()

c_ds_vertical = ROOT.TCanvas("c_ds_vertical")
h_ds_vertical.Draw()
c_ds_vertical.Draw()

c_ds_horizontal = ROOT.TCanvas("c_ds_horizontal")
h_ds_horizontal.Draw()
c_ds_horizontal.Draw()

c_x_hits = ROOT.TCanvas("c_x_hits")
h_x_hits.Draw()
c_x_hits.Draw()

c_y_hits = ROOT.TCanvas("c_y_hits")
h_y_hits.Draw()
c_y_hits.Draw()

c_z_hits = ROOT.TCanvas("c_z_hits")
h_z_hits.Draw()
c_z_hits.Draw()

c_x_hits_scifi = ROOT.TCanvas("c_x_hits_scifi")
h_x_hits_scifi.Draw()
c_x_hits_scifi.Draw()

c_y_hits_scifi = ROOT.TCanvas("c_y_hits_scifi")
h_y_hits_scifi.Draw()
c_y_hits_scifi.Draw()

c_z_hits_scifi = ROOT.TCanvas("c_z_hits_scifi")
h_z_hits_scifi.Draw()
c_z_hits_scifi.Draw()

c_x_hits_mufilter = ROOT.TCanvas("c_x_hits_mufilter")
h_x_hits_mufilter.Draw()
c_x_hits_mufilter.Draw()

c_y_hits_mufilter = ROOT.TCanvas("c_y_hits_mufilter")
h_y_hits_mufilter.Draw()
c_y_hits_mufilter.Draw()

c_z_hits_mufilter = ROOT.TCanvas("c_z_hits_mufilter")
h_z_hits_mufilter.Draw()
c_z_hits_mufilter.Draw()

c_x_hits_veto = ROOT.TCanvas("c_x_hits_veto")
h_x_hits_veto.Draw()
c_x_hits_veto.Draw()

c_y_hits_veto = ROOT.TCanvas("c_y_hits_veto")
h_y_hits_veto.Draw()
c_y_hits_veto.Draw()

c_z_hits_veto = ROOT.TCanvas("c_z_hits_veto")
h_z_hits_veto.Draw()
c_z_hits_veto.Draw()

c_x_hits_us = ROOT.TCanvas("c_x_hits_us")
h_x_hits_us.Draw()
c_x_hits_us.Draw()

c_y_hits_us = ROOT.TCanvas("c_y_hits_us")
h_y_hits_us.Draw()
c_y_hits_us.Draw()

c_z_hits_us = ROOT.TCanvas("c_z_hits_us")
h_z_hits_us.Draw()
c_z_hits_us.Draw()

c_x_hits_ds = ROOT.TCanvas("c_x_hits_ds")
h_x_hits_ds.Draw()
c_x_hits_ds.Draw()

c_y_hits_ds = ROOT.TCanvas("c_y_hits_ds")
h_y_hits_ds.Draw()
c_y_hits_ds.Draw()

c_z_hits_ds = ROOT.TCanvas("c_z_hits_ds")
h_z_hits_ds.Draw()
c_z_hits_ds.Draw()

c_us_sipm = ROOT.TCanvas("c_us_sipm")
h_us_sipm.Draw()
c_us_sipm.Draw()

c_us_small = ROOT.TCanvas("c_us_small")
h_us_small.Draw()
c_us_small.Draw()

'''c_incoming_x_zero = ROOT.TCanvas("c_incoming_x_zero")
h_incoming_x_zero.Draw()
c_incoming_x_zero.Draw()

c_incoming_y_zero = ROOT.TCanvas("c_incoming_y_zero")
h_incoming_y_zero.Draw()
c_incoming_y_zero.Draw()

c_incoming_z_zero = ROOT.TCanvas("c_incoming_z_zero")
h_incoming_z_zero.Draw()
c_incoming_z_zero.Draw()

c_incoming_xy_zero = ROOT.TCanvas("c_incoming_xy_zero")
h_incoming_xy_zero.Draw("COLZ")
c_incoming_xy_zero.Draw()

c_incoming_zy_zero = ROOT.TCanvas("c_incoming_zy_zero")
h_incoming_zy_zero.Draw("COLZ")
c_incoming_zy_zero.Draw()

c_incoming_zx_zero = ROOT.TCanvas("c_incoming_zx_zero")
h_incoming_zx_zero.Draw("COLZ")
c_incoming_zx_zero.Draw()'''

c_scifi_qdc = ROOT.TCanvas("c_scifi_qdc")
h_scifi_qdc.Draw("COLZ")
c_scifi_qdc.Draw()

c_scifi_qdc_station = {}
for i in range(1, 6):
    c_scifi_qdc_station[i] = ROOT.TCanvas(f"c_scifi_qdc_station{i}")
    h_scifi_qdc_station[i].Draw()
    c_scifi_qdc_station[i].Draw()

c_mufi_us_qdc = ROOT.TCanvas("c_mufi_us_qdc")
h_mufi_us_qdc.Draw("COLZ")
c_mufi_us_qdc.Draw()

c_mufi_us_qdc_plane = {}
for i in range(0, 5):
    c_mufi_us_qdc_plane[i] = ROOT.TCanvas(f"c_mufi_us_qdc_plane{i}")
    h_mufi_us_qdc_plane[i].Draw()
    c_mufi_us_qdc_plane[i].Draw()

c_scifi_energy_loss = ROOT.TCanvas("c_scifi_energy_loss")
h_scifi_energy_loss.Draw()
c_scifi_energy_loss.Draw()

c_scifi_energy_loss_total = ROOT.TCanvas("c_scifi_energy_loss_total")
h_scifi_energy_loss_total.Draw()
c_scifi_energy_loss_total.Draw()

c_z_scifi_energy_loss = ROOT.TCanvas("c_z_scifi_energy_loss")
h_z_scifi_energy_loss.Draw("COLZ")
c_z_scifi_energy_loss.Draw()
'''
c_mufi_energy_loss = ROOT.TCanvas("c_mufi_energy_loss")
h_mufi_energy_loss.Draw()
c_mufi_energy_loss.Draw()
'''
#c_scifi_energy_loss_station = {}
c_scifi_energy_loss_total_station = {}
for i in range(1, 6):
    '''c_scifi_energy_loss_station[i] = ROOT.TCanvas(f"c_scifi_energy_loss_station{i}")
    h_scifi_energy_loss_station[i].Draw()
    c_scifi_energy_loss_station[i].Draw()'''
    c_scifi_energy_loss_total_station[i] = ROOT.TCanvas(f"c_scifi_energy_loss_total_station{i}")
    h_scifi_energy_loss_total_station[i].Draw()
    c_scifi_energy_loss_total_station[i].Draw()
'''
c_mufi_veto_energy_loss = ROOT.TCanvas("c_mufi_veto_energy_loss")
h_mufi_veto_energy_loss.Draw()
c_mufi_veto_energy_loss.Draw()

c_mufi_veto_energy_loss_plane = {}
for i in range (0, 3):
    c_mufi_veto_energy_loss_plane[i] = ROOT.TCanvas(f"c_mufi_veto_energy_loss_plane{i}")
    h_mufi_veto_energy_loss_plane[i].Draw()
    c_mufi_veto_energy_loss_plane[i].Draw()
'''
c_mufi_us_energy_loss = ROOT.TCanvas("c_mufi_us_energy_loss")
h_mufi_us_energy_loss.Draw()
c_mufi_us_energy_loss.Draw()

#c_mufi_us_energy_loss_plane = {}
c_mufi_us_energy_loss_total_plane = {}
c_total_e_loss_scifi_us_plane = {}
for i in range (0, 5):
    '''c_mufi_us_energy_loss_plane[i] = ROOT.TCanvas(f"c_mufi_us_energy_loss_plane{i}")
    h_mufi_us_energy_loss_plane[i].Draw()
    c_mufi_us_energy_loss_plane[i].Draw()'''
    c_mufi_us_energy_loss_total_plane[i] = ROOT.TCanvas(f"c_mufi_us_energy_loss_total_plane{i}")
    h_mufi_us_energy_loss_total_plane[i].Draw()
    c_mufi_us_energy_loss_total_plane[i].Draw()
    c_total_e_loss_scifi_us_plane[i] = ROOT.TCanvas(f"c_total_e_loss_scifi_us_plane{i}")
    h_total_e_loss_scifi_us_plane[i].Draw()
    c_total_e_loss_scifi_us_plane[i].Draw()

c_mufi_us_energy_loss_total = ROOT.TCanvas("c_mufi_us_energy_loss_total")
h_mufi_us_energy_loss_total.Draw()
c_mufi_us_energy_loss_total.Draw()

c_z_us_energy_loss = ROOT.TCanvas("c_z_us_energy_loss")
h_z_us_energy_loss.Draw("COLZ")
c_z_us_energy_loss.Draw()
'''
c_mufi_ds_energy_loss = ROOT.TCanvas("c_mufi_ds_energy_loss")
h_mufi_ds_energy_loss.Draw()
c_mufi_ds_energy_loss.Draw()

c_mufi_ds_energy_loss_plane = {}
for i in range (0, 4):
    c_mufi_ds_energy_loss_plane[i] = ROOT.TCanvas(f"c_mufi_ds_energy_loss_plane{i}")
    h_mufi_ds_energy_loss_plane[i].Draw()
    c_mufi_ds_energy_loss_plane[i].Draw()
'''
c_scifi_us_energy_loss = ROOT.TCanvas("c_scifi_us_energy_loss")
h_scifi_us_energy_loss.Draw()
c_scifi_us_energy_loss.Draw()

output = ROOT.TFile("muonDIS_plots.root", "RECREATE")

h_incoming_xy.Write()
h_incoming_zy.Write()
h_incoming_zx.Write()

h_incoming_x.Write()
h_incoming_y.Write()
h_incoming_z.Write()

h_scifi_hits.Write()
h_mufilter_hits.Write()
h_mufilter_US_hits.Write()
h_mufilter_DS_hits.Write()
h_mufilter_veto_hits.Write()

h_scifi_stations.Write()
h_veto_planes.Write()
h_us_planes.Write()
h_ds_planes.Write()

h_energy.Write()

h_scifi_vertical.Write()
h_scifi_horizontal.Write()

h_ds_vertical.Write()
h_ds_horizontal.Write()

h_x_hits.Write()
h_y_hits.Write()
h_z_hits.Write()

h_x_hits_scifi.Write()
h_y_hits_scifi.Write()
h_z_hits_scifi.Write()

h_x_hits_mufilter.Write()
h_y_hits_mufilter.Write()
h_z_hits_mufilter.Write()

h_x_hits_veto.Write()
h_y_hits_veto.Write()
h_z_hits_veto.Write()

h_x_hits_us.Write()
h_y_hits_us.Write()
h_z_hits_us.Write()

h_x_hits_ds.Write()
h_y_hits_ds.Write()
h_z_hits_ds.Write()

h_us_sipm.Write()
h_us_small.Write()

'''h_incoming_x_zero.Write()
h_incoming_y_zero.Write()
h_incoming_z_zero.Write()

h_incoming_xy_zero.Write()
h_incoming_zy_zero.Write()
h_incoming_zx_zero.Write()
'''
h_scifi_qdc.Write()
for i in range(1, 6):
    h_scifi_qdc_station[i].Write()

h_mufi_us_qdc.Write()
for i in range(0, 5):
    h_mufi_us_qdc_plane[i].Write()

h_scifi_energy_loss.Write()
h_scifi_energy_loss_total.Write()
h_z_scifi_energy_loss.Write()
#h_mufi_energy_loss.Write()
for i in range(1, 6):
    #h_scifi_energy_loss_station[i].Write()
    h_scifi_energy_loss_total_station[i].Write()
'''h_mufi_veto_energy_loss.Write()
for i in range(0, 3):
    h_mufi_veto_energy_loss_plane[i].Write()'''   
h_mufi_us_energy_loss.Write()
h_mufi_us_energy_loss_total.Write()
h_z_us_energy_loss.Write()
for i in range(0, 5):
    #h_mufi_us_energy_loss_plane[i].Write()
    h_mufi_us_energy_loss_total_plane[i].Write()
    h_total_e_loss_scifi_us_plane[i].Write()
'''h_mufi_ds_energy_loss.Write()
for i in range(0, 4):
    h_mufi_ds_energy_loss_plane[i].Write()'''

h_scifi_us_energy_loss.Write()

output.Close()
