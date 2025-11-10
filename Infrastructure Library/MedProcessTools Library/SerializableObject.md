# SerializableObject
## **General**
SerializableObject is a class many classes inherit from. It contains tools for the following:

- Serialization via the:
    - get_size , serialize , deserialize methods.
    - the MedSerialize:: namespace mechanisms including the very useful ADD_SERIALIZATION_FUNCS mechanism
- Read/Write objects from/to files: this is a general wrapper on top of the serialization.
- init_from_string mechanism :
    - parsing of the init string
    - support the brackets {} mechanism for parameters
    - support reading parameters from a file (the pFile option)
Together this class provides a powerful and easy way to handle those very needed functionalities.
To start using the SerializableObject class, simply inherit from it in the definition.
## **Serialization**
### The virtual serialization methods
SerializableObject contains the declaration of the three major serialization methods:
```c++
	// Virtual serialization
	virtual size_t get_size() { return 0; } ///<Gets bytes sizes for serializations
	virtual size_t serialize(unsigned char *blob) { return 0; } ///<Serialiazing object to blob memory. return number ob bytes wrote to memory
	virtual size_t deserialize(unsigned char *blob) { return 0; } ///<Deserialiazing blob to object. returns number of bytes read
```
Each inheriting class should implement these methods in order to allow for its serialization. There are 2 main methods to do it:

- Directly implementing the methods - recommended only in very complex situations (mainly when using other packages not using this terminology with a need to wrap their internal way to serialize).
- Using the ADD_SERIALIZATION_FUNCS() macro : this should be the way to go and should always be preffered over any other way.
 
When using the serialzation mechanism of SerializableObject to its full power (using the ADD_SERIALIZATION_FUNCS macro) one automatically gets the following serializations:

- All needed basic types
- All supported stl containers (add yours if it is not supported : see below)
- Recusive on all used classes in variables
- A pointer to a supported class (but only to single ones, not to arrays allocated like that).
- Immunity to changes of adding more variables to the serialization - in the sense that you will still be able to read objects serialized before that change.
- Immuinity to changes of deleting variables from a serialization
- Immunity to changes of changing the order of variables in the serialization.
- Correct allocation of derived classes when deserializing a pointer to the base class.
- Note: not immune to changes in the names of variables. So changing a variable name will break serializations - try to avoid this if possible.
### ADD_SERIALIZATION_FUNCS
The ADD_SERIALIZATION_FUNCS() is a macro that adds the needed get_size, serialize and deserialize methods to the class, thus saving us the tedious work of writing it.
To use it , simply add ADD_SERIALIZATION_FUNCS to the public side of your class (that inherits from SerializableObject) with the list of the variables you need to serialize. That's it. As simple as that. Any order you like, it is not important.
The supported variables are:

