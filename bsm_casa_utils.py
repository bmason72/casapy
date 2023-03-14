
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

def nearestGoodPrime(n):
  """ 
  choose the nearest number greater than or equal to n which can be factored
  into powers of 2, 3, & 5. Works for n up to 2e4
  list of primes is pre-tabulated from our IDL code sometime i should re-write
  it in python : )
  """
  goodPrimes = np.array([1,2,3,4,5,6,8,9,10,12,15,16,18,20,24,25,27,30,32,36,40,45,48,50,54,60,64,72,75,80,81,90,96,100,108,120,125,128,135,144,150,160,162,180,192,200,216,225,240,243,250,256,270,288,300,320,324,360,375,384,400,405,432,450,480,486,500,512,540,576,600,625,640,648,675,720,729,750,768,800,810,864,900,960,972,1000,1024,1080,1125,1152,1200,1215,1250,1280,1296,1350,1440,1458,1500,1536,1600,1620,1728,1800,1875,1920,1944,2000,2025,2048,2160,2187,2250,2304,2400,2430,2500,2560,2592,2700,2880,2916,3000,3072,3125,3200,3240,3375,3456,3600,3645,3750,3840,3888,4000,4050,4096,4320,4374,4500,4608,4800,4860,5000,5120,5184,5400,5625,5760,5832,6000,6075,6144,6250,6400,6480,6561,6750,6912,7200,7290,7500,7680,7776,8000,8100,8192,8640,8748,9000,9216,9375,9600,9720,10000,10125,10240,10368,10800,10935,11250,11520,11664,12000,12150,12288,12500,12800,12960,13122,13500,13824,14400,14580,15000,15360,15552,15625,16000,16200,16384,16875,17280,17496,18000,18225,18432,18750,19200,19440,19683,20000])
  
  if n > goodPrimes.max():
    print "**** ERROR: primes only tabulated up to "+str(goodPrimes.max())
    return -1
  else:
    result = goodPrimes[(np.argwhere(goodPrimes-n > 0)[0])][0]

  return result

