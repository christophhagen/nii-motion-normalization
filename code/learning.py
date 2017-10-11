#HMM model for learning
from hmmlearn import hmm
#Unix style pathname pattern expansion
import glob
#random numbers, multi-dimensional arrays
import numpy
#Ignore deprecation warning from hmmlearn package
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
#python modules for machine learning and data mining
import sklearn
import normalization
import input
import plot

import os.path as string

def createGMMComponents(components):
    """!
    Create the Gaussion Mixture Models for the HMM

    @param components Int: The number of components to use
    """
    #empty list of GM models
    gmms = []
    for i in range(0,components):
        # Add mixture models to the list for each state of the HMM
        newModel = sklearn.mixture.GMM()
        gmms.append(newModel)
    return gmms

def createMotionsAndLengths(path, translate='', rotate='', scale=''):
    """!
    Read the motions from a folder and create a concatenated array with the lengths.

    The given directory 'path' must contain a subdirectory 'training' containing the motions
    as individual csv files.

    @param path String: The path to the motion data.
    @param translate: The normalization for translating the motions
    @param rotate: The normalization for rotating the motions
    @param scale: The normalization for scaling the motions
    @return: The concatenated motions and a list of the motion lengths
    """
    # list of motions read from the file
    motions = []
    # length of motions read from the file
    lengths = []
    count = 0
    plot.clearPlot()
    input.logLn('\n- ' + '{:<10}'.format(path + ':'))
    # read all files from directory associated with one motion
    for file in sorted(glob.glob(path + '/training/*.csv')):
        print(file)
        input.logLn(string.basename(string.splitext(file)[0]))
        count += 1
        #read motion and normalize
        motion = input.read(file)
        motion,t,r,s = normalization.normalize(motion, translate, rotate, scale)

        # Add to plot all training plots
        plot.addPlot(motion[:,1:4], file)

        # Add motion to the list of motions
        motions.append(motion)
        # Add length (number of poses in motion) to the list of lengths
        lengths.append(len(motion))
    _, folderName = string.split(string.dirname(path))
    # Plot all training motions
    plot.plot('../plots/' + folderName + ' training')
    # The observations are a list of poses
    X = numpy.concatenate(motions)
    return X, lengths

def learnMotions(components, states, iterations, dataPath='../data', translate='', rotate='', scale=''):
    """!
    Learn all the (normalized) motions and return the trained models.

    This functions looks for the motions in a directory.
    Each motion type is specified by it's own directory, which must include a subdirectory 'training'.
    This directory contains the training motions as csv files.
    For the default dataPath '../recordings' the structure is as follows:

    + code:

      - learning.py <- This file

    + recordings:

      + motion1:

        + training:

          - sample1.csv

          - sample2.csv

          ...

      + motion2:

        ...

    @param components Int: The number of components to use
    @param states Int: The number of HMM states
    @param iterations Int: The number of iterations to converge to the model
    @param translate: The normalization for translating the motions
    @param rotate: The normalization for rotating the motions
    @param scale: The normalization for scaling the motions
    @return the trained models
    """
    # empty list for the trained models, one model for each motion, here 2
    models = []

    input.logLn('Learning motions.')
    input.logLn('-------------------------------------')
    input.logLn('Available motions:')
    # go through all motions
    for folder in sorted(glob.glob(dataPath + '/*/')):
        #model = hmm.GaussianHMM(n_components=components, n_iter = iterations, init_params="smt")
        #initialize model as Hidden Markov Model with Gaussion Mixture emissions
        # n_components: Number of states in the model
        # n_iter: Maximum number of iterations for the EM algorithm to find optimal solution
        # n_mix: Number of states in the Gaussion Mixture Model
        # init_params: s: startprob, m: means, t: transmat
        model = hmm.GMMHMM(n_components=components,
        init_params="smt",
        n_iter = iterations,
        n_mix = states)

        # Add the GMMs to the HMM
        model.gmms_ = createGMMComponents(components)

        # create concatenated motions and length array
        X, lengths = createMotionsAndLengths(folder, translate, rotate, scale)

        # use the observations and the lengths of the motions to fit the model
        model.fit(X,lengths)
        # add the model to the list of models
        models.append(model)
    input.logLn('')
    return models

def recognizeFile(models, file, translate='', rotate='', scale=''):
    """!
    Match a single file and return the resulting scores as well as the
    normalization parameters.

    @param models list: The previously trained HMM models
    @param file String: The file containing the motion.
    @param translate String: The normalization type for correcting translation
    @param rotate String: The normalization type for correcting rotation
    @param scale String: The normalization type for correcting scaling
    @return An array of the model scores, translation, rotation, scaling parameters
    """
    #print(file)
    #read motion and normalize
    motion = input.read(file)
    motion,t,r,s = normalization.normalize(motion, translate, rotate, scale)

    plot.addPlot(motion[:,1:4], file)
    #writePointsToGrapherFile(motion, file)

    scores = []
    # check motion score (likelyhood) for each recording
    for i,model in enumerate(models):
        scores.append(float(model.score(motion)))
    return numpy.array(scores), t, r, s

