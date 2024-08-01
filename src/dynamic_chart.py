from tkinter import *
from tkinter.ttk import *
from tkinter import font
import threading
import time
from data_generator import DataGenerator 


class DynamicDisplayView(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Dynamic Display")

        # config ----------------
        self.width = 600    # width - container
        self.height = 300   # height - container
        self.maxTick = 20   # num of tick in the graph
        self.minValue = 16  # min value for data generator
        self.maxValue = 27  # max value for data generator
        self.xOffsetGraph = 40  # left margin of the graph
        self.yOffsetGraph = 50  # top margin of the graph
        #top right corner - (0,0)
        self.xMaxGraph = 590    # x - coordinate of the graph (right)
        self.yMaxGraph = 280    # y - coordinate of the graph (bottom)
        #------------------------
      
        self.ticks = []
        self.points = []
        self.lines = []
        self.pointLabels = []
        self.bars = []
        self.tickLabels = []
        self.isconnected = False
        
        Canvas(self, width=self.width, height=self.height).pack(padx=20, pady=20)
        container = Frame(self)
        container.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        self.create_ui(container)
        
        style = Style()
        style.theme_use('clam')
        style.configure('.', bd=0, background='white')
        style.configure('CustomButton.TButton', bd=4, background='white')
        style.configure("CustomCombobox.TCombobox", background="lightgray")
        style.configure("TLabel", background="lightgray")
        

        # start the data thread
        self.dataThead = threading.Thread(target=self.updateData)
        self.dataThead.daemon = True
        self.dataThead.start()


    def create_ui(self, parent=None):
        if not parent: parent = self

        # header
        header = Frame(parent, style='TLabel')
        header.pack(fill = "x")
        Label(header, text='========================================', width=21).pack(side=LEFT, anchor=CENTER, expand=True)
        self.btnAction = Button(header, command=self.toggleConnection, text='Go', style="CustomButton.TButton")
        self.btnAction.pack(side=LEFT, padx=5, anchor=CENTER, expand=False)
        Label(header, text='========================================', width=21).pack(side=LEFT, anchor=CENTER, expand=True)

        # graph
        self.canvas = Canvas(parent, background='pink')
        self.canvas.create_text(20, 20, anchor=W, font=font.Font(size=16, weight='normal'), text='Temperature')
        # Draw the X and Y axes
        self.createXAxis()
        self.createYAxis()
        
        self.canvas.pack(fill=BOTH, expand=1)

    def createYAxis(self):
        self.canvas.create_line(self.xOffsetGraph, self.yMaxGraph, self.xMaxGraph, self.yMaxGraph, arrow=LAST) # vertical line
        # assume min is 0, interval is 5 
        numLabel = int(self.maxValue / 5) + 1 if int(self.maxValue % 5) > 0 else int(self.maxValue / 5)
        numLabel = numLabel + 1 # add 1 more for label 0
        hInterval = (self.yMaxGraph - self.yOffsetGraph) / numLabel
        for index in range(0,numLabel):
            # draw horizontal marker, skip label 0
            if(index != 0): 
                self.canvas.create_line(self.xOffsetGraph - 5, self.yMaxGraph - hInterval * index, self.xOffsetGraph, self.yMaxGraph - hInterval * index)  # X axis
            
            # draw maker label
            markerLabel = 5 * index
            if markerLabel >= 10 :
                self.canvas.create_text(self.xOffsetGraph - 25, self.yMaxGraph - hInterval * index, anchor=W, font=font.Font(size=14, weight='normal'), text=markerLabel)
            else: # adjust x position for label 0 & 5
                self.canvas.create_text(self.xOffsetGraph - 18, self.yMaxGraph - hInterval * index, anchor=W, font=font.Font(size=14, weight='normal'), text=markerLabel)


    def createXAxis(self):
        self.canvas.create_line(self.xOffsetGraph, self.yMaxGraph, self.xOffsetGraph,  self.yOffsetGraph, arrow=LAST) # horizontal line
    
    # update line chart & bar chart
    def updateChart(self):
        self.clearAllGraph()
        x_p = 0
        y_p = 0
        # calculate the width of the bar in bar chart, add 1 more tick so that it will not over the x-axis
        widthTick = (self.xMaxGraph - self.xOffsetGraph) / (self.maxTick + 1)
        # calculate unit length in y axis
        numLabel = int(self.maxValue / 5) + 1 if int(self.maxValue % 5) > 0 else int(self.maxValue / 5)
        numLabel = numLabel + 1 # include 0
        hUnit = (self.yMaxGraph - self.yOffsetGraph) / numLabel / 5
        for index, tick in enumerate(self.ticks):
            if index > 0: # save previous tick to draw line
                x_p = xCenter 
                y_p = y
            # calculate x-coordinate and shift a little bit so that it is the mid-point of bar in bar chart
            xCenter = self.xOffsetGraph + (index + 1) * widthTick - widthTick / 2
            # calculate y-coordinate
            y = int(self.yMaxGraph  - (tick.get('value') * hUnit))
            self.pointLabels.append(self.canvas.create_text(xCenter - 10, y - 15, anchor=W, font=font.Font(size=12, weight='normal'), text="{:.1f}".format(tick.get('value')[0])))
            test = 0.5 * len(str(tick.get('index')))
            self.tickLabels.append(self.canvas.create_text(xCenter - test, self.yMaxGraph + 8, anchor=CENTER, fill='green', font=font.Font(size=12, weight='normal'), text=tick.get('index')))
            # Draw bar chart
            self.bars.append(self.canvas.create_rectangle(xCenter - widthTick / 4, y, xCenter + widthTick / 4, self.yMaxGraph, outline='', fill='#1f1'))

            # Draw line chart
            self.points.append(self.canvas.create_oval(xCenter - 1, y - 1, xCenter + 1, y + 1, outline='red', fill='red', width=1))
            if index > 0 : # draw the line if previous data point exist
                self.lines.append(self.canvas.create_line(xCenter, y, x_p, y_p, fill='red', smooth=True))
    
    # clear all point, line, bar in the graph
    def clearAllGraph(self):
        for point in self.points:
            self.canvas.delete(point)
        for line in self.lines:
            self.canvas.delete(line)
        for label in self.pointLabels:
            self.canvas.delete(label)
        for label in self.tickLabels:
            self.canvas.delete(label)
        for bar in self.bars:
            self.canvas.delete(bar)
        self.points = []
        self.lines = []
        self.pointLabels = []
        self.bars = []
        self.tickLabels = []
      
    # start or pause the data generator
    def toggleConnection(self):
        self.isconnected = not self.isconnected
        if self.isconnected :
            self.btnAction.config(text='Pause')
        else:
            self.btnAction.config(text='Go')

    # data thread - generate new data every 0.5s
    def updateData(self):
        count = 1
        while(True):
            if self.isconnected:
                generator = DataGenerator(1)
                newValue = generator.getTemperatureSensorDataset(self.minValue, self.maxValue)
                # Add a new random value to the end of the list
                self.ticks.append({'index': count, 'value': newValue}) 
                # Remove the first item in the list of values if reach max ticks
                self.ticks = self.ticks[-self.maxTick:]
                self.updateChart()
                count = count + 1
            time.sleep(0.5)


app = DynamicDisplayView()
app.mainloop()
