#
# 20jun14 RI (nrao) wrote initial script to compute fraction of failed phase solutions
#             for INT and INF tables, and RMS phases of the solutions, for ALMA PL data.
#             makes summary plot of the phase solutions for each project.
#
# 27jun14 BSM (nrao)
#             -migrate to stand-alone function that works for both INT and INF tables
#             -fix bandwidth output in table (output spw_widths not widths)
#             -remove nspw=4 assumption
#             -make default phase-cal src ID selection overridable
#             -capture plots and numbers to file output
#             -add phase RMS and # solutions to text output
#
# 25aug14 BSM (nrao) - write mapNarrowSpw() routine
#               implementing the heuristic in our ALMA memo (BSM, RI, S.Schnee) on low-snr phase calibration
#
# dec17 bsm - update to handle single-poln data.
#           - change name of output text file (beware of this, may break old scripts)
#
# apr2020 bsm - add modules for spw phase offset QA specifically
#

# old syntax-
#from lib_EVLApipeutils import getCalFlaggedSoln
# new syntax, as of Cycle 5-
from pipeline.hifv.heuristics.lib_EVLApipeutils import getCalFlaggedSoln
import analysisUtils as au
import pylab as pl
import glob
import re
import pickle

try:
    # pre CASA 6
    from taskinit import *
except:
    # CASA 6 - need to generalize this:
    execfile("/users/bmason/casapy/newTaskInit.py")

def calcAlmaPlPhaseSolStats(plDir=None,phaseField=None,outDir='./'):
#
# run calcOneTablePhases() on both INT and INF tables of all executions in an ALMA PL 
#  directory.
#
# optional inputs:
#  plDir -- ALMA pipeline directory (eg, the default below)
#  phaseField -- field ID to use for the phase calibrator (defaults to highest field id)
#  outDir -- defaults to './'
#
    if plDir == None:
        plDir = "/lustre/naasc/rindebet/pipeline/root/2012.1.00178.S_2014_06_09T18_42_17.215/SOUS_uid___A002_X684eb5_X3b/GOUS_uid___A002_X684eb5_X3c/MOUS_uid___A002_X684eb5_X3f/working/"

    # count the number of EBs in an ALMA pipeline directory
    #  and construct lists of INT and corresponding INF phase cal tables
    ##inttables=glob.glob(plDir+"*gfluxscale*solintint*tbl")
    inttables=glob.glob(plDir+"*solintint*tbl")
    neb=len(inttables)
    print(neb)
    inftables=glob.glob(plDir+"*solintinf*tbl")
    ##inftables=[]
    # construct the list of inftables from this
    ##for i in range(neb):
    ##    inftables.append(glob.glob(inttables[i].split("gfluxscale")[0]+"*solintinf.gpcal.tbl")[0])

    for i in range(neb):
        calcOneTablePhases(inttables[i],solnTag='INT',phaseField=phaseField,outDir=outDir)
        calcOneTablePhases(inftables[i],solnTag='INF',phaseField=phaseField,outDir=outDir)

def calcAlmaManPlPhaseSolStats(plDir=None,phaseField=None,outDir='./'):
#
# run calcOneTablePhases() on both INT and INF tables of all executions in an ALMA Manual PL 
#  reduction directory. The difference between manual pipeline and automatic one is that
#  the calibration tables for the manual pipeline are generated for the split data set 
#  (sci spws only)
#
# optional inputs:
#  plDir -- ALMA manual pipeline reduction directory (eg, the default below)
#  phaseField -- field ID to use for the phase calibrator (defaults to highest field id)
#  outDir -- defaults to './'
#
    if plDir == None:
        plDir = "/lustre/naasc/bmason/datareduc/scops-119/cal_X340/"

    # count the number of EBs in an ALMA pipeline directory
    #  and construct lists of INT and corresponding INF phase cal tables
    inttables=glob.glob(plDir+"*ms.split.phase_int")
    neb=len(inttables)
    inftables=glob.glob(plDir+"*ms.split.phase_inf")

    for i in range(neb):
        calcOneTablePhases(inttables[i],solnTag='INT',phaseField=phaseField,outDir=outDir,manPl=True)
        calcOneTablePhases(inftables[i],solnTag='INF',phaseField=phaseField,outDir=outDir,manPl=True)

