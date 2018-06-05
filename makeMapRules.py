import tkinter as tk

class Data:
    def __init__(self):
        self.cellList = CellList()
        self.cellList.CreateCellList()
                
class CellRow:
    def __init__(self, ID, frame):
        self.frame = frame
        self.cellId = tk.Label(self.frame, text = str(ID), font = ('Helvetica', 20))
        self.cellName = tk.Label(self.frame, text = 'Empty', font = ('Helvetica', 20))
        self.cellColor = tk.Canvas(self.frame, width=20, height=20, bg="black")
        self.deleteButton = tk.Button(self.frame, text = "delete", command = self.ClearRow)

    def UpdateRow(self, rowNum, rowData):
        #cellId = tk.Label(self.frame, text = str(orderNumber), font = ('Helvetica', 20))
        self.cellId['text'] = str(rowNum)
        self.cellId.grid(column = 0, row = rowNum)

        #cellName = tk.Label(self.frame, text = rowData[0], font = ('Helvetica', 20))
        self.cellName['text'] = rowData[0]
        self.cellName.grid(column = 1, row = rowNum)

        #self.cellColor = tk.Canvas(self.frame, width=20, height=20, bg="black")
        self.cellColor.grid(column = 2, row = rowNum)

        self.deleteButton.grid(column = 3, row = rowNum)

    def ClearRow(self):
        print('debug clear row')
        
        
class CellList:
    def __init__(self):
        self.row_data = [['Empty', (0,0,0,0)]] * 11
        self.row_gui = []
        self.cellListFrame = tk.Frame(master)
        self.cellListFrame.grid(column=0, row=0)
        self.CreateRows()

    def CreateRows(self):
        self.cellListLabel = tk.Label(self.cellListFrame, text="Cell List", font=('Helvetica', 20))
        self.cellListLabel.grid(column=0, row=0, columnspan=4)
        for i in range(0, 10):
            print('updating')
            cellRow = CellRow(i, self.cellListFrame)
            self.row_gui.append(cellRow)
            cellRow.UpdateRow(i, self.row_data[i])

    def Delete_cell_data(self, inInt):
        print('test ' + str(inInt))

    def create_cell_add_gui(self):
        addCellLabel = tk.Label(self.cellListFrame, text = "add cell", font = ('Times', 20))
        addCellLabel.grid(column = 0, row = 15)

def add_to_list(self):
    print("adding to list")


root = tk.Tk()
root.geometry('1200x800')

master = tk.Frame(root)
master.grid(column=0, row=0)

data = Data()

#this_cellList = CellList()

#this_cellList.create_cell_list()
#this_cellList.create_cell_add_gui()

root.mainloop()





