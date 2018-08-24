from shapely.geometry import Polygon
from shapely.geometry import LineString, Point
import pdb
import numpy as np
from scipy.spatial import distance
from shapely_geojson import Feature

def _point_on_line(line, point):
  a = line[0]
  b = line[1]
  c = point
  return distance.euclidean(a,c) + distance.euclidean(c,b) - distance.euclidean(a,b)

def insert_dot_in_polygon(polygon, point):
  polygon = polygon.copy()
  distances = []
  for polygon_interval_index in range(0, len(polygon)):
    polygon_interval = [polygon[polygon_interval_index], polygon[(polygon_interval_index + 1) % len(polygon)]]
    distances.append(_point_on_line(polygon_interval, point))
  polygon.insert((np.argmin(distances) + 1) % len(polygon), point)
  return polygon

def sort_by_distance(points, point):
  distances = [distance.euclidean(p, point) for p in points]
  return np.array(points)[np.argsort(distances)].tolist()

def _extract_points(intersection, point):
  if type(intersection) == Point:
    return [intersection.bounds[0:2]]
  else:
    intersection_points = [p.bounds[0:2] for p in intersection]
    return sort_by_distance(intersection_points, point)

def get_intersection(line, polygon):
  print(polygon)
  polygon = LineString(polygon)
  intersection = []
  intervals = []
  for line_interval_index in range(0, len(line) - 1):
    line_interval = LineString([line[line_interval_index], line[(line_interval_index + 1) % len(line)]])
    points = _extract_points(line_interval.intersection(polygon), line[line_interval_index])
    intersection += points
    intervals += [line_interval_index] * len(points)
  return intersection, intervals

def find_subway(point1, point2, polygon, direction=1):
  subway = []
  polygon = insert_dot_in_polygon(polygon, point1)
  polygon = insert_dot_in_polygon(polygon, point2)
  print(polygon)
  index1 = polygon.index(point1)
  index2 = polygon.index(point2)
  index = index1
  while index != index2:
    subway.append(polygon[index])
    index = (index + direction) % len(polygon)
  subway.append(point2)
  return subway

def get_length(line):
  return LineString(line).length

def find_way(line, polygon):
  intersection, intervals = get_intersection(line, polygon)
  new_line = []
  last_interval = 0
  print(intervals)
  for point_index in range(0, len(intersection), 2):
    subway1 = find_subway(intersection[point_index], intersection[point_index + 1], polygon, 1)
    subway2 = find_subway(intersection[point_index], intersection[point_index + 1], polygon, -1)
    selected_subway = subway1
    print(selected_subway)
    if get_length(subway1) > get_length(subway2):
      selected_subway = subway2
    for i in range(last_interval, intervals[point_index]):
      new_line.append(line[i])
    new_line.append(line[intervals[point_index]])
    new_line += selected_subway
    last_interval = intervals[point_index + 1] + 1
  new_line.append(line[-1])
  return new_line

def to_json(line):
  feature = Feature(LineString(line))
  return feature