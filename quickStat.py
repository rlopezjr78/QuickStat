"""
A app for retreiving statistics from a csv file.
"""
# create a virtual environment in your current directory
# python -m virtualenv kivy_venv

# activate virtual environment
# kivy_venv\Scripts\activate

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import filechooser
import pandas as pd
from pandas.api.types import is_numeric_dtype
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.properties import ObjectProperty


# Set the app size
Window.size = (400, 260)

# Global variables
FILEPATH = ''
DF = pd.DataFrame()


# Main screen/window.
class Startup(Screen):
    """Startup screen with buttons for csv file selection"""
    # Get the csv file
    def file_chooser(self):
        """Lets a user select a csv file"""
        global FILEPATH
        FILEPATH = filechooser.open_file(
            title="Pick a CSV file..",
            filters=[("Comma-separated Values", "*.csv")])
        # print(FILEPATH)


# Data Analysis screen/window
class Display(Screen):
    """Screen for displaying statistics from given csv file."""
    
    def switchScreens(self, value):
        if self.manager.current == 'display':
            self.manager.current = 'startup'


    def build_columns_as_tabs(self):
        """Create, populate & add tabbed_panel"""
        global FILEPATH
        global DF
        DF = pd.read_csv(FILEPATH[0])
        grid = GridLayout(cols=2)
        tp = TabbedPanel()
        tp.do_default_tab = False

        for col_name in DF:
            col = DF[col_name]
            is_num = is_numeric_dtype(col)
            if is_num:
                th = TabbedPanelHeader(text=col_name)
                grid.add_widget(Label(text="Number of entries: " + str(col.count())))
                grid.add_widget(Label(text="Mean: " + str(col.mean())))
                grid.add_widget(Label(text="Median: " + str(col.median())))
                grid.add_widget(Label(text="Max: " + str(col.max())))
                grid.add_widget(Label(text="Min: " + str(col.min())))
                th.content = grid
                tp.add_widget(th)
                grid = GridLayout(cols=2)

        grid = GridLayout(cols=1)
        back_btn = Button(text="Select Another Data Set")
        back_btn.bind(on_press=self.switchScreens)
        grid.add_widget(tp)
        grid.add_widget(back_btn)
        self.add_widget(grid)

class Manager(ScreenManager):
    display = ObjectProperty(None)
    startup = ObjectProperty(None)


class QuickStat(App):
    """Main application"""
    # Window Title
    title = 'QuickStat'

    def build(self):
        """Builds the app"""
        m = Manager()
        return m


if __name__ == '__main__':
    QuickStat().run()
