
#
# bsm march 2020
#  routines to help with analysis and processing of ALMA source catalog 
#  data, in particular, pipeline runs that call the flux service and
#  comparison with AU/flux.csv values
#

import sys,pickle,os,glob
import analysisUtils as au
import numpy as np

def assemble_fluxes(mous_list='',new_style=False,outfile_name='test',my_intent='PHASE'):
    """
    mous_list defaults to looking for working directories in ./ named MOOUS_* (old validation run style)
    new_style=True looks for files like flux.csv (for au) and flux.csv.original (for dB) (new style)
    """
    mous_name = []
    vis_name = []

    start_dir = os.getcwd()

    # accumulate information about sources 
    #  from benchmark and new runs in big-ass structures
    if (len(mous_list) == 0):
        mous_list = glob.glob("MOUS_*")
    all_sources = []
    for i in range(len(mous_list)):
        dirname = mous_list[i]
        print " ***** MOUS ",i," ",dirname
        try:
            os.chdir(dirname)
            changed_dir = True
        except:
            print " *** ERROR: could not cd into directory: ",dirname
            changed_dir = False
            # if we couldn't cd into this directory, go on to the next one
            continue
        ms_list = glob.glob("*.ms")
        for my_vis in ms_list:
            if (new_style):
                sdb = au.readFluxcsv('flux.csv.original',intent=my_intent,vis=my_vis)
                sau = au.readFluxcsv('flux.csv',intent=my_intent,vis=my_vis)
            else:
                sdb = au.readFluxcsv('flux.csv',intent=my_intent,vis=my_vis)
                sau = au.readFluxcsv('benchmark_flux/flux.csv',intent=my_intent,vis=my_vis)
            if (sdb is not None and sau is not None):
                all_sources.append({'mousnum':mous_list[i],'vis':my_vis,'dbflux':sdb,'auflux':sau})
                mous_name.append(mous_list[i])
                vis_name.append(my_vis)
            else:
                print " *** WARNING: did not get successful queries for both benchmark and new runs ",mous_list[i],my_vis
        os.chdir(start_dir)

    pickle.dump(all_sources,open(outfile_name+'.pkl',"wb"))


def compare_fluxes(all_sources,outfile_name='test',frac_thresh = 0.01):
    n_eb = len(all_sources)
    nqueries=0
    mean_flux = np.array([])
    flux_diff = np.array([])
    freqs = np.array([])
    old_flux = np.array([])
    new_flux = np.array([])
    exec_number = np.array([])
    mous_name = []
    vis_name = []
    
    for i in range(n_eb):
        if type(all_sources[i]['auflux']) != type(all_sources[i]['dbflux']):
            print "**** ERROR: one of the queries failed for ",all_sources[i]['mousnum']
        else:
            #print " *** ",all_sources[i]['mousnum']
            #print all_sources[i]['auflux']
            #print all_sources[i]['dbflux']
            if len(all_sources[i]['dbflux']) != len(all_sources[i]['auflux']):
                print "**** ERROR: queries are of different length ",all_sources[i]['mousnum']
                continue 
            nspw = len(all_sources[i]['dbflux'][0])
            for j in range(nspw):
                db_flux = all_sources[i]['dbflux'][0][j] # or '}[0][j] ??
                au_flux = all_sources[i]['auflux'][0][j] 
                mean_flux=np.append(mean_flux, 0.5*(db_flux + au_flux))
                flux_diff=np.append(flux_diff, (db_flux - au_flux))
                freqs=np.append(freqs,all_sources[i]['auflux'][1][j])
                old_flux = np.append(old_flux,all_sources[i]['auflux'][0][j])
                new_flux = np.append(new_flux,all_sources[i]['dbflux'][0][j])
                exec_number = np.append(exec_number,i)
                vis_name.append(all_sources[i]['vis'])
                mous_name.append(all_sources[i]['mousnum'])
                nqueries += len(all_sources[i]['dbflux'][3])

    fhandle = open(outfile_name+'.txt',"w")
    fhandle.write("# MOUS_num EB.ms old_flux new_flux fractional_flux_difference\n")

    for i in range(len(new_flux)):
        if ( np.abs(flux_diff[i]/mean_flux[i]) > frac_thresh):
            print i,mous_name[i],vis_name[i], old_flux[i], new_flux[i], flux_diff[i]/mean_flux[i]
            mystr = mous_name[i] + " " + vis_name[i]+" "+str(old_flux[i]) +" "+ str(new_flux[i])+" "+str( flux_diff[i]/mean_flux[i])+'\n'
            fhandle.write(mystr)

    fhandle.close()

    return old_flux,new_flux,flux_diff/mean_flux

def old_compare_fluxes(outfile_name='test'):
    n_eb = len(all_sources)
    nqueries=0
    mean_flux = np.array([])
    flux_diff = np.array([])
    freqs = np.array([])
    old_flux = np.array([])
    new_flux = np.array([])
    exec_number = np.array([])

    for i in range(n_eb):
        if type(all_sources[i][0]) != type(all_sources[i][1]):
            print "**** ERROR: one of the queries failed for ",mous_list[i]
        else:
            print " *** ",mous_list[i]
            print all_sources[i][0]
            print all_sources[i][1]
            if len(all_sources[i][0]) != len(all_sources[i][1]):
                print "**** ERROR: queries are of different length ",mous_list[i]
                continue 
            nspw = len(all_sources[i][1][0])
            for j in range(nspw):
                mean_flux=np.append(mean_flux, 0.5*(all_sources[i][0][0][j] + all_sources[i][1][0][j]) )
                flux_diff=np.append(flux_diff, (all_sources[i][1][0][j] - all_sources[i][0][0][j]) )
                freqs=np.append(freqs,all_sources[i][1][1][j])
                old_flux = np.append(old_flux,all_sources[i][1][0][j])
                new_flux = np.append(new_flux,all_sources[i][0][0][j])
                exec_number = np.append(exec_number,i)
                nqueries += len(all_sources[i][1][3])

    fhandle = open(outfile_name+'.txt',"w")
    fhandle.write("# MOUS_num old_flux new_flux fractional_flux_difference")

    for i in range(len(exec_number)):
        print mous_list[int(exec_number[i])], old_flux[i], new_flux[i], flux_diff[i]/mean_flux[i]
        mystr = mous_list[int(exec_number[i])] + " " + str(old_flux[i]) +" "+ str(new_flux[i])+" "+str( flux_diff[i]/mean_flux[i])+'\n'
        fhandle.write(mystr)

    fhandle.close()
