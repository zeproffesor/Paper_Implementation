import matplotlib.pyplot as plt
import numpy as np

class Visualizer:

    def visualize(self):
        with open("data.txt", "r") as f:
            ts = [eval(line) for line in f.readlines()]

        timestamps = []
        for state in ts:
            orders_ts = []
            p_ts = []
            n = len(state)
            i = 0
            p = 0
            while i<n:
                if type(state[i])==tuple:
                    if state[i][0]:
                        orders_ts.append(state[i][0])
                    else:
                        orders_ts.append(-state[i][1])
                    p_ts.append(p)
                    i += 1
                    p += 1
                else:
                    # for j in range(state[i]):
                    #     uncompressed_ts.append(0)
                    p += state[i]
                    i += 1
            timestamps.append(zip(orders_ts, p_ts))

        # ax = plt.axes(projection='3d')

        # p = np.linspace(0,10000,10001)
        # # t = np.linspace(0,99,1)
        # num_ords = np.array(uncompressed_ts)

        # ax.plot3d(t,p,num_ords)

        for t in range(100, 1001, 100):
            orders_ts, p_ts = zip(*timestamps[t])
            orders_ts = np.array(orders_ts)
            p_ts = np.array(p_ts)
            plt.plot(p_ts, orders_ts)
            plt.show()


def main():
    visualizer = Visualizer()
    visualizer.visualize()

main()