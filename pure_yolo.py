from ultralytics import YOLO

# model = YOLO('hand_detection/best_cups_2024_1_26.pt')
model = YOLO('/usr/src/2024_1000_pict.pt')

results = model(source=0, show=True, conf = 0.8)
# for result in results:
#     print("the boxes is")
#     print(result.boxes)
#     print("\n")


# print(f"student's class: {type(results)}")

# for r in results:
#         im_array = r.plot()  # plot a BGR numpy array of predictions
#         # im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
#         # im.show()  # show image
#         # im.save('results.jpg') 