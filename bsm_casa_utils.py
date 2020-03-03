
import numpy as np

def show_gc_snr(gcs):
  # print out results from au.gaincalSnr()
  # input should be the dictionary au.gaincalSNR() returns

  if type(gcs)==dict:
    gcs_keys = gcs.keys()
    print "======================"
    print gcs['calibrator']
    all_spws=np.array([])
    for k in gcs_keys:
      if type(k)==np.int32:
        all_spws=np.append(all_spws,k)
    all_spws=np.sort(all_spws)
    for k in all_spws:
      if type(gcs[k])==dict:
        print "SPW ",k," SNR = ", gcs[k]['snr']
  else:
    print "Input to show_gc_snr() was not a dictionary as required"