- Basic types (int, float, double, string, etc...)
- Stl containers (vector<T> , map<T,S> , pair<T,S>, etc..)
- Other classes that are under SerializableObject and had implemented the serialization methods.
- T * : pointer to a single allocated (via new) SerializeObject supported class. Note : a single element and not an array (there's no way in c++ to know that size just by seeing the pointer... hence it is recommended to use vector<> when in need of something like that)
- A recursive combination of the above, for example : vector<MedModel *> , map<string, vector<vector<RepProcessor *>>> , etc...
Example : this is all that is needed to be done to serialize some classes :
```c++
// MedModel serialization line
ADD_SERIALIZATION_FUNCS(rep_processors, generators, feature_processors, predictor, serialize_learning_set, LearningSet)
 
// BasicFeatGenerator serialization line
ADD_SERIALIZATION_FUNCS(generator_type, type, tags, serial_id, win_from, win_to, d_win_from, d_win_to,
		time_unit_win, time_channel, val_channel, sum_channel, signalName, sets,
		names, req_signals, in_set_name ,bound_outcomeTime, timeRangeSignalName, timeRangeType)
```
### ADD_CLASS_NAME , MEDSERIALIZE_SUPPORT
In order to get the full functionality of the serialization process, it is needed to add the following macros for each inheriting class:

- ADD_CLASS_NAME(class name) : in the public area of the class : this creates a functions that returns the class name, and is very useful when serializing T * cases, and polymorphic classes.
- MEDSERIALIZE_SUPPORT(class name) : this should be added in the same h file but outside the class (typically we add it at the bottom of the h file). It is needed in order to connect the class serialization functions to the general recursive serialization methods.
Simply add those two simple lines for each new SerializableObject inheritting class you write.
Example:
```c++
class Example : public SerializableObject {
public:
	string name = "";
	vector<int> vec_of_ints = {0,1,2};
	vector<MedModel *> models;
 
	// ...
 
	// serialization
	ADD_CLASS_NAME(Example)
	ADD_SERIALIZATION_FUNCS(name, vec_of_ints, models)
 
}
 
//... later in the same h file
 
MEDSERIALIZE_SUPPORT(Example)
```
 
### Polymorphic classes support
If you have a Base class with inheriting classes , all inheriting from SerializableObject, you may have the following issue:
Some other class contains an element of : Base * var , but var is allocated dynamically to be one of the derived classes of Base. When serializing var we will use the serialization functions of the derived class, BUT when deserializing if we do nothing var will be newed into a Base element, and hence be Base and not the correct derived class, and we will be using its deserialization function that doesn't match the serialization function we used.
To solve that the serilizer of SerializableObject saves the type name before each T * serialization, the name is taken from the derived class, so the derived class name will be used.
When deserializing the Base class needs to provide a new_polymorphic function that returns the new to its derived class given its name.
So , to summarize:

- SerializableObject has a virtual function : void * new_polymorphic(string derived_class_name); by default it returns NULL.
- Base classes should implement it : it is easy , as it mainly contains lines of the type : if (derived_class_name == string_name_of_derived1) return new derived1; etc...
- To make implementation of the new_polymorphic function even easier, one can use the CONDITIONAL_NEW_CLASS() macro
Example : this is the new_polymorphic function of FeatureGenerator
```c++
//.......................................................................................
void *FeatureGenerator::new_polymorphic(string dname) {
	CONDITIONAL_NEW_CLASS(dname, BasicFeatGenerator);
	CONDITIONAL_NEW_CLASS(dname, AgeGenerator);
	CONDITIONAL_NEW_CLASS(dname, GenderGenerator);
	CONDITIONAL_NEW_CLASS(dname, SingletonGenerator);
	CONDITIONAL_NEW_CLASS(dname, BinnedLmEstimates);
	CONDITIONAL_NEW_CLASS(dname, SmokingGenerator);
	CONDITIONAL_NEW_CLASS(dname, KpSmokingGenerator);
	CONDITIONAL_NEW_CLASS(dname, AlcoholGenerator);
	CONDITIONAL_NEW_CLASS(dname, RangeFeatGenerator);
	CONDITIONAL_NEW_CLASS(dname, DrugIntakeGenerator);
	CONDITIONAL_NEW_CLASS(dname, ModelFeatGenerator);
	return NULL;
}
 
```
PreSerialization / PostDeSerialization
If you need to run a few commands before the serialization starts you can put them in the pre_serialization method inside your class. This is needed for example when you need to clean some of the serialized variables based on some condition before it starts.
In the same manner you can implement in the function post_deserialization operations that are needed to be done after the deserialization. This can be handy and helped convert some models (such as xgb) to use this serialization methods.
Example: this is the pre_serialization function in MedModel:
```c++
// allows for conditional serialization of LearningSet while allowing the use of the ADD_SERIALIZATION_FUNCS macro
virtual void pre_serialization() 
{ 
	if (!serialize_learning_set) 
		LearningSet = NULL; /*no need to clear(), as this was given by the user*/ 
}
```
 
### Serialization check list
1. Inherit from SerializableObject or from a class inheritting from it.
2. add the ADD_CLASS_NAME(class name) macro to your class.
3. add the MEDSERIALIZE_SUPPORT(class name) after your class definition in the same h file.
4. Use the ADD_SERIALIZATION_FUNCS(...) macro to list the variables you need to serialize.
  
1. if you can't: maybe the pre_serialization() trick can solve your problem? if so - great, implement it, and use the macro.
  
2. If you still can't due to a complex case: implement the get_size, serialize, and deserialize methods directly.
2. If your class is a Base class , make sure to implement the new_polymorphic method for it.
3. If your class is a derived class, make sure the new_polymorphic method of its base class supports your derived class.
4. Avoid changing variable names , as it will break the serialization backward support.
5. Avoid using a variable names size . This is an unclear bug (may be a compiler bug) , but using it makes the compiler think its type is different. Simply don't use it as a serialized variable.
### Tips for writing an easily serialized class and a correct one
1. Do not use c style arrays such as int * to different sizes using new or malloc. Use vector<> instead.
2. Give good names to variables (so that later they won't be changed) (don't use size as a varialble -> there's a bug when using it)
3. Use basic types, stl, other serialized classes, recursively if you need.
4. If needed you can use T * for a single element (it's ok to have a vector or map of those of course) , as long as T is a class supported by MedSerialize.
5. If needed use pre_serialization and/or post_deserialization options. Very handy when there's an inner 3rd party class with its own serialization function.
6. Make all the efforts to be able to use the ADD_SERIALIZATION_FUNCS as your serialization implementation. It is the most powerful method.
### How to use ADD_SERIALIZATION_FUNCS if my class uses a forward declaration?
Sometimes it happens that we can't use ADD_SERIALIZATION_FUNCS in the h file due to for example forward declarations of classes used, and hence this can only be compiled in the c file.
If you need that, you have the ADD_SERIALIZATION_HEADERS() in your declaration (this is to allow virtuality in base classes, otherwise not a must),
and you can use the ADD_SERIALIZATION_FUNCS_CPP(classname, ...) inside your cpp file. It is the same as the ADD_SERIALIZATION_FUNCS macro but you need to add your class name at the start.
### My stl container is not supported , how can I add it?
Help others and implement it in SerializableObject_imp.h , see there many examples for stl containers support.
 
### Known BUGS
- DO NOT USE 'size' as a variable ending up in the ADD_SERIALIZATION_FUNCS() list : possibly a compiler bug makes the serializer get the wrong type for it.
## **Init from string**
The other usage of SerializableObject is the init_from_string parsing you get for free.
When you call **init_from_string**(string init_s) for your SerializableObject class, it will parse init_s to pairs of string <-> string loaded into a map and call your **init**(map<string, string>& map) method according to the following rules:

- init_s is separated by ;
- After sepration each part is separated by = : the first element is the variable name, the second is its value (as a string)
- Should clear whitespaces before and after the variables names and values.
- If you use var=**{**value**}** then var will be the variable name and value will be its value BUT you can use ; and = inside value (!!) . This helps when passing parameters to another class via a variable. Value can contain {} variables on its own, which is also very useful at times.
- The **pFile**=fname is a reserved command: when given , init_from_string will open fname, concatenate its lines to one long string, and feed it to the usual init_from_string() method. This allows to keep parameters in a file.
- if a param is : var=**FILE:**fname : the string for the variable will be replaced by a string created by reading the file fname, getting rid of all comment and empty lines, getting rid of each line start/end spaces and eols.
- if a param is : var="**LIST:**fname" or var="**list:**fname" : the variable list will be replaced like when using the "FILE:" option, but commas (,) will be added between the string objects in the file (separated by spaces or end-of-lines, or even commas, in the file)
 
 
 
