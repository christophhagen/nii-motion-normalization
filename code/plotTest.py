# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
import numpy

import input
import plot
import glob

import clean

#for file in sorted(glob.glob('../recordings/writing/training/*.csv')):
motion = input.read('../recordings/wiping/translated/17-09-01 16-47-01.csv')
motion, _ = clean.removeDoublePoints(motion)
newMotion, count = clean.removeInvalidParts(motion)
print('Removed ' + str(count) + ' points')
print('New length is ', len(newMotion[:,0]))
plot.addPlot(motion[:,1:4], "Original")
plot.addPlot(newMotion[:,1:4], "Cleaned")
plot.plot()

#
# motion = input.read('all/17-09-01 16-44-48.csv')
# motion2 = input.read('all/17-09-01 16-44-51.csv')
#
#
# plot.addPlot(motion[:,1:4], 'Something')
# plot.addPlot(motion2[:,1:4], 'Something else')
# plot.plot()


# from os.path import basename
#
# # now you can call it directly with basename
# print(basename("/a/b/c.txt"))

# from input import read
#
# def plotMotion(fig, motion, style):
#     x = motion[:,1]
#     print(x)
#     y = motion[:,2]
#     z = motion[:,3]
#     ax.plot(x, y, z, style)
#
# file = 'all/17-09-01 16-44-48.csv'
# motion = read(file)
#
# file2 = 'all/17-09-01 16-44-51.csv'
# motion2 = read(file2)
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# plotMotion(fig, motion, 'b-')
# plotMotion(fig, motion2, 'r-')
# plt.show()
