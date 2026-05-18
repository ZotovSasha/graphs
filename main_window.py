import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dialogs import WarningDialog, InstructionsDialog, InputDialog
from delegate import Delegate
from graph import Graph
from matrix import (
    MatrixParseError,
    adjacency_matrix,
    edge_headers,
    edges_from_adjacency_matrix,
    edges_from_incidence_matrix,
    format_matrix,
    incidence_matrix,
    parse_adjacency_matrix as parse_adjacency_text,
    parse_incidence_matrix as parse_incidence_text,
)
from models import EdgeType, Vertex


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drawing_board_size = QRectF(15, 85, 750, 700)
        self.graph = Graph()
        self.parse_matrix_mode = "adj"
        self.add_mode = "edge"
        self.vertex_radius = 18
        self.start_vertex = -1
        self.dragged_vertex_index = -1
        self.cursor_pos = [0, 0]
        self.delete = False
        self.setupUi()
        self.setupButtonsConnections()
        self.toggle_add_vertex()
        self.setMinimumSize(960, 720)
        self.resize(1250, 900)
        self.show()

    @property
    def vertices(self):
        return self.graph.vertices

    @property
    def edges(self):
        return self.graph.edges

    def setupUi(self):
        self.dialog = InputDialog(self)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Graph Drawer")
        self.centralwidget = QWidget(self)
        self.setStyleSheet("QMainWindow {background-color: #e8f3fc;}")

        self.DisplayAdjMatrixButton = QPushButton(self.centralwidget, text="Матрица\nсмежности")
        self.set_button_style(self.DisplayAdjMatrixButton, "#90AFFF", "#7CA0FF", "#a0bbff")
        self.DisplayIncMatrixButton = QPushButton(self.centralwidget, text="Матрица\nинцидентности")
        self.set_button_style(self.DisplayIncMatrixButton, "#90AFFF", "#7CA0FF", "#a0bbff")
        self.EdgeModeButton = QPushButton(self.centralwidget, text="Конструктор\nсвязей")
        self.VertexModeButton = QPushButton(self.centralwidget, text="Конструктор\nвершин")
        self.DeleteButton = QPushButton(self.centralwidget, text="Удалить\nвершину")
        self.set_button_style(self.DeleteButton, "#ff9d9d", "#ff7474", "#ff7474")
        self.ClearButton = QPushButton(self.centralwidget, text="Очистить поле")
        self.set_button_style(self.ClearButton, "#FF7474", "#FF5C5C", "#FF7474")

        self.TextOutput = QTextEdit(self.centralwidget)
        font = QFont("Rubik", 14)
        self.TextOutput.setFont(font)
        self.TextOutput.setStyleSheet(
            "border: 4px solid #90AFFF; border-radius: 10px; padding: 10px; background-color: #ffffff;")
        self.TextOutput.setWordWrapMode(QTextOption.NoWrap)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        table_style = """QTableView { background-color: #e8f3fc; border: 4px solid #90AFFF; border-radius: 10px; padding: 10px; gridline-color: #90AFFF; selection-background-color: #c0dcf4; }"""
        self.tableWidget.setStyleSheet(table_style)
        self.tableWidget.setItemDelegate(Delegate(self.tableWidget))
        self.tableWidget.setShowGrid(0)

        self.trashButton = QPushButton(QIcon('pictures/trashbin_button.png'), '', self.centralwidget)
        self.trashButton.setIconSize(QSize(30, 30))
        self.set_button_style(self.trashButton, "#90AFFF", "#7CA0FF", "#a0bbff")

        self.guideButton = QPushButton(QIcon('pictures/info_button.png'), '', self.centralwidget)
        self.guideButton.setIconSize(QSize(25, 25))
        self.guideButton.setCursor(Qt.PointingHandCursor)
        self.guideButton.setStyleSheet(
            "QPushButton { border-radius: 22px; padding: 10px; font-family: 'Rubik'; font-size: 28pt; background-color: #90AFFF; color: #ffffff; } QPushButton:hover { background-color: #81a4ff } QPushButton:pressed { background-color: #a0bbff }")

        self.InputMatrixSelectorCombo = QComboBox(self.centralwidget)
        self.InputMatrixSelectorCombo.addItems(["   Матрица\n   смежности", "   Матрица\n   инцидентности"])
        self.InputMatrixSelectorCombo.setCursor(Qt.PointingHandCursor)
        self.InputMatrixSelectorCombo.setStyleSheet(
            "border: 4px #90AFFF; border-radius: 8px; padding: 2px; font-family: 'Rubik'; font-size: 14pt; font-weight: bold; text-align: center; background-color: #90AFFF; color: #ffffff;")

        self.BuildGraphButton = QPushButton(self.centralwidget, text="Построить граф")
        self.set_button_style(self.BuildGraphButton, "#90AFFF", "#7CA0FF", "#a0bbff")
        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)

    def setupGeometry(self, width, height):
        window_border = 20
        columns_padding = 30
        width -= window_border * 2 + columns_padding
        height -= window_border * 2
        left_column_width = int(width / 7 * 4)
        left_column_lines_padding = 20
        top_buttons_padding = 20
        top_butons_width = int((left_column_width - top_buttons_padding * 3) / 4)
        top_buttons_height = 55
        bottom_buttons_padding = 40
        bottom_buttons_width = min(180, int((left_column_width - bottom_buttons_padding) / 2))
        bottom_buttons_height = 64
        right_column_lines_padding = 35
        right_column_width = width - left_column_width
        text_output_height = int(height / 3)
        table_widget_height = int(height / 4)
        trash_button_size = 45
        right_buttons_padding = 15
        right_buttons_width = int((right_column_width - trash_button_size - right_buttons_padding * 2) / 2)

        self.drawing_board_size = QRectF(window_border, window_border + top_buttons_height + left_column_lines_padding,
                                         left_column_width,
                                         height - top_buttons_height - bottom_buttons_height - left_column_lines_padding * 2)
        self.DisplayAdjMatrixButton.setGeometry(
            QRect(window_border + int(left_column_width / 2) - int(bottom_buttons_padding / 2) - bottom_buttons_width,
                  window_border + height - bottom_buttons_height, bottom_buttons_width, bottom_buttons_height))
        self.DisplayIncMatrixButton.setGeometry(
            QRect(window_border + int(left_column_width / 2) + int(bottom_buttons_padding / 2),
                  window_border + height - bottom_buttons_height, bottom_buttons_width, bottom_buttons_height))
        self.EdgeModeButton.setGeometry(QRect(window_border, window_border, top_butons_width, top_buttons_height))
        self.VertexModeButton.setGeometry(
            QRect(window_border + (top_butons_width + top_buttons_padding), window_border, top_butons_width,
                  top_buttons_height))
        self.DeleteButton.setGeometry(
            QRect(window_border + (top_butons_width + top_buttons_padding) * 2, window_border, top_butons_width,
                  top_buttons_height))
        self.ClearButton.setGeometry(
            QRect(window_border + (top_butons_width + top_buttons_padding) * 3, window_border, top_butons_width,
                  top_buttons_height))
        self.TextOutput.setGeometry(
            QRect(window_border + left_column_width + columns_padding, window_border, right_column_width,
                  text_output_height))
        self.tableWidget.setGeometry(QRect(window_border + left_column_width + columns_padding,
                                           window_border + text_output_height + right_column_lines_padding * 2 + trash_button_size,
                                           right_column_width, table_widget_height))
        self.InputMatrixSelectorCombo.setGeometry(QRect(window_border + left_column_width + columns_padding,
                                                        window_border + text_output_height + right_column_lines_padding,
                                                        right_buttons_width, trash_button_size))
        self.BuildGraphButton.setGeometry(
            QRect(window_border + left_column_width + columns_padding + right_buttons_padding + right_buttons_width,
                  window_border + text_output_height + right_column_lines_padding, right_buttons_width,
                  trash_button_size))
        self.trashButton.setGeometry(QRect(
            window_border + left_column_width + columns_padding + right_buttons_padding * 2 + right_buttons_width * 2,
            window_border + text_output_height + right_column_lines_padding, trash_button_size, trash_button_size))
        self.guideButton.setGeometry(QRect(window_border + width + columns_padding - trash_button_size,
                                           window_border + height - trash_button_size, trash_button_size,
                                           trash_button_size))

    def clipVertices(self):
        for vertex in self.vertices:
            vertex.x = min(max(self.drawing_board_size.x() + self.vertex_radius, vertex.x),
                           self.drawing_board_size.x() + self.drawing_board_size.width() - self.vertex_radius)
            vertex.y = min(max(self.drawing_board_size.y() + self.vertex_radius, vertex.y),
                           self.drawing_board_size.y() + self.drawing_board_size.height() - self.vertex_radius)

    def warningPopup(self, title, _text):
        WarningDialog(title, _text).exec_()

    def set_button_style(self, button, default_color, hover_color, pressed_color):
        button.setStyleSheet(
            f"QPushButton {{ background-color: {default_color}; color: #ffffff; border-radius: 12px; font-family: 'Rubik'; font-size: 14pt; font-weight: bold; }} QPushButton:hover {{ background-color: {hover_color}; }} QPushButton:pressed {{ background-color: {pressed_color}; }}")
        button.setCursor(Qt.PointingHandCursor)

    def setupButtonsConnections(self):
        self.DisplayAdjMatrixButton.clicked.connect(self.display_adjacency_matrix)
        self.DisplayIncMatrixButton.clicked.connect(self.display_incidence_matrix)
        self.EdgeModeButton.clicked.connect(self.toggle_add_edge)
        self.VertexModeButton.clicked.connect(self.toggle_add_vertex)
        self.DeleteButton.clicked.connect(self.toggle_delete_mode)
        self.ClearButton.clicked.connect(self.clear_graph)
        self.InputMatrixSelectorCombo.currentIndexChanged.connect(self.index_changed)
        self.BuildGraphButton.clicked.connect(self.build_graph)
        self.trashButton.clicked.connect(self.trash_matrix)
        self.guideButton.clicked.connect(lambda: InstructionsDialog(self).exec_())

    def show_instructions(self):
        InstructionsDialog(self).exec_()

    def trash_matrix(self):
        self.TextOutput.clear()
        self.clear_matrix_table()

    def clear_matrix_table(self):
        self.tableWidget.setUpdatesEnabled(False)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setUpdatesEnabled(True)

    def toggle_delete_mode(self):
        self.delete = True
        self.set_button_style(self.DeleteButton, "#FF8383", "#FF5C5C", "#FF5C5C")
        self.set_button_style(self.VertexModeButton, "#90AFFF", "#7CA0FF", "#7CA0FF")
        self.set_button_style(self.EdgeModeButton, "#90AFFF", "#7CA0FF", "#7CA0FF")

    def toggle_add_vertex(self):
        self.delete = False
        self.set_button_style(self.EdgeModeButton, "#90AFFF", "#7CA0FF", "#7CA0FF")
        self.set_button_style(self.DeleteButton, "#90AFFF", "#FF7474", "#FF7474")
        self.set_button_style(self.VertexModeButton, "#7DD6DB", "#4BCFD6", "#4BCFD6")
        self.add_mode = "vertex"

    def toggle_add_edge(self):
        self.delete = False
        self.set_button_style(self.VertexModeButton, "#90AFFF", "#7CA0FF", "#7CA0FF")
        self.set_button_style(self.DeleteButton, "#90AFFF", "#FF7474", "#FF7474")
        self.set_button_style(self.EdgeModeButton, "#7DD6DB", "#4BCFD6", "#4BCFD6")
        self.add_mode = "edge"

    def index_changed(self, index):
        self.parse_matrix_mode = "adj" if index == 0 else "inc"

    def vertex_at(self, x, y):
        for index, vertex in enumerate(self.vertices):
            if abs(vertex.x - x) < self.vertex_radius and abs(vertex.y - y) < self.vertex_radius:
                return index
        return -1

    def mousePressEvent(self, event):
        db = self.drawing_board_size
        r = self.vertex_radius
        if db.x() + r < event.x() < db.x() + db.width() - r and db.y() + r < event.y() < db.y() + db.height() - r:
            vertex_index = self.vertex_at(event.x(), event.y())
            if self.delete:
                if vertex_index != -1:
                    self.graph.delete_vertex(vertex_index)
                    self.update()
                    return
            elif self.add_mode == "vertex":
                if vertex_index != -1:
                    self.dragged_vertex_index = vertex_index
                    return
                self.graph.add_vertex(event.x(), event.y())
                self.update()
            elif self.add_mode == "edge":
                if vertex_index != -1:
                    self.start_vertex = vertex_index
                    return

    def mouseMoveEvent(self, event):
        db = self.drawing_board_size
        r = self.vertex_radius
        if db.x() + r < event.x() < db.x() + db.width() - r and db.y() + r < event.y() < db.y() + db.height() - r:
            if self.dragged_vertex_index != -1:
                self.graph.move_vertex(self.dragged_vertex_index, event.x(), event.y())
            if self.start_vertex != -1:
                self.cursor_pos = [event.x(), event.y()]
            self.update()
        else:
            self.dragged_vertex_index = -1
            self.start_vertex = -1

    def ask_for_weight(self):
        weight = -1
        while int(weight) < 0:
            if self.dialog.exec():
                weight, edge_type = self.dialog.getInputs()
                try:
                    if weight.strip() == "":
                        return [1, EdgeType.from_value(edge_type)]
                    weight = int(weight)
                    if weight < 0:
                        self.warningPopup(" ",
                                          "<h3>&nbsp;Предупреждение!</h3>\n&nbsp;&nbsp;Вес должен быть положительным.<br><br>")
                        continue
                    return [weight, EdgeType.from_value(edge_type)]
                except ValueError:
                    weight = -1
                    self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Вес должен быть целым числом.<br><br>")
            else:
                return [None, EdgeType.UNDIRECTED]

    def mouseReleaseEvent(self, event):
        if self.start_vertex != -1:
            end_vertex = self.vertex_at(event.x(), event.y())
            if end_vertex != -1:
                result = self.ask_for_weight()
                if result and result[0] is not None:
                    self.add_edge(self.start_vertex, end_vertex, result[0], result[1])
        self.dragged_vertex_index = -1
        self.start_vertex = -1
        self.update()

    def resizeEvent(self, event):
        self.setupGeometry(event.size().width(), event.size().height())
        self.clipVertices()

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            self.draw_frame(painter)
            if self.start_vertex != -1 and len(self.vertices) > self.start_vertex:
                start_vertex = self.vertices[self.start_vertex]
                self.draw_edge(
                    painter,
                    start_vertex.x,
                    start_vertex.y,
                    self.cursor_pos[0],
                    self.cursor_pos[1],
                )
            self.draw_edges(painter)
            self.draw_vertices(painter)
        except Exception as e:
            print(f"Paint error suppressed: {e}")
        finally:
            painter.end()

    def draw_vertices(self, painter):
        for i, vertex in enumerate(self.vertices):
            self.draw_vertex(painter, vertex.x, vertex.y, str(i + 1))

    def draw_vertex(self, painter, x, y, index):
        painter.save()
        painter.setPen(QPen(QColor("#81a4ff"), 2))
        painter.setBrush(QColor("#81a4ff"))
        painter.drawEllipse(
            QRectF(x - self.vertex_radius, y - self.vertex_radius, self.vertex_radius * 2, self.vertex_radius * 2))
        painter.setPen(QColor(Qt.white))
        painter.setFont(QFont("Rubik", 14))
        painter.drawText(
            QRectF(x - self.vertex_radius, y - self.vertex_radius, self.vertex_radius * 2, self.vertex_radius * 2),
            Qt.AlignCenter, str(index))
        painter.restore()

    def draw_edges(self, painter):
        for edge in self.graph.valid_edges():
            start_vertex = self.vertices[edge.start_index]
            end_vertex = self.vertices[edge.end_index]
            self.draw_edge(
                painter,
                start_vertex.x,
                start_vertex.y,
                end_vertex.x,
                end_vertex.y,
                edge.weight,
                edge.edge_type,
            )

    def draw_edge(self, painter, x1, y1, x2, y2, weight=-1, edge_type=EdgeType.UNDIRECTED):
        edge_type = EdgeType.from_value(edge_type)
        painter.save()
        painter.setPen(QPen(QColor("#5A88FF"), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        text_x, text_y = x2, y2

        if x1 == x2 and y1 == y2:
            painter.drawArc(
                QRect(int(x1) - self.vertex_radius * 2, int(y1) - self.vertex_radius * 2, self.vertex_radius * 2,
                      self.vertex_radius * 2), 0, 270 * 16)
            text_x = int(x1) - self.vertex_radius * 2
            text_y = int(y1) - self.vertex_radius * 2
        else:
            if edge_type == EdgeType.DIRECTED:
                angle1 = math.atan2(y2 - y1, x2 - x1)
                x2 = x2 - self.vertex_radius * math.cos(angle1)
                y2 = y2 - self.vertex_radius * math.sin(angle1)
                length = int(math.hypot(x1 - x2, y1 - y2))
                points = [QPoint(int(length / 3), 30), QPoint(int(length * 2 / 3), 30), QPoint(length, 0)]
                for i in range(3):
                    x = x1 + points[i].x() * math.cos(angle1) - points[i].y() * math.sin(angle1)
                    y = y1 + points[i].x() * math.sin(angle1) + points[i].y() * math.cos(angle1)
                    points[i] = QPoint(int(x), int(y))
                path = QPainterPath(QPoint(int(x1 + self.vertex_radius * math.cos(angle1)),
                                           int(y1 + self.vertex_radius * math.sin(angle1))))
                path.cubicTo(points[0], points[1], points[2])
                painter.drawPath(path)
                angle2 = math.atan2(y2 - points[1].y(), x2 - points[1].x())
                arrow_len, arrow_open_angle = 15, math.pi / 10
                painter.setBrush(QColor("#5A88FF"))
                painter.drawConvexPolygon([
                    QPointF(x2, y2),
                    QPointF(x2 - arrow_len * math.cos(angle2 + arrow_open_angle),
                            y2 - arrow_len * math.sin(angle2 + arrow_open_angle)),
                    QPointF(x2 - arrow_len * math.cos(angle2 - arrow_open_angle),
                            y2 - arrow_len * math.sin(angle2 - arrow_open_angle))
                ])
                text_x, text_y = points[1].x(), points[1].y()
            if edge_type == EdgeType.UNDIRECTED:
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
                text_x = int(x2) - (x2 - x1) // 4
                text_y = int(y2) - (y2 - y1) // 4

        if weight != -1 and str(weight) != "1":
            font = QFont("Rubik", 12)
            fm = QFontMetrics(font)
            w = max(30, int(fm.horizontalAdvance(str(weight)) if hasattr(fm, 'horizontalAdvance') else fm.width(
                str(weight))))
            h = int(fm.height())
            painter.setBrush(Qt.white)
            painter.setFont(font)
            rx, ry = int(text_x - w / 2 - 2), int(text_y - h / 2 - 2)
            painter.drawRect(rx, ry, w + 4, h + 4)
            painter.setPen(Qt.black)
            painter.drawText(QRectF(rx + 2, ry + 2, w, h), Qt.AlignCenter, str(weight))
        painter.restore()

    def draw_frame(self, painter):
        painter.save()
        painter.setPen(QPen(QColor("#90AFFF"), 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QColor("#ffffff"))
        painter.drawRoundedRect(self.drawing_board_size, 10, 10)
        painter.restore()

    def build_graph(self):
        try:
            if self.parse_matrix_mode == "adj":
                matrix = parse_adjacency_text(self.TextOutput.toPlainText())
                edges = edges_from_adjacency_matrix(matrix)
            else:
                matrix = parse_incidence_text(self.TextOutput.toPlainText())
                edges = edges_from_incidence_matrix(matrix)
        except MatrixParseError as error:
            self.show_matrix_error(error)
            return

        self.graph.replace(self.create_vertices(len(matrix)), edges)
        self.start_vertex, self.dragged_vertex_index = -1, -1
        self.update()

    def add_edge(self, start_vertex, end_vertex, weight, edge_type):
        self.graph.add_edge(start_vertex, end_vertex, weight, edge_type)
        self.update()

    def clear_graph(self):
        self.graph.clear()
        self.start_vertex, self.dragged_vertex_index = -1, -1
        self.update()

    def display_adjacency_matrix(self):
        if not self.vertices:
            self.show_empty_graph()
            return
        matrix = adjacency_matrix(len(self.vertices), self.edges)
        self.display_matrix(matrix)

    def display_incidence_matrix(self):
        edges = self.graph.valid_edges()
        if not self.vertices or not edges:
            self.show_empty_graph()
            return
        matrix = incidence_matrix(len(self.vertices), edges)
        self.display_matrix(matrix, edge_headers(edges))

    def display_matrix(self, matrix, headers=None):
        self.TextOutput.setText(format_matrix(matrix))
        self.tableWidget.setUpdatesEnabled(False)
        try:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(len(matrix))
            self.tableWidget.setColumnCount(len(matrix[0]) if matrix else 0)
            if headers:
                self.tableWidget.setHorizontalHeaderLabels(headers)

            font = QFont("Rubik", 12)
            for i, row in enumerate(matrix):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setFont(font)
                    self.tableWidget.setItem(i, j, item)
        finally:
            self.tableWidget.setUpdatesEnabled(True)

    def show_empty_graph(self):
        self.TextOutput.setText("Пустой граф")
        self.clear_matrix_table()

    def show_matrix_error(self, error):
        message = self.matrix_error_message(error)
        text = f"<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;{message}<br><br>"
        self.warningPopup(" ", text)

    def matrix_error_message(self, error):
        code = error.code if isinstance(error, MatrixParseError) else error
        if code == "empty":
            return "Введите матрицу."
        if code == "empty_row":
            return f"Строка {error.row} не содержит значений."
        if code == "not_integer":
            return f"Строка {error.row}, столбец {error.column}: значение '{error.value}' не является целым числом."
        if code == "row_length":
            return f"Строка {error.row}: найдено {error.actual} значений, ожидалось {error.expected}."
        if code == "square":
            if error.row is not None:
                return f"Матрица смежности должна быть квадратной: в строке {error.row} найдено {error.actual} значений, ожидалось {error.expected}."
            return f"Матрица смежности должна быть квадратной: строк {error.expected}, столбцов {error.actual}."
        if code == "negative_weight":
            return f"Строка {error.row}, столбец {error.column}: вес не может быть отрицательным."
        if code == "incidence_column_size":
            return f"Столбец {error.column}: у связи должно быть не больше двух ненулевых значений, найдено {error.actual}."
        if code == "incidence_weight_mismatch":
            return f"Столбец {error.column}: веса должны совпадать по модулю ({error.value})."
        return "Формат матрицы неверен."

    def create_vertices(self, vertices_count):
        if vertices_count <= 0:
            return []

        cx = self.drawing_board_size.x() + self.drawing_board_size.width() / 2
        cy = self.drawing_board_size.y() + self.drawing_board_size.height() / 2
        radius = min(
            cx / 7 * 6 - self.drawing_board_size.x(),
            cy / 7 * 6 - self.drawing_board_size.y(),
        )
        vertices = []
        for i in range(vertices_count):
            vertices.append(Vertex(
                cx + radius * math.cos(2 * math.pi * i / vertices_count),
                cy + radius * math.sin(2 * math.pi * i / vertices_count),
            ))
        return vertices
