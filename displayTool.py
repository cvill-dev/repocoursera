from IPython.display import display, Markdown

def printmd(string):
    display(Markdown(string))
    
def printmd(string, color=None):
    colorstr = "<span style='color:{}'>{}</span>".format(color, string)
    display(Markdown(colorstr))
