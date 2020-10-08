from PyQt5.QtWidgets import *
import json
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


class ScrollLabel(QScrollArea):

    # contructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

        # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        with open('recipe.json') as f:
            d = json.load(f)

        self.data = d["Recipe"]

        self.ingredients = []
        self.seasoning = ["Salt", "Pepper", "Siracha", "Maggi", "Chicken powder", "Red pepper paste", "Fish sauce",
                          "Sugar", "Brown sugar", "Lemon extract", "Soy sauce", "Red pepper flake"]

        for r in self.data:
            for d in self.data[r]:
                for key, val in d.items():
                    if key == "Ingredients":
                        for v in val:
                            if v[0].isnumeric():
                                v = v.split(" ", 1)[1]
                            if v not in self.ingredients and v not in self.seasoning:
                                self.ingredients.append(v)

        self.ingredients = sorted(self.ingredients)

        # setting title
        self.setWindowTitle("Recipe ")

        # setting geometry
        self.setGeometry(100, 100, 900, 400)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    def UiComponents(self):

        self.list_widget_recipe = QListWidget(self)

        self.list_widget_recipe.setGeometry(50, 70, 150, 300)

        for d in self.data:
            self.list_widget_recipe.addItem(QListWidgetItem(d))

        self.list_widget_ingredients = QListWidget(self)
        self.list_widget_ingredients.setGeometry(700, 70, 150, 300)

        for ing in self.ingredients:
            item = QListWidgetItem(ing)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.list_widget_ingredients.addItem(item)

        button_recipe = QPushButton("Recipe ", self)
        button_recipe.pressed.connect(self.find_recipe)
        button_recipe.move(50, 30)

        self.label = ScrollLabel(self)

        # setting geometry of the label
        self.label.setGeometry(250, 70, 400, 300)

        button_add = QPushButton("Add ", self)
        button_add.pressed.connect(self.add_recipe)
        button_add.move(150, 30)

        button_filter = QPushButton("Filter ", self)
        button_filter.pressed.connect(self.filter)
        button_filter.move(250, 30)

    def find_recipe(self):

        # finding the content of current item in combo box
        if not self.list_widget_recipe.currentItem():
            self.label.setText("")
            return
        
        content = self.list_widget_recipe.currentItem().text()

        s = ""
        for d in self.data[content]:
            for key, val in d.items():
                s += key + "\n"
                for v in val:
                    s += "\t" + v + "\n"

        # showing content on the screen though label
        self.label.setText(s)

    def add_recipe(self):
        name, done1 = QInputDialog.getText(
            self, 'Input Dialog', 'Recipe name:')

        ingredients, done2 = QInputDialog.getText(
            self, 'Input Dialog', 'Ingredients:')

        recipe, done3 = QInputDialog.getText(
            self, 'Input Dialog', 'Recipe:')

        if done1 and done2 and done3:
            self.data[name] = [{"Ingredients": [x for x in ingredients.split(",")]},
                               {"Recipe": [x for x in recipe.split(",")]}]
            for x in ingredients.split(","):
                if x not in self.ingredients and x not in self.seasoning:
                    self.ingredients.append(x)
                    item = QListWidgetItem(x)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    self.list_widget_ingredients.addItem(item)

            with open("recipe.json",'w') as f:
                json.dump({"Recipe": self.data}, f)
            self.list_widget_recipe.addItem(QListWidgetItem(name))

    def filter(self):
        cur_ing = []
        for index in range(self.list_widget_ingredients.count()):
            cur = self.list_widget_ingredients.item(index)
            if cur.checkState():
                cur_ing.append(cur.text())
        self.list_widget_recipe.clear()
        for r in self.data:
            for d in self.data[r]:
                for key, val in d.items():
                    if key == "Ingredients":
                        for ing in cur_ing:
                            if ing in d["Ingredients"]:
                                self.list_widget_recipe.addItem(QListWidgetItem(r))
                                break
        if not cur_ing:
            for d in self.data:
                self.list_widget_recipe.addItem(QListWidgetItem(d))

App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())