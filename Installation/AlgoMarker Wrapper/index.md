# AlgoMarker Wrapper

## Description
The AlgoMarker Wrapper provides a REST API for the AlgoMarker C++ Library. There are two wrappers available:

1. [C++ Native Wrapper](C++%20Native%20Wrapper.md): Minimal dependencies, very fast and efficient. Uses Boost Beast. Can be installed in a minimal Ubuntu Chiselled Docker image with just glibc.
2. [Python Server Wrapper](Python%20Server%20Wrapper.md): Built with FastAPI, more flexible for changes, and supports the old AlgoMarker API. It is slower and has more dependencies but is friendlier for testing. 