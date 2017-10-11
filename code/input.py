import numpy

"""!
The file used for logging
"""
fileToPrint = 0

def setLogFile(file):
    """!
    Set an output file for logging purposes.

    Only opens the file if no logging file is set yet.

    @param file String: The file to open
    """
    global fileToPrint
    if fileToPrint == 0:
        fileToPrint = open(file, "w")

def logLn(output=''):
    """!
    Write a line (including a line break) to the log file.

    Does nothing if no output file is specified.
    """
    global fileToPrint
    if fileToPrint != 0:
        fileToPrint.write(output + '\n')

def log(output=''):
    """!
    Write to the output file without a line break.

    Does nothing if no output file is specified.
    """
    global fileToPrint
    if fileToPrint != 0:
        fileToPrint.write(output)

def closeLogFile():
    """!
    Close the output file.

    Does nothing if no output file is specified.
    """
    global fileToPrint
    if fileToPrint != 0:
        fileToPrint.close()
        fileToPrint = 0

def read(file, separator = ','):
    """!
    Read a motion from a file path.

    The file needs to be a csv file with the rows separated by line breaks
    and the columns separated by a specified separator.
    Lines containing a value that can't be converted to a float will be ignored.
    The format of the data should contain the frame, position and rotation:

    | Frame Number | Pos x | Pos y | Pos z | Rot w | Rot x | Rot y | Rot z |

    The rotation is given as a unit quaternion.

    @param file String: The file to read from
    @param separator String: The Character between values, defaults to ','

    @return A numpy array of the motion
    """
    motion = []
    for line in open(file):
        itemList = line[:-1].split(separator)
        lineIsReadable = True
        for item in itemList:
            try:
                float(item)
            except Exception as e:
                lineIsReadable = False
        if lineIsReadable:
            pose = list(map(float,itemList))
            motion.append(pose)
    return numpy.array(motion)
