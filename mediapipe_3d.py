import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
triangles = [[0, 1, 2]]


# ax.set_xlim(0.2,0.55)
# ax.set_ylim(0.6,0.9)
# ax.set_zlim(-0.03,0.03)

# detect keyboard input to quit
# def on_key(event):
    # if event.key == 'q':
    #     plt.close()



while True:
    try:
        with open('frame_keypoints.pkl', 'rb') as f:
            frame_keypoints = pickle.load(f)
            frame_keypoints = np.array(frame_keypoints) * 0.5
    except EOFError:
        continue

    ax.clear()

    # 限制坐标轴范围，但是目前效果不算好，先注释掉，因为需求是形状，而不是量化的坐标
    # ax.set_xlim(0.2,0.55)
    # ax.set_ylim(0.6,0.9)
    # ax.set_zlim(-0.03,0.03)

    # Hide axis values
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    # for frame in frame_keypoints:
    #     xs = frame[0]
    #     ys = frame[1]
    #     zs = frame[2]
    #     ax.scatter(xs, ys, zs)
    #         #    if len(frame) > 1:
    #     ax.plot(xs, ys, zs)

    #draw 3D plotting 
    thumb_f = [[0,1],[1,2],[2,3],[3,4]]
    index_f = [[0,5],[5,6],[6,7],[7,8]]
    middle_f = [[0,9],[9,10],[10,11],[11, 12]]
    ring_f = [[0,13],[13,14],[14,15],[15,16]]
    pinkie_f = [[0,17],[17,18],[18,19],[19,20]]
    fingers = [pinkie_f, ring_f, middle_f, index_f, thumb_f]
    fingers_colors = ['red', 'blue', 'green', 'black', 'orange']

    for frame in frame_keypoints:
        xs = frame[0]
        ys = frame[1]
        zs = frame[2]
        ax.scatter(xs, ys, zs,c='red', s=100)

    # ax.plot_trisurf(frame_keypoints[0], frame_keypoints[5], frame_keypoints[17], triangles=triangles)

    for finger, finger_color in zip(fingers, fingers_colors):
        for point_pair_index in finger:
            ax.plot(xs=[frame_keypoints[point_pair_index[0]][0],frame_keypoints[point_pair_index[1]][0]],
                    ys=[frame_keypoints[point_pair_index[0]][1],frame_keypoints[point_pair_index[1]][1]],
                    zs=[frame_keypoints[point_pair_index[0]][2],frame_keypoints[point_pair_index[1]][2]],
                    linewidth = 4,
                    c = finger_color
                    )

    plt.draw()
    plt.pause(0.01)



