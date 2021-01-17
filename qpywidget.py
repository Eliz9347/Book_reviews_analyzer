# This Python file uses the following encoding: utf-8

import sys
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QSizePolicy
from PySide2.QtCharts import QtCharts

import review_parser
import watson
import monkey


class QPyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        # super().__init__()
        loader = QUiLoader()
        ui_file = QFile("form.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.ui.allRadioButton.setChecked(True)
        title_str = self.ui.analyseButton.clicked.connect(self.analyse)

    def add_chart(self, res_dict):
        # Построение графика
        self.chart = QtCharts.QChart()
        self.add_bar_series(res_dict)
        self.chart.setTitle('Emotions in Reviews')
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)

        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        size = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size.setVerticalStretch(200)
        size.setHorizontalStretch(10)
        self.chart_view.setSizePolicy(size)

        self.chart_view.setMinimumHeight(250)
        self.chart_view.setMinimumWidth(30)
        self.ui.Layout.addWidget(self.chart_view)

    def add_bar_series(self, res_dict):
        self.barset = QtCharts.QBarSet('Watson')
        cats = []
        for item in res_dict:
            self.barset.append(res_dict[item])
            cats.append(item)

        self.series = QtCharts.QBarSeries()
        self.series.append(self.barset)
        self.chart.addSeries(self.series)

        # Setting X-axis
        self.axis_x = QtCharts.QBarCategoryAxis()
        cat = ('sadness', 'joy', 'fear', 'disgust', 'anger')
        self.axis_x.append(cat)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        # Setting Y-axis
        self.axis_y = QtCharts.QValueAxis()
        # self.axis_y.setTitleText("Percentage")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

    def analyse(self):
        book_title = self.ui.urlEdit.text()
        self.ui.listWidget.clear()
        # Извлечение информации с сайта
        r_parser = review_parser.ReviewParser(book_title)
        reviews = r_parser.get_reviews(r_parser.book_tree)
        # Удаление предыдущего графика
        if self.ui.Layout.count() == 1:
            self.ui.Layout.removeItem(self.ui.Layout.takeAt(0))
        self.analyser_picker(reviews)

    def analyser_picker(self, reviews):
        if self.ui.watsonRadioButton.isChecked():
            self.ui.listWidget.addItem("IBM Watson")
            # Анализ отзывов с помощью IBM Watson
            watson_analyser = watson.Watson(reviews)
            sentiment = watson_analyser.get_s_res()
            self.ui.listWidget.addItem(sentiment)
            watson_res = watson_analyser.get_res()
            self.add_chart(watson_res)
        elif self.ui.monkeyRadioButton.isChecked():
            self.ui.listWidget.addItem("MonkeyLearn")
            # Анализ отзывов с помощью MonkeyLearn
            review_list = [reviews]
            monkey_analyser = monkey.Monkey(review_list)
            monkey_res = monkey_analyser.get_res()
            self.ui.listWidget.addItem(monkey_res)
        else:
            self.ui.listWidget.addItem("MonkeyLearn")
            # Анализ отзывов с помощью MonkeyLearn и IBM Watson
            review_list = [reviews]
            monkey_analyser = monkey.Monkey(review_list)
            monkey_res = monkey_analyser.get_res()
            self.ui.listWidget.addItem(monkey_res)
            self.ui.listWidget.addItem("IBM Watson")
            watson_analyser = watson.Watson(reviews)
            sentiment = watson_analyser.get_s_res()
            self.ui.listWidget.addItem(sentiment)
            watson_res = watson_analyser.get_res()
            # Отрисовка графика для эмоций отзывов, определённых IBM Watson
            self.add_chart(watson_res)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = QPyWidget()
    window.setWindowTitle('Анализ отзывов о книгах на английском')
    window.show()
    sys.exit(app.exec_())
