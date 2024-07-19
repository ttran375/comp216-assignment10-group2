# Lab 10 -- Display a Dynamic Line Chart

You will display a line chart of a dynamic dataset. It is advised that you start with lab 11 and add the capability to update the display. You will add the capability of dynamically displaying a changing dataset. We will build a GUI to display a set of values. You will display the values using both a line chart and a bar chart on the same app. You will implement the following:

1. Create an additional method that will be executed in a thread. This method will do the following in an infinite loop:
    - Remove the first item in the list of values
    - Add a new random value to the end of the list
    - Call the method to display the list on the canvas
    - Sleep for a short while (0.5 of a second).

2. In the initUI() method do the following at the end:
    - You may remove the Entry widget. This is not used in this application.
    - Create a thread and set the target to the method in step 1
    - Set the daemon property of the above thread to True. This will terminate the thread when the GUI closes.
    - Start the thread.

3. Modify the method that draws the rectangle and line to just draw lines.

### Submission

1. Your code file will be named `group_«your_group_number»_dynamic_chart.py` (e.g., `group_1_dynamic_chart.py`).
2. Must be uploaded to course dropbox.

![](media/image1.png)

### Rubrics

| **Class**           | 4/4 |
|---------------------|-----|
| **unitUI Method**   | 3/3 |
| **Thread Method**   | 8/8 |
| **Update GUI**      | 10/10 |
| **GUI**             | 2/2 |
| **Aesthetics**      | 3/3 |
| **Total**           | **30/30** |