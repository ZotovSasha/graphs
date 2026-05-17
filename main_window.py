import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from models import Edge, Vertex
from dialogs import WarningDialog, InstructionsDialog, InputDialog
from delegate import Delegate

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drawing_board_size = QRectF(15, 85, 750, 700)
        self.vertices = []
        self.edges = []
        self.matrix_weight_mode = "no_weight"
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
            vertex[0] = min(max(self.drawing_board_size.x() + self.vertex_radius, vertex[0]),
                            self.drawing_board_size.x() + self.drawing_board_size.width() - self.vertex_radius)
            vertex[1] = min(max(self.drawing_board_size.y() + self.vertex_radius, vertex[1]),
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

    def mousePressEvent(self, event):
        db = self.drawing_board_size
        r = self.vertex_radius
        if db.x() + r < event.x() < db.x() + db.width() - r and db.y() + r < event.y() < db.y() + db.height() - r:
            if self.delete:
                for i, vertex in enumerate(self.vertices):
                    if abs(vertex[0] - event.x()) < r and abs(vertex[1] - event.y()) < r:
                        self.vertices.pop(i)
                        self.edges = [e for e in self.edges if e.start_index != i and e.end_index != i]
                        for e in self.edges:
                            if e.start_index > i: e.start_index -= 1
                            if e.end_index > i: e.end_index -= 1
                        self.update()
                        return
            elif self.add_mode == "vertex":
                for i in range(len(self.vertices)):
                    if abs(self.vertices[i][0] - event.x()) < r and abs(self.vertices[i][1] - event.y()) < r:
                        self.dragged_vertex_index = i
                        return
                self.vertices.append([event.x(), event.y(), 1])
                self.update()
            elif self.add_mode == "edge":
                for i, vertex in enumerate(self.vertices):
                    if abs(vertex[0] - event.x()) < r and abs(vertex[1] - event.y()) < r:
                        self.start_vertex = i
                        return

    def mouseMoveEvent(self, event):
        db = self.drawing_board_size
        r = self.vertex_radius
        if db.x() + r < event.x() < db.x() + db.width() - r and db.y() + r < event.y() < db.y() + db.height() - r:
            if self.dragged_vertex_index != -1:
                self.vertices[self.dragged_vertex_index][0] = event.x()
                self.vertices[self.dragged_vertex_index][1] = event.y()
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
                weight, type = self.dialog.getInputs()
                try:
                    if weight.strip() == "": return [1, type]
                    weight = int(weight)
                    if weight < 0:
                        self.warningPopup(" ",
                                          "<h3>&nbsp;Предупреждение!</h3>\n&nbsp;&nbsp;Вес должен быть положительным.<br><br>")
                        continue
                    return [weight, type]
                except ValueError:
                    weight = -1
                    self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Вес должен быть целым числом.<br><br>")
            else:
                return [None, -1]

    def mouseReleaseEvent(self, event):
        if self.start_vertex != -1:
            for i, vertex in enumerate(self.vertices):
                if abs(vertex[0] - event.x()) < self.vertex_radius and abs(vertex[1] - event.y()) < self.vertex_radius:
                    result = self.ask_for_weight()
                    if result and result[0] is not None:
                        self.end_edge(self.start_vertex, i, result[0], result[1])
                    break
        self.dragged_vertex_index = -1
        self.start_vertex = -1
        self.update()

    def resizeEvent(self, event):
        self.setupGeometry(event.size().width(), event.size().height())
        self.clipVertices()

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            self.DrawFrame(painter)
            if self.start_vertex != -1 and len(self.vertices) > self.start_vertex:
                self.DrawEdge(painter, self.vertices[self.start_vertex][0], self.vertices[self.start_vertex][1],
                              self.cursor_pos[0], self.cursor_pos[1])
            self.DrawEdges(painter)
            self.DrawVertices(painter)
        except Exception as e:
            print(f"Paint error suppressed: {e}")
        finally:
            painter.end()

    def DrawVertices(self, painter):
        for i, vertex in enumerate(self.vertices):
            self.DrawVertex(painter, vertex[0], vertex[1], str(i + 1))

    def DrawVertex(self, painter, x, y, index):
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

    def DrawEdges(self, painter):
        v_count = len(self.vertices)
        for edge in self.edges:
            if 0 <= edge.start_index < v_count and 0 <= edge.end_index < v_count:
                self.DrawEdge(painter, self.vertices[edge.start_index][0], self.vertices[edge.start_index][1],
                              self.vertices[edge.end_index][0], self.vertices[edge.end_index][1], edge.weight,
                              edge.type)

    def DrawEdge(self, painter, x1, y1, x2, y2, weight=-1, type=1):
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
            if type == 0:
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
            if type == 1:
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

    def DrawFrame(self, painter):
        painter.save()
        painter.setPen(QPen(QColor("#90AFFF"), 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QColor("#ffffff"))
        painter.drawRoundedRect(self.drawing_board_size, 10, 10)
        painter.restore()

    def build_graph(self):
        if self.parse_matrix_mode == "adj":
            self.parse_adjacency_matrix()
        else:
            self.parse_incidence_matrix()

    def end_edge(self, start_vertex, end_vertex, weight, type):
        weight = self.edge_weight_value(weight)
        i = 0
        while i < len(self.edges):
            edge = self.edges[i]
            if type == edge.type:
                if edge.start_index == start_vertex and edge.end_index == end_vertex: self.edges.pop(i); continue
                if type == 1 and edge.start_index == end_vertex and edge.end_index == start_vertex: self.edges.pop(
                    i); continue
            if type != edge.type and ((edge.start_index == start_vertex and edge.end_index == end_vertex) or (
                    edge.start_index == end_vertex and edge.end_index == start_vertex)):
                self.edges.pop(i);
                continue
            i += 1
        self.edges.append(Edge(start_vertex, end_vertex, weight, type))
        self.update()

    def edge_weight_value(self, weight):
        try:
            return int(weight)
        except (TypeError, ValueError):
            return 1

    def graph_edges(self):
        v_count = len(self.vertices)
        return [e for e in self.edges if 0 <= e.start_index < v_count and 0 <= e.end_index < v_count]

    def clear_graph(self):
        self.vertices, self.edges = [], []
        self.start_vertex, self.dragged_vertex_index = -1, -1
        self.update()

    def display_adjacency_matrix(self):
        if not self.vertices:
            self.TextOutput.setText("Пустой граф")
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return
        n = len(self.vertices)
        mat = [[0] * n for _ in range(n)]
        for e in self.graph_edges():
            weight = self.edge_weight_value(e.weight)
            mat[e.start_index][e.end_index] = weight
            if e.type == 1: mat[e.end_index][e.start_index] = weight

        max_len = max(len(str(x)) for row in mat for x in row)
        out = "\n".join("  ".join(f"{v:>{max_len}}" for v in r) for r in mat)
        self.TextOutput.setText(out)

        self.tableWidget.setUpdatesEnabled(False)
        self.tableWidget.setRowCount(n)
        self.tableWidget.setColumnCount(n)
        font = QFont("Rubik", 12)
        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem(str(mat[i][j]))
                item.setFont(font)
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.setUpdatesEnabled(True)

    def display_incidence_matrix(self):
        edges = self.graph_edges()
        if not self.vertices or not edges:
            self.TextOutput.setText("Пустой граф")
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return
        n, m = len(self.vertices), len(edges)
        mat = [[0] * m for _ in range(n)]
        for j, e in enumerate(edges):
            weight = self.edge_weight_value(e.weight)
            if e.type == 0:
                mat[e.start_index][j] = weight
                mat[e.end_index][j] = -weight
            else:
                mat[e.start_index][j] = weight
                mat[e.end_index][j] = weight

        max_len = max(len(str(x)) for row in mat for x in row)
        out = "\n".join("  ".join(f"{v:>{max_len}}" for v in r) for r in mat)
        self.TextOutput.setText(out)

        self.tableWidget.setUpdatesEnabled(False)
        self.tableWidget.setRowCount(n)
        self.tableWidget.setColumnCount(m)
        self.tableWidget.setHorizontalHeaderLabels([f"{e.start_index + 1}-{e.end_index + 1}" for e in edges])
        font = QFont("Rubik", 12)
        for i in range(n):
            for j in range(m):
                item = QTableWidgetItem(str(mat[i][j]))
                item.setFont(font)
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.setUpdatesEnabled(True)

    def create_graph(self, vertices_count):
        cx, cy = self.drawing_board_size.x() + self.drawing_board_size.width() / 2, self.drawing_board_size.y() + self.drawing_board_size.height() / 2
        radius = min(cx / 7 * 6 - self.drawing_board_size.x(), cy / 7 * 6 - self.drawing_board_size.y())
        for i in range(vertices_count):
            self.vertices.append([cx + radius * math.cos(2 * math.pi * i / vertices_count),
                                  cy + radius * math.sin(2 * math.pi * i / vertices_count), 1])

    def parse_adjacency_matrix(self):
        lines = self.TextOutput.toPlainText().strip().split("\n")
        self.clear_graph()
        if not lines or len(lines[0].strip()) == 0: self.warningPopup(" ",
                                                                      "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Формат матрицы неверен.<br><br>"); return
        try:
            matrix = [list(map(int, ln.split())) for ln in lines if ln.strip()]
        except:
            self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Формат матрицы неверен.<br><br>"); return
        if any(len(r) != len(matrix) for r in matrix): self.warningPopup(" ",
                                                                         "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Матрица должна быть квадратной.<br><br>"); return

        self.create_graph(len(matrix))
        temp_edges = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                w = matrix[i][j]
                if w > 0:
                    found = False
                    for idx, e in enumerate(temp_edges):
                        if e.start_index == j and e.end_index == i and e.weight == w and e.type == 0:
                            temp_edges[idx] = Edge(j, i, w, 1);
                            found = True;
                            break
                    if not found: temp_edges.append(Edge(i, j, w, 0))
        self.edges = temp_edges
        self.update()

    def parse_incidence_matrix(self):
        lines = self.TextOutput.toPlainText().strip().split("\n")
        self.clear_graph()
        if not lines or len(lines[0].strip()) == 0: self.warningPopup(" ",
                                                                      "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Формат матрицы неверен.<br><br>"); return
        try:
            matrix = [list(map(int, ln.split())) for ln in lines if ln.strip()]
        except:
            self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Формат матрицы неверен.<br><br>"); return
        if any(len(r) != len(matrix[0]) for r in matrix): self.warningPopup(" ",
                                                                            "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Матрица должна быть требуемых размеров.<br><br>"); return

        n, m = len(matrix), len(matrix[0])
        self.create_graph(n)
        for col in range(m):
            start_v, start_w, ended = -1, 0, False
            for row in range(n):
                if matrix[row][col] != 0:
                    if start_v == -1:
                        start_v, start_w = row, matrix[row][col]
                    else:
                        if start_w == matrix[row][col]:
                            self.end_edge(start_v, row, start_w, 1)
                        elif start_w > 0:
                            self.end_edge(start_v, row, start_w, 0)
                        else:
                            self.end_edge(row, start_v, -start_w, 0)
                        ended = True;
                        break
            if not ended and start_v != -1: self.end_edge(start_v, start_v, abs(start_w), 0)
