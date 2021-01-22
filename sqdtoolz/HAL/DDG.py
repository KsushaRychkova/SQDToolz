
class DDG:
    '''
    Class to handle interfacing with digital delay generators.
    '''

    def __init__(self, instr_ddg):
        '''
        '''
        self._instr_ddg = instr_ddg
        self._name = instr_ddg.name

    @property
    def name(self):
        return self._name

    def get_trigger_output(self, outputID):
        '''
        Returns a TriggerSource object 
        '''
        return self._instr_ddg.get_trigger_output(outputID)

    def get_all_outputs(self):
        return self._instr_ddg.get_all_trigger_sources()

    def set_trigger_output_params(self, trigOutputName, trigPulseDelay, trigPulseLength=-1, trigPulsePolarity=1):
        '''
        trigPulseLength must be positive (otherwise, it is not set)
        '''
        if (trigPulseLength > 0):
            self.get_trigger_output(trigOutputName).TrigPulseLength = 50e-9        
        self.get_trigger_output(trigOutputName).TrigPolarity = trigPulsePolarity
        self.get_trigger_output(trigOutputName).TrigPulseDelay = trigPulseDelay

    def _get_current_config(self):
        #Get settings for the trigger objects
        trigObjs = self.get_all_outputs()
        trigDict = {}
        for cur_trig in trigObjs:
            trigDict = {**trigDict, **cur_trig._get_current_config()}
        retDict = {
            'instrument' : self.name,
            'type' : 'DDG',
            'triggers' : trigDict
            }
        return retDict

    def _set_current_config(self, dict_config, instr_obj = None):
        assert dict_config['type'] == 'DDG', 'Cannot set configuration to a DDG with a configuration that is of type ' + dict_config['type']
        if (instr_obj != None):
            self._instr_ddg = instr_obj
        for cur_trig_name in dict_config['triggers']:
            self.get_trigger_output(cur_trig_name)._set_current_config(dict_config['triggers'][cur_trig_name])
