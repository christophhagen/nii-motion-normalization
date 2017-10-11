import numpy

def scale(motion, mode=''):
    """!
    Scale the motion by the defined option. Operates directly on the
    given numpy array. Scales the points according to the given reference.

    Available options:

        'components': Scale each component seperately to size 1
        'largest': Scale proportionally, with the largest dimension to size 1
        'smallest': Scale proportionally, with the smallest dimension to size 1

    If none of the options is given, then this function does nothing and
    returns the origin.

    The motion format should be:

    | Frame | x | y | z | RotW | RotX | RotY | RotZ |

    @param motion numpy.array: The motion in the above format
    @param mode: The scaling reference, choose one of the options above
    @return: The normalization scaling for each dimension
    """
    if 'components' in options:
        return scaleComponents(motion)
    if 'largest' in options:
        return scaleLargest(motion)
    if 'smallest' in options:
        return scaleSmallest(motion)
    return numpy.zeros(3)



def scaleComponents(motion):
    maximums = numpy.max(motion, axis=0)
    minimums = numpy.min(motion, axis=0)
    diff =  (maximums - minimums)
    # Center of each dimension
    c = (maximums + minimums) / 2
    # scaling factors
    m = 1 / diff

    for pose in motion:
        pose[0] = c[0] + (pose[0] - c[0]) * m[0]
        pose[1] = c[1] + (pose[1] - c[1]) * m[1]
        pose[2] = c[2] + (pose[2] - c[2]) * m[2]
    return m

def scaleLargest(motion):
    maximums = numpy.max(motion, axis=0)
    minimums = numpy.min(motion, axis=0)
    diff =  (maximums - minimums)
    # largest dimension
    m = 1 / numpy.max(diff)

    # Center of each dimension
    c = (maximums + minimums) / 2

    for pose in motion:
        pose[0] = c[0] + (pose[0] - c[0]) * m
        pose[1] = c[1] + (pose[1] - c[1]) * m
        pose[2] = c[2] + (pose[2] - c[2]) * m
    return numpy.array([m, m, m])

def scaleSmallest(motion):
    maximums = numpy.max(motion, axis=0)
    minimums = numpy.min(motion, axis=0)
    diff =  (maximums - minimums)
    # smallest dimension
    m = 1 / numpy.min(diff)

    # Center of each dimension
    c = (maximums + minimums) / 2

    for pose in motion:
        pose[0] = c[0] + (pose[0] - c[0]) * m
        pose[1] = c[1] + (pose[1] - c[1]) * m
        pose[2] = c[2] + (pose[2] - c[2]) * m
    return numpy.array([m, m, m])
