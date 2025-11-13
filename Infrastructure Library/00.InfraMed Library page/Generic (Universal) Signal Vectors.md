## MedRepository SignalTypes

Legacy signal types were previously referenced by numeric IDs-this approach is now deprecated:
```c++
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

When defining C structs, compilers may add padding bytes to align fields for optimal memory access. For certain types (like T_TimeVal, T_TimeRangeVal, T_DateVal2, and T_TimeShort4), padding was added to maintain compatibility with older C structures.  
For example, T_TimeRangeVal corresponds to the GSV string "T(l,l),V(f),p,p,p,p", meaning each record contains two `long long` time channels, one `float` value channel, and four padding bytes.

## GSV Declarations in .signal Files

In repository `.signal` files, you can specify a signal’s type using either the legacy numeric code or a GSV string specification.  
If multiple signals share the same type, you can define a type alias to avoid repetition and improve clarity.  
Define an alias using:  
**GENERIC_SIGNAL_TYPE** [*type_alias*] [*GSV_string_spec*]  
(Remember: `.signal` files are tab-separated.)

Example :
**.signal file example**
```txt
GENERIC_SIGNAL_TYPE	mytype0	V(f)
GENERIC_SIGNAL_TYPE	mytype1	T(i),V(f)
SIGNAL	GENDER	100	16:mytype0	Male=1,Female=2	0
SIGNAL	BMI	902 16:mytype1	0
SIGNAL	ICD9_Hospitalization	2300	T(i,i),V(f)	1
SIGNAL	RBC	1001	1	0
...
```
In this example:

- The first two lines define type aliases (`mytype0`, `mytype1`).  
- The next two lines use these aliases for the GENDER and BMI signals.  
- The following lines show direct type specification and use of a legacy type code.

## Using GSV 
The `GenericSigVec` class implements GSVs, replacing the old USV system. You can still use `UniversalSigVec` as an alias for `GenericSigVec` for backward compatibility:
```c++
typedef class GenericSigVec UniversalSigVec;
```
The previous USV implementation is now called `UniversalSigVec_legacy` and will be removed in the future.

Initialization can be done as follows:
```c++
	GenericSigVec()
	GenericSigVec(const string& signalSpec, int time_unit = MedTime::Undefined)
	GenericSigVec(SigType sigtype, int time_unit = MedTime::Undefined)
	GenericSigVec(const GenericSigVec& other)
 
	void init(const SignalInfo &info)
	void init_from_spec(const string& signalSpec);
	void init_from_sigtype(SigType sigtype);
	void init_from_repo(MedRepository& repo, int sid);
```
The string specification replaces the old `SigType`. You can also initialize from a `SignalInfo` object for better performance, as it avoids runtime parsing.

## Implementation

The core logic is in the value getter function:
```c++
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

- This template function retrieves values (defaulting to `float`, but other types are supported).
- It calculates the value’s location using `val_channel_offsets`.
- The correct type cast is chosen based on `val_channel_types`.

## Changes for GSV Support

- `MedConvert` now supports GSVs when creating new repositories.
- `MedPyExport` can export GSVs to Python. **Exported field names are now `time0`, `time1`, ..., `val0`, `val1`, ...**
- [Virtual signals](../01.Rep%20Processors%20Practical%20Guide/Virtual%20Signals.md) now support the new type specification strings.

## Performance

Performance testing shows a slight improvement over the old implementation, likely because the new approach avoids C function callbacks, allowing better compiler optimization.

 