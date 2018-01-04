import sys
import ROOT
import classes as c
ROOT.gROOT.SetBatch()



# This function is called when looping over each event
def analyze(self):

    # the event generator particles are accessible through self.genparticles (list of genparticle objects)
    for p in self.leptons:
    
        p4 = p.p4 # access to the Lorentzvector (see ROOT manual)
        pdfId = p.pdfId # particle ID for the paricle (muon = 13, Higgs = 25) http://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf

        # fill eta and pt histograms for muons only
        if abs(pdfId) == 13:
            
            gen_mu_pt.Fill(p4.Pt())
            gen_mu_eta.Fill(p4.Eta())

        
    # now we try to reconstruct the 4 leptons to the Higgs mass
    # we make an empty Lorentzvector and add all the muons to it
    higgs = ROOT.TLorentzVector()
    genMuFound = 0 # we need exactly 4 muons
    for p in self.leptons:

        if abs(p.pdfId) != 13: continue
        genMuFound += 1
        higgs += p.p4


    if genMuFound == 4:

        #print higgs.M() 
        gen_mass_h.Fill(higgs.M())
        
        
if __name__ == "__main__":

    c.Analyzer.analyze = analyze # override # do not remove

    ##### INITIALIZATION: define the file and event loop settings (see comments)

    # start the analyzer object: define the file were to run on
    analyzer = c.Analyzer("roottree_leptons_GluGluHToZZTo4L_M125_14TeV_powheg2_JHUgenV702_pythia8_noPU.root")

    # load the TTree in the file
    analyzer.initTree("HZZ4LeptonsAnalysis")

    # set here the maximum amount of events you want to run over (useful for debugging)
    # comment line if all events must be used
    #analyzer.setMaxEvents(50)


    ##### HISTOGRAMS: define all the histograms needed
    gen_mass_h = ROOT.TH1D("gen_mass_h", "Reconstructed Higgs mass (gen)", 50, 100, 150) # bins of 1 GeV
    gen_mu_pt = ROOT.TH1D("gen_mu_pt", "Muon pt (gen)", 50, 0, 500) # bins of 10 GeV
    gen_mu_eta = ROOT.TH1D("gen_mu_eta", "Eta distribution of muons (gen)", 100, -5, 5) # bins of .1 in eta

    ##### LOOP OVER ALL THE EVENTS
    # loop over all the events and execute the code in the analyze() function as defined above
    analyzer.loop()

    ##### WRITE HISTOGRAMS TO FILE: write each histo to file
    fOut = ROOT.TFile("output.root", "RECREATE")

    gen_mass_h.Write()
    gen_mu_eta.Write()
    gen_mu_pt.Write()

    fOut.Close()
