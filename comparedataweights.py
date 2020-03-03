
import numpy as np
from taskinit import *
 
def comparedataweights(vis,spw=0,field=0,minchan=12,maxchan=116,pol=0,cutzeros=False):
    ''' july2015 bsm - routine to compare data weights in an MS
      with actual data RMS.  supply spw, field, pol, and min/max chans to do
      the calculation over. *All are integers - not strings*
      example
        import comparedataweights as cdw
        foo=cdw.comparedataweights('test.ms',spw=1,field=3,minchan=25,maxchan=215)
      returns a dictionary.
    ASSUMES spw#=datadescid -- check this via ms.open(), ms.getspectralwindowinfo()
    '''
    ms.open(vis)
    ms.selectinit(reset=True)
    # to get the actual lookup table between datadescid and spw do the following - 
    print " The spectral window setups -- including the relationship between "
    print "  data descriptor ID and spectral window number-- is as follows--"
    print "=================================================================="
    print ms.getspectralwindowinfo()
    print "=================================================================="
    ms.selectinit(datadescid=spw)
    ms.select({'field_id':[field]})
    mydat1=ms.getdata(['weight','real','imaginary','flag_row','flag'])
    ms.close()
    # shape = npol,nrows-
    w1=mydat1['weight']
    # shape = npol,nchan,nrows- 
    im1=mydat1['imaginary']
    # flag shape = npol,nchan,nrows-
    f1=mydat1['flag']
    # rowflag shape = nrows-
    fr1=mydat1['flag_row']
    # new row-flagged array  that is npol x nrows. we will set it to True = FLAGGED if
    #  a) any of the channels in the range of interest are flagged
    #  b) the row_flag was explicitly set in the MS (in some of these datasets,
    #      it is not, in spite of all channels in that row beingn flagged)
    #  c) the weight is NaN. (probably this one was a red herring and could be deleted)
    datashape=im1.shape
    nrf=np.zeros([datashape[0],datashape[2]],dtype=np.bool)
    npol=datashape[0]
    nchan=datashape[1]
    nrows=datashape[2]
    # i is pol , j is row
    for i in range(npol):
        for j in range(nrows):
            # ensure that flagged rows are also flagged in the master flag array -
            if (fr1[j]):
                f1[i,minchan:maxchan,j] = True
            # change from any() to all()-
            nrf[i,j] = f1[i,minchan:maxchan,j].all() | fr1[j] | np.isnan(w1[i,j])
            # flag zero values if requested - only looks at imaginary, as this whole script does-
            if (cutzeros):
                zvalinds= (im1[i,minchan:maxchan,j] == 0.0)
                if (zvalinds.max()):
                    f1[i,zvalinds,j] = True

    # flag ranges to be excluded from calculation-
    if (minchan > 0):
        f1[:,0:minchan-1,:] = True
    if (maxchan < nchan-1):
        f1[:,maxchan:nchan-1,:]=True
    if (np.min(nrf) == True):
        print "*** ERROR: all data flagged"
        print " someething is wrong with your data selection "
        print " (field, spw, or min/max chan) "
        return {'status':False}

    # use master flag array for real data, not row-flags
    datasd=np.std(im1[np.logical_not(f1)])
    datamedian=np.median(im1[np.logical_not(f1)])
    datamad=np.median(np.abs(datamedian - im1[np.logical_not(f1)]))
    #datasd=np.std(im1[pol,minchan:maxchan, np.logical_not(nrf[pol,:])])
    #datamedian=np.median(im1[pol,minchan:maxchan, np.logical_not(nrf[pol,:])])
    #datamad=np.median( np.abs( datamedian - im1[pol,minchan:maxchan, np.logical_not(nrf[pol,:])]))
    minwt=np.min(w1[pol,np.logical_not(nrf[pol,:])])
    meanwt=np.mean(w1[pol,np.logical_not(nrf[pol,:])])
    medwt=np.median(w1[pol,np.logical_not(nrf[pol,:])])
    maxwt=np.max(w1[pol,np.logical_not(nrf[pol,:])])

    # simple monte carlo to check the sd vs weights since the weights
    #  are not constant (i.e., the data are not legitimately described by a 
    #  single mean weight, so what should we expect the SD of the ensemble of given weights to be?)-
    fakedata=im1[pol,minchan:maxchan,np.logical_not(nrf[pol,:])]
    gooddatwts=w1[pol,np.logical_not(nrf[pol,:])]
    fds=fakedata.shape
    # i indexes row (weights vary)- (weights constant over chan)
    for i in range(fds[0]):
        fakedata[i,:] = np.random.randn(1,fds[1]) / np.sqrt(gooddatwts[i])

    fakesd=np.std(fakedata)

    print " "
    print "=================================================================="
    print " Data RMS , implied weight: "+str(datasd)+" , " + str(1.0/datasd**2)
    print "   data MAD (normalized) = "+str(datamad/0.6745)
    print " Actual Weight (min, mean, median, max): " + str(minwt)+" , "+ str(meanwt)+" , "+ str(medwt)+" , "+ str(maxwt)
    print " simulated data RMS, implied weight: "+str(fakesd)+" , "+str(1.0/fakesd**2)
    wtratio=1.0/(datasd**2*meanwt)
    print " data-implied weight / mean weight: "+str(wtratio)
    print "  # rows selected , # unflagged rows " + str(nrows) + " " + str(gooddatwts.size)
    print "=================================================================="

    foo={'datasd':datasd,'meanwt':meanwt,'medwt':medwt,'simsd':fakesd,
         'simsd':fakesd,'wtratio':wtratio,'nrows_selected':nrows,'nrows_good':gooddatwts.size,
         'minwt':minwt,'meanwt':meanwt,'medwt':medwt,'maxwt':maxwt,
         'status':True}

    return foo
