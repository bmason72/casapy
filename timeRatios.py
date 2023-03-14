
# 
# Routines to calculate ALMA array time ratios
#  bsm 2017~2020 
#
# originally based on a script by Eric Villard, off SCIREQ-766
#   oct2016
#


import os
import re
import sys
import glob
import math
import numpy
import itertools

cycle = 5
configs = '*'


def capRatios(tapers):
  return -1


def runTimeRatios(uvtapers,cfg_pair,usenull=False):
    """
    usenull = use null taper for 2nd in pair (assumes uvtapers[0] is null taper)
    """
    bl=getBaselineLengths()
    tsums2,tsums=getTaperedSums(bl,uvtapers)

    i=0
    print("cfg1   cfg2   t2/t1(perPtg)   t2/t1(mosaic)    nb1   nb2 taper")
    for this_pair in cfg_pair:

        tperptg,tmos,nb1,nb2 = compareTwoConfigs(tsums,tsums2,this_pair['bmind'],cfg1 = this_pair['cfgA'], diam_1 = this_pair['dA'],
                                                    cfg2 = this_pair['cfgB'], diam_2 = this_pair['dB'],usenull=usenull)
        cfg_pair[i]['tptg'] = tperptg
        cfg_pair[i]['tmos'] = tmos
        cfg_pair[i]['nb1'] = nb1
        cfg_pair[i]['nb2'] = nb2

        print(this_pair['cfgA'], this_pair['dA'],this_pair['cfgB'], this_pair['dB'],tperptg, "***",tmos,"***", nb1, nb2,this_pair['bmind'])
        i += 1
        
    return -1
 

# um why is lambda in there twice - answer: because the result is in meters
def arcsec2uv(arcsecTapers,lam = 0.003):
    """
    convert FWHM beams to corresponding Gaussian FWHM in aperture space (units of meters)
    assuming wavelength is lam [meters]
    """  
    uvTapers = 0.882 *lam /(arcsecTapers *3.1415/180.0/3600.0 * (lam/0.003))
    #uvTapers = 0.882 *lam /(arcsecTapers *3.1415/180.0/3600.0)
    return uvTapers

def compareTwoConfigs(tsums,tsums2,bmind,cfg1="alma.cycle7.1",diam_1 = 12.0, cfg2="aca.cycle7",diam_2 = 7.0,usenull=False):
    """
    compute integration time in config 2 / integ time in config 1, using provided effective number of baselines
    tsums: dictionary with sum squared weights
    cfg1, d_1 : name of cfg 1 and diam of antennas [meters]
    bmind tells you which element of tsums, tsums2 to use (each element is a sum of weights for a given taper)
    if cfg2 is 'tp', calculate the time ratio for total power (N_B = 0.5 effectively)
    usenull indicates to use the null taper for cfg2; null taper is assumed to be in tsums[0],tsums2[0]
    etc
    """

    nb1 = (tsums[cfg1][bmind])**2 / tsums2[cfg1][bmind]

    if cfg2 != 'tp':
      if not(usenull):
        nb2 = (tsums[cfg2][bmind])**2 / tsums2[cfg2][bmind]
      else:
        nb2 = (tsums[cfg2][0])**2 / tsums2[cfg2][0]
    else:
      print(" CAUTION: tp times are for a single antenna")
      nb2 = 0.5

    t2_t1_perPtg = ( nb1 / nb2) * (diam_1/diam_2)**4
    t2_t1_mosaic = t2_t1_perPtg / (diam_1/diam_2)**2

    return t2_t1_perPtg , t2_t1_mosaic,nb1,nb2


# input is baseline dictionary returned by getBaselineLengths-
#  tapers should also be a numpy array
#  tapers is fwhm illum in meters
def getTaperedSums(bl,tapers):
    tsums={}
    tsums2={}
    for i in bl.keys():
        # baseline distances -
        bldist = numpy.array(bl[i].values())
        tsums[i] = numpy.zeros(tapers.size)
        tsums2[i] = numpy.zeros(tapers.size)
        for j in range(tapers.size):
            tsums[i][j] = ((numpy.exp(-0.5 * bldist**2 / (tapers[j]/2.354)**2)).sum())
            tsums2[i][j] = ((numpy.exp(-1.0 * bldist**2 / (tapers[j]/2.354)**2)).sum())
    return tsums2,tsums

def demeanConfig(cfg,add_mean=None):
    # add_mean -- if specified will add this (3 element numpy array)
    #  to each position.

    # dict() is needed to make an actual copy-
    new_cfg = dict(cfg)
    station_list = cfg.keys()
    print(station_list)
    x1_vals = numpy.array([])
    x2_vals = numpy.array([])
    x3_vals = numpy.array([])
    if add_mean == None:
        for this_station in station_list:
            print(this_station)
            x1_vals=numpy.append(x1_vals,(float(cfg[this_station]['coord'][0])))
            x2_vals=numpy.append(x2_vals,(float(cfg[this_station]['coord'][1])))
            x3_vals=numpy.append(x3_vals,(float(cfg[this_station]['coord'][2])))
            print(x1_vals)
            x1_mn = numpy.mean(x1_vals)
            x2_mn = numpy.mean(x2_vals)
            x3_mn = numpy.mean(x3_vals)
    else: 
        # put the sign in here so add_mean gets added not subtracted
        x1_mn = -1.0*add_mean[0]
        x2_mn = -1.0*add_mean[1]
        x3_mn = -1.0*add_mean[2]
    for this_station in station_list:
        new_cfg[this_station]['coord'][0] = str(float(new_cfg[this_station]['coord'][0]) - x1_mn)
        new_cfg[this_station]['coord'][1] = str(float(new_cfg[this_station]['coord'][1]) - x2_mn)
        new_cfg[this_station]['coord'][2] = str(float(new_cfg[this_station]['coord'][2]) - x3_mn)
    new_cfg['coord_means'] = numpy.array([x1_mn,x2_mn,x3_mn])
    return new_cfg

