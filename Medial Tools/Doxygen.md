# Doxygen
Automatic HTML Documentation with C++.

# **Creating Comments in Libs**

- You can create local documentation for your code for [MR_LIBS](https://github.com/Medial-EarlySign/MR_LIBS/) by runnig this:

```bash
MR_LIBS/document_code_user.sh
```

The documentation will be created in /home/$USER/html/libs/html, please edit the script to change the desired location if needed. 
To access, you can just open the index.html file or host the directory with `python -m http.server -d /home/$USER/html/libs/html 8000` on port 8000

The build process of this repository is being executed by runnnig this script:
```bash
MR_LIBS/document_code_server.sh
```
the documentation will be availabe in [https://Medial-EarlySign.github.io/MR_LIBS](https://Medial-EarlySign.github.io/MR_LIBS)


# **General Use of Doxygen tool for other projects:**
1. Create a Doxygen configuration file by running (on Linux) to create default config file:

```bash
doxygen -g
```

2. Edit the following lines in the created file Doxyfile:
  1. PROJECT_NAME - write project name
  2. OUTPUT_DIRECTORY - the output html directory. If empty, docs will be written to html/ in the project directory. For public use, change to /var/www/html/${YOUR_DOCUMENTATION_ROOT_NAME, e.g., "Libs"}
  3. JAVADOC_AUTOBRIEF = YES
  4. OPTIMIZE_OUTPUT_FOR_C = YES
  5. QUIET = YES
  6. RECURSIVE= YES
  7. GENERATE_LATEX = NO
3. The following command will generate html documentation from comments in the code (see next section). Re-run the command if you want newly-added Doxygen comments to be incorporated.

```bash
sudo doxygen Doxyfile
```

If OUTPUT_DIRECTORY was empty, simply view html/index.html in the project directory with any browser. The public documentation (e.g., for Libs) look for Creating Lib documentation section

# How to create documentation in code
1. An example of documenting class members:

```
string predictor; ///<the predictor type - same as in the json file: qrf,lightgbm...
```

The "///" initiates a Doxygen comment and the "<" specifies that the comment comes after the element declaration. A second option is to add a comment before the member declaration:

```
 ///the predictor type - same as in the json file: qrf,lightgbm...
string predictor;
```

2. To document a class or a file, put this section before the class declaration:

```
/** ImportanceFeatureSelector(importance_selector) - selector which uses feature importance method for sepcific
* model to rank the feature importance and select them
* 
* To Use this selector specify "importance_selector"
*/
```
The first paragraph, up to a dot or an empty line, is used for a brief description, which appears at the head of the documentation page. The rest of the comment is placed in a detailed description section that appears further down on the documentation page.

3. For functions, the following syntax is better:
```
/// <summary>
/// Compares features created by current instance are compatible to features
/// </summary>
/// <returns>
/// Null if compatible, otherwise the difference
/// </returns>
```

For more details, see (external network):
https://www.stack.nl/~dimitri/doxygen/manual/docblocks.html

