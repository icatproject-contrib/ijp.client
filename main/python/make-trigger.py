#!/usr/bin/env python
import os

data = "/mnt/Octopus/Data/SingleMolecule4"
os.chdir(data)
mol = os.path.basename(data)

top = "20130214"

# Find datasets
cfgs = []
for root, dirs, files in os.walk(top):
    for file in files:
        if file == "dataset.cfg":
            cfgs.append(os.path.join(root, file))
            break
        elif file == "run.cfg": 
            cfgs.append(os.path.join(root, file))
            break

triggerdir = set()
checkfiles = set()         
# For each dataset generate the trigger files
for cfg in cfgs:
    cfgdict = {}
    with open (cfg, "r") as cfgfile:
        cfgdir = os.path.dirname(cfg)
        for line in cfgfile:
            line = line.partition(" ")
            name = line[0].strip()
            value = line[2].replace("\\", "/").strip()
            if value.startswith("[DATA]/"):
                value = value[7:]
                if not value.startswith(cfgdir):
                    if not os.path.exists(value):
                        print value, "referenced by", cfg, "does not exist"
                        sys.exit(1)
                    if not name.endswith("Dir"):
                        if name == "CheckImage":
                            checkfiles.add(value)
                        elif name not in cfgdict:
                            cfgdict[name] = {value}
                        else:
                            cfgdict[name].add(value)
                    else:
                        fname = os.path.join(value, os.path.basename(value)+".cfg")
                        if not os.path.exists(fname):
                            print fname, "referenced by", cfg, "does not exist"
                            sys.exit(1)
                        with open (fname, "r") as depfiles:
                            for line in depfiles:
                                line = line.partition(" ")
                                name = line[0].strip()
                                dvalue = os.path.join(value, line[2].strip())
                                if not os.path.exists(dvalue):
                                    print dvalue, "referenced by", cfg, "does not exist"
                                    sys.exit(1)
                                if name not in cfgdict:
                                    cfgdict[name] = {dvalue}
                                else:
                                    cfgdict[name].add(dvalue)
  

        
    
    triggerdir.add(os.path.dirname(cfg))           
    for typ in cfgdict:
        for entry in cfgdict[typ]:
            triggerdir.add(os.path.dirname(entry))

for t in triggerdir:
    contents = os.path.join(data, t)
    name = os.path.expanduser(os.path.join("~","triggers", mol + "_" + t.replace("/","_") + ".trigger"))
    with open (name, "w") as depfile:
        depfile.write(contents)
    print name


for t in checkfiles:
    contents = os.path.join(data, t)
    name =os.path.expanduser(os.path.join("~","triggers", mol + "_" + t.replace("/","_") + ".trigger"))
    with open (name, "w") as depfile:
        depfile.write(contents)
    print name