def mapNarrowSpw(ms,useSpwZero=False,bwbreak=0.3):
#
# Input: MS name
#
# Optional Input: 
#  useSpwZero -- use spw0: should be False (the default) for Pipeline reductions
#     since the Pipeline sometimes produces a bogus spw0.
#     if you are using this routine on a split'ted MS (eg from the manual pipeline)
#     you may want to set it to true.
#  bwbreak -- upper limit in bandwidth defining what is a "narrow" SPW that will
#     get mapped, in MHz.
#
# Return: spwmap as a numpy array object.
#

    #-----------------------
    # get science spws for this EB
    v=au.ValueMapping(ms)
    scispws=pl.array(v.getSpwsForIntent("OBSERVE_TARGET#ON_SOURCE"))
    # sometimes the Pipeline MS has a bogus spw-
    if (scispws[0]==0 and not(useSpwZero)):
        scispws=scispws[1:]
    widths=pl.zeros(len(scispws))
    freqs=pl.zeros(len(scispws))
    for j in range(len(scispws)):
        widths[j]=v.spwInfo[scispws[j]]['bandwidth']/1e9
        freqs[j]=v.spwInfo[scispws[j]]['meanFreq']/1e9
        # filter out the TP-only spw's
        if len(v.spwInfo[scispws[j]]['chanFreqs'])<2: 
            widths[j]=-1            
    z=pl.where(widths>0)[0]
    scispws=scispws[z]
    spw_widths=widths[z]
    spw_freqs=freqs[z]

    # count unique SPW ID's
    nspw=len(scispws)
   
    print("Sci Spw BW/GHz: ",spw_widths)
    print("Sci Spw center freq/GHz: ",spw_freqs)

    spwmap=pl.arange(nspw)

    # and is not elementwise ; & (bitwise and) is; you can also use np.logical_and for element wise ops

    bigband=0.8*spw_widths.max()

    for j in range(nspw):
        if (spw_widths[j] < bwbreak):
            # i worry about spw_widths being very close but not exactly equal
            #   eg, vel-frame issues... put fudge factor of 1.1 in - 
            # list of channel indices -- assume as should be the case that spw_widths has 1D only:
            gchind= (((spw_widths>bigband)&(spw_widths>1.1*spw_widths[j])).nonzero())[0]
            if (len(gchind) > 0):
                df=pl.absolute(spw_freqs[gchind] - spw_freqs[j])
                bestchind=pl.where(df==df.min())
                # in case there were multiple equally good matches choose the 1st one-
                spwmap[j]=gchind[bestchind[0]]

            # remind myself how to do it with boolean indexing instead-
            #gchmask= (spw_widths>bigband)&(spw_widths>1.1*spw_widths[j])
            #if (gchmask.any()):
            #    df=pl.absolute(spw_freqs[gchmask] - spw_freqs[j])
            #    bestchind=pl.where(df==df.min())
            #    spwmap[j]=(pl.where(gchmask))[0][bestchind[0]]
            #     spwmap[j]=mygoodchanind[bestchind[0]]

    print("FINAL SPWMAP: ",spwmap)

    return spwmap

