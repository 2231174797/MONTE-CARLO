import ROOT
import copy
ROOT.gROOT.SetBatch()

branches = ["MC_PT", "MC_ETA", "MC_PHI", "MC_E", "MC_PDGID", "RECO_NMU", "RECOMU_PT", "RECOMU_ETA", "RECOMU_PHI", "RECOMU_E", "RECOMU_CHARGE" ]



class genParticle:

    p4  = None
    pdgId = None

    def __init__(self, pt, eta, phi, e, pdgId):
        
        self.p4 = ROOT.TLorentzVector()
        self.p4.SetPtEtaPhiE(pt, eta, phi, e)
        self.pdgId = pdgId


class lepton:

    p4 = None
    pdgId = None
    charge = None

    def __init__(self, pt, eta, phi, e, charge):
        
        self.p4 = ROOT.TLorentzVector()
        self.p4.SetPtEtaPhiE(pt, eta, phi, e)
        self.pdfId = 13 * charge
        self.charge = charge




class Analyzer:

    leptons = []
    genparticles = []
    evtNum = -1
    

    evTree = None
    file = None
    fIn = None
    maxEvents = 1e10


    def __init__(self, file):

        self.file = file
        self.fIn = ROOT.TFile(file)

    def initTree(self, name):

        self.evTree = self.fIn.Get(name)

        # set only necessary branches to speed up
        self.evTree.SetBranchStatus("*", 0)
        for b in branches: self.evTree.SetBranchStatus(b, 1)



    def analyze(self): # override 

        pass

    def setMaxEvents(self, max):
    
        self.maxEvents = max


    def loop(self):

        if self.evTree == None: return
        totEvents = min(self.maxEvents, self.evTree.GetEntries())
        for i in range(0, totEvents+1):

            if i%1000 == 0:
                print "Loop over event %d/%d (%d%%)" % (i, totEvents, int(100*i/totEvents))
            
            self.evTree.GetEntry(i)
            self.fillEvent()
            
            self.analyze()


    def fillEvent(self):

        # reset variables
        del self.genparticles[:]
        del self.leptons[:]

        for i in range(0, len(self.evTree.MC_E)): # loop over all gen particles

            p = genParticle(self.evTree.MC_PT[i], self.evTree.MC_ETA[i], self.evTree.MC_PHI[i], self.evTree.MC_E[i], self.evTree.MC_PDGID[i])
            self.genparticles.append(p)


            

        for i in range(0, self.evTree.RECO_NMU): # loop over all RECO muons

            p = lepton(self.evTree.RECOMU_PT[i], self.evTree.RECOMU_ETA[i], self.evTree.RECOMU_PHI[i], self.evTree.RECOMU_E[i], self.evTree.RECOMU_CHARGE[i])
            self.leptons.append(p)




    def __del__(self):

        self.fIn.Close()

