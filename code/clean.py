
import numpy

def clean(motion, correctFrames=True, threshold= 1E-7, factor=3):
    """!
    Clean a motion.

    @param correctFrames Boolean: If the frame numbering should be corrected, defaults to True
    @param threshold Number: The distance between two points to be considered equal, default 1E-7
    @param factor Number: The threshold for detecting jumps as a multiple of the mean distance between all points, default 3
    @return The largest section of the motion without dublicate points, the number of removed points
    """
    out, count1 = removeDoublePoints(motion)
    out, count2 = removeInvalidParts(motion)
    return out, count1 + count2

def removeDoublePoints(motion, correctFrames = True, threshold = 1E-7):
    """!
    Remove all dublicate points (very similiar x,y,z coordinates)
    The input is a numpy array of the motion, with each data point in one row:

    | FrameIndex | x | y | z | ... The rest of the data |

    The FrameIndex can be updated to again be consecutive numbers.

    The threshold for two consecutive points to be considered equal can be passed
    by using the parameter 'threshold'

    @param motion numpy array: the motion as an array, with [:,1:4] being the xyz coordinates
    @param correctFrames Boolean: If the frame numbering should be corrected, defaults to True
    @param threshold Number: The distance between two points to be considered equal, default 1E-7

    @return A copy of the motion with the dublicate points (rows) removed, and the number of removed points
    """
    outMotion = []
    p = numpy.array([0.0, 0.0, 0.0])
    # count number of skipped items
    count = 0
    for item in motion:
        distance = numpy.sqrt((p[0]-item[1])**2 + (p[1]-item[2])**2 + (p[2]-item[3])**2)
        if distance > 1E-7:
            outMotion.append(item)
            p = item[1:4]
        else:
            count += 1

    outArray = numpy.array(outMotion)
    # correct frame count
    if correctFrames:
        for i in range(0, len(outArray[:,0])):
            outArray[i][0] = i+1
    return outArray, count

def removeInvalidParts(motion, correctFrames = True, factor = 3):
    """!
    Detects large jumps between consecutive points and selects the largest
    sequence of points between all jumps.

    The input is a numpy array of the motion, with each data point in one row:

    | FrameIndex | x | y | z | ... The rest of the data |

    The FrameIndex can be updated to again be consecutive numbers.

    @param motion numpy array: The original motion (not modified), with [:,1:4] being the xyz coordinates
    @param correctFrames Boolean: If the frame numbering should be corrected, defaults to True
    @param factor Number: The threshold for detecting jumps as a multiple of the mean distance between all points, default 3

    @return The motion with the jumps removed, and the number of dropped points
    """
    rows = len(motion[:,0])
    # save distances between points, calcuate mean
    distances = []
    p = motion[0][1:4]
    for index, item in enumerate(motion[1:]):
        distance = numpy.sqrt((p[0]-item[1])**2 + (p[1]-item[2])**2 + (p[2]-item[3])**2)
        distances.append(distance)
        p = motion[index][1:4]
    m = numpy.mean(distances)

    # check all distances for too large gaps
    jumps = []
    p = motion[0][1:4]
    for index, item in enumerate(motion[1:]):
        distance = numpy.sqrt((p[0]-item[1])**2 + (p[1]-item[2])**2 + (p[2]-item[3])**2)
        if distance / m > factor:
            jumps.append(index+1)
            #print('At index ' + str(index) + ': ' + str(distance / m))
        p = item[1:4]
        d = distance

    # pick largest part between jumps
    jumps.append(rows)
    #print(jumps)
    start = 0
    end = rows
    prev = 0
    m = 0
    for item in jumps:
        l = item - prev
        if l > m:
            m = l
            start = prev
            end = item
        prev = item
    outMotion = motion[start:end]
    # correct frame count
    if correctFrames:
        for i in range(0, len(outMotion[:,0])):
            outMotion[i][0] = i+1
    return outMotion, rows - end + start