def readConfigurationFiles():

    if cycle == '' or configs == '': return {}

    #cfgFiles = glob.glob(os.path.expanduser('./a*cycle5*.cfg'))
    cfgFiles = glob.glob(os.path.expanduser('./*.cfg'))

    cfgInfo = {}

    for i in range(len(cfgFiles)):

        cfgName = os.path.basename(cfgFiles[i]).replace('.cfg', '')
        #print("Reading "+cfgFiles[i])

        f = open(cfgFiles[i])
        fc = f.readlines()
        f.close()

        cfgInfo[cfgName] = {}

        for j in range(len(fc)):
    
            fc1 = fc[j].strip()

            #print fc1

            try:
              if fc1[0] == '#': continue
              fc1 = fc1.split()
              coordX = fc1[0]
              coordY = fc1[1]
              coordZ = fc1[2]
              padName = fc1[4]
            except:
              print(" ERROR! Bad line")
              print(fc[j])
              print("  in file: "+cfgFiles[i])
              break

            cfgInfo[cfgName][padName] = {}
            cfgInfo[cfgName][padName]['coord'] = [coordX, coordY, coordZ]

    return cfgInfo

def getBaselineLengths():

    cfgInfo = readConfigurationFiles()
    
    blInfo = {}
    
    for i in cfgInfo.keys():

        blInfo[i] = {}

        for j in itertools.combinations(cfgInfo[i].keys(), 2):

            dist2 = 0
            # BSM - this should probably be range(2) but for the ngvla config files i have
            #  the z dims are all zero so ok.... -- actually this is ok. 
            for k in range(2):
                dist2 += (float(cfgInfo[i][j[0]]['coord'][k]) - float(cfgInfo[i][j[1]]['coord'][k]))**2

            blInfo[i][j] = math.sqrt(dist2)

    return blInfo

def getUv():
    # bsm note - this returns *physical* baselines. to get uv coverage
    #  you need to add in mirror-reflected points (u,v) -> (-u,-v)
    cfgInfo = readConfigurationFiles()
    
    blInfo = {}
    
    for i in cfgInfo.keys():

        blInfo[i] = {}

        npoints = itertools.combinations(cfgInfo[i].keys(), 2)
        for j in npoints:
            distx = (float(cfgInfo[i][j[0]]['coord'][0]) - float(cfgInfo[i][j[1]]['coord'][0]))
            disty = (float(cfgInfo[i][j[0]]['coord'][1]) - float(cfgInfo[i][j[1]]['coord'][1]))
            blInfo[i][j] = numpy.array([distx,disty])


    return blInfo

def getBaselineStats():

    blInfo = getBaselineLengths()

    for i in sorted(blInfo.keys()):
    
        print( i, round(numpy.min(blInfo[i].values()), 1), round(numpy.mean(blInfo[i].values()), 1), round(numpy.max(blInfo[i].values()), 1))

def getConfigurationOverlap():

    blInfo = getBaselineLengths()
    
    for i in itertools.combinations(blInfo.keys(), 2):

        minBL = []
        maxBL = []

        for j in range(2):
            minBL.append(numpy.min(blInfo[i[j]].values()))
            maxBL.append(numpy.max(blInfo[i[j]].values()))

        if maxBL[1] > maxBL[0]:
            cfgComp = 0
            cfgExt = 1
        else:
            cfgComp = 1
            cfgExt = 0

        if re.search('^ACA*', i[cfgComp], re.IGNORECASE) != None:
            diaComp = 7
        else:
            diaComp = 12

        if re.search('^ACA*', i[cfgExt], re.IGNORECASE) != None:
            diaExt = 7
        else:
            diaExt = 12

        overlapComp = len(numpy.where(numpy.array(blInfo[i[cfgComp]].values()) >= minBL[cfgExt])[0])
        overlapExt = len(numpy.where(numpy.array(blInfo[i[cfgExt]].values()) <= maxBL[cfgComp])[0])
        try:
            timeRatio = ( 1.*overlapExt / overlapComp ) * ( 1.*diaExt / diaComp )**2
        except:
            timeRatio = 0

#         print 'compact = '+i[cfgComp]+' extended = '+i[cfgExt]
#         print 'overlap min/max [m]:', round(minBL[cfgExt], 1), round(maxBL[cfgComp], 1)
#         print 'number & fraction overlap [compact]:', overlapComp, round(1.0*overlapComp/len(blInfo[i[cfgComp]].values()), 4)
#         print 'number & fraction overlap [extended]:', overlapExt, round(1.0*overlapExt/len(blInfo[i[cfgExt]].values()), 4)
#         print 'time ratio', round(timeRatio, 3)
#         print ''

        print(i[cfgComp], i[cfgExt], round(timeRatio, 2))

def getPadLocations(myCfg):
    cfgInfo = readConfigurationFiles()
    xvals = numpy.array([])
    yvals = numpy.array([])
    if myCfg not in cfgInfo.keys():
        print(" **** ERROR: requested configuration file not found")
        return numpy.array(-1.0),numpy.array(-1.0)
    else:
        pads = cfgInfo[myCfg].keys()
        for this_pad in pads:
            xvals=numpy.append(xvals, (float(cfgInfo[myCfg][this_pad]['coord'][0])))
            yvals=numpy.append(yvals, (float(cfgInfo[myCfg][this_pad]['coord'][1])))
        return xvals,yvals

