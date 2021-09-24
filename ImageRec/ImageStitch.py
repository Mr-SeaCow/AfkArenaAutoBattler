import cv2
import matplotlib.pyplot as plt
import numpy as np
from Util import get_grayscale


def cropImg(img):
    return img[220:img.shape[0]-600 :].copy()

def showPlot(img, name=""):
    plt.imshow(im_v)
    plt.title(name)
    plt.show()


img_ = cropImg(cv2.imread('ScreenCap4.png'))
img = cropImg(cv2.imread('ScreenCap3.png'))

img1 = get_grayscale(img_.copy())#, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE
img2 = get_grayscale(img.copy())
cv2.imwrite("CroppedImg1.png", img1)
cv2.imwrite("CroppedImg2.png", img2)


#crop_img1 = cropImg(img1)
#crop_img2 = cropImg(img2)

### plt.imshow(crop_img1)
### plt.show()
### plt.imshow(crop_img2)
### plt.show()
height,width = img2.shape
img1_mask = cv2.rectangle(img1.copy(), (0, 0), (width, height-270), (255, 255, 255), cv2.FILLED)
img2_mask = cv2.rectangle(img2.copy(), (0, 270), (width, height), (0, 255, 0), cv2.FILLED)
#plt.imshow(img1_mask)
#plt.show()

#plt.imshow(img2_mask)
#plt.show()




#sift = cv2.SIFT_create()
#
#kp1, des1 = sift.detectAndCompute(img1,None)
#kp2, des2 = sift.detectAndCompute(img2_mask,None)
#
#bf = cv2.BFMatcher()
#matches = bf.knnMatch(des1,des2, k=2)
#
#
#
#good = []
#for m in matches:
#    if (m[0].distance < .1*m[1].distance):
#        good.append(m)
#
#matches = np.asarray(good)
#
#
#if (len(matches[:,0]) >= 2):
#    src = np.float32([ kp1[m.queryIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
#    dst = np.float32([ kp2[m.trainIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
#    H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
#else:
#    raise AssertionError('Can’t find enough keypoints.')
#dst = cv2.warpPerspective(img1,H,((img1.shape[1]), (img1.shape[0] + img2.shape[0])))
#
#cv2.imwrite('test.jpg',dst)
#dst[img1.shape[0]:img1.shape[0] + img2.shape[0], 0:img2.shape[1]] = img2
#dst[0:img1.shape[0], 0:img1.shape[1]] = img1
##dst[img1.shape[0]:img1.shape[0]+img2.shape[0], 0:img2.shape[1]] = img2 #stitched image
#cv2.imwrite('output.jpg',dst)
#
##plt.imshow(dst)
##plt.show()
#img3 = np.zeros((5,5,3), np.uint8)
#img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,img3, flags=2)
#plt.imshow(dst),plt.show()


sift = cv2.SIFT_create()
# find key points
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

match = cv2.BFMatcher()
matches = match.knnMatch(des1,des2,k=2)

good = []
for m,n in matches:
    if .03*m.distance < 0.03*n.distance:
        good.append(m)

draw_params = dict(matchColor=(0,255,0),
                       singlePointColor=None,
                       flags=2)

img3 = cv2.drawMatches(img_,kp1,img,kp2,good,None,**draw_params)
#cv2.imshow("original_image_drawMatches.jpg", img3)
#plt.imshow(img3)
#plt.show()

MIN_MATCH_COUNT = 10
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,2,1)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,2,1)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts, M)
    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    #cv2.imshow("original_image_overlapping.jpg", img2)
   #plt.imshow(img2)
   #plt.title("Image 2")
   #plt.show()
else:
    print("Not enought matches are found - %d/%d", (len(good)/MIN_MATCH_COUNT))

dst = cv2.warpPerspective(img_,M,(img.shape[1], img.shape[0]))
#dst[0:img.shape[0],0:img.shape[1]] = img
#plt.imshow(dst)
#plt.title("DST")
#plt.show()
def trim(frame):
    #crop top
    if not np.sum(frame[0]):
        return trim(frame[1:])
    #crop top
    if not np.sum(frame[-1]):
        return trim(frame[:-2])
    #crop top
    if not np.sum(frame[:,0]):
        return trim(frame[:,1:])
    #crop top
    if not np.sum(frame[:,-1]):
        return trim(frame[:,:-2])
    return frame
trimmed_dst= trim(dst)
print(trimmed_dst.shape)


imgToBeConcat = img_[0:img_.shape[0]-trimmed_dst.shape[0] :].copy()
im_v = cv2.vconcat([imgToBeConcat, img])

def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))


#kmeans = kmeans_color_quantization(im_v, clusters=4)
#result = kmeans.copy()

seed_point = (10, 10)
#cv2.floodFill(result, None, seedPoint=seed_point, newVal=(0, 0, 0), loDiff=(52, 52, 52, 52), upDiff=(52, 52, 52, 52))


d=15

cv2.floodFill(im_v, None, seedPoint=seed_point, newVal=(0, 0, 0), loDiff=(d,d,d,d), upDiff=(d,d,d,d))

seed_point = (10, img_.shape[0])

cv2.floodFill(im_v, None, seedPoint=seed_point, newVal=(0, 0, 0), loDiff=(d,d,d,d), upDiff=(d,d,d,d))

cv2.imwrite("Final.png", im_v)