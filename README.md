# Environment
1. Python 3.6
2. Ubuntu 18.04

# How to run
1. Download and install the installation package of opensmile-2.3.0 from the official website:[https://www.audeering.com/opensmile/](https://www.audeering.com/opensmile/)
2. Copy entire 'config_lld' folder under the installed 'opensmile-2.3.0' root folder  
3. Set the opensmile root path and input data path (e.g., XXX_wav) in the feature_extraction.py file
4. Run feature_extraction.py
5. Extraction outputs will be generated under 'XXX_llds' folder, which contains both .arff and .mat output files 

# Others
Two feature sets are currently supported: IS13ComParE and eGeMAPS
