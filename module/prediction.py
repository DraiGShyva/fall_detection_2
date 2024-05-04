def acceleration(df, fps, alarmThreshold=4.0):
    list = []
    max = 0

    # vòng lặp lấy vị trí của đầu [0] mỗi 3 frame để tính gia tốc theo chiều dọc (x): a(t) = |(p3 - 2 * p2 + p1) / t²|
    for i in range(0, len(df), 3):
        if i + 3 < len(df):
            p1 = df[i][0][1]
            p2 = df[i + 1][0][1]
            p3 = df[i + 2][0][1]
            a = abs((p3 - 2 * p2 + p1) / ((1 / fps) ** 2))
            list.append(a)
            if a > max:
                max = a

    try:
        # gia tốc trung bình
        tb = sum(list) / len(list)

        # Nếu gia tốc trung bình lớn hơn 5 thì có thể xảy ra ngã
        if max / tb > alarmThreshold:
            return True

    except:
        pass

    return False


def check_coordinate(df):
    for i in range(0, len(df), 3):
        if i + 3 < len(df):
            if (
                df[i][0][1] > df[i][1][1]
                or df[i][0][1] > df[i][7][1]
                or df[i][0][1] > df[i][8][1]
                or df[i][0][1] > df[i][9][1]
                or df[i][0][1] > df[i][10][1]
            ):
                return True
    return False


def check_static(df):
    # kiểm tra tất cả các điểm có sự giao động hơn chiều dài từ vai đến hông so với frame trước không (bao gồm cả x y z)
    for j in range(13):
        if (
            abs(df[0][j][0] - df[1][j][0]) > (df[0][1][0] - df[0][7][0])
            or abs(df[0][j][1] - df[1][j][1]) > (df[0][1][0] - df[0][7][0])
            or abs(df[0][j][2] - df[1][j][2]) > (df[0][1][0] - df[0][7][0])
        ):
            return False
    return True
