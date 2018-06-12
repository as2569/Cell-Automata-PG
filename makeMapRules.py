import tkinter as tk
from tkinter.colorchooser import * 

class Data:
    def __init__(self):
        self.cellList = CellList()
                
class CellRow:
    def __init__(self, rowNum, frame):
        self.frame = frame
        self.rowNum = rowNum
        self.cellId = tk.Label(self.frame, text = str(rowNum), font = ('Helvetica', 20)) # do I even need to provide params?
        self.cellName = tk.Label(self.frame, text = 'Empty', font = ('Helvetica', 20))
        self.cellColor = tk.Canvas(self.frame, width=20, height=20, bg="black")
        self.deleteButton = tk.Button(self.frame, text = "Delete", command = self.ClearRow)

    def UpdateRow(self, rowNum, rowData):
        newRowData = rowData
        if newRowData is None:
            newRowData = ['Empty',(0,0,0,0)]
            
        self.cellId['text'] = str(rowNum)
        self.cellId.grid(column = 0, row = rowNum+1)

        self.cellName['text'] = newRowData[0]
        self.cellName.grid(column = 1, row = rowNum+1)

        self.cellColor.grid(column = 2, row = rowNum+1)

        self.deleteButton.grid(column = 3, row = rowNum+1)

    def ClearRow(self):
        data.cellList.row_data[self.rowNum] = None
        data.cellList.UpdateRows()
        print('clear row ' + str(self.rowNum))
        
class CellList:
    def __init__(self):
        self.maxCells = 10
        self.row_data = [None] * self.maxCells
        self.row_gui = []
        self.cellListFrame = tk.Frame(master)
        self.cellListFrame.grid(column=0, row=0)
        self.CreateCellList()
        self.UpdateRows()

    def CreateCellList(self):
        #Cell list label
        self.cellListLabel = tk.Label(self.cellListFrame, text="Cell List", font=('Helvetica', 20)) 
        self.cellListLabel.grid(column=0, row=0, columnspan=4)
        #Cell rows
        for i in range(0, self.maxCells):
            cellRow = CellRow(i, self.cellListFrame)
            self.row_gui.append(cellRow)
        #Add cell label    
        self.newCellLabel = tk.Label(self.cellListFrame, text = "Add cell", font = ('Helvetica', 20))
        self.newCellLabel.grid(column=0, row=self.maxCells+1, columnspan=4)
        #Add cell widgets
        self.newCellName = tk.Entry(self.cellListFrame) #Name entry
        self.newCellName.grid(column=0, row=self.maxCells+2)
        self.newCellColor = tk.Button(self.cellListFrame, bg="black", bitmap="gray12", height=24, width=24, command = self.GetCellColor) #Pick color button   
        self.newCellColor.grid(column=1, row=self.maxCells+2)
        self.newCellButton = tk.Button(self.cellListFrame, text = "Add cell", command = self.AddCell) #Add button
        self.newCellButton.grid(column=2, row=self.maxCells+2)
        
    def GetCellColor(self):
        color = askcolor()
        self.newCellColor['bg'] = color[1]
        print(color)

    def SortRowData(self):
        for i in range(0, self.maxCells):
            if self.row_data[i] is None:
                self.row_data.pop(i)
                self.row_data.append(None)
        print(self.row_data)
                
    def FindEmptyRow(self):
        for i in range(0, self.maxCells):
            if self.row_data[i] is None:
                return i
        return False
            
    def UpdateRows(self):
        self.SortRowData()
        for i in range(0, self.maxCells):
            self.row_gui[i].UpdateRow(i, self.row_data[i])

    def AddCell(self):
        newCellIndex = self.FindEmptyRow()
        print('adding cell at ' + str(newCellIndex))
        if newCellIndex is False:
           print("all full")
           return
        
        newCell = [self.newCellName.get(), (0,0,0,0)]
        self.row_data[newCellIndex] = newCell
        self.UpdateRows()
        print(self.row_data[newCellIndex])
              
root = tk.Tk()
root.geometry('1200x800')

master = tk.Frame(root)
master.grid(column=0, row=0)

data = Data()

root.mainloop()





