from tkinter import *
from tkinter.ttk import *
from tkinter import font
from tkinter import messagebox
import threading
import time
from group_2_data_generator import DataGenerator


class DynamicDisplayView(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Dynamic Display")

        self.width = 600
        self.height = 300
        self.maxTick = 20
        self.minValue = 16
        self.maxValue = 27
        self.xOffsetGraph = 40
        self.yOffsetGraph = 50
        self.xMaxGraph = 590
        self.yMaxGraph = 280
        self.isShowLineChart = True
        self.isShowBarChart = False

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
        style.theme_use("clam")
        style.configure(".", bd=0, background="white")
        style.configure("CustomButton.TButton", bd=4, background="white")
        style.configure("CustomCombobox.TCombobox", background="lightgray")
        style.configure("TLabel", background="lightgray")

        self.dataThead = threading.Thread(target=self.updateData)
        self.dataThead.daemon = True
        self.dataThead.start()

    def create_ui(self, parent=None):
        if not parent:
            parent = self

        header = Frame(parent, style="TLabel")
        header.pack(fill="x")
        Label(header, text="===============================", width=21).pack(side=LEFT)
        self.btnAction = Button(
            header,
            command=self.toggleConnection,
            text="Go",
            style="CustomButton.TButton",
        )
        self.btnAction.pack(side=LEFT, padx=5)
        self.btnSwitch = Button(
            header,
            command=self.toggleChart,
            text="Switch",
            style="CustomButton.TButton",
        )
        self.btnSwitch.pack(side=LEFT, padx=5)
        Label(header, text="===============================", width=21).pack(side=LEFT)

        self.canvas = Canvas(parent, background="pink")
        self.canvas.create_text(
            20,
            20,
            anchor=W,
            font=font.Font(size=16, weight="normal"),
            text="Temperature",
        )

        self.createXAxis()
        self.createYAxis()

        self.canvas.pack(fill=BOTH, expand=1)

    def createYAxis(self):
        self.canvas.create_line(
            self.xOffsetGraph,
            self.yMaxGraph,
            self.xMaxGraph,
            self.yMaxGraph,
            arrow=LAST,
        )

        numLabel = (
            int(self.maxValue / 5) + 1
            if int(self.maxValue % 5) > 0
            else int(self.maxValue / 5)
        )
        numLabel = numLabel + 1
        hInterval = (self.yMaxGraph - self.yOffsetGraph) / numLabel
        for index in range(0, numLabel):

            if index != 0:
                self.canvas.create_line(
                    self.xOffsetGraph - 5,
                    self.yMaxGraph - hInterval * index,
                    self.xOffsetGraph,
                    self.yMaxGraph - hInterval * index,
                )

            markerLabel = 5 * index
            if markerLabel >= 10:
                self.canvas.create_text(
                    self.xOffsetGraph - 25,
                    self.yMaxGraph - hInterval * index,
                    anchor=W,
                    font=font.Font(size=14, weight="normal"),
                    text=markerLabel,
                )
            else:
                self.canvas.create_text(
                    self.xOffsetGraph - 18,
                    self.yMaxGraph - hInterval * index,
                    anchor=W,
                    font=font.Font(size=14, weight="normal"),
                    text=markerLabel,
                )

    def createXAxis(self):
        self.canvas.create_line(
            self.xOffsetGraph,
            self.yMaxGraph,
            self.xOffsetGraph,
            self.yOffsetGraph,
            arrow=LAST,
        )

    def updateChart(self):
        self.clearAllGraph()
        x_p = 0
        y_p = 0

        widthTick = (self.xMaxGraph - self.xOffsetGraph) / (self.maxTick + 1)

        numLabel = (
            int(self.maxValue / 5) + 1
            if int(self.maxValue % 5) > 0
            else int(self.maxValue / 5)
        )
        numLabel = numLabel + 1
        hUnit = (self.yMaxGraph - self.yOffsetGraph) / numLabel / 5
        for index, tick in enumerate(self.ticks):
            if index > 0:
                x_p = xCenter
                y_p = y

            xCenter = self.xOffsetGraph + (index + 1) * widthTick - widthTick / 2

            y = int(self.yMaxGraph - (tick.get("value") * hUnit))
            self.pointLabels.append(
                self.canvas.create_text(
                    xCenter - 10,
                    y - 15,
                    anchor=W,
                    font=font.Font(size=12, weight="normal"),
                    text="{:.1f}".format(tick.get("value")[0]),
                )
            )
            test = 0.5 * len(str(tick.get("index")))
            self.tickLabels.append(
                self.canvas.create_text(
                    xCenter - test,
                    self.yMaxGraph + 8,
                    anchor=CENTER,
                    fill="green",
                    font=font.Font(size=12, weight="normal"),
                    text=tick.get("index"),
                )
            )
            if self.isShowBarChart:
                self.bars.append(
                    self.canvas.create_rectangle(
                        xCenter - widthTick / 4,
                        y,
                        xCenter + widthTick / 4,
                        self.yMaxGraph,
                        outline="",
                        fill="#1f1",
                    )
                )

            if self.isShowLineChart:
                if not self.isShowBarChart:
                    self.points.append(
                        self.canvas.create_oval(
                            xCenter - 1,
                            y - 1,
                            xCenter + 1,
                            y + 1,
                            outline="red",
                            fill="red",
                            width=1,
                        )
                    )
                if index > 0:
                    self.lines.append(
                        self.canvas.create_line(
                            xCenter, y, x_p, y_p, fill="red", smooth=True
                        )
                    )

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

    def toggleChart(self):
        self.isShowBarChart = not self.isShowBarChart
        self.updateChart()

    def toggleConnection(self):
        self.isconnected = not self.isconnected
        if self.isconnected:
            self.btnAction.config(text="Pause")
        else:
            self.btnAction.config(text="Go")

    def updateData(self):
        count = 1
        while True:
            if self.isconnected:
                generator = DataGenerator(1)
                newValue = generator.getTemperatureSensorDataset(
                    self.minValue, self.maxValue
                )

                self.ticks.append({"index": count, "value": newValue})

                self.ticks = self.ticks[-self.maxTick :]
                self.updateChart()
                count = count + 1
            time.sleep(0.5)


app = DynamicDisplayView()
app.mainloop()
