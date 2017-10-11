import numpy
from pyquaternion import Quaternion
from averageQuaternions import averageQuaternions

def rotate(motion, mode=''):
    """!
    Rotate the motion by the defined option. Operates directly on the
    given numpy array. Rotates the points and the rotation quaternions
    by the given reference.

    Available options:

        'mean': Rotate by the average of all rotation quaternions
        'start': Rotate by the rotation of the first point
        'end': Rotate by the rotation of the last point

    If none of the options is given, then this function does nothing and
    returns the identity quaternion.

    The motion format should be:

    | Frame | x | y | z | RotW | RotX | RotY | RotZ |

    @param motion numpy.array: The motion in the above format
    @param mode: The rotation reference, choose one of the options above
    @return: The normalization rotation
    """
    if 'mean' in mode:
        return byMean(motion)
    elif 'start' in mode:
        return byStart(motion)
    elif 'end' in mode:
        return byEnd(motion)
    return numpy.array([1.0,0.0,0.0,0.0])

def byMean(motion):
    reference = averageQuaternions(numpy.array(motion[:,3:7]))
    rotateBy(motion, reference)
    return reference

def byStart(motion):
    reference = motion[0,3:7]
    rotateBy(motion, reference)
    return reference

def byEnd(motion):
    reference = motion[-1,3:7]
    rotateBy(motion, reference)
    return reference

def rotateBy(motion, elements):
    q = Quaternion(elements).inverse
    for pose in motion:
        v = numpy.array(pose[0:3])
        qn = Quaternion(pose[3:7])
        a = (qn * q).elements
        b = q.rotate(v)

        pose[0] = b[0]
        pose[1] = b[1]
        pose[2] = b[2]

        pose[3] = a[0]
        pose[4] = a[1]
        pose[5] = a[2]
        pose[6] = a[3]
