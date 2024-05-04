import time
from cv2 import imshow, waitKey, VideoCapture, CAP_PROP_FPS
from module.prediction import acceleration, check_coordinate, check_static
from module.pose_landmarker import extract_pose_features, draw, mp_pose

fps = 15.0
sampling_interval = 1.5  # Độ dài của mẫu
prediction_interval = 0.5  # Khoảng cách giữa các mẫu
# Tức là sau 1,5 giây đầu tiên, mỗi 0,5 giây sẽ dự đoán một lần
# Mỗi lần dự đoán sẽ lấy số lượng mẫu bằng độ dài mẫu * tốc độ khung hình


cap = VideoCapture(0)
cap.set(CAP_PROP_FPS, fps)
df = []

# bật camera
cap.read()

# đợi 5 giây sau khi cam bật lên để ổn định
time.sleep(5)

fall = False
time_no_static = 0
time_static = 5

while True:
    # Đọc frame từ webcam
    frame = cap.read()[1]

    # Trích xuất mask
    # segments = mp_pose.process(frame).segmentation_mask  # type: ignore

    # Trích xuất các điểm mốc
    landmarks = extract_pose_features(frame)

    # Nếu có điểm mốc thì vẽ các điểm mốc
    if landmarks is not None:
        frame = draw(frame, landmarks)
        # Lưu các điểm mốc vào dataframe
        df.append(landmarks)

    # Hiển thị kết quả
    imshow("Pose Detection", frame)

    # Nếu nhấn phím Esc thì dừng chương trình
    if waitKey(1) == 27 or cap.read()[0] == False:
        print("Program stopped")
        cap.release()
        break

    if fall:
        if check_static(df):
            time_no_static += 1
        else:
            time_static += 1

    if time_static > 21:
        time_no_static = 0
        time_static = 0
        fall = False

    if time_no_static > 42:
        print("Fall detected")
        fall = False
        time_no_static = 0

    if len(df) >= sampling_interval * fps:

        # Nếu quá 30% mẫu có tọa độ bằng 0 thì bỏ qua (của tất cả các điểm mốc chứ không phải của mỗi điểm 0)
        if (
            sum([1 for i in df for j in i for k in j if k == -1])
            > len(df) * 13 * 3 * 0.3
        ):
            df = df[int(prediction_interval * fps) :]
            continue

        if not fall:
            print("----")

        if acceleration(df, fps) and check_coordinate(df):
            fall = True
            print("-------------")

        df = df[int(prediction_interval * fps) :]
