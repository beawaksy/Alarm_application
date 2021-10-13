from tkinter import *
import datetime
import time
import os
import cv2
import imutils
import pickle
import pygame
from imutils.video import VideoStream
from imutils.video import FPS
from imutils import paths
import face_recognition
from tkinter import simpledialog




""

 

def klasor_olustur(isim):
    pwd = os.getcwd()
    os.chdir(f"{pwd}/dataset")
    
    os.mkdir(isim)
    
    os.chdir(pwd)


def yuz_tani():
    import face_recognition

    print("[INFO] start processing faces...")
    imagePaths = list(paths.list_images("dataset"))


    knownEncodings = []
    knownNames = []

  
    for (i, imagePath) in enumerate(imagePaths):
        
        print("[INFO] processing image {}/{}".format(i + 1,
            len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

        
       
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        
        
        boxes = face_recognition.face_locations(rgb,
            model="hog")

       
        encodings = face_recognition.face_encodings(rgb, boxes)

       
        for encoding in encodings:
          
            
            knownEncodings.append(encoding)
            knownNames.append(name)

 
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()

 

def yuz_cek(isim):
    klasor_olustur(isim)
    
    
    name = isim 

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("press space to take a photo", 500, 300)

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("press space to take a photo", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
          
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
           
            img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()
    
    
    time.sleep(5)
    yuz_tani()
    

 
def check_event():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            time.sleep(2)
            pygame.mixer.music.play()      
    clock.after(100, check_event)

 

 

def goruntu_isle(isim):

    currentname = "Taninmadi"

    encodingsP = "encodings.pickle"
  
    cascade = "haarcascade_frontalface_default.xml"


    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())
    detector = cv2.CascadeClassifier(cascade)


    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
   
    time.sleep(2.0)

    
    fps = FPS().start()

    
    while True:
        check_event()

        frame = vs.read()
        frame = imutils.resize(frame, width=500)
   
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

 
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for encoding in encodings:
          
        
            matches = face_recognition.compare_faces(data["encodings"],
                encoding)
            name = "Taninmadi" 

         
            if True in matches:
          
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

         
                name = max(counts, key=counts.get)
                
    
                if currentname != name:
                    currentname = name
                    print(currentname)
                    if currentname.lower() == isim.lower():
                        time.sleep(2.5)
                        exit()
        
            names.append(name)

      
        for ((top, right, bottom, left), name) in zip(boxes, names):
        
            cv2.rectangle(frame, (left, top), (right, bottom),
                (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                .8, (0, 255, 255), 2)

     
        cv2.imshow("Facial Recognition is Running", frame)
        key = cv2.waitKey(1) & 0xFF

      
        if key == ord("q"):
            break

      
        fps.update()

    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()
    vs.stop()

 

 

 


def alarm(set_alarm_timer, isim):
    MUSIC_END = pygame.USEREVENT+1
    pygame.mixer.music.set_endevent(MUSIC_END)


    while True:
        current_time = datetime.datetime.now()
        now = current_time.strftime("%H:%M:%S")
        if now == set_alarm_timer:
            pygame.mixer.music.play()
            goruntu_isle(isim)     

      
            
            
            
            
def actual_time(isim):
    set_alarm_timer= f"{hour.get()}:{min.get()}:{sec.get()}"
    alarm(set_alarm_timer, isim) 


clock = Tk()
clock.title("ALARM")
clock.geometry("400x200")

pygame.init()
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)
pygame.mixer.music.load("siren.mp3")

isim = simpledialog.askstring("Input", "Adınız nedir", parent = clock )


if not (isim in os.listdir(f"{os.getcwd()}/dataset")):
    yuz_cek(isim)

check_event()

time_format=Label(clock, text= "Saati 24 saat formatında Girin ", fg="red",bg="black",font="Arial").place(x=60,y=120)

addTime = Label(clock,text = "Saat  Dakika  Saniye",font=10).place(x = 170)
setYourAlarm = Label(clock,text = "Ne zaman uyanmak istiyorsunuz ?",fg="blue",relief = "solid",font=("Helevetica",7,"bold")).place(x=0, y=29)

hour = StringVar()
min = StringVar()
sec = StringVar()


hourTime= Entry(clock,textvariable = hour,bg = "pink",width = 15).place(x=170,y=30)
minTime= Entry(clock,textvariable = min,bg = "pink",width = 15).place(x=210,y=30)
secTime = Entry(clock,textvariable = sec,bg = "pink",width = 15).place(x=250,y=30)


submit = Button(clock,text = "Alarmı Oluştur",fg="red",width = 20,command = lambda : actual_time(isim)).place(x =110,y=70)



clock.mainloop()
