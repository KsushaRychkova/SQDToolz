from sqdtoolz.Experiment import*
from sqdtoolz.HAL.WaveformGeneric import*
from sqdtoolz.HAL.WaveformSegments import*
from sqdtoolz.Utilities.DataFitting import*
from sqdtoolz.Utilities.DataIQNormalise import DataIQNormalise

class ExpCalibGE(Experiment):
    def __init__(self, name, expt_config, wfmt_qubit_drive, num_points_per_calib, SPEC_qubit, iq_indices = [0,1], **kwargs):
        super().__init__(name, expt_config)

        self._iq_indices = iq_indices
        self._wfmt_qubit_drive = wfmt_qubit_drive
        
        # self._range_amps = kwargs.get('range_amps', None)
        self._num_points_per_calib = num_points_per_calib

        self._SPEC_qubit = SPEC_qubit

        #Calculate default load-time via T1 of qubit or default to 40e-6
        def_load_time = self._SPEC_qubit['GE T1'].Value * 4
        if def_load_time == 0:
            def_load_time = 40e-6
        #Override the load-time if one is specified explicitly
        self.load_time = kwargs.get('load_time', def_load_time)

        self.readout_time = kwargs.get('readout_time', 2e-6)
        self.drive_time = kwargs.get('drive_time', self._SPEC_qubit['GE X-Gate Time'].Value)

        self.cur_data = None
    
    def _run(self, file_path, sweep_vars=[], **kwargs):
        assert len(sweep_vars) == 0, "Cannot specify sweeping variables in this experiment."

        self._expt_config.init_instruments()

        wfm = WaveformGeneric(['qubit'], ['readout'])
        wfm.set_waveform('qubit', [
            WFS_Constant("SEQPAD", None, -1, 0.0),
            WFS_Constant("init", None, self.load_time, 0.0),
            WFS_Gaussian("drive", self._wfmt_qubit_drive.apply(phase=0), self.drive_time, 0.001),
            WFS_Constant("pad", None, 5e-9, 0.0),
            WFS_Constant("read", None, self.readout_time, 0.0)
        ])
        wfm.set_digital_segments('readout', 'qubit', ['read'])
        self._temp_vars = self._expt_config.update_waveforms(wfm, [('Drive Amplitude', 'qubit', 'drive', 'Amplitude')] )

        sweep_vars = [(self._temp_vars[0], np.array([0.0]*self._num_points_per_calib + [self._SPEC_qubit['GE X-Gate Amplitude'].Value]*self._num_points_per_calib))]
        
        kwargs['skip_init_instruments'] = True

        self._cur_param_name = self._temp_vars[0].Name
        self.cur_data = super()._run(file_path, sweep_vars, **kwargs)
        return self.cur_data

    def _post_process(self, data):
        pass

    def normalise_data(self, iq_data_array, ax=None):
        #iq_data_array is a Nx2 array
        assert not self.cur_data is None, "Must run the calibration experiment first."

        data_norm = DataIQNormalise.calibrateFromFileIOReader(self.cur_data, self._iq_indices, True)

        return data_norm.normalise_data(iq_data_array, ax)



