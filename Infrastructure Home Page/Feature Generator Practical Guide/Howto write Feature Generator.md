# Howto write Feature Generator
Feature generator procedures flow by MedModel.
This is the order of call functions for feature generator
- Ctor call
- init_defaults() - is called to initial a default values for the Rep Processor
  - [In Learning]: int init(map<string, string>& mapper) - after parsing the string argument into dictionary of key,value by SerializableObject::init_from_string.
  - [On apply] - The arguments are initialized from the disk, the arguments of the rep processors are stored under: "ADD_SERIALIZATION_FUNCS", the other fields set by this process
- fit_for_repository(MedPidRepositry) - transform/change the generator due to fit the repository inputs. For example, change the logic in smoking generator if there are no certain signals in the repository
- get_required_signal_ids() - returns the list of required signal ids to learn/apply this feature  generator (as part of init_all - can we remove this call? since this will be called again later and currently it's not initialized?)
- set_required_signal_ids(MedDictionarySections) - stores the needed signal id's to learn/apply this generator using dicts
- set_signal_ids(MedSignals) - stores the needed signal id's to learn/apply this generator using signals
- init_tables(MedDictionarySections) - stores the needed signal id's to learn/apply this generator using dicts
- filter_features() - getting all "required" features from next steps and returns if we need this generator, or can we drop it? For example, if there is feature selection and this feature is no longer needed, we don't need to calculate this. boolean function and it checks if this generators "touches" something that the model needs
- get_required_signal_names() - returns all needed signals to run this generator
- learn() (called ONLY in LEARNING)
- prepare() - to prepare the feature, attributes, allocate space
- get_p_data() - initialize the address of the generator output (for parallelism)
- get_required_signal_ids() - returns the list of required signal ids to learn/apply this feature  generator
- generate() - generate the feature
- make_summary() - makes summary after generation on all data (since generate is called in parallel for each sample) we want to have ability to collect some stats in the end
