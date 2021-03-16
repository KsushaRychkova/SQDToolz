
# ACQ data format

The ACQ data format is made to be flexible to data gathering across multiple channels, segments, samples and repetitions. Over a given experiment window (that is, the timing diagram in which the trigger pulses and waveforms are sent), there may be multiple acquisition events (synchronised to trigger pulses) in which the ACQ instrument records a certain number of samples. These acquisition events are referred to as 'segments' while the individual data points taken within each acquisition event are referred to as 'samples'. Now the experiment window can be triggered multiple times to create many 'repetitions' which may be averaged to yield the average signal across each segment. Although this can be done by the user calling repeatedly calling the `get_data` function, there are cases where requesting a large cache of data is more efficient to overcome communication overheads.

The format breakdown is mapped onto the required properties for ACQ-compatible driver instruments:

- `NumSamples` - The number of sample points to take in a given acquisition segment
- `NumSegments` - Number of segments within an experiment window
- `NumRepetitions` - Number of experiment windows to capture

Note that each reptitition is typically synchronised via a sequence trigger along with the individual acquisition triggers over each individual segment. The resulting array is referenced as `data[channel][repetition][segment][sample]`. Note that the channels are set or queried via the mandatory driver property `ChannelsAcquired` which holds a boolean list of enabled channels. If multiple channels are to be acquired in a disjointed manner, then one may subdivide the instrument driver into channels which are themselves ACQ-compatible driver objects; a pattern similar to that adopted with the AWG or microwave source drivers. The reason to 