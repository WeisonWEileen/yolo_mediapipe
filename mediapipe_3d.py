import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

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

    for frame in frame_keypoints:
        xs = frame[0]
        ys = frame[1]
        zs = frame[2]
        ax.scatter(xs, ys, zs)

    plt.draw()
    plt.pause(0.01)



# 第二版
# import pickle
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# with open('frame_keypoints.pkl', 'rb') as f:
#     frame_keypoints = pickle.load(f)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# for frame in frame_keypoints:
#     xs = frame[0]
#     ys = frame[1]
#     zs = frame[2]
#     ax.scatter(xs, ys, zs)

# plt.show()



# 第二版
# import pickle
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# while True:
#     with open('frame_keypoints.pkl', 'rb') as f:
#         frame_keypoints = pickle.load(f)

#     ax.clear()
#     for frame in frame_keypoints:
#         xs = frame[0]
#         ys = frame[1]
#         zs = frame[2]
#         ax.scatter(xs, ys, zs)

#     plt.draw()
#     plt.pause(0.01)