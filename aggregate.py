from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import MDS
import pandas as pd

colors = ['#990033', '#0000FF', '#00CC33', '#CC0000', '#3300CC', '#CC6600',
          '#990000', '#660000', '#66AA55', '#33FFBB', '#555588', '#990088',
          '#CCCC66', '#6699FF', '#FF9966', '#009999', '#118855', '#660066']


class Prim:
    def __init__(self, arr):
        self._edges = []
        self._arr = arr
        self._dim = len(arr)
        for i in range(self._dim):
            nex = [-1, 1000000.0]
            for j in range(i + 1, self._dim):
                if nex[1] > (arr[i][j] + arr[j][i]) / 2:
                    nex = [j, (arr[i][j] + arr[j][i]) / 2]
            self._edges.append({
                'x': i,
                'y': nex[0],
                'dis': nex[1]
            })
        self._edges = sorted(self._edges, key=itemgetter('dis'))
        self._father = None

    def _find_father(self, x: int) -> int:
        if self._father[x][0] == x:
            return x
        self._father[x][0] = self._find_father(self._father[x][0])
        return self._father[x][0]

    def _merge(self, x: int, y: int):
        if x < y:
            x, y = y, x
        fx = self._find_father(x)
        fy = self._find_father(y)
        if fx != fy:
            self._father[fx][0] = fy
            self._father[fy][1] += self._father[fx][1]
            return True
        return False

    def solve(self, grp: int):
        self._father = [[it1, 1] for it1 in range(len(data))]
        cur_grp = len(self._arr)
        cur_dis = 0
        for edge in self._edges:
            if cur_grp > grp:
                if self._merge(edge['x'], edge['y']):
                    cur_grp -= 1
                    cur_dis = edge['dis']
            else:
                break
        # 实际分得的组数和组内的最远距离
        for idx_t in range(self._dim):
            self._father[idx_t][0] = self._find_father(idx_t)
        return cur_grp, cur_dis, self._father

    @property
    def edge(self):
        return self._edges

    @property
    def father(self):
        return self._father

    @property
    def arr(self):
        return self._arr

    @property
    def dim(self):
        return self._dim


if __name__ == '__main__':
    data = np.loadtxt('test.csv', delimiter=',')
    method = Prim(data)

    ret, dis, grp_list = method.solve(99)

    grp_arr = []
    item = 0
    for idx in range(len(grp_list)):
        if idx == grp_list[idx][0] and grp_list[idx][1] >= 10:
            item += grp_list[idx][1]
            grp_arr.append(grp_list[idx][0])
    print(len(grp_arr))
    elements = []

    color_dict = {grp_arr[idx_grp]: colors[idx_grp] for idx_grp in range(len(grp_arr))}
    print(color_dict)
    for idx in range(method.dim):
        # print(idx, method.father[idx])
        if method.father[idx][0] in grp_arr:
            elements.append([idx, method.father[idx][0]])
    # print(elements)
    # print(len(elements))
    dist = []
    for item1 in elements:
        tmp_dist = []
        for item2 in elements:
            tmp_dist.append(method.arr[item1[0]][item2[0]])
        dist.append(tmp_dist)

    MDS()

    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist)
    xs, ys = pos[:, 0], pos[:, 1]
    print('points count:', len(pos))

    fig, ax = plt.subplots(figsize=(17, 9))
    ax.margins(0.05)
    for idx_pos in range(len(pos)):
        plt.scatter(pos[idx_pos][0], pos[idx_pos][1], c=color_dict[elements[idx_pos][1]])
    # plt.show()
    plt.savefig(fname="result.svg", format="svg")
