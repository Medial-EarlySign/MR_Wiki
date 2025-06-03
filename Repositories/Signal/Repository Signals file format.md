# Repository Signals file format
comments starts with "#"
each line can start with either
- GENERIC_SIGNAL_TYPE - definition of new signal type ([Generic (Universal) Signal Vectors](/Infrastructure%20Home%20Page/Generic%20(Universal) Signal Vectors)). Format of line is GENERIC_SIGNAL_TYPE  [*type_alias*] [*GSV_string_spec*] (tab seperated of 3 tokens)
  - GENERIC_SIGNAL_TYPE - first token is the keyword GENERIC_SIGNAL_TYPE  to specify we declare a new signal type
  - *GSV_string_spec - alias name for the signal type definition*
  - *GSV_string_spec - the definition. You start with time channels (If you have) and than move to value channels (if you have).If you have time channels you start with T(X) - The X is a comma separated list of basic types as specified in the link above. For example i - is integer. T(i) means 1 time channel of integer. T(i,i) means 2 time channels for integers (Can also write T(i),T(i)). Than you specify the value channels types if you have)*
- SIGNAL - definition of signal - a line with at least 6 tokens (if you specify more, then rest are omitted). If you have less tokens, there are defaults for 5-6 tokens, that will be described:
  - SIGNAL - first token is the keyword SIGNAL to specify we declare a new signal
  - signal_name - you specify the signal name
  - signal unique code - you must provide a unique number for this signal, this code will be used internally by the infrastructure for this current repository. When using other repository, you can use different numbers.
  - signal_type - You can specify the type directly in format of "*GSV_string_spec" (for example T(i),V(f) - to specify a signal with 1 integer time channel and 1 value channel of type float), You can also provide a type declare above by GENERIC_SIGNAL_TYPE , by starting with 16:signal_type_namer*
  - A free text comment - Which is ignored. Please pay attention this is a free text comment and can be left empty. The next token is important so please pay attention you have. The default is empty text
  - A bit mask of the value channels that specify which of the value channels is categorical. For example signal with 2 value channels that the first is categorical and the second one is numeric will be coded as "10" (Default is 0 for all value channels). 
  - An optional field to document the signal unit with "|" separated for different channels
