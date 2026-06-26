import numpy as np
import scipy.io as spio
def getXEB(px,data,data_set_ref,dataset_cz,save_path=''):
     result = px.XEB(data, [dataset_cz], collect=True)
     res_cz = result[dataset_cz]
     output_data = {}
     output_data['ms_cz'] = res_cz['ms']
     output_data['XEB_fids_cz'] = res_cz['XEB_fids']

     result = px.XEB(data, [data_set_ref], collect=True)
     res_ref = result[data_set_ref]
     output_data['ms_ref'] = res_ref['ms']
     output_data['XEB_fids_ref'] = res_ref['XEB_fids']
     spio.savemat(save_path,output_data)

