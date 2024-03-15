# YOLO-v8 + Mediapipe to assist the daily life of patients with hemiplegia grasping

>Tips: Here I may change the source code of     ultralytics to improve the performance of this project.
## how to run the container
Firstly, we need to  build the image using the Dockerfile(you should run the following command in the parent folder of Dockerfile )
```
docker build -t yolo-medpip-eletron
```
Then run the container 
```
sudo docker run -dit \
--name=yolo_mediapip_eletronic \
--privileged  \
-v /dev:/dev \
-v /tmp/.X11-unix:/tmp/.X11-unix  \
-e DISPLAY=unix$DISPLAY \
-w /usr/src \
--net=host \
--ipc=host \
--gpus all \
yolo-medpip-eletron
```
## This is the plotting call stack
```mermaid
flowchart TB;

    subgraph distance computing
        id6
        id10
    end

    subgraph yolov8
    direction TB
        id1[result]--select bottle-->id2[annotator]-->id3[boxes]--pred_boxes_show_boxes-->id4["box_label() "]-->id5["cv2_rectangle() cv2_circle()"]
        id3-->id6["box_center"]
    end

    subgraph mediapipe
    direction TB;
        id8[result]-->id9[hand_landmarks]-->id10[index_9 landmark]
        id9-->id14["cv2.circle()"]
    end
    
```
Tips:
- add name property `name_handler` in the Box class for the result extract in the main function, which is assigned in the `Results.plot()`.
    ```
    d.name_handler = label
    ```
- and the final 2D box center is also assigned in the `Results.plot().annotate.box_label()` function.
    ```
    self.center_handler = 0
    ```
# The key data format transform about plotting the result: from tensor to array
from the given markdown description, we can see the `xyxy` is in Tensor format
| Name      | Type                      | Description                                                        |
|-----------|---------------------------|--------------------------------------------------------------------|
| `cpu()`   | Method                    | Move the object to CPU memory.                                     |
| `numpy()` | Method                    | Convert the object to a numpy array.                               |
| `cuda()`  | Method                    | Move the object to CUDA memory.                                    |
| `to()`    | Method                    | Move the object to the specified device.                           |
| `xyxy`    | Property (`torch.Tensor`) | Return the boxes in xyxy format.                                   |
| `conf`    | Property (`torch.Tensor`) | Return the confidence values of the boxes.                         |
| `cls`     | Property (`torch.Tensor`) | Return the class values of the boxes.                              |
| `id`      | Property (`torch.Tensor`) | Return the track IDs of the boxes (if available).                  |
| `xywh`    | Property (`torch.Tensor`) | Return the boxes in xywh format.                                   |
| `xyxyn`   | Property (`torch.Tensor`) | Return the boxes in xyxy format normalized by original image size. |
| `xywhn`   | Property (`torch.Tensor`) | Return the boxes in xywh format normalized by original image size. |

and then the numpy `squeeze()` function transfer the four detect point into 
```
annotator.box_label(d.xyxy.squeeze(), label, color=colors(c, True))
```

### ```combine.py``` 是最终的运行文件
@ TODO
- 读对面的，记录电刺激参数的帧末尾处理，记录，下次读进来作为，读杯子的宽度
