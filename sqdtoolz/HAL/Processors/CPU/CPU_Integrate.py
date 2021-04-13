from sqdtoolz.HAL.Processors.ProcessorCPU import*
import numpy as np

class CPU_Integrate(ProcNodeCPU):
    def __init__(self, index_parameter_name):
        '''
        General function that adds all values in each channel across some parameter - e.g. over repetition or over all the samples. 

        Inputs:
            - index_parameter_name - Name of the parameter in which to sum across.
        '''
        self._param_name = index_parameter_name

    def input_format(self):
        return ['repetition', 'segment', 'sample']

    def output_format(self):
        return ['repetition', 'segment', 'sample']

    def process_data(self, data_pkt, **kwargs):
        assert self._param_name in data_pkt['parameters'], f"The indexing parameter '{self._param_name}' is not in the current dataset."

        end_stage = kwargs.get('EndStage', False)

        axis_num = data_pkt['parameters'].index(self._param_name)
        assert (not end_stage) or axis_num > 0, "Cannot and should not take the mean across the first variable unless it is in the end-stages."

        #Process sums on a per-channel basis
        for ch_ind, cur_ch in enumerate(data_pkt['data'].keys()):
            data_pkt['data'][cur_ch] = np.sum(data_pkt['data'][cur_ch], axis=axis_num)

        #Remove the parameter as it no longer exists after the averaging...
        data_pkt['parameters'].pop(axis_num)

        return data_pkt
