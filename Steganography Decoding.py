import cv2
import numpy as np

# 이미지 입력
img = cv2.imread("이미지 경로")

if img is None:
    print("이미지를 로드하지 못했습니다.")
    exit(0)

text_length = [0] * 14
lo_inf = [0] * 8
text_inf = [0] * 8
length = 0
cnt = 0
x, y = 0, 0
text = 0
lo = 0
str_data = []

# 텍스트 길이 정보 비트 추출
for t in range(14):
    if img[0, t][0] % 2 == 1:
        text_length[t] = 1
    else:
        text_length[t] = 0

# 텍스트 길이 값
for t in range(14):
    length += text_length[t] * 2 ** (13 - t)

# 텍스트 길이가 포함된 14비트 길이
x = 14

while cnt < length:
    # 위치 정보 비트 추출
    for t in range(8):
        if x < img.shape[1] and y < img.shape[0]:
            if img[y, x][0] % 2 == 1:
                lo_inf[t] = 1
            else:
                lo_inf[t] = 0
            x += 1
            if x == img.shape[1]:
                x = 0
                y += 1

    # 위치 정보 값
    for t in range(8):
        lo += lo_inf[t] * 2 ** (7 - t)

    x += lo
    if x >= img.shape[1]:
        x -= img.shape[1]
        y += 1

    # 텍스트 정보 비트 추출
    for t in range(8):
        if x < img.shape[1] and y < img.shape[0]:
            if img[y, x][0] % 2 == 1:
                text_inf[t] = 1
            else:
                text_inf[t] = 0
            x += 1
            if x == img.shape[1]:
                x = 0
                y += 1
                if y == img.shape[0]:
                    print("디코딩 오류..")

    # 텍스트 정보 값
    for t in range(8):
        text += text_inf[t] * 2 ** (7 - t)

    # 정보 저장
    str_data.append(chr(text))

    # 초기화
    lo = 0
    text = 0

    cnt += 1

print("받은 텍스트:", ''.join(str_data))
