from Bezier import Bezier
import numpy as np
import matplotlib.pyplot as plt



t_points = np.arange(0, 1, 0.001) #................................. Creates an iterable list from 0 to 1.
points1 = np.array([[0, 0], [0, 8.5], [5, 10], [9, 7]]) #.... Creates an array of coordinates.
curve1 = Bezier.Curve(t_points, points1) #......................... Returns an array of coordinates.

print (points1)


plt.figure()
plt.plot(
	curve1[:, 0],   # x-coordinates.
	curve1[:, 1]    # y-coordinates.
)
plt.plot(
	points1[:, 0],  # x-coordinates.
	points1[:, 1],  # y-coordinates.
	'ro:'           # Styling (red, circles, dotted).
)
plt.grid()
plt.show()