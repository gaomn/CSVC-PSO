# -*- encoding = utf-8 -*-
# @Time : 2022/6/17 14:24
# @Author : 高猛
# @File : demo.py
# @Software : PyCharm

import csv
import math
import os

from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin

from configs import set_param
from csvc_component import MPB
from tqdm import tqdm
import copy
import numpy as np
from csvc_component.PSO import PSO
from csvc_component.CSVC_Model import CSVC_Model


def CSVC_PSO(args):
    """
    main loop of csvc-pso
    """

    '''  init environment '''
    csvc_pso = CSVC_Model(args)
    mp = MPB.MovingPeaks(dim=args.x_dim, npeaks=1, number_severity=0.1, args=args)
    f_sum = 0.

    '''  loop star '''
    progress_bar = tqdm(range(args.max_step), desc=f'ID:{args.sample_id}', total=args.max_step)
    for t in range(args.max_step):

        # choose individual by csvc-pso
        x_best = csvc_pso.choose_individual(t, mp)

        # get fitness
        fit = mp.test({'x': x_best})
        f_sum += fit

        # apply solution
        mp.changePeaks(x_best)

        # save data
        with open(args.filename, 'a', newline='') as f:
            row = [int(t), float(fit), float(f_sum), x_best]
            writer = csv.writer(f)
            writer.writerow(row)

        progress_bar.update()
    progress_bar.close()


def PSO_only(args):
    mp = MPB.MovingPeaks(dim=args.x_dim, npeaks=1, number_severity=0.1, args=args)
    f_sum = 0.

    for t in range(args.max_step):

        # use pso
        pso = PSO(args, {'plm': mp})
        pso_dict = pso.update()
        x_pso_best = pso_dict['best_x']

        # get fitness
        fit = mp.test({'x': x_pso_best})
        f_sum += fit
        mp.changePeaks(x_pso_best)

        # save data
        with open(args.filename, 'a', newline='') as f:
            row = [int(t), float(fit), float(f_sum)]
            writer = csv.writer(f)
            writer.writerow(row)


def Optimal(args):
    mp = MPB.MovingPeaks(dim=args.x_dim, npeaks=1, number_severity=0.1, args=args)
    f_sum = 0.

    for t in range(args.max_step):

        # find optimal solution
        maxinum = mp.maximums()[0]
        x_ = maxinum[1]
        bt_type = args.bt_type
        if bt_type == 'linear':
            if x_[0] >= 0:
                x_best = x_
            else:
                x_temp = copy.deepcopy(x_)
                x_temp[0] = 0
                if mp.test({'name': 'MP', 'x': x_}) > (mp.test({'name': 'MP', 'x': x_temp}) + 2 * args.time_fac):
                    x_best = x_
                else:
                    x_best = x_temp
        elif bt_type == 'sin':
            if 2 * np.sin(0.2 * np.pi * x_[0]) <= x_[1]:
                x_best = x_
            else:
                x_temp = copy.deepcopy(x_)
                x_temp[1] = 2 * np.sin(0.2 * np.pi * x_[0])
                if mp.test({'name': 'MP', 'x': x_}) > (mp.test({'name': 'MP', 'x': x_temp}) + 2 * args.time_fac):
                    x_best = x_
                else:
                    x_best = x_temp
        elif bt_type == 'cir':
            if x_[0]**2 + x_[1]**2 <= 15.9:
                x_best = x_
            else:
                x_temp = copy.deepcopy(x_)
                sr = (15.89/(x_[0]**2 + x_[1]**2))**0.5
                x_temp[0] = x_[0] * sr
                x_temp[1] = x_[1] * sr

                if mp.test({'name': 'MP', 'x': x_}) > (mp.test({'name': 'MP', 'x': x_temp}) + 2 * args.time_fac):
                    x_best = x_
                else:
                    x_best = x_temp
        elif bt_type == 'rect':
            if -3.54 <= x_[0] <= 3.54 and -3.54 <= x_[1] <= 3.54:
                x_best = x_
            else:
                x_temp = copy.deepcopy(x_)

                # 方形边界
                dots = [[-3.54, -3.54], [-3.54, 3.54], [3.54, -3.54], [3.54, 3.54], ]
                n = np.argmin([math.sqrt((di[0] - x_[0])**2 + (di[1] - x_[1])**2) for di in dots])
                if -3.54 <= x_[0] <= 3.54 and -3.54 <= x_[1] <= 3.54:
                    x_temp = x_
                elif -3.54 <= x_[0] <= 3.54:
                    x_temp = [dots[n][1] if xi == 1 else xd for xi, xd in enumerate(x_temp)]
                elif -3.54 <= x_[1] <= 3.54:
                    x_temp = [dots[n][0] if xi == 0 else xd for xi, xd in enumerate(x_temp)]
                else:
                    x_temp = dots[n] + x_[2:]

                if mp.test({'name': 'MP', 'x': x_}) > (mp.test({'name': 'MP', 'x': x_temp}) + 2 * args.time_fac):
                    x_best = x_
                else:
                    x_best = x_temp
        elif bt_type == 'linear4':
            xb = set_param().x_bound
            x_0 = copy.deepcopy(x_)

            x_1 = copy.deepcopy(x_)
            x_1[0] = xb/2.

            x_2 = copy.deepcopy(x_)
            x_2[0] = 0.

            x_3 = copy.deepcopy(x_)
            x_3[0] = -xb/2.

            x_lst = [x_0, x_1, x_2, x_3]
            v_lst = [mp.test({'name': 'MP', 'x': x_tmp}) +
                     MPB.MovingPeaks.get_sym(x_tmp) * args.time_fac for x_tmp in x_lst]
            x_best = x_lst[int(np.argmax(v_lst))]

        else:
            print("bt_type error! ensure your bt_type: 'linear', 'sin', 'cir', 'rect'")
            raise

        # get fitness
        fit = mp.test({'x': x_best})
        f_sum += fit
        mp.changePeaks(x_best)

        # save data
        with open(args.filename, 'a', newline='') as f:
            row = [int(t), float(fit), float(f_sum)]
            writer = csv.writer(f)
            writer.writerow(row)



