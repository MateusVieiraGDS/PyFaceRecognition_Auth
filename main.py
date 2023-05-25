import cv2
import face_recognition as fr
import threading
import time


webcam = cv2.VideoCapture(0)
locations = []
encodings = []
compress_value = 50 #0 - 90
cont = 0

def detect_face():
    global locations, cont, encodings
    cv = compress_value
    cv = (100 - ((cv if cv > 0 else 1) if cv <= 90 else 90))
    print(cv)
    while webcam.isOpened():
        v, f = webcam.read()
        r_prop = (cv / 100)
        f_resize = cv2.resize(f, (int(f.shape[1] * r_prop), int(f.shape[0] * r_prop)))
        f_gray = cv2.cvtColor(f_resize, cv2.COLOR_BGR2GRAY)
        lcs = fr.face_locations(f_gray)
        #new_lcs = list(map(lambda face: list(map(lambda cord: cord*4, face)), lcs))
        new_lcs = []
        
        for i, face in enumerate(lcs):            
            new_lcs.append([])            
            for i2, cord in enumerate(face):
                new_lcs[i].append(int((cord * 100) / cv))            
        #encodings = new_enc
        locations = new_lcs
        print(encodings)
        cont += 1

t1 = threading.Thread(target=detect_face)
t1.start()

while True:
    verificador, frame = webcam.read()

    if not verificador:
        break

    for faceLoc in locations:
        cv2.rectangle(frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0,255,0), 2)

    cv2.imshow("Rostos na Webcam", frame)

    waitKey = cv2.waitKey(5)
    if waitKey == 27:
        break
    elif waitKey == 32:
        break

webcam.release()
cv2.destroyAllWindows()