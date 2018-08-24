import unittest
from waypoints_finder import *
from shapely_geojson import dumps, Feature
import matplotlib.pyplot as plt
import numpy as np
from shapely_geojson import dumps

class WaypointsFinderTestCase(unittest.TestCase):
  def _draw_points(self, points, annotate=True):
    transposed_points = np.array(points).transpose()
    if annotate:
      plt.scatter(transposed_points[0], transposed_points[1])
      plt.plot(transposed_points[0], transposed_points[1])
      for i, point in enumerate(points):
        plt.annotate(str(i), (point[0], point[1]))

  def _draw_polygon(self, polygon):
    polygon_points = np.array(polygon).transpose()
    plt.scatter(polygon_points[0], polygon_points[1], color="r")
    plt.fill(polygon_points[0], polygon_points[1], alpha=0.1)

  def test_sort_by_distance_random_points(self):
    points = np.random.rand(10, 2)
    point = np.random.rand(2)
    sorted_points = sort_by_distance(points, point)
    self._draw_points(sorted_points)
    self._draw_points([point])
    plt.show()

  def test_get_intersection(self):
    line = TEST_LINE_ONE_POINT["features"][0]["geometry"]["coordinates"]
    polygon = TEST_POLYGON["features"][0]["geometry"]["coordinates"][0]
    points, _ = get_intersection(line, polygon)
    self._draw_polygon(polygon)
    self._draw_points(line)
    self._draw_points(points)
    plt.show()

  def test_insert_dot_in_polygon(self):
    polygon = [[0, 0], [0, 1], [1, 1], [1, 0]]
    point = [0.5, 0]
    new_polygon = insert_dot_in_polygon(polygon, point)
    self._draw_points(new_polygon)
    plt.show()

  def test_find_subway(self):
    polygon = [[0, 0], [0, 1], [1, 1], [1, 0]]
    point1 = [0.5, 0]
    point2 = [1, 0.5]
    subway = find_subway(point1, point2, polygon, -1)
    print(subway)
    self._draw_polygon(polygon)
    self._draw_points(subway)
    plt.show()

  def test_find_way(self):
    plt.figure(figsize=(20, 20))
    line = TEST_LINE_ONE_POINT["features"][0]["geometry"]["coordinates"]
    polygon = TEST_POLYGON["features"][0]["geometry"]["coordinates"][0]
    way = find_way(line, polygon)
    self._draw_polygon(polygon)
    self._draw_points(line)
    self._draw_points(way, True)
    # print(dumps(to_json(way), intent=2))
    print(len(way))

    plt.show()

TEST_POLYGON = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              49.36380386352539,
              53.52107395114979
            ],
            [
              49.3560791015625,
              53.50688560601091
            ],
            [
              49.374704360961914,
              53.4984622192073
            ],
            [
              49.377965927124016,
              53.505864678570084
            ],
            [
              49.392642974853516,
              53.5007086193426
            ],
            [
              49.410667419433594,
              53.50867216986307
            ],
            [
              49.39805030822754,
              53.52479888018507
            ],
            [
              49.36380386352539,
              53.52107395114979
            ]
          ]
          # [
          #   [
          #     49.355735778808594,
          #     53.50867216986307
          #   ],
          #   [
          #     49.3861198425293,
          #     53.50867216986307
          #   ],
          #   [
          #     49.3861198425293,
          #     53.52745205453687
          #   ],
          #   [
          #     49.355735778808594,
          #     53.52745205453687
          #   ],
          #   [
          #     49.355735778808594,
          #     53.50867216986307
          #   ]
          # ]
        ]
      }
    }
  ]
}

TEST_LINE_ONE_POINT = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "LineString",
        "coordinates": [
          # [
          #   49.38963890075683,
          #   53.51464385098228
          # ],
          # [
          #   49.38191413879394,
          #   53.51061178249584
          # ],
          # [
          #   49.37856674194336,
          #   53.505456300708495
          # ],
          # [
          #   49.35161590576172,
          #   53.512296110925206
          # ],
          # [
          #   49.36689376831055,
          #   53.53015608045644
          # ],
          # [
          #   49.37702178955078,
          #   53.523472230686004
          # ],
          # [
          #   49.3919563293457,
          #   53.5239824854104
          # ]
          [
            49.368267059326165,
            53.4976453169204
          ],
          [
            49.34955596923828,
            53.516787326134
          ],
          [
            49.36423301696777,
            53.511581555524835
          ],
          [
            49.36509132385254,
            53.51500110437085
          ],
          [
            49.37985420227051,
            53.500147030467296
          ],
          [
            49.40457344055176,
            53.503363302415224
          ],
          [
            49.38363075256348,
            53.52566628239279
          ],
          [
            49.40749168395996,
            53.50489477472464
          ],
          [
            49.39101219177246,
            53.527605117217334
          ],
          [
            # 49.42877914428711,
            # 53.50040939026965
            49.40877914428711,
            53.5140939026965
          ]
        ]
      }
    }
  ]
}