
import input
import learning

#number of states in the model
components = 100
mixture_states = 50
iterations = 50

# Log to file
input.setLogFile('../Log.txt')

models = learning.learnMotions(components, mixture_states, iterations, translate='median', rotate='mean', scale='largest')

learning.recognizeMotions(models, translate='median', rotate='mean', scale='largest')

input.closeLogFile()