if __name__ == '__main__':
    args = set_param()
    mp = MPB.MovingPeaks(dim=args.x_dim, npeaks=1, number_severity=0.1, args=args)
    flst = []
    for t in range(args.max_step):

        # use pso
        pso = PSO(args, {'plm': mp})
        pso_dict = pso.update()
        x_pso_best = pso_dict['best_x']

        # get fitness
        fit = mp.test({'x': x_pso_best})
        if t > 0:
            flst.append(fit)
        mp.changePeaks(x_pso_best)

        if len(flst) > 8 and t % 10 == 0:
            import numpy as np
            from sklearn.cluster import KMeans
            import matplotlib.pyplot as plt

            # colors = ['#FF00004D', '#00FF004D', '#0000FF4D', '#FFA5004D', '#8000804D']
            colors = ['r', 'b', 'g', 'orange', '#8000804D']

            f_sorted = np.sort(flst)
            X = f_sorted.reshape(-1, 1)
            plt.scatter(f_sorted, -1 * np.ones_like(f_sorted), c=colors[0])

            # 使用K-means聚类成5类
            for i in range(4):
                c_num = i+2
                kmeans = KMeans(n_clusters=c_num, n_init=10, random_state=0)
                labels = kmeans.fit_predict(X)
                centers = kmeans.cluster_centers_
                datas = [[]for _ in range(c_num)]
                for li, ld in enumerate(labels):
                    datas[int(ld)].append(f_sorted[int(li)])

                m_s = [[np.mean(k), np.std(k)] for k in datas]

                print(list([int(l) for l in f_sorted]))
                print(list(labels))
                print([[int(k2) for k2 in k1] for k1 in datas])
                print([[int(k2) for k2 in k1] for k1 in m_s])
                print()

                for fi, li, ci, in zip(f_sorted, i*np.ones_like(f_sorted),[colors[label] for label in labels]):
                    plt.scatter(fi, li, c=ci, s=30)
                # plt.scatter(f_sorted, i*np.ones_like(f_sorted), c=[colors[label] for label in labels], cmap='viridis')
                # plt.scatter(centers, i*np.ones_like(centers) - 0.2, c='r', marker='o', s=100)  # 显示聚类中心点
                for k in range(c_num):
                    plt.scatter(centers[k], (i * np.ones_like(centers) - 0.2)[k], c=colors[k], marker='o', s=30)
                    plt.plot([m_s[k][0] - m_s[k][1], m_s[k][0] + m_s[k][1]], [i-0.2, i-0.2], c=colors[k])


            # # 使用K-means聚类成4类
            # kmeans = KMeans(n_clusters=4, n_init=10, random_state=0)
            # labels = kmeans.fit_predict(X)
            # centers = kmeans.cluster_centers_
            # plt.scatter(f_sorted, np.zeros_like(f_sorted), c=labels, cmap='viridis')
            # plt.scatter(centers, np.zeros_like(centers), c='red', marker='x', s=100)  # 显示聚类中心点

            # 添加标题和标签
            plt.title(f"K-means Clustering ({t})")
            plt.xlabel("f")
            plt.yticks([])  # 隐藏y轴

            # 显示图表
            plt.show()










