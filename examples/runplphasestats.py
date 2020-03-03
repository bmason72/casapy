
import calcPhaseTableStats as cpt

# need to find that one pathological case -- all narrow spws -- and see that it does nothing.

cpt.mapNarrowSpw('/lustre/naasc/nbrunett/narrow_band/683/X38/control/uid___A002_X75ab74_X5fd.ms.split',manPl=True)
cpt.mapNarrowSpw('/lustre/naasc/hmedlin/pipeline/root/2012.1.00129.S_2014_06_03T19_33_07.761/SOUS_uid___A002_X6444ba_Xec/GOUS_uid___A002_X6444ba_Xed/MOUS_uid___A002_X6444ba_Xee/working/uid___A002_X7310ce_Xc66.ms')

# run on manual pipeline datasets-
cpt.calcAlmaManPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/683/X38/control/',outDir='./manplphases/683/')
cpt.calcAlmaManPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/683/X311/control/',outDir='./manplphases/683/')
cpt.calcAlmaManPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/178/Xc42/control/',outDir='./manplphases/178/')
cpt.calcAlmaManPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/178/X10d4/control/',outDir='./manplphases/178/')
cpt.calcAlmaManPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/178/X14de/control/',outDir='./manplphases/178/')
cpt.calcAlmaManPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/394/control/',outDir='./manplphases/394/')
cpt.calcAlmaManPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/554/control/',outDir='./manplphases/554/')
cpt.calcAlmaManPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/129/control/',outDir='./manplphases/129/')
cpt.calcAlmaManPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/422/control/',outDir='./manplphases/422/')

#################################
cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/narrow_band/683/X311/control/',
                            outDir='./plphases/2012.1.00683b/')


#################################

#cpt.calcAlmaPlPhaseSolStats()


cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00178.S_2014_06_09T18_42_17.215/SOUS_uid___A002_X684eb5_X3b/GOUS_uid___A002_X684eb5_X3c/MOUS_uid___A002_X684eb5_X3f/working/',
                            outDir='./plphases/2012.1.00178/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00178.S_2014_06_09T18_45_09.834/SOUS_uid___A002_X684eb5_X35/GOUS_uid___A002_X684eb5_X36/MOUS_uid___A002_X684eb5_X39/working/',
                            outDir='./plphases/2012.1.00178/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/hmedlin/pipeline/root/2012.1.00129.S_2014_06_03T19_33_07.761/SOUS_uid___A002_X6444ba_Xec/GOUS_uid___A002_X6444ba_Xed/MOUS_uid___A002_X6444ba_Xee/working/',
                            outDir='./plphases/2012.1.00129/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/PipelineTestData/2012.1.01069.S_2014_02_20T19_15_12.327/SOUS_uid___A002_X67ccb6_X36/GOUS_uid___A002_X67ccb6_X37/MOUS_uid___A002_X67ccb6_X3a/working/',
                            outDir='./plphases/2012.1.01069/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/dmedlin/pipeline/root/2012.1.00554.S_2014_06_03T18_45_03.900/SOUS_uid___A002_X5d7935_X3a7/GOUS_uid___A002_X5d7935_X3a8/MOUS_uid___A002_X5d7935_X3ab/working/',
                            outDir='./plphases/2012.1.00554/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/swood/pipeline/root/2012.1.00554.S_2014_05_30T21_11_18.046/SOUS_uid___A002_X5d7935_X3b3/GOUS_uid___A002_X5d7935_X3b4/MOUS_uid___A002_X5d7935_X3b5/working/',
                            outDir='./plphases/2012.1.00554/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00554.S_2014_06_11T15_43_00.338/SOUS_uid___A002_X5d7935_X3b3/GOUS_uid___A002_X5d7935_X3b4/MOUS_uid___A002_X5d7935_X3b7/working/',
                            outDir='./plphases/2012.1.00554/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/dmedlin/pipeline/root/2012.1.00554.S_2014_06_04T20_39_10.533/SOUS_uid___A002_X5d7935_X3ad/GOUS_uid___A002_X5d7935_X3ae/MOUS_uid___A002_X5d7935_X3af/working/',
                            outDir='./plphases/2012.1.00554/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/pipeline/root/2012.1.00554.S_2014_05_30T20_26_18.561/SOUS_uid___A002_X5d7935_X3ad/GOUS_uid___A002_X5d7935_X3ae/MOUS_uid___A002_X5d7935_X3b1/working/',
                            outDir='./plphases/2012.1.00554/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00554.S_2014_06_11T15_52_20.669/SOUS_uid___A002_X5d7935_X3b9/GOUS_uid___A002_X5d7935_X3ba/MOUS_uid___A002_X5d7935_X3bd/working/',
                            outDir='./plphases/2012.1.00554/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00394.S_2014_06_10T17_47_37.355/SOUS_uid___A002_X639a2a_X53/GOUS_uid___A002_X639a2a_X54/MOUS_uid___A002_X639a2a_X57/working/',
                            outDir='./plphases/2012.1.00394/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00394.S_2014_06_11T15_09_10.805/SOUS_uid___A002_X639a2a_X5b/GOUS_uid___A002_X639a2a_X5c/MOUS_uid___A002_X639a2a_X5f/working/',
                            outDir='./plphases/2012.1.00394/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/pipeline/root/2012.1.00394.S_2014_05_30T20_22_16.421/SOUS_uid___A002_X639a2a_X43/GOUS_uid___A002_X639a2a_X44/MOUS_uid___A002_X639a2a_X45/working/',
                            outDir='./plphases/2012.1.00394/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/dkim/pipeline/root/2012.1.00394.S_2014_05_30T16_59_45.220/SOUS_uid___A002_X639a2a_X4b/GOUS_uid___A002_X639a2a_X4c/MOUS_uid___A002_X639a2a_X4d/working_X5e5//',
                            outDir='./plphases/2012.1.00394/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/PipelineTestData/2012.1.00394.S_2014_02_27T15_15_59.497/SOUS_uid___A002_X639a2a_X4b/GOUS_uid___A002_X639a2a_X4c/MOUS_uid___A002_X639a2a_X4f/working/',
                            outDir='./plphases/2012.1.00394/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/hmedlin/pipeline/root/2012.1.00382.S_2014_06_04T20_29_23.214/SOUS_uid___A002_X5a9a13_X6e2/GOUS_uid___A002_X5a9a13_X6e3/MOUS_uid___A002_X5a9a13_X6e4/working/',
                            outDir='./plphases/2012.1.00382/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00368.S_2014_06_11T15_22_45.297/SOUS_uid___A002_X628157_X29/GOUS_uid___A002_X628157_X2a/MOUS_uid___A002_X628157_X2d/working/',
                            outDir='./plphases/2012.1.00368/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00368.S_2014_06_11T16_21_33.725/SOUS_uid___A002_X628157_X31/GOUS_uid___A002_X628157_X32/MOUS_uid___A002_X628157_X33/working/',
                            outDir='./plphases/2012.1.00368/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00368.S_2014_06_11T17_39_28.211/SOUS_uid___A002_X628157_X31/GOUS_uid___A002_X628157_X32/MOUS_uid___A002_X628157_X35/working/',
                            outDir='./plphases/2012.1.00368/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/dkim/pipeline/root/2012.1.01011.S_2014_06_06T13_04_35.208/SOUS_uid___A002_X6444ba_Xc3/GOUS_uid___A002_X6444ba_Xc4/MOUS_uid___A002_X6444ba_Xc5/working/',
                            outDir='./plphases/2012.1.01011/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00603.S_2014_05_30T19_55_43.053/SOUS_uid___A002_X6f9b0f_Xee/GOUS_uid___A002_X6f9b0f_Xef/MOUS_uid___A002_X6f9b0f_Xf0/working/',
                            outDir='./plphases/2012.1.00603/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00603.S_2014_05_30T19_42_35.543/SOUS_uid___A002_X6f9b0f_Xf8/GOUS_uid___A002_X6f9b0f_Xf9/MOUS_uid___A002_X6f9b0f_Xfa/working/',
                            outDir='./plphases/2012.1.00603/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/dkim/pipeline/root/2012.1.00603.S_2014_06_05T18_38_29.056/SOUS_uid___A002_X6f9b0f_Xda/GOUS_uid___A002_X6f9b0f_Xdb/working/',
                            outDir='./plphases/2012.1.00603/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/swood/pipeline/root/2012.1.00031.S_2014_02_25T14_57_37.741/SOUS_uid___A002_X5a9a13_X12a/GOUS_uid___A002_X5a9a13_X12b/MOUS_uid___A002_X5a9a13_X12c/working/',
                            outDir='./plphases/2012.1.00031/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00603.S_2014_05_30T19_42_35.543/SOUS_uid___A002_X6f9b0f_Xf8/GOUS_uid___A002_X6f9b0f_Xf9/MOUS_uid___A002_X6f9b0f_Xfa/working/',
                            outDir='./plphases/2012.1.00603/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/pipeline/root/2012.1.00683.S_2014_06_04T14_15_34.441/SOUS_uid___A002_X74fe5d_X36/GOUS_uid___A002_X74fe5d_X37/MOUS_uid___A002_X74fe5d_X3a/workng/',
                            outDir='./plphases/2012.1.00683/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/nbrunett/pipeline/root/2012.1.00683.S_2014_06_04T14_19_44.482/SOUS_uid___A002_X74fe5d_X36/GOUS_uid___A002_X74fe5d_X37/MOUS_uid___A002_X74fe5d_X38/working/',
                            outDir='./plphases/2012.1.00683/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/dkim/pipeline/root/2012.1.00195.S_2013_11_07T16_52_27.526/SOUS_uid___A002_X5a9a13_X11c/GOUS_uid___A002_X5a9a13_X11d/MOUS_uid___A002_X5a9a13_X11e/working/',
                            outDir='./plphases/2012.1.00195/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00346.S_2014_06_12T18_08_27.281/SOUS_uid___A002_X5a9a13_X7c5/GOUS_uid___A002_X5a9a13_X7c6/MOUS_uid___A002_X5a9a13_X7c7/working/',
                            outDir='./plphases/2012.1.00346/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00346.S_2014_06_13T13_45_48.241/SOUS_uid___A002_X5a9a13_X7c9/GOUS_uid___A002_X5a9a13_X7ca/MOUS_uid___A002_X5a9a13_X7cb/working/',
                            outDir='./plphases/2012.1.00346/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/hmedlin/pipeline/root/2012.1.00496.S_2014_06_03T18_03_16.500/SOUS_uid___A002_X5d7935_X244/GOUS_uid___A002_X5d7935_X245/MOUS_uid___A002_X5d7935_X246/working/',
                            outDir='./plphases/2012.1.00496/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00688.S_2014_06_12T20_51_08.130/SOUS_uid___A002_X5ce05d_X18b/GOUS_uid___A002_X5ce05d_X18c/MOUS_uid___A002_X5ce05d_X18d/working/',
                            outDir='./plphases/2012.1.00688/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00422.S_2014_06_12T20_16_09.769/SOUS_uid___A002_X5ce05d_X9/GOUS_uid___A002_X5ce05d_Xa/MOUS_uid___A002_X5ce05d_Xb/working/',
                            outDir='./plphases/2012.1.00422/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/dmedlin/pipeline/root/2012.1.00720.S_2014_06_03T17_59_03.516/SOUS_uid___A002_X6444ba_Xd3/GOUS_uid___A002_X6444ba_Xd4/MOUS_uid___A002_X6444ba_Xd5/working/',
                            outDir='./plphases/2012.1.00720/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/PipelineTestData/2012.1.00001.S_2014_01_14T16_43_19.216/SOUS_uid___A002_X5a9a13_X7ab/GOUS_uid___A002_X5a9a13_X7ac/MOUS_uid___A002_X5a9a13_X7af/SBS_uid___A002_X6f9b0f_X7f/working/',
                            outDir='./plphases/2012.1.00001/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00196.S_2014_06_13T14_58_47.739/SOUS_uid___A002_X5a9a13_X156/GOUS_uid___A002_X5a9a13_X157/MOUS_uid___A002_X5a9a13_X158/working/',
                            outDir='./plphases/2012.1.00196/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00229.S_2014_02_21T17_53_12.132/SOUS_uid___A002_X628157_Xcf/GOUS_uid___A002_X628157_Xd0/MOUS_uid___A002_X628157_Xd1/working/',
                            outDir='./plphases/2012.1.00229/')

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/rindebet/pipeline/root/2012.1.00979.S_2014_06_13T19_43_12.679/SOUS_uid___A002_X5d7935_X3c7/GOUS_uid___A002_X5d7935_X3c8/MOUS_uid___A002_X5d7935_X3c9/working/',
                            outDir='./plphases/2012.1.00979/')


#############

cpt.calcAlmaPlPhaseSolStats(plDir='/lustre/naasc/bmason/datareduc/image518/2013.1.00518.S.MOUS.uid___A001_X11f_X8.SBNAME.BHR71_a_06_7M-analysis/sg_ouss_id/group_ouss_id/member_ouss_id/calibrated/working/',outDir='./plphases/2013.1.00518/',phaseField=3)

