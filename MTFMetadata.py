import subprocess
import re
import missingspecs
import backend

class MetaDataReader:
    def __init__(self):
        print "MetaDataReader for MTF initialized"
        self.Output = {"Duration" : -1,
                       "Resolution_H" : -1,
                       "Resolution_W" : -1 }
        
    def GetMetaData(self, filename):
        #Install ffmpeg
        probeOut = subprocess.Popen(["ffprobe", filename],
                                    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

        probe = []
        for x in probeOut.stdout.readlines():
            probe.append(x)
        #print probe
        self.Output["Duration"] = self.GetDuration(probe)        
        self.Output["Resolution_W"],self.Output["Resolution_H"] = self.GetResolution(probe)
        #print self.Output
        return self.Output
        
    def GetDuration(self, probeOutput):
        line = [x for x in probeOutput if "Duration" in x]
        return re.findall('[0-9][0-9]:[0-9][0-9]:[0-9][0-9]',line[0])[0]
    
    def GetResolution(self, probeOutput):
        lines = []
        for x in probeOutput:
            if "Stream" in x:
                lines.append(x)
        resset = False
        for line in lines:
            #print line,"-->",re.findall('[0-9][0-9]+x[0-9]+',line)
            resolution =  re.findall('[0-9][0-9]+x[0-9]+',line)
            if len(resolution) == 1:
                out = resolution[0].split('x')
                resset = True
            else:
                if resset == False:
                    out = ["1","1"]
        return out[0],out[1]


def resetForAllEntries(directory):
    reader = MetaDataReader()
    DB = backend.database(1,directory)
    for entry in DB.entrys:
        metaD = reader.GetMetaData(entry.getSpec("PATH"))
        print metaD
        entry.changeSpec("DURATION",metaD["Duration"])
        entry.changeSpec("WIDTH",metaD["Resolution_W"])
        entry.changeSpec("HEIGHT",metaD["Resolution_H"])
        #raw_input("next")
        #entry.changeSpec("DURATION",
    DB.saveDB()

def main():
    #output = reader.GetMetaData("/home/korbinian/jd2/Downloads/BLACKED.17.01.10.Kendra.Sunderland.And.Ana.Foxxx.mp4")
    resetForAllEntries("/media/truecrypt12/Video/")
    
if __name__ == '__main__':
    main()
