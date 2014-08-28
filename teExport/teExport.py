from Tkinter import Tk
import os.path

class export (object):
    def __init__(self, rr):
        self.color = ['blue', 'green', 'red', 'black']
        self.xlabel = 'x'
        self.ylabel = 'y'
        self.legend = None
        self.exportClipboard = False
        self.exportComplete = False
        self.coorPerRow = 6
        self.saveto = None
        self.exportType = 'pgfplot'
        self.fileName = 'Model'
        
    def saveToFile(self, result):
        """Creates .txt files for plotting result fo simulation with LaTeX. Outputs one file with
        code to be pasted into LaTeX, and one data file for each variable in results after the 
        first. Takes two arguments, results of simulation and name of file to be created. 
        Setting self.exportClipboard to True also copies LaTeX code to clipboard, while 
        setting self.exportComplete to True adds necessary code to build doc right away. 
        
        result = rr.simulate(0, 6, 20, ['Time', 'S1', 'S2'])
        p.export(result, model1)"""
        
        columnNumber = result.shape[1] - 1
        for i in range(columnNumber):  
            if self.saveto is not None:
                completeName = os.path.join(self.saveto, '%s_data%s.txt' % (self.filename, (i + 1)))
            else:
                completeName = '%s_data%s.txt' % (self.filename, (i + 1))
            with open(completeName, 'w') as f:
                r = result[:, [0,(i + 1)]]
                for row in r:
                    row.tolist()
                    row = ' '.join(str(e) for e in row)
                    f.write("%s\n" %row)
                
        if self.saveto is not None:
            completeName = os.path.join(self.saveto, '%s_code.txt' % self.filename)
        else:
            completeName = '%s_code.txt' % self.filename
        f = open(completeName, 'w')
        if self.exportComplete is True:
            f.write('\\documentclass{article}\n')
            f.write('\\usepackage[usenames,dvipsnames]{color}\n')
            f.write('\\usepackage{pgfplots}\n')
            f.write('\\begin{document}\n\n')
        f.write('\\begin{tikzpicture}[scale = 1.0]\n')
        f.write('\\begin{{axis}}[xlabel=${}$, ylabel=${}$, axis lines = middle, xlabel near ticks,'
                ' ylabel near ticks\n'.format(self.xlabel, self.ylabel))
        for i in range(columnNumber):
            f.write('\\addplot[%s, thin] table {%s_data%s.txt};\n' 
                    % (self.color[i], self.filename, (i + 1)))
            
        if self.legend is not None:
            f.write('\\legend{')
            for i in range(columnNumber - 1):
                f.write('%s,' % self.legend[i])
                f.write('%s}\n' % self.legend[i])
                
        f.write('\\end{axis}\n')
        f.write('\\end{tikzpicture}\n\n')
        if self.exportComplete is True: f.write('\\end{document}')
        f.close()
                    
        if self.exportClipboard is True:
            if self.saveto is not None:
                completeName = os.path.join(self.saveto, '%s_code.txt' % self.filename)
            else:
                completeName = '%s_code.txt' % self.filename
            with open(completeName, 'r') as f:
                s = f.read()
                global exportString
                exportString = s
                r = Tk()
                r.withdraw()
                r.clipboard_clear()
                r.clipboard_append('{}'.format(s))
                r.destroy()
        
                
    def saveToOneFile(self, result):
        """Creates one .txt file with LaTeX code and results. Takes two arguments, results of 
        simulation and name of file to be created. Same options as for saveToFile method.
        
        result = rr.simulate(0, 6, 20, ['Time', 'S1', 'S2'])
        p.exportOne(result, model1)"""
        
        columnNumber = result.shape[1] - 1
        if self.saveto is not None:
            completeName = os.path.join(self.saveto, '%s.txt' % self.filename)
        else:
            completeName = '%s.txt' % self.filename
        with open(completeName, 'w') as f:
            if self.exportComplete is True:
                f.write('\\documentclass{article}\n')
                f.write('\\usepackage[usenames,dvipsnames]{color}\n')
                f.write('\\usepackage{pgfplots}\n')
                f.write('\\begin{document}\n\n')
            f.write('\\begin{tikzpicture}[scale = 1.0]\n')
            f.write('\\begin{{axis}}[xlabel=${}$, ylabel=${}$, axis lines = middle, xlabel near'
                    ' ticks, ylabel near ticks\n'.format(self.xlabel, self.ylabel))
            for i in range(columnNumber):
                f.write('\\addplot coordinates {\n')
                r = result[:, [0,(i + 1)]]
                count = 1
                for row in r:
                    row.tolist()
                    coor = ', '.join(str(e) for e in row)
                    coor = '({})'.format(coor)
                    if count % self.coorPerRow == 0:
                        f.write('{}\n'.format(coor))
                    else:
                        f.write('{}'.format(coor))
                    count += 1
                f.write('\n};\n')
            f.write('\\end{axis}\n')
            f.write('\\end{tikzpicture}\n\n')
            if self.exportComplete is True: f.write('\\end{document}')
                
        if self.exportClipboard is True:
            if self.saveto is not None:
                completeName = os.path.join(self.saveto, '%s.txt' % self.filename)
            else:
                completeName = '%s.txt' % self.filename
            with open(completeName, 'r') as f:
                s = f.read()
                global exportString
                exportString = s
                r = Tk()
                r.withdraw()
                r.clipboard_clear()
                r.clipboard_append('{}'.format(s))
                r.destroy() 
    
    def getString(self):
        print exportString
        
        