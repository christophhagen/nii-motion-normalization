import numpy

def translate(motion, mode=''):
    """!
    Translate the motion by the defined option. Operates directly on the
    given numpy array. Translates the points according to the given reference.

    Available options:

        'start': Translate all points so that the first point is at origin
        'median': Translate so that the median of each component is at 0
        'mean': Translate so that the mean of each component is at 0
        'end': Translate all points so that the last point is at origin

    If none of the options is given, then this function does nothing and
    returns the origin.

    The motion format should be:

    | Frame | x | y | z | RotW | RotX | RotY | RotZ |

    @param motion numpy.array: The motion in the above format
    @param options: The translation reference, choose one of the options above
    @return: The normalization translation for each dimension
    """
    if 'start' in mode:
        return toStartPoint(motion)
    if 'median' in mode:
        return toMedianCenter(motion)
    if 'mean' in mode:
        return toMeanCenter(motion)
    if 'end' in mode:
        return toEndPoint(motion)
    return numpy.zeros(3)

# translate to move the mean in the three directions to the origin
def toMeanCenter(motion):
    center = numpy.mean(motion, axis=0)
    moveByVector(motion, center)
    return center

# translate to move the median in the three directions to the origin
def toMedianCenter(motion):
    center = numpy.median(motion, axis=0)
    moveByVector(motion, center)
    return center

# translate to move the start point to the origin
def toStartPoint(motion):
    center = motion[0]
    moveByVector(motion, center)
    return center

def toEndPoint(motion):
    center = motion[end]
    moveByVector(motion, center)
    return center

# substract the motion by a given vector
def moveByVector(motion, vector):
    for pose in motion:
        pose[0] -= vector[0]
        pose[1] -= vector[1]
        pose[2] -= vector[2]
