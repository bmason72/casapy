
import analysisUtils as au
import numpy as np

def get_flux_ratios(pl_run = '/lustre/naasc/sciops/comm/bmason/pipeline/root/2017.1.00015.S_2017_11_23T22_07_54.573',desired_field = ['J0547+1223'],outfile=''):

  # if given a string, read the file. otherwise assume we are given
  understood_type = False
  if (type(pl_run) == tuple):
      if (type(pl_run[0])==dict) & (type(pl_run[1])==dict):
          print 'interpreting argument to get_flux_ratios() as the tuple of dictionaries returned by au.getFluxesFromAquaReport()'
          understood_type = True
          f = pl_run
  if (type(pl_run)==str):
      understood_type = True
      f=au.getFluxesFromAquaReport(pl_run)
      # f[0] is the fluxes in the report (dict)
      # f[1] is the catalog fluxes (")
  if not(understood_type):
      print ' get_flux_ratios() does not understand the type of the argument you provided for pl_run ',pl_run,type(pl_run)
      print ' You should give a string with the pipeline-run directory (root/2017.1..54.573/) or the tuple of dicts returned by au.getFluxesFromAquaReport()'

  # unique lists (not sets :) - so indexable:
  ms_set = list(set(f[0]['ms']))

  print "pipeline run:" , pl_run
  print "MS's:", ms_set

  # these are of length the full arrays returned by getFluxesFromAquaReport-
  field_array=np.array(f[0]['fieldname'])
  spw_array=np.array(f[0]['spw'])
  ms_array=np.array(f[0]['ms'])
  freq_array=np.array(f[0]['freq'])
  flux_array=np.array(f[0]['I'])
  eflux_array=np.array(f[0]['dI'])

  # ditto, but for the catalog fluxes-
  cat_field_array=np.array(f[1]['fieldname'])
  cat_spw_array=np.array(f[1]['spw'])
  cat_ms_array=np.array(f[1]['asdm'])
  cat_flux_array=np.array(f[1]['I'])

  print "Catalog info: ", f[1]

  print "ASDM  FieldName  SPW  Freq  Flux Error  SNR  CatFlux CatFluxRatio   cfrToMaxSnrCfr " 
  for ms in ms_set:
      ms_idx = np.where(ms == ms_array)
      # the set of fields for this ms-
      field_set = set(field_array[ms_idx])
      for field in field_set:
        # if the field in question is one of the desired fields-
        if (set([field]).issubset(set(desired_field))):
          print " Field: ",field
          field_idx=np.where(np.all([field == field_array,ms==ms_array],axis=0))
          spw_list = list(spw_array[field_idx])
          fluxes=np.array([])
          errs=np.array([])
          freqs=np.array([])
          snr=np.array([])
          best_snr = -1.0
          cat_fluxes=np.array([])
          print "## #####"
          for spw in spw_list:
              this_idx=np.where(np.all([ms==ms_array,field==field_array,spw==spw_array],axis=0))
              # was if len(this_idx[0] != 0) -->
              #  if len(this_idx[0] != 0):
              if len(this_idx) != 0:
                  strings = flux_array[this_idx]
                  fluxes=np.append(fluxes, strings.astype(np.float))
                  strings = eflux_array[this_idx]
                  errs=np.append(errs,strings.astype(np.float))
                  strings=freq_array[this_idx]
                  freqs=np.append(freqs,strings.astype(np.float))
                  cat_idx=np.where(np.all([ms==cat_ms_array,field==cat_field_array,spw==cat_spw_array],axis=0))
                  this_snr = fluxes[-1] / errs[-1]
                  snr=np.append(snr,this_snr)
                  if (this_snr > best_snr):
                      best_snr = this_snr
                  #if len(cat_idx[0] != 0):
                  print "cat index: ", cat_idx,len(cat_idx)
                  if len(cat_idx[0]) != 0:
                      strings=cat_flux_array[cat_idx]
                      cat_fluxes=np.append(cat_fluxes,strings.astype(np.float))
                  else:
                      cat_fluxes=np.append(cat_fluxes,-1.0)
                  #print ms, field, spw, freqs[-1], fluxes[-1], errs[-1],snr[-1]
              else:
                  # this should not happen - 
                  print " *** ERROR in get_flux_ratios() -- did not find desired ms, field, spw / in  ",pl_run
          snr = fluxes / errs
          imax = np.where(snr==snr.max())
          #max_snr_spw = spw[imax]
          #for spw in spw_set:
          snr_max_flux_ratio = fluxes[imax] / cat_fluxes[imax]
          flux_ratios=np.array([])
          if ( (len(outfile) > 0) & (len(fluxes) > 0)):
              fptr=open(outfile,'a')
          for i in range(len(fluxes)):
              flux_ratios=np.append(flux_ratios, fluxes[i]/cat_fluxes[i])
          for i in range(len(spw_list)):
              print ms, field, spw_list[i] , freqs[i], fluxes[i], errs[i],snr[i], cat_fluxes[i],flux_ratios[i], flux_ratios[i] / snr_max_flux_ratio[0]
              if (len(outfile)>0):
                  mystr=ms+' '+field+' '+str(spw_list[i])+' '+str(freqs[i])+' '+str(fluxes[i])+' '+str(errs[i])+' '+str(snr[i])+' '+str(cat_fluxes[i])+' '+str(flux_ratios[i])+' '+str(flux_ratios[i] / snr_max_flux_ratio[0])+'\n'
                  fptr.write(mystr)
          if ( (len(outfile)>0) & (len(fluxes)>0)):
              fptr.close()
  return f
