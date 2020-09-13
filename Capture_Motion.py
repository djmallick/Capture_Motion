import PIL
import pandas
from tkinter import*
import cv2
import datetime, time
from PIL import Image, ImageTk
from tkinter import filedialog
from bokeh.plotting import figure
from bokeh.io import output_file, show

class Window(object):


    def __init__(self,window):

        self.window = window
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

        window.title("Motion detector")
        window.geometry("1600x700+0+0")

        Tops = Frame(window,bg="white",width = 1600,height=50,relief=SUNKEN)
        Tops.pack(side=TOP)

        self.f1 = Frame(window,width = 900,height=700,relief=SUNKEN)
        self.f1.pack(padx = 100, side=LEFT)

        self.list1= Listbox(self.f1,font=('ariel' ,16,'bold'), height =5, width = 25)
        self.list1.grid(row =1, column = 0, columnspan = 1)

        l1 = Label(self.f1,text = "     ")
        l1.grid(row = 2, column = 0, rowspan = 2)

        self.b1=Button(self.f1,padx=18,pady=5, bd=5 ,fg="black",font=('ariel' ,14,'bold'),width=10, text="Static frame", bg="powder blue",command= self.snap)
        self.b1.grid(row=4, column=0)

        self.b11=Button(self.f1,padx=18,pady=5, bd=5 ,fg="black",font=('ariel' ,14,'bold'),width=10, text="Retake", bg="powder blue",command= self.snap)
        

        l2 = Label(self.f1,text = "     ")
        l2.grid(row = 5, column = 0)

        self.b2=Button(self.f1,padx=10,pady=5, bd=5 ,fg="black",font=('ariel' ,14,'bold'),width=10, text="Start", bg="powder blue", command = self.start)

        l3 = Label(self.f1,text = "     ")
        l3.grid(row = 7, column = 0)

        self.b3=Button(self.f1,padx=14,pady=5, bd=5 ,fg="black",font=('ariel' ,14,'bold'),width=10, text="Stop & Save", bg="powder blue", command = self.stop)
        
        l4 = Label(self.f1, text = "       ")
        l4.grid(row = 9, column = 0)

        l5 = Label(self.f1, text = "                                                         ")
        l5.grid(row = 0, column = 1)

        self.l9 = Label(self.f1)
        self.l9.grid(row = 1, column = 2, rowspan = 10)

        self.b4=Button(self.f1,padx=10,pady=5, bd=5 ,fg="black",font=('ariel' ,14,'bold'),width=10, text="Capture", bg="powder blue", command = self.cap)
    
        l6 = Label(self.f1, text = "       ")
        l6.grid(row = 0, column = 3)

        self.scale = Scale(self.f1, from_=10000, to = 500, orient = HORIZONTAL, label = 'Sensitivity', font=('ariel' ,14,'bold'),bd = 4, bg="powder blue", length = 250, showvalue=0)
        self.scale.set(5000)

        self.b5=Button(self.f1,padx=14,pady=5, bd=5 ,fg="black",font=('ariel' ,14,'bold'),width=10, text="Open", bg="powder blue", command = self.open)
        self.b5.grid(row = 8, column = 0)

        self.flag = 0
        self.flag1 = 0
        self.df = pandas.DataFrame(columns = ["Start", "End"])
        self.time = []
        self.a = [0,0]
    
    def start(self):
        try:
            scl = self.scale.get()
            self.scale.grid(row = 10, column = 0)
            self.b11.grid_forget()
            self.b4.grid_forget()
            self.b2.grid_forget()
            self.b3.grid(row=6, column=0)                      
            status = 0
            self.list1.delete(0,END)
            i=0  
            check, frame = self.video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21,21),0)

            delta_frame = cv2.absdiff(self.first_frame, gray)
            thresh_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame,None,iterations = 2)

            (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in cnts:
                if cv2.contourArea(contour) < scl:
                    continue
                else:
                    self.list1.delete(0,END)
                    self.list1.insert(END,"         Object detected")
                    (x,y,w,h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame,(x,y),(x+w,y+h), (0,255,0),3)
                    i=1
                    status = 1

            self.a.append(i)

            if self.a[-1] ==1 and self.a[-2] ==0:
                self.time.append(datetime.datetime.now().strftime("%H:%M:%S"))    

            
            if self.a[-1] ==0 and self.a[-2] ==1:
                self.time.append(datetime.datetime.now().strftime("%H:%M:%S"))

            if len(self.a) >4:
                del self.a[0]

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            im = PIL.Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=im)
            if self.flag == 0:
                self.l9.imgtk = imgtk
                self.l9.configure(image=imgtk)
                self.l9.after(10,self.start)
            else:
                self.b3.grid_forget()
                self.scale.grid_forget()
                self.scale.set(5000)
                

                self.l9.config(image = '')
                if status ==1:
                    self.time.append(datetime.datetime.now().strftime("%H:%M:%S"))
                for j in range(0, len(self.time), 2):
                    self.df = self.df.append({"Start": self.time[j], "End":self.time[j+1]}, ignore_index=True)
                self.df.to_csv("Time.csv")
                if self.time == []:
                    self.list1.insert(END,"No Motion detected...")  
                    self.flag = 0
                    self.flag = 0
                    self.first_frame = []
                    self.df = pandas.DataFrame(columns = ["Start", "End"])
                    self.b1.grid(row=4, column=0)
                    self.b5.grid(row = 8, column = 0)

                    
                else:
                    self.save()
                    self.time = []
                    self.a = [0,0]
                    self.flag = 0
                    self.flag1 = 0
                    self.first_frame = []
                    self.df = pandas.DataFrame(columns = ["Start", "End"])
                    self.b1.grid(row=4, column=0)
                    self.list1.delete(0,END)
                    self.b5.grid(row = 8, column = 0)

                                    

        except:
            self.list1.delete(0,END)
            self.list1.insert(END," Please Capture static frame")

    def snap(self):
        self.b5.grid_forget()
        self.b11.grid_forget()
        self.b1.grid_forget()
        self.b2.grid_forget()
        self.b4.grid(row=5, column=0)
        check, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21,21),0)
        self.list1.delete(0,END)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        im = PIL.Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        self.l9.imgtk = imgtk
        self.l9.configure(image=imgtk)
        if self.flag1 == 0:
            self.l9.after(10,self.snap)
        else:
            self.first_frame = gray
            self.flag1 = 0         
            self.list1.insert(END,"    Captured Successfully!!")
            self.b2.grid(row=6, column=0)
            self.b11.grid(row=4, column=0)
            self.b4.grid_forget()




    def save(self):
        name=filedialog.asksaveasfile(mode='w',defaultextension=".csv")
        if name != None:
            self.df.to_csv(name)

    def stop(self):
        self.flag = 1

    def cap(self):
        self.flag1 = 1

    def open(self):
        try:
            self.list1.delete(0,END)
            path = filedialog.askopenfile(mode = 'r')
            df = pandas.read_csv(path)
            df['Start'] = pandas.to_datetime(df.Start)
            df['End'] = pandas.to_datetime(df.End)
            y1 = df["Start"]
            y2 = df["End"]
            f = figure(title = "Motion Graph", plot_width = 1000, plot_height = 200, x_axis_type = 'datetime')
            f.xaxis.axis_label="Motion Duration"
            f.yaxis.minor_tick_line_color = None
            f.yaxis[0].ticker.desired_num_ticks = 1
            f.grid.grid_line_alpha = 0
            f.quad(top = 1, bottom =0 , left = y1, right = y2, alpha = 0.3, color = 'blue')
            show(f)
        except:
            self.list1.insert(END,"      Wrong file")



        

window = Tk()

Window(window)

window.mainloop()    

