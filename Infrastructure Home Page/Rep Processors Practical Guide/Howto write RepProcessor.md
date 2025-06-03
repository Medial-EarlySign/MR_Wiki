# Howto write RepProcessor
Rep processor procedures flow by MedModel.
This is the order of call functions for rep processor:
- Ctor call
- init_defaults() - is called to initial a default values for the Rep Processor
  - [In Learning]: int init(map<string, string>& mapper) - after parsing the string argument into dictionary of key,value by SerializableObject::init_from_string.
  - [On apply] - The arguments are initialized from the disk, the arguments of the rep processors are stored under: "ADD_SERIALIZATION_FUNCS", the other fields set by this process
- fit_for_repository(MedPidRepository) - fits and alters the processors to fit the repository - for example to understand that BMI doesn't exists so to create a virtual signal of BMI for this processor
- LEARNING Process additional calls: 
  - get_required_signal_names() - is called in here to understand what are the required singals
  - filter() - A call to understand if we "need" this rep processor, or we can remove it. For examples if we are going to create virtual signal, but no one is going to use it, we want to remove this rep processors.
- add_virtual_signals - retrieve list of "virtual signals" this rep processors wants to generate with their type
- register_virtual_section_name_id - registers the virtual signal to "dict" if this signal is categorical
- set_affected_signal_ids(MedDictionarySections) - sets the "output" signal id using the repository dict that we are going to process
- set_required_signal_ids(MedDictionarySections) - sets the "input" signal ids using the repository dict that we are going to process
- set_signal_ids(MedSignals) - sets "input/output" signals settings using MedSignals. Kind of duplicate of previous 2 steps?
- init_tables(MedDictionarySections, MedSignals) - final settings of the processors using repository  (We could "eliminate" all other steps and do all logic in here, but this "sepratioin" allow us to have good defaults that in most cases doesn't need override, init_tables in most cases will be overrided, but with less logic).
-  init_attributes() - 
- get_required_signal_names() -  adds required "signals" by the rep processor to fetch from the repository to process
- conditional_apply(PidDynamicRec, MedIdSamples) - apply the logic of the rep processor on the "Repository" (PidDynamicRec is kind of dynamic ni memory repository for a single patient that we can change the data) for this patient in all his data points.
- make_summary() - generates summary after rep processor was fully called. For example output how many outliers were, in percentage? Since rep processors is called on parallel multiple times by Feature Generators before accessing the signals by the repository, it's beneficial to have a summary call in the end
 