def recognizeFilesInFolder(models, folder, translate='', rotate='', scale=''):
    """!
    Match all files in a folder and return the resulting scores as well as the
    normalization parameters.

    @param models list: The previously trained HMM models
    @param folder String: The folder path containing the motions.
    @param translate String: The normalization type for correcting translation
    @param rotate String: The normalization type for correcting rotation
    @param scale String: The normalization type for correcting scaling
    @return An list of arrays of the model scores, lists of the translation, rotation, scaling parameters
    """
    scores = []
    tr = []
    ro = []
    sc = []
    names = []
    print(folder)
    for file in sorted(glob.glob(folder + '/*csv')):
        print(file)
        score, t, r, s = recognizeFile(models, file, translate, rotate, scale)
        scores.append(score)
        tr.append(t)
        ro.append(r)
        sc.append(s)
        names.append(string.basename(string.splitext(file)[0]))
    return scores, tr, ro, sc, names

def plotFile(file, translate='', rotate='', scale=''):
    """!
    Read a single motion from a file and add it to the current plot list.

    @param file String: The file containing the motion.
    @param translate String: The normalization type for correcting translation
    @param rotate String: The normalization type for correcting rotation
    @param scale String: The normalization type for correcting scaling
    """
    #read motion and normalize
    motion = input.read(file)
    motion,t,r,s = normalization.normalize(motion, translate, rotate, scale)

    plot.addPlot(motion[:,1:4], file)

def plotFilesInFolder(folder, translate='', rotate='', scale=''):
    """!
    Read all motions from a folder and add them to the current plot list.

    @param folder String: The folder path containing the motions.
    @param translate String: The normalization type for correcting translation
    @param rotate String: The normalization type for correcting rotation
    @param scale String: The normalization type for correcting scaling
    """
    for file in sorted(glob.glob(folder + '/*csv')):
        plotFile(file, translate, rotate, scale)

def recognizeMotions(models, dataPath = '../data', translate='', rotate='', scale=''):
    """!
    Recognize all motions in an appropriate directory structure.

    For the default dataPath '../recordings' the structure is as follows:

    + code:

      - learning.py <- This file

    + recordings:

      + motion1:

        + training:

          - sample1.csv

          - sample2.csv

          ...

      + motion2:

        ...

    The resulting model scores and normalization parameters are saved in a csv
    file with the relative file path '../Scores.csv'. Additionally multiple
    plots are created in the folder '../plots' which contain the training motions,
    the recognized motions, and the wrongly recognized motions together with the
    training motions for comparison.

    @param models list: A list of the previously trained models.
    @param dataPath: The directory containing the motion files.
    @param translate String: The normalization type for correcting translation
    @param rotate String: The normalization type for correcting rotation
    @param scale String: The normalization type for correcting scaling
    """

    # create list of motion types
    motionTypes = []
    for motionType in sorted(glob.glob(dataPath + '/*/')):
        motionTypes.append(string.split(string.dirname(motionType))[1])
    # write file header
    fileToPrint = open(dataPath + '/' + "../scores.csv", "w")
    fileToPrint.write('Motion,Variation,Name,Translation X,Translation Y,Translation Z')
    fileToPrint.write(',Rotation W,Rotation X,Rotation Y,Rotation Z')
    fileToPrint.write(',Scaling X,Scaling Y,Scaling Z')
    for path in motionTypes:
        fileToPrint.write(',' + path)
    fileToPrint.write(',Recognized,Correct\n')

    for pathIndex, path in enumerate(motionTypes):
        #print("Motion: " + path)
        wrongMotions = []
        plot.clearPlot()
        variations = []
        for variation in sorted(glob.glob(dataPath + '/' + path + '/*/')):
            variations.append(string.split(string.dirname(variation))[1])
        for variation in variations:
            #print("Variation: " + variation)
            folder = dataPath + '/' + path + '/' + variation
            scores, tr, ro, sc, names = recognizeFilesInFolder(models, folder, translate, rotate, scale)
            # write scores to file
            for i, name in enumerate(names):
                fileToPrint.write(path + ',' + variation + ',{:<20},'.format(name))
                t = tr[i]
                fileToPrint.write("{:8.3f},{:8.3f},{:8.3f}".format(t[0], t[1], t[2]))
                r = ro[i]
                fileToPrint.write(",{:8.3f},{:8.3f},{:8.3f},{:8.3f}".format(r[0], r[1], r[2], r[3]))
                s = sc[i]
                fileToPrint.write(",{:8.3f},{:8.3f},{:8.3f}".format(s[0], s[1], s[2]))
                for score in scores[i]:
                    fileToPrint.write(",{:7d}".format(int(score)))
                # find maximum score index
                m = numpy.argmax(scores[i])
                fileToPrint.write(',' + motionTypes[m] + ',')
                fileToPrint.write(str(m == pathIndex))
                fileToPrint.write('\n')
                if m != pathIndex:
                    wrongMotions.append(folder + '/' + name + '.csv')
        plot.plot('../plots/' + path + ' recognition')
        # Plot wrongly identified motions
        if len(wrongMotions) > 0:
            plotFilesInFolder(dataPath + '/' + path + '/training', translate, rotate, scale)
            for file in wrongMotions:
                plotFile(file, translate, rotate, scale)
            plot.plot('../plots/' + path + ' wrong')
    fileToPrint.close()
