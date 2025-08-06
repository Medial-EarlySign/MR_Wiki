string GenericSigVec::get_type_generic_spec(SigType t)
{
	switch (t) {
	case T_Value: return "V(f)";					//  0
	case T_DateVal: return "T(i),V(f)";				//  1
	case T_TimeVal: return "T(l),V(f),p,p,p,p";		//  2
	case T_DateRangeVal: return "T(i,i),V(f)";		//  3
	case T_TimeStamp: return "T(l)";				//  4
	case T_TimeRangeVal: return "T(l,l),V(f),p,p,p,p"; //  5
	case T_DateVal2: return "T(i),V(f,us),p,p";		//  6
	case T_TimeLongVal: return "T(l),V(l)";			//  7
	case T_DateShort2: return "T(i),V(s,s)";		//  8
	case T_ValShort2: return "V(s,s)";				//  9
	case T_ValShort4: return "V(s,s,s,s)";			// 10
	case T_CompactDateVal: return "T(us),V(us)";	// 11
	case T_DateRangeVal2: return "T(i,i),V(f,f)";	// 12
	case T_DateFloat2: return "T(i),V(f,f)";		// 13
	case T_TimeRange: return "T(l,l)";				// 14
	case T_TimeShort4: return "T(i),p,p,p,p,V(s,s,s,s)"; //15
	default:
		MTHROW_AND_ERR("Cannot get generic spec of signal type %d\n", t);
	}
	return 0;
}
```
While defining a C struct the compiler will sometimes pad a struct field to align it to a 64bit address in order to optimize access times to that field .
Note that in the case of T_TimeVal, T_TimeRangeVal, T_DateVal2 and T_TimeShort4, some padding bytes were required in order to maintain binary compatibility with the old C structs. 
For example, The type T_TimeRangeVal translates to the GSV string specification "T(l,l),V(f),p,p,p,p" Which means that each data record will have 2 time channels of the type long long , one value channels of the type float and 4 padding bytes.
## GSV declarations in .signal files
Currently, In a repository .signal file you may define or view a signal's type using the old Number coding or you may choose to place a GSV string spec instead.
If you have several signals of the exact same type you may define a Spec Alias and use that alias instead. That will help to avoid bloat and improve readability.
Such alias is defined like this: **GENERIC_SIGNAL_TYPE** [*type_alias*] [*GSV_string_spec*]. Note that .signals file is a TSV which means there must be a tab between each text field.
Example :
**.signal file example**
```
GENERIC_SIGNAL_TYPE	mytype0	V(f)
GENERIC_SIGNAL_TYPE	mytype1	T(i),V(f)
SIGNAL	GENDER	100	mytype0	Male=1,Female=2	0
SIGNAL	BMI	902 mytype1	0
SIGNAL	ICD9_Hospitalization	2300	T(i,i),V(f)	1
SIGNAL	RBC	1001	1	0
...
```
In the above example we see on **lines 1-2**, 2 signals aliases defined using the GENERIC_SIGNAL_TYPE statement, named mytype0,mytype1.
Then on **lines 3-4** we see BMI and GENDER signals defined using those aliases in the type field.
On **line 5** we defined the signal directly with no alias.
On **line 6** we defined the RBC signal using it's signal type code 1 (which translates to T_DateVal ... which is identical to mytype1 actually).
## Using GSV 
The GSV implementation is defined in the class GenericSigVec which currently overrides the old USV implementation. You may still use UniversalSigVec and everything should work as usual.
```
typedef class GenericSigVec UniversalSigVec;
```
The old USV implemetation was renamed to UniversalSigVec_legacy and will later be removed.
The initialization is performed using uget() as usual. Other than that, the following constructors and init() functions were added:
```
	GenericSigVec()
	GenericSigVec(const string& signalSpec, int time_unit = MedTime::Undefined)
	GenericSigVec(SigType sigtype, int time_unit = MedTime::Undefined)
	GenericSigVec(const GenericSigVec& other)
 
	void init(const SignalInfo &info)
	void init_from_spec(const string& signalSpec);
	void init_from_sigtype(SigType sigtype);
	void init_from_repo(MedRepository& repo, int sid);
```
The old SigType is replaced by a string specification. You can also initialize it from a SignalInfo (which might be faster since the coded arrays spec is cached and no parsing will be required at runtime)
## Implementation
The implementation can be fully understood simply by reading the following value-getter function:
```
	template<typename T = float>
	T Val(int idx, int chan, const void* data_) const {
		auto field_ptr = ((char*)data_) + idx * struct_size + val_channel_offsets[chan];
		switch (val_channel_types[chan]) {
		case type_enc::FLOAT32: return (T)(*(float*)(field_ptr));
		case type_enc::INT16:   return (T)(*(short*)(field_ptr));
		case type_enc::UINT16:  return (T)(*(unsigned short*)(field_ptr));
		case type_enc::UINT8:   return (T)(*(unsigned char*)(field_ptr));
		case type_enc::UINT32:  return (T)(*(unsigned int*)(field_ptr));
		case type_enc::UINT64:  return (T)(*(unsigned long long*)(field_ptr));
		case type_enc::INT8:    return (T)(*(char*)(field_ptr));
		case type_enc::INT32:   return (T)(*(int*)(field_ptr));
		case type_enc::INT64:   return (T)(*(long long*)(field_ptr));
		case type_enc::FLOAT64: return (T)(*(double*)(field_ptr));
		case type_enc::FLOAT80: return (T)(*(long double*)(field_ptr));
		}
		return 0;
	}
```
- The function is a template allowing to retrieve float by defualt but supports other types as well.
- Location of the requested value is calculated and stored in field_ptr. val_channel_offsets array is used for that.
- 
```
The val_channel_types array is inspected to select the correct casting to type T and the value is returned.
```
## Parts that required modification to support the new GSVs
- MedConvert was modified to support GSVs duing the creation of a new repository
- MedPyExport was modified to support exporting GSVs to Python. **Note that exported Field names are now time0, time1, time2 ... val0, val1, val2 ... **
- Virtual signals were modified to support the new type secification strings in virtual signal modification.
## Performance
Performance tests showed a slight improvement comparing to the old implementation. 
That might be due to the fact that the new implementation eliminates the used of C function callbacks which are un-optimizable by C/C++ compilers.
 