def calcOneTablePhases(table,ms=None,phaseField=None,solnTag='',outDir='./',manPl=False):
#
# calculate phase solution stats (RMS of phase solution, fraction failed, and # of solutions)
#  for INF and INT phase cal solutions on the phase calibrator in a given directory.
#
# INPUTS
#  table -- calibration table
# OPTIONAL INPUTS
#  ms -- if not provided, guess from the table name, assuming the table name is contructed
#         per ALMA conventions
#  phaseField -- field ID to use for phase calibrator selection (default to highest field ID in ea execution)
#  solnTag -- a string to embed in file output names and annotate the plots with (eg 'INT' or 'INF' or whatever)
#  outDir -- directory to write plots and text output to
#  manPl -- look at tables named *.ms.split and don't ignore spw 0
#       **note: i'm not positive the flags are getting gotten correctly in the manPl=True case
#

    tb=casac.table()

    # if the ms name was not passed in, guess it from the table name
    if ms == None:
        ms=table.split(".ms")[0]+".ms"
    if manPl:
        ms=ms+".split"

    tb.open(table)
    field=tb.getcol("FIELD_ID")
    time=tb.getcol("TIME")
    gain=tb.getcol("CPARAM")
    ant=tb.getcol("ANTENNA1")
    flag=tb.getcol("FLAG")
    spw=tb.getcol("SPECTRAL_WINDOW_ID")
    scan=tb.getcol("SCAN_NUMBER")
    tb.done()

    n_pol = gain.shape[0]

    # set up plot
    pl.clf()
    font={'size':12}
    pl.rc('font', **font)

    # default to the phase cal being the highest field ID
    if phaseField == None:
        phaseField=max(field)

    # a long time ago (very pre- Cycle 5) this used to work--
    #flags=getCalFlaggedSoln(table,field=phaseField)
    flags=getCalFlaggedSoln(table)

    #-----------------------
    # get science spws for this EB
    v=au.ValueMapping(ms)
    scispws=pl.array(v.getSpwsForIntent("OBSERVE_TARGET#ON_SOURCE"))
    # sometimes it gets a bogus spw
    if (scispws[0]==0 and not(manPl)):
        scispws=scispws[1:]
    widths=pl.zeros(len(scispws))
    freqs=pl.zeros(len(scispws))
    # dec2017 - the list of windows returned by v.getSpwsForIntent and v.spwInfo() doesn't always agree
    #  anymore.  explicitly test for membership and flag windows appropriately.
    spw_set=set(v.spwInfo.keys())
    for j in range(len(scispws)):
        if (set([scispws[j]]).issubset(spw_set)):
            widths[j]=v.spwInfo[scispws[j]]['bandwidth']/1e9
            freqs[j]=v.spwInfo[scispws[j]]['meanFreq']/1e9
            # filter out the TP-only spw's
            if len(v.spwInfo[scispws[j]]['chanFreqs'])<2: 
                widths[j]=-1
        else:
            widths[j]=-1
    z=pl.where(widths>0)[0]
    scispws=scispws[z]
    spw_widths=widths[z]
    spw_freqs=freqs[z]

    # count unique SPW ID's
    nspw=len(scispws)

    # identify "good" antennas by their flag fraction across _all_ spws
    median=flags['antmedian']['fraction']
    # take ants which have less flagging than 2xmedian, or if that's zero, less than 10%
    maxflaglevel=max([0.1,2*median])
    #-----------------------
    # collect flag levels by ant and spw
    # in case of skipped ant indices in dict, set all levels to 1 to start
    flaglevelbyant=pl.zeros((nspw,max(flags['ant'].keys())+2))+10.

    # also open table to calculate phase angle for rms
    # angle lists
    dang=[[] for _ in range(nspw)]

    flagfrac=pl.zeros(nspw)
    rms=pl.zeros(nspw)
    ndata=pl.zeros(nspw)

    # define an array of symbols to use, one for each spw (more than we're likely to need)
    psyms=['o','^','*','+','1','2','3','4','8','s','p']

    print(nspw)
    print(scispws)

    for ispw in range(nspw):
        # loop over antennas present in each spw
        if flags['antspw'][flags['ant'].keys()[0]].has_key(scispws[ispw]):
            for iant in flags['ant'].keys():
                # bsm dec2017 - now allow for singleton returns (one IF / T soln)-
                #if (len(flags['antspw'][iant][scispws[ispw]]) > 1):
                if (n_pol >1):
                    flaglevelbyant[ispw,iant] = \
                                                max([flags['antspw'][iant][scispws[ispw]][0]['fraction'],
                                                     flags['antspw'][iant][scispws[ispw]][1]['fraction']])
                else:
                    flaglevelbyant[ispw,iant] = flags['antspw'][iant][scispws[ispw]][0]['fraction']
            goodants = pl.where(flaglevelbyant[ispw,:]<maxflaglevel)[0]
            # convert to percent
            flagfrac[ispw] = \
                pl.average(flaglevelbyant[ispw,goodants])*100 

            zk=[]
            for k in pl.array(flags['ant'].keys())[goodants]:
                if (n_pol > 1):
                    znk=pl.where((field==phaseField)*(spw==scispws[ispw])*(flag[0,0,:]==False)*(flag[1,0,:]==False)*(ant==k))[0]
                else:
                    znk=pl.where((field==phaseField)*(spw==scispws[ispw])*(flag[0,0,:]==False)*(ant==k))[0]

                if len(znk)>0:
                    # average angle: normalize, vector ave, take angle
                    # of the result.  
                    # TODO is the complex difference of gains a better
                    # measure than the angle difference?
                    #  bsm dec 2017 - add support for T solns ie single poln
                    if (n_pol > 1): 
                        # bsm - this was what was here. seems weird. amps up rms by root 2?
                        dang0=pl.angle(gain[0,0,znk.astype('int')])-pl.angle(gain[1,0,znk.astype('int')])
                    else:
                        # bsm - original implementation. not what we want: we want the straight rms, no mean or median removed.
                        #       this will give you a metric w.r.t. a phase that's expected to be zero, which is relevant
                        #       for instance to spw-phased-up phases, or to final 'ap' phases....
                        #dang0=pl.angle(gain[0,0,znk.astype('int')])-pl.nanmedian(gain[0,0,znk.astype('int')])
                        dang0=pl.angle(gain[0,0,znk.astype('int')])
                    # I think the subtraction will work better if  
                    # first restricted to -180,180
                    z=pl.where(dang0>pl.pi)[0]
                    if len(z)>0: dang0[z]=dang0[z]-2*pl.pi
                    z=pl.where(dang0<-pl.pi)[0]
                    if len(z)>0: dang0[z]=dang0[z]+2*pl.pi
                    dvec0=pl.exp((1j)*dang0)
                    dang0mean=pl.angle(dvec0.mean())
                    dang0=dang0-dang0mean

                    z=pl.where(dang0>pl.pi)[0]
                    if len(z)>0: dang0[z]=dang0[z]-2*pl.pi
                    z=pl.where(dang0<-pl.pi)[0]
                    if len(z)>0: dang0[z]=dang0[z]+2*pl.pi
                    dang[ispw]=pl.concatenate((dang[ispw],dang0*180/pl.pi))
                    zk=pl.concatenate((zk,znk))

            my_nums = pl.array(dang[ispw])
            my_finite_nums = my_nums[pl.isfinite(my_nums)]
            rms[ispw] = pl.rms_flat(my_finite_nums)
            ndata[ispw]= len(my_finite_nums)
            print(ispw,ndata[ispw])
            pl.plot(dang[ispw],psyms[ispw % len(psyms)],label="%d rms=%4.1f flg=%4.1f" % (scispws[ispw],rms[ispw],flagfrac[ispw]))

    # annotate plot & capture hard copy of it
    # bsm dec2017 - change out file to table which is much smarter than ms!
    #outfNameRoot = outDir+ms.split("/")[-1]+solnTag+'phaseSolns'
    outfNameRoot = outDir+table.split("/")[-1]+'-Fld'+str(phaseField)+'-'+solnTag+'-phaseStats'
    pl.title(ms.split("/")[-1]+solnTag)
    pl.legend(prop={'size':7})
    pl.savefig(outfNameRoot+'.png')

    # write numbers to file and stdout
    fh=open(outfNameRoot+'.txt','w')
    mystr="# %25s %s nwin "% (' ',ms)
    for i in range(nspw): mystr+="  %6.0fMHz(%2i)   " % (spw_widths[i]*1000,scispws[i])
    for i in range(nspw): mystr+="  %10s %12s  " % ('BW/MHz','CFreq/GHz')  
    print(mystr)
    fh.write(mystr+'\n')   
    mystr="%18s %s-flag" % (' ',solnTag)
    mystr+=" %3i " % nspw
    for i in range(nspw): mystr+="  %8.1f pct  " % (flagfrac[i])
    for i in range(nspw): mystr+="  %6.0f %8.2f " % (spw_widths[i]*1000,spw_freqs[i])
    print(mystr)
    fh.write(mystr+'\n')
    mystr="%19s %s-rms"%(" ",solnTag)
    mystr+=" %3i " % nspw
    for i in range(nspw): mystr+="  %8.1f deg  " % (rms[i])
    for i in range(nspw): mystr+="  %6.0f %8.2f  " % (spw_widths[i]*1000,spw_freqs[i])
    print(mystr)
    fh.write(mystr+'\n')
    mystr="%21s %s-N" %(" ",solnTag)
    mystr+=" %3i " % nspw
    for i in range(nspw): mystr+="  %11i  " % (ndata[i])
    for i in range(nspw): mystr+="  %6.0f %8.2f  " % (spw_widths[i]*1000,spw_freqs[i])
    print(mystr)
    fh.write(mystr+'\n')
    fh.close()

