from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class WarningDialog(QDialog):
    def __init__(self, title, text):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(350, 260)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("QDialog { border: 4px solid #f65656; border-radius: 5px; background: #ffffff;}")

        error_icon = QPixmap('pictures/error.png')
        if not error_icon.isNull():
            error_label = QLabel(self)
            error_label.setPixmap(error_icon.scaled(60, 60))
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setGeometry(0, 30, 350, 60)

        text_label = QLabel(self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setGeometry(0, 105, 350, 120)
        text_label.setText(text)
        font = QFont("Rubik", 16)
        text_label.setFont(font)
        text_label.setWordWrap(True)

        close_button = QPushButton("Закрыть", self)
        close_button.setStyleSheet(
            "QPushButton { background-color: #f65656; color: #ffffff; border-radius: 5px; font-family: Rubik; font-size: 14pt; } "
            "QPushButton:hover { background-color: #FF7474; }"
        )
        close_button.clicked.connect(self.reject)
        close_button.setGeometry(0, 215, 350, 45)
        close_button.setCursor(Qt.PointingHandCursor)

class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Instructions")
        self.layout = QVBoxLayout(self)
        self.stack = QStackedWidget(self)
        self.setStyleSheet("QDialog {background-color: #FFFFFF;}")

        instructions_pages = [
            {
                "text": "<h1>Список возможностей приложения:</h1><h2>1. Добавление вершин:</h2><p>• Выберите режим 'Конструктор вершин', нажав ЛКМ на кнопку 'Конструктор вершин'.</p><p>• Щелкните ЛКМ/ПКМ по пустой области в пределах рамки для графа, чтобы добавить новую вершину.</p><p>• Если вершину необходимо переместить, переключитесь в режим 'Конструктор вершин' и <br>перетащите вершину в новое место, зажав ЛКМ/ПКМ на нужную вершину.</p>",
                "gif_paths": ["videos/video1.gif", "videos/video1.2.gif"]},
            {
                "text": "<h2>2. Добавление связей:</h2><p>• Выберите режим 'Конструктор связей', нажав ЛКМ на кнопку 'Конструктор связей'.</p><p>• Чтобы создать связь между двумя вершинами, зажмите ЛКМ/ПКМ на одной вершине и проведите связь до другой вершины.</p><p>• При создании связи вам будет предложено ввести вес ребра и тип («Дуга» или «Ребро»).</p>",
                "gif_paths": ["videos/video2.gif"]},
            {
                "text": "<h2>3. Удаление вершин:</h2><p>• Выберите режим 'Удалить вершину', нажав ЛКМ на кнопку 'Удалить вершину'.</p><p>• Щелкните ЛКМ/ПКМ по существующей вершине, чтобы удалить её из графа.</p>",
                "gif_paths": ["videos/video3.gif"]},
            {
                "text": "<h2>4. Очистка поля:</h2><p>• Нажмите ЛКМ на кнопку 'Очистить поле', чтобы удалить все вершины и рёбра из графа.</p>",
                "gif_paths": ["videos/video4.gif"]},
            {
                "text": "<h2>5. Вывод матриц:</h2><p>• Вы можете просмотреть матрицу смежности или матрицу инцидентности, нажав <br>ЛКМ на соответствующую кнопку ('Матрица смежности' или 'Матрица инцидентности').</p><p>• Результат отображается в окне текстового вывода.</p>",
                "gif_paths": ["videos/video5.gif"]},
            {
                "text": "<h2>6. Построение графа по матрице:</h2><p>• Выберите тип матрицы ('Матрица смежности' или 'Матрица инцидентности') с помощью выпадающего списка.</p><p>• Введите матрицу в окно текстового вывода.</p><p>• Нажмите ЛКМ на кнопку 'Построить граф' для создания графа на основе введенной матрицы.</p>",
                "gif_paths": ["videos/video6.gif", "videos/video7.gif"]},
            {
                "text": "<h2>7. Особенности интерфейса:</h2><p>• Рамка для графа находится в пределах области наибольшей синей рамки. <br>Вершины не могут быть созданы или перемещены за пределы этой области.</p><p>• Цвет вершин - синий, цвет рёбер - светло-синий.</p><p>• Рамка и кнопки имеют стилизованный дизайн для улучшения визуального восприятия.</p>",
                "gif_paths": []},
            {
                "text": "<h2>8. Выход из приложения:</h2><p>• Приложение может быть закрыто при нажатии ЛКМ на крестик в верхнем правом углу окна.</p><p>При использовании приложения рекомендуется внимательно следить за сообщениями об ошибках</p><p>и предупреждениями в случае неправильного ввода данных или выполнения операций.</p>",
                "gif_paths": ["videos/video8.gif"]},
        ]

        for page_info in instructions_pages:
            page_widget = QWidget(self)
            page_layout = QVBoxLayout(page_widget)
            text_label = QLabel(page_info["text"], self)
            text_label.setStyleSheet("font-family: Rubik; font-size: 14pt; color: #1e3b70;")
            page_layout.addWidget(text_label)
            gifs_layout = QHBoxLayout()
            for gif_path in page_info["gif_paths"]:
                gif_label = QLabel(self)
                movie = QMovie(gif_path)
                gif_label.setMovie(movie)
                gif_label.setStyleSheet("border: 4px solid #90AFFF; border-radius: 10px; ")
                gif_label.setFixedSize(600, 450)
                movie.start()
                gifs_layout.addWidget(gif_label)
            page_layout.addLayout(gifs_layout)
            self.stack.addWidget(page_widget)

        self.layout.addWidget(self.stack)
        navigation_layout = QHBoxLayout()
        for txt, cmd in [("<", lambda: self.stack.setCurrentIndex(max(0, self.stack.currentIndex() - 1))),
                         (">", lambda: self.stack.setCurrentIndex(
                             min(self.stack.count() - 1, self.stack.currentIndex() + 1)))]:
            btn = QPushButton(txt, self)
            btn.clicked.connect(cmd)
            btn.setStyleSheet(
                "QPushButton { background-color: #90AFFF; color: #ffffff; border-radius: 24px; font-family: Rubik; font-size: 20pt; font-weight: bold; } QPushButton:hover { background-color: #7CA0FF; }")
            btn.setFixedSize(50, 50)
            btn.setCursor(Qt.PointingHandCursor)
            navigation_layout.addWidget(btn)
        self.layout.addLayout(navigation_layout)

        exit_button = QPushButton("Выход", self)
        exit_button.clicked.connect(self.accept)
        exit_button.setStyleSheet(
            "QPushButton { background-color: #FF7474; color: #ffffff; border-radius: 12px; font-family: Rubik; font-size: 18pt; font-weight: bold; } QPushButton:hover { background-color: #FF5C5C; }")
        exit_button.setFixedSize(140, 50)
        self.layout.addWidget(exit_button, alignment=Qt.AlignCenter)
        self.finished.connect(self.deleteLater)
        exit_button.setCursor(Qt.PointingHandCursor)

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        button_style = "QPushButton { background-color: #90AFFF; color: #ffffff; border-radius: 5px; font-size: 11pt; font-weight: bold; } QPushButton:hover { background-color: #7CA0FF; }"
        input_style = "border: 4px #90AFFF; border-radius: 8px; padding: 2px; font-size: 11pt; font-weight: bold; text-align: center; background-color: #90AFFF; color: #ffffff;"
        self.setWindowTitle(" ")
        layout = QFormLayout(self)
        self.setStyleSheet("InputDialog {background-color: #e8f3fc; font-family: Rubik; }")
        label = QLabel("Введите вес:", self)
        label.setStyleSheet("font-size: 11pt; color: #1e3b70;")
        self.input = QLineEdit(self)
        self.input.setStyleSheet(input_style)
        layout.addRow(label, self.input)
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Дуга")
        self.comboBox.addItem("Ребро")
        self.comboBox.setStyleSheet(input_style)
        self.comboBox.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.comboBox)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        ok_button = buttonBox.button(QDialogButtonBox.Ok)
        ok_button.setText("Принять")
        ok_button.setStyleSheet(button_style)
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setFixedSize(100, 24)
        cancel_button = buttonBox.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Отмена")
        cancel_button.setStyleSheet(button_style)
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setFixedSize(100, 24)
        buttonBox.move(150, 200)
        layout.addWidget(buttonBox)

    def getInputs(self):
        result = [self.input.text(), self.comboBox.currentIndex()]
        self.input.setText("")
        return result