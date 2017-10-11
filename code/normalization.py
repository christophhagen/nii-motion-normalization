
from input import read
import translation
import rotation
import scaling
import clean

def readNormalized(file, translate='', rotate='', scale='', clean=True):
    """!
    Read a motion from a file path and apply normalization to it.

    @param file String: The file path of the motion
    @param translate: The normalization for translating the motions
    @param rotate: The normalization for rotating the motions
    @param scale: The normalization for scaling the motions
    @param cleaning: Remove duplicate points and large jumps, default true
    @return: The normalized motion and the normalization parameters
    """
    motion = read(file)
    motion, t, r, s = normalize(motion, translate, rotate, scale, cleaning)
    return motion, t, r, s

def normalize(motion, translate='', rotate='', scale='', clean=True):
    """!
    Apply normalization to a motion.

    The input motion is not modified.

    @param motion numpy.array: The motion to normalize
    @param translate: The normalization for translating the motions
    @param rotate: The normalization for rotating the motions
    @param scale: The normalization for scaling the motions
    @param cleaning: Remove duplicate points and large jumps, default true
    @return: The normalized motion and the normalization parameters
    """
    out = motion
    translationRef = translation.tranlate(out[:,1:4], translate)
    rotationRef = rotation.rotate(out[:,4:8], rotate)
    scalingRef = scaling.scale(out[:,1:4], scale)
    out, removedPoints = clean.clean(motion)
    return out, translationRef, rotationRef, scalingRef