#from pipeline.hifv.heuristics.lib_EVLApipeutils import getCalFlaggedSoln

def calcOneTablePhaseStats(table='',phaseField='',solnTag='',outDir=''):
  """
  Improved version of calcOneTablePhases. operates sensibly on single or dual pol solutions
  returns results in a dictionary.
  """

  #solnTag="test"
  #outDir="./"
  manPl=False

  ms=table.split(".ms")[0]+".ms"

  # default to the phase cal being the highest field ID
  if phaseField == '' or phaseField == None:
      all_phasecals = au.getPhaseCalibrators(vis=ms)
      if (len(all_phasecals) > 1):
          print("***** WARNING multiple phase cals found using the lowest one")
          phaseField = pl.amin(all_phasecals)
      else:
          phaseField = all_phasecals[0]

  if (len(outDir) > 0):
      outfNameRoot = outDir+table.split("/")[-1]+'-Fld'+str(phaseField)+'-'+solnTag+'-phaseStats'  

  tb.open(table)
  field=tb.getcol("FIELD_ID")
  time=tb.getcol("TIME")
  gain=tb.getcol("CPARAM")
  ant=tb.getcol("ANTENNA1")
  flag=tb.getcol("FLAG")
  spw=tb.getcol("SPECTRAL_WINDOW_ID")
  scan=tb.getcol("SCAN_NUMBER")
  snr=tb.getcol("SNR")
  tb.done()

  n_ant = len(ant[pl.unique(ant)])
  n_pol = gain.shape[0]
  print(" # ant / # pol: ",str(n_ant)," " ,str(n_pol))

  if (n_pol > 1):
      print("**** WARNING: n_pol > 1!!! Expect offset table to be a T solution")
      print(table)

  # set up plot
  #pl.clf()
  #font={'size':12}
  #pl.rc('font', **font)

  # note: v.antennaNamesForAntennaIds[3] etc

  #flags=getCalFlaggedSoln(table,field=phaseField)
  flags=getCalFlaggedSoln(table)

  #-----------------------
  # get science spws for this EB
  v=au.ValueMapping(ms)
  scispws=pl.array(v.getSpwsForIntent("OBSERVE_TARGET#ON_SOURCE"))
  # sometimes it gets a bogus spw
  if (scispws[0]==0 and not(manPl)):
      scispws=scispws[1:]
  widths=pl.zeros(len(scispws))
  freqs=pl.zeros(len(scispws))
  # dec2017 - the list of windows returned by v.getSpwsForIntent and v.spwInfo() doesn't always agree
  #  anymore.  explicitly test for membership and flag windows appropriately.
  spw_set=set(v.spwInfo.keys())
  for j in range(len(scispws)):
    if (set([scispws[j]]).issubset(spw_set)):
        widths[j]=v.spwInfo[scispws[j]]['bandwidth']/1e9
        freqs[j]=v.spwInfo[scispws[j]]['meanFreq']/1e9
        # filter out the TP-only spw's 
        if len(v.spwInfo[scispws[j]]['chanFreqs'])<2: 
            widths[j]=-1
    else:
        widths[j]=-1
  z=pl.where(widths>0)[0]
  scispws=scispws[z]
  spw_widths=widths[z]
  spw_freqs=freqs[z]
  # count unique SPW ID's
  nspw=len(scispws)

  # identify "good" antennas by their flag fraction across _all_ spws
  median=flags['antmedian']['fraction']
  # take ants which have less flagging than 2xmedian, or if that's zero, less than 10%
  maxflaglevel=max([0.1,2*median])
  #-----------------------
  # collect flag levels by ant and spw
  # in case of skipped ant indices in dict, set all levels to 1 to start
  flaglevelbyant=pl.zeros((nspw,max(flags['ant'].keys())+2))+10.

  # also open table to calculate phase angle for rms
  # angle lists
  dang=[[] for _ in range(nspw)]

  # index as mean_phase[spw][ant][pol]-
  #mean_phase = [ [[[] for _ in range(n_pol)] for _ in range(n_ant)] for _ in range(nspw)]
  #rms_phase = [ [[[] for _ in range(n_pol)] for _ in range(n_ant)] for _ in range(nspw)]
  mean_phase=pl.zeros([nspw,n_ant,n_pol])
  rms_phase=pl.zeros([nspw,n_ant,n_pol])
  max_phase=pl.zeros([nspw,n_ant,n_pol])
  med_snr = pl.zeros([nspw,n_ant,n_pol])
  
  is_valid = pl.zeros([nspw,n_ant,n_pol])
  nDataAntSpwPol = pl.zeros([nspw,n_ant,n_pol])
  all_phases=[ [] for _ in range(nspw)]
  all_snrs=[ [] for _ in range(nspw)]
  spw_phase_rms = pl.zeros(nspw)

  flagfrac=pl.zeros(nspw)
  rms=pl.zeros(nspw)
  ndata=pl.zeros(nspw)
  spw_snr=pl.zeros(nspw)

  # define an array of symbols to use, one for each spw (more than we're likely to need)
  psyms=['o','^','*','+','1','2','3','4','8','s','p']

  print(" NSPWs, sciSPWs: ",str(nspw)," ",str(scispws))

  for ispw in range(nspw):
      # loop over antennas present in each spw
      if flags['antspw'][flags['ant'].keys()[0]].has_key(scispws[ispw]):
          for iant in flags['ant'].keys():
              # bsm dec2017 - now allow for singleton returns (one IF / T soln)-
              #if (len(flags['antspw'][iant][scispws[ispw]]) > 1):
              if (n_pol >1):
                  flaglevelbyant[ispw,iant] = \
                                              max([flags['antspw'][iant][scispws[ispw]][0]['fraction'],
                                                   flags['antspw'][iant][scispws[ispw]][1]['fraction']])
              else:
                  flaglevelbyant[ispw,iant] = flags['antspw'][iant][scispws[ispw]][0]['fraction']
          goodants = pl.where(flaglevelbyant[ispw,:]<maxflaglevel)[0]
          print("Ngoodants: ",str(len(goodants))," SPW ",str(scispws[ispw]))
          # convert to percent
          flagfrac[ispw] = \
              pl.average(flaglevelbyant[ispw,goodants])*100 


          zk=[]
          # loop over ant, pol and calculate phase solution stats
          for k in pl.array(flags['ant'].keys())[goodants]:
            for pp in range(n_pol):
              znk=pl.where((field==phaseField)*(spw==scispws[ispw])*(flag[pp,0,:]==False)*(ant==k))[0]
              if len(znk)>0:
                  # phases of the requested field, spw, ant,pol solns-
                  this_phase=pl.angle(gain[pp,0,znk.astype('int')])
                  # ensure that the solutions are sorted in increasing scan order
                  these_scans = scan[znk]
                  this_snr = snr[pp,0,znk.astype('int')]
                  scan_sort_ind = pl.argsort(these_scans)
                  these_scans = these_scans[scan_sort_ind]
                  this_phase = this_phase[scan_sort_ind]
                  # skip unwrapping, it causes problems at v.high noise-
                  #unwrapped_phase = pl.unwrap(this_phase) * 180.0/pl.pi
                  unwrapped_phase = this_phase * 180.0/pl.pi
                  mean_phase[ispw,k,pp] = unwrapped_phase.mean() 
                  rms_phase[ispw,k,pp] = pl.std(unwrapped_phase)
                  max_phase[ispw,k,pp] = pl.amax(pl.absolute(unwrapped_phase))
                  med_snr[ispw,k,pp] = pl.median(this_snr)
                  is_valid[ispw,k,pp] = 1
                  nDataAntSpwPol[ispw,k,pp] = len(znk)
                  all_phases[ispw] = pl.concatenate((all_phases[ispw],list(unwrapped_phase)))
                  all_snrs[ispw] = pl.concatenate((all_snrs[ispw],list(this_snr)))

  spw_avg_phase = pl.zeros([nspw])
  all_phases = pl.array(all_phases)
  #spw_avg_phase = pl.median(all_phases,axis=1)
  for i in range(nspw):
      spw_avg_phase[i] = pl.median(all_phases[i])
      spw_phase_rms[i] = au.MAD(all_phases[i])
      spw_snr[i]=pl.median(all_snrs[i])

  #results = {'scispws':scispws,'freq':spw_freqs,'width':spw_widths,'npol':n_pol,'nant':n_ant,'nDataAntSpwPol': nDataAntSpwPol,
  #           'meanPhaseAntSpw':mean_phase,'rmsPhaseAntSpw':rms_phase,'rmsPhaseSpw':spw_phase_rms,
  #           'flagFracSpw':flagfrac,'valueMapping':v,'isValid':is_valid,'tableName':table,'phaseField':phaseField}

  results = {'scispws':scispws,'freq':spw_freqs,'width':spw_widths,'npol':n_pol,'nant':n_ant,'nDataAntSpwPol': nDataAntSpwPol,
             'meanPhaseAntSpw':mean_phase,'rmsPhaseAntSpw':rms_phase,'rmsPhaseSpw':spw_phase_rms,'maxPhaseAntSpw': max_phase,
             'flagFracSpw':flagfrac,'valueMapping':v.antennaNamesForAntennaIds,'isValid':is_valid,'tableName':table,
             'phaseField':phaseField,'spw_snr':spw_snr,'med_snr':med_snr}

  # write numbers to file and stdout
  if (len(outDir) > 0):
    print(" OPENING "+outfNameRoot+".txt")
    fh=open(outfNameRoot+'.txt','w')
    fh.write("# "+table+'\n')
    mystr="# %25s %s nwin "% (' ',ms)
    for i in range(nspw): mystr+="  %6.0fMHz(%2i)   " % (spw_widths[i]*1000,scispws[i])
    for i in range(nspw): mystr+="  %10s %12s  " % ('BW/MHz','CFreq/GHz')  
    print(mystr)
    fh.write(mystr+'\n')   
    mystr="%18s %s-flag" % (' ',solnTag)
    mystr+=" %3i " % nspw
    for i in range(nspw): mystr+="  %8.1f pct  " % (flagfrac[i])
    for i in range(nspw): mystr+="  %6.0f %8.2f " % (spw_widths[i]*1000,spw_freqs[i])
    print(mystr)
    fh.write(mystr+'\n')
    mystr="%19s %s-rms"%(" ",solnTag)
    mystr+=" %3i " % nspw
    for i in range(nspw): mystr+="  %8.1f deg  " % (spw_phase_rms[i])
    for i in range(nspw): mystr+="  %6.0f %8.2f  " % (spw_widths[i]*1000,spw_freqs[i])
    print(mystr)
    fh.write(mystr+'\n')
    mystr="%21s %s-N" %(" ",solnTag)
    mystr+=" %3i " % nspw
    for i in range(nspw): mystr+="  %11i  " % (ndata[i])
    for i in range(nspw): mystr+="  %6.0f %8.2f  " % (spw_widths[i]*1000,spw_freqs[i])
    fh.close()
    print(" SAVING raw results ")
    fh2=open(outfNameRoot+'.pkl',"wb")
    pickle.dump(results,fh2)
    fh2.close()

  return results

