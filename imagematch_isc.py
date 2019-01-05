import cv2

def img_incsign(img_gray, img_h, img_w):
    # initialize
    val = [[0 for i in range(img_w)] for j in range(img_h)]
    incSign = [[0 for i in range(img_w)] for j in range(img_h)]

    for i in range(img_h):
        for j in range(img_w):
            val[i][j] = img_gray[i, j]

    for i in range(img_h):
        for j in range(img_w-1):
            sign_val = int(val[i][j+1]) - int(val[i][j])
            if(sign_val >= 0):
                incSign[i][j] = 1
            else:
                incSign[i][j] = 0

    return incSign

def calc_score(temp_IncSign, temp_h, temp_w, org_IncSign, i, j, thining_rate):
    n_m = 0.0
    n_u = 0.0
    C = 0.0
    for k in range(0, temp_h, thining_rate):
        for l in range(0, temp_w, thining_rate):
            if (temp_IncSign[k][l] == org_IncSign[k+i][l+j]):
                n_m = n_m + 1
            else:
                n_u = n_u + 1
    nm = n_m + n_u
    C = n_m / nm

    return C


if __name__ == '__main__':
    # open template image
    img_temp = cv2.imread("./lena_eye.jpg")
    img_gray_temp = cv2.cvtColor(img_temp, cv2.COLOR_BGR2GRAY)

    # open original image
    img_org = cv2.imread("./lena_dark.jpg")
    img_gray_org = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)

    # get image size
    temp_h = img_gray_temp.shape[0]
    temp_w = img_gray_temp.shape[1]
    org_h = img_gray_org.shape[0]
    org_w = img_gray_org.shape[1]

    # generate increment sign from temp image
    temp_IncSign = img_incsign(img_gray_temp, temp_h, temp_w)

    # generate increment sign from original image
    org_IncSign = img_incsign(img_gray_org, org_h, org_w)

    # compare increment sign by all pixels
    C_MAX = 0
    thining_rate = 2
    for i in range(org_h - temp_h):
        for j in range(org_w - temp_w):
            C = calc_score(temp_IncSign, temp_h, temp_w, org_IncSign, i, j, thining_rate)
            if (C > C_MAX):
                # store point
                C_MAX = C
                # store coordinate
                x = i
                y = j


    # output matching result
    cv2.rectangle(img_org, (y, x), (y+temp_w, x+temp_h), (0, 0, 255), 2)
    cv2.imwrite("./result.jpg", img_org)
    score = C_MAX * 100 #[%]
    print("match rate : ", score)