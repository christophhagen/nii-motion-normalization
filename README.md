# nii-motion-normalization
Python code to modify recorded motions and perform translation, rotation and scaling operations to increase the recognition rate of HMM-based motion recognition. Additionally cleans the motions by removing duplicate points and large jumps in the trajectory.

## Prerequisites

The normalization part requires [numpy](http://www.numpy.org/). Additionally requires [hmmlearn](https://github.com/hmmlearn/hmmlearn) for the recognition part. Tested with Python 3.

## Usage

There are different ways to use the code. It can be used to normalize individual motions, or perform batch recognition on files in a folder structure. The code includes comments for all important functions.

Example use to read a file from a csv file:
````
from normalization import readNormalized

file = 'example.csv'
motion, t, r, s = readNormalized(
        file,
        translate = 'median',
        rotate = 'mean',
        scale = 'largest',
        clean = True)
````

The csv files must contain each frames in a seperate line. A frame consists of:
````
| Frame Number | X | Y | Z | rotW | rotX | rotY | rotZ |
````

See the `example.py` and `learning.py` files for details on the use with HMM recognition.
