import cv2
import numpy as np
import time
# Harry Potter menggunakan jubah itu untuk menjadi tidak terlihat
# teknik deteksi warna dan segmentasi
# pada green screening kita menghapus latar belakang, pada teknik ini kita menghapus latar depan

# alias python='/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6'
# mengganti piksel yang sesuai dengan piksel latar belakang untuk menghasilkan efek tidak terlihat

# Hue : Kanal ini menyimpan informasi warna. Hue dapat dianggap seperti sudut,
#       di mana 0 derajat mewakili warna merah,
#       120 derajat mewakili warna hijau,
#       dan 240 derajat mewakili warna biru.
# Saturation : Kanal ini menyimpan tingkat intensitas/kemurnian warna.
#              Contohnya warna pink kurang jenuh dibanding merah.
# Value : Kanal ini menyimpan tingkat kecerahan warna.
#         Bayangan dan kilau pada gambar muncul di kanal ini.
# membaca video menggunakan video capture

print(cv2.__version__)
capture_video = cv2.VideoCapture("video.mp4")

#biarkan kamera memanas
time.sleep(1) 
count = 0 
background = 0 

#menangkap latar belakang dalam rentang 60
for i in range(60):
	return_val , background = capture_video.read()
	if return_val == False :
		continue 

background = np.flip(background, axis=1)

#kita membaca dari video
while (capture_video.isOpened()):
	return_val, img = capture_video.read()
	if not return_val :
		break 
	count = count + 1
	img = np.flip(img , axis=1)
    # konversi gambar - BGR ke HSV
    # karena kami fokus pada deteksi warna merah
	hsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    # menghasilkan masker untuk mendeteksi warna merah
    # HSV
    # Seharusnya kain satu warna
    # kisaran bawah
	lower_red = np.array([100, 40, 40])
	upper_red = np.array([100, 255, 255])
	mask1 = cv2.inRange(hsv,lower_red,upper_red)

	lower_red = np.array([155, 40, 40])
	upper_red = np.array([180, 255, 255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)

	mask1 = mask1+mask2

    # Memperbaiki masker yang sesuai dengan warna merah yang terdeteksi
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
	mask1 = cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations = 1)
	mask2 = cv2.bitwise_not(mask1)

    # Menghasilkan keluaran akhir
	res1 = cv2.bitwise_and(background,background,mask=mask1)
	res2 = cv2.bitwise_and(img,img,mask=mask2)
	final_output = cv2.addWeighted(res1,1,res2,1,0)

	cv2.imshow("INVISIBLE MAN",final_output)
	k = cv2.waitKey(10)
	if k == 27:
		break






