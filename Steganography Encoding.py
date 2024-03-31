import cv2
import numpy as np
import random

# 이미지 입력
img = cv2.imread("C:/Users/USER/Downloads/2024-04-01.jpg")

if img is None:
    print("이미지를 불러올 수 없습니다.")
    exit(1)

max_text = img.shape[1] * img.shape[0]  # 텍스트 작성 최대 범위 변수
t_length = 0  # 입력 텍스트 길이
t_length_clone = 0
inf_lo = 0  # 위치 정보 변수
data_text = 0
data_start = 0
x, y = 0, 0  # 좌표
cnt = 0

str_input = input("TEXT: ")

if max_text < 50 * 50:
    print("50x50 크기 이상의 이미지를 입력하세요.")
    exit(0)

max_text = (max_text - 14) // 25 if (max_text - 14) // 25 < 10000 else 10000 - 1

while True:
    print(f"입력 가능 텍스트 수(띄어쓰기 포함): {max_text}\n")
    str_input = input("TEXT: ")
    t_length = len(str_input)
    print(f"\nText length: {t_length}\n")

    if t_length == 0:
        print("텍스트를 입력하지 않았습니다.")
        print("다시 입력해주세요.\n\n")
    elif t_length > max_text + 1:
        print("입력 가능 텍스트 수를 초과하였습니다.")
        print("다시 입력해주세요.\n\n")
    else:
        break

# 14bit 내, 위치 정보 저장 (범위 0~37,777)
t_length_clone = t_length  # 복사

# 입력 텍스트 길이 2진수 14비트로 저장
text_length = [0] * 14
for t in range(14):
    if t_length_clone > 0:
        text_length[13 - t] = t_length_clone % 2
        t_length_clone //= 2
    else:
        text_length[13 - t] = 0

# 입력 텍스트 길이 데이터 좌표에 입력
for t in range(14):
    if img[y, x][0] % 2 == 1:
        if text_length[x] == 0:
            img[y, x][0] -= 1
    else:
        if text_length[x] == 1:
            img[y, x][0] += 1

    x += 1
    if x == img.shape[1]:
        x = 0
        y += 1

random.seed()  # 랜덤값

while cnt < t_length:
    inf_lo = random.randint(0, 10)

    data_start = inf_lo

    data_text = ord(str_input[cnt])

    e_bit_text = [0] * 8
    e_bit_lo = [0] * 8

    for t in range(8):
        if inf_lo > 0:
            e_bit_lo[7 - t] = inf_lo % 2
            inf_lo //= 2
        else:
            e_bit_lo[7 - t] = 0

        if data_text > 0:
            e_bit_text[7 - t] = data_text % 2
            data_text //= 2
        else:
            e_bit_text[7 - t] = 0

    for q in range(8):
        if img[y, x][0] % 2 == 1:
            if e_bit_lo[q] == 0:
                img[y, x][0] -= 1
        else:
            if e_bit_lo[q] == 1:
                img[y, x][0] += 1

        x += 1
        if x == img.shape[1]:
            x = 0
            y += 1

    x += data_start
    if x >= img.shape[1]:
        x -= img.shape[1]
        y += 1

    for q in range(8):
        if img[y, x][0] % 2 == 1:
            if e_bit_text[q] == 0:
                img[y, x][0] -= 1
        else:
            if e_bit_text[q] == 1:
                img[y, x][0] += 1

        x += 1
        if x == img.shape[1]:
            x = 0
            y += 1
            if y == img.shape[0]:
                print("텍스트 입력 가능 범위 초과")

    cnt += 1

cv2.imwrite("Encording_image.bmp", img)
print("텍스트 인코딩 완료!!!")