def doSpwPhaseQa(phaseStatDict,outdir=''):
  # threshold in deg
  #S0info = 2.0
  #S0warn = 5.0
  #Finfo = 5.0
  #Fwarn = 5.0
  #Ginfo = 5.0
  #Gwarn = 5.0

  #results = {'scispws':scispws,'freq':spw_freqs,'width':spw_widths,'npol':n_pol,nant:n_ant,
  #           'meanPhaseAntSpw':mean_phase,'rmsPhaseAntSpw':rms_phase,'rmsPhaseSpw':spw_phase_rms,
  #           'flagFracSpw':flagfrac,'valueMapping':v}

  nspw = len(phaseStatDict['scispws'])
  spw_phase_rms = phaseStatDict['rmsPhaseSpw']
  n_pol = phaseStatDict['npol']
  n_ant = phaseStatDict['nant']
  is_valid = phaseStatDict['isValid']
  mean_phase = phaseStatDict['meanPhaseAntSpw']
  rms_phase = phaseStatDict['rmsPhaseAntSpw']
  max_phase = phaseStatDict['maxPhaseAntSpw']
  scispws = phaseStatDict['scispws']
  valueMapping = phaseStatDict['valueMapping']
  table = phaseStatDict['tableName']
  nDataAntSpwPol = phaseStatDict['nDataAntSpwPol']

  mousName = (table.split("MOUS_uid___"))[-1].split('/')[0]
  # ebName = (mousName.split("working/"))[-1]
  ebName = table.split("MOUS_uid___")[-1].split("working/")[1].split(".ms")[0]
  #search for project in table name...
  projName = "NoProj"
  m=re.search("20[1,2,3][0-9]\..\.[0-9][0-9][0-9][0-9][0-9]\..",table)
  if (m != None):
    projName = m.group(0)
  m=re.search("E2E[0-9]\..\.[0-9][0-9][0-9][0-9][0-9]\..",table)
  if (m != None):
    projName = m.group(0)

  if (len(outdir) > 0):
      #outfNameRoot = outdir+table.split("/")[-1]+'-Fld'+str(phaseField)+'-spwPhaseQAInfo'  
      #outfNameRoot = outdir+table.split("/")[-1]+'-spwPhaseQAInfo'  
      outfNameRoot = outdir+projName+"_"+mousName+"_"+ebName+"-spwPhaseQAInfo" 
      fh=open(outfNameRoot+'.txt','w')
      doFile=True
  else:
    doFile=False

  mystring = projName + " " + mousName + " " + ebName
  print(mystring)
  if (doFile): fh.write(mystring+'\n')

  print("# Mean, RMS spwRms (RMS/spwRms) max (max/RMS) for each SPW, Ant, {Pol}")
  for antind in range(n_ant):
    for spwind in range(nspw):
      for polind in range(n_pol):
        mystr = "# "+valueMapping[antind]+" SPW"+str(scispws[spwind])
        mystr+= " "+str(polind)
        mystr+= " "+str(mean_phase[spwind,antind,polind])+' , '+str(rms_phase[spwind,antind,polind]) + '   '+str(spw_phase_rms[spwind]) + ' (' + str(rms_phase[spwind,antind,polind]/spw_phase_rms[spwind])+') ' + str(max_phase[spwind,antind,polind]) + ' ('+str(max_phase[spwind,antind,polind]/rms_phase[spwind,antind,polind])+')'
        print(mystr)
        if (doFile and is_valid[spwind,antind,polind]): fh.write(mystr+'\n')

  print(" Evaluating SPW Phase Offset QA For Table: ",phaseStatDict['tableName'])

  antSpwQaScore = pl.ones([nspw,n_ant,n_pol])
  # bsm NEW-
  antSpwDataSufficient = pl.ones([nspw,n_ant,n_pol])
  for spwind in range(nspw):
      good_data = True
      # 15 deg threshold is SNR~3 per solution. it is also about where we start failing
      #  to detect 60 deg mean spw phase offsets when we have 2 solutions.
      if spw_phase_rms[spwind] > 15.0:
          good_data = False
          mystring = "QQ NOTICE: phase noise generally too high to evaluate SPW relative phase stability"+ projName+" "+mousName+" "+ebName+" spw: "+str(scispws[spwind])
          print(mystring)
          fh.write(mystring+'\n')
      # write message here. 
      for antind in range(n_ant):
          for polind in range(n_pol):
              # propagate the score to each ant/spw/pol if the phase RMS was high-
              if (not(good_data) and is_valid[spwind,antind,polind]):
                  antSpwQaScore[spwind,antind,polind] =  0.8
              elif is_valid[spwind,antind,polind]: 
                  skip_rms = False
                  # require at least 4 data points 
                  ndata = nDataAntSpwPol[spwind,antind,polind]
                  if ndata < 4:
                      skip_rms = True
                      # bsm NEW
                      antSpwDataSufficient[spwind,antind,polind] = 0.8
                  #if (skip_rms):
                      #antSpwQaScore[spwind,antind,polind] = 0.8
                      #mystring = "QQ NOTICE: insufficient data to fully evaluate SPW Phase Offsets for "+ projName+" "+mousNa  me+" "+ebName+" spw: "+str(scispws[spwind])+" "+str(valueMapping[antind])+" pol: "+str(polind)
                      #print mystring
                      #fh.write(mystring+'\n')

                  mn_info_thresh = pl.amax([6.0*spw_phase_rms[spwind]/(ndata)**0.5,15.0])
                  mn_warn_thresh = pl.amax([6.0*spw_phase_rms[spwind]/(ndata)**0.5,30.0])
                  rms_info_thresh = pl.amax([2.0*spw_phase_rms[spwind],15.0])
                  rms_warn_thresh = pl.amax([4.0*spw_phase_rms[spwind],30.0])
                  max_info_thresh = pl.amax([6.0*spw_phase_rms[spwind],15.0])
                  max_warn_thresh = pl.amax([6.0*spw_phase_rms[spwind],30.0])

                  trig_mn_info = (pl.absolute(mean_phase[spwind,antind,polind]) > mn_info_thresh)
                  trig_mn_warn = (pl.absolute(mean_phase[spwind,antind,polind]) > mn_warn_thresh)
                  if skip_rms:
                      trig_rms_info = False
                      trig_rms_warn = False
                  else:
                      trig_rms_info = (rms_phase[spwind,antind,polind] > rms_info_thresh)
                      trig_rms_warn = (rms_phase[spwind,antind,polind] > rms_warn_thresh)
                  trig_max_info = max_phase[spwind,antind,polind] > max_info_thresh
                  trig_max_warn = max_phase[spwind,antind,polind] > max_warn_thresh
                  if (trig_rms_info or trig_mn_info or trig_max_info):
                    antSpwQaScore[spwind,antind,polind] = 0.8
                  if (trig_rms_warn or trig_mn_warn or trig_max_warn):
                    antSpwQaScore[spwind,antind,polind] = 0.5
                  # write antenna-specific QA score and supporting diagnostic info if appropriate-
                  if (antSpwQaScore[spwind,antind,polind] < 1.0):
                    mystring = " NOTICE: "
                    if ((antSpwQaScore[spwind,antind,polind] < 0.8)):
                      mystring = " WARNING: "
                    mystring += projName+" "+mousName+" "+ebName+" spw: "+str(scispws[spwind])+" "+str(valueMapping[antind])+" pol: "+str(polind)+" mean,rms,spwRms "+str(mean_phase[spwind,antind,polind])+" "+str(rms_phase[spwind,antind,polind])+" "+str(spw_phase_rms[spwind])+" QAscore (fromMean?,fromRms?,fromMax?): "+str(antSpwQaScore[spwind,antind,polind])+ " (" + str(int(trig_mn_info or trig_mn_warn)) + " " + str(int(trig_rms_info or trig_rms_warn))+" "+str(int(trig_max_info or trig_max_warn))+")"
                    print(mystring)
                    if (doFile): fh.write(mystring+'\n')
                    #print(mystring," spw,ant,pol, mean phase, rms phase, spw rms phase /// QA Score: ",scispws[spwind],v.antennaNamesForAntennaIds[antind],polind,mean_phase[spwind,antind,polind],rms_phase[spwind,antind,polind],spw_phase_rms[spwind]," /// ",antSpwQaScore[spwind,antind,polind])

  spwQaScore = pl.ones(nspw)              
  spwPhaseRms_notices = 0
  spwPhaseRms_tot = nspw
  for spwind in range(nspw):
      mystring= " INFO: "+ projName+" "+mousName+" "+ ebName+" spw: "+str(scispws[spwind])+" SPW RMS ("+str(spw_phase_rms[spwind])+" deg.)"
      print(mystring)
      if (doFile): fh.write(mystring+'\n')
      #if spw_phase_rms[spwind] > 5.0*S0info:
      #    spwQaScore[spwind] = 0.8
      #    mystring= " INFO: "+ projName+" "+mousName+" "+ ebName+" spw: "+str(scispws[spwind])+" high SPW RMS ("+str(spw_phase_rms[spwind])+" deg.) QAscore: "+str(spwQaScore[spwind])
         
  # bsm NEW-
  #finalScore = pl.amin( [pl.amin(antSpwQaScore),pl.amin(spwQaScore)])
  dataSufficiencyScore = pl.amin(antSpwDataSufficient)
  finalScore = pl.amin([dataSufficiencyScore,pl.amin(antSpwQaScore)])
  mystring= "QQ FINAL QAscore "+projName+" "+mousName+" "+ebName+" "+str(finalScore)
  print(mystring)
  if (doFile): 
    fh.write(mystring+'\n')
    fh.write(" Table: "+table+'\n')

  # to be finished -- loop for problem antennas goes here - 
  print("# Mean, RMS spwRms (RMS/spwRms) max (max/RMS) for each SPW, Ant, {Pol}")
  for spwind in range(nspw):
    mystr = "QQ Problem Antennas for SPW "+str(scispws[spwind])+" "
    was_problem = False
    for antind in range(n_ant):
      thisQa = 1.0
      for polind in range(n_pol):
          thisQa = pl.amin([thisQa,antSpwQaScore[spwind,antind,polind]])
      if thisQa < 0.66:
          mystr += "*"
      if thisQa < 0.9:
          mystr += valueMapping[antind]+","
          was_problem = True
    if was_problem:
        print(mystr)
        if (doFile): fh.write(mystr+'\n')
  # bsm NEW - separately call out the "insufficient data" ant/spws
  for spwind in range(nspw):
    mystr = "QQ Antennas with insufficient data for SPW "+str(scispws[spwind])+" "
    was_problem = False
    for antind in range(n_ant):
      thisQa = 1.0
      for polind in range(n_pol):
          thisQa = pl.amin([thisQa,antSpwDataSufficient[spwind,antind,polind]])
      if thisQa < 0.9:
          mystr += valueMapping[antind]+","
          was_problem = True
    if was_problem:
        print(mystr)
        if (doFile): fh.write(mystr+'\n')

  if (doFile): fh.close()

  return finalScore

  # end
