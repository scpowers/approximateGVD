import numpy as np
from shapely import Polygon, Point, geometrycollections
from shapely.ops import voronoi_diagram
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as plt_poly

obs1_xrange = np.linspace(3, 6, 10)
obs1_yrange = np.linspace(3, 6, 10)
obs1_coords = [(x, obs1_yrange[0]) for x in obs1_xrange]
obs1_coords += [(obs1_xrange[-1], y) for y in obs1_yrange]
obs1_coords += [(x, obs1_yrange[-1]) for x in np.flip(obs1_xrange)]
obs1_coords += [(obs1_xrange[0], y) for y in np.flip(obs1_yrange)]
obs1 = Polygon((tuple(obs1_coords)))

outer_xrange = np.linspace(0, 10, 10)
outer_yrange = np.linspace(0, 10, 10)
outer_coords = [(x, outer_yrange[0]) for x in outer_xrange]
outer_coords += [(outer_xrange[-1], y) for y in outer_yrange]
outer_coords += [(x, outer_yrange[-1]) for x in np.flip(outer_xrange)]
outer_coords += [(outer_xrange[0], y) for y in np.flip(outer_yrange)]
outer_poly = Polygon((tuple(outer_coords)))

geoms = geometrycollections([outer_poly, obs1])
diag = voronoi_diagram(geoms, edges=True)
# remove all edges that lie on or inside of a polygon
tmp_edges = []
for ls in diag.geoms[0].geoms:
    if not obs1.crosses(ls) and not outer_poly.crosses(ls) and not obs1.contains(ls):
        tmp_edges.append(ls)
# remove stragglers
relevant_edges = []
tol = 2.5
for ls in tmp_edges:
    coords = np.array(ls.coords)
    first_pt = coords[0, :]
    second_pt = coords[1, :]
    p1_dist_diff = abs(obs1.distance(Point(first_pt)) - outer_poly.distance(Point(first_pt)))
    print(f'p1 dist diff: {p1_dist_diff}')
    p2_dist_diff = abs(obs1.distance(Point(second_pt)) - outer_poly.distance(Point(second_pt)))
    print(f'p2 dist diff: {p2_dist_diff}')
    if p1_dist_diff < tol and p2_dist_diff < tol:
        relevant_edges.append(ls)

fig, ax = plt.subplots()

coords = np.array(outer_poly.exterior.coords)
poly = plt_poly(coords, fill=False)
ax.add_patch(poly)

coords = np.array(obs1.exterior.coords)
poly = plt_poly(coords, fill=False)
ax.add_patch(poly)

for ls in relevant_edges:
    xy = np.array(ls.coords)
    plt.plot(xy[:, 0], xy[:, 1])

plt.xlim(0, 10)
plt.ylim(0, 10)
plt.show()
