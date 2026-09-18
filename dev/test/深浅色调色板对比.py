import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDateTimeEdit,
    QDial,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QStyleFactory,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from config.setting import setting
from theme.palette import palette
from theme.themeMode import ThemeMode


class TestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("自定义 QDialog 测试窗口")
        self.resize(320, 200)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("检查弹窗背景与输入框的灰色底调:"))
        layout.addWidget(QLineEdit("默认文本..."))

        combo = QComboBox()
        combo.addItems(["弹窗选项 1", "弹窗选项 2"])
        layout.addWidget(combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 主题与样式综合测试平台")

        self.is_default_palette = True

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("文件")
        file_menu.addAction("新建")
        file_menu.addAction("打开")
        file_menu.addSeparator()
        file_menu.addAction("exit")

        toolbar = QToolBar("控制工具栏")
        self.addToolBar(toolbar)

        toolbar.addWidget(QLabel(" QStyle 样式: "))
        self.style_combo = QComboBox()
        self.style_combo.addItems(list(map(str.lower, QStyleFactory.keys())))
        self.style_combo.setCurrentText(QApplication.style().name().lower())
        self.style_combo.currentTextChanged.connect(self.change_style)
        toolbar.addWidget(self.style_combo)

        toolbar.addSeparator()

        self.theme_btn = QPushButton("切换深浅模式")
        self.theme_btn.clicked.connect(self.toggle_theme_mode)
        toolbar.addWidget(self.theme_btn)

        self.theme_btn2 = QPushButton("切换调色板")
        self.theme_btn2.clicked.connect(self.toggle_palette)
        toolbar.addWidget(self.theme_btn2)

        self.statusBar().showMessage("就绪 - 可以在上方切换 Style 与 Palette")

        self.setup_central_ui()

    def setup_central_ui(self):
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # 各功能选项卡
        tab_widget.addTab(self.create_basic_controls_tab(), "基础与输入控件")
        tab_widget.addTab(self.create_views_tab(), "数据视图 (Base/AlternateBase)")
        tab_widget.addTab(self.create_containers_tab(), "容器与复杂控件")
        tab_widget.addTab(self.create_dialogs_tab(), "对话框与消息框")

    def create_basic_controls_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # 左侧: 按钮与单选/复选框
        left_box = QGroupBox("按钮与选择框 (含 Disable 状态)")
        left_layout = QVBoxLayout(left_box)

        btn_normal = QPushButton("普通按钮")
        btn_default = QPushButton("默认/主按钮")
        btn_default.setDefault(True)
        btn_disabled = QPushButton("禁用按钮")
        btn_disabled.setEnabled(False)

        left_layout.addWidget(btn_normal)
        left_layout.addWidget(btn_default)
        left_layout.addWidget(btn_disabled)

        left_layout.addSpacing(10)
        cb_normal = QCheckBox("复选框 - 正常")
        cb_checked = QCheckBox("复选框 - 选中")
        cb_checked.setChecked(True)
        cb_disabled = QCheckBox("复选框 - 禁用")
        cb_disabled.setEnabled(False)
        left_layout.addWidget(cb_normal)
        left_layout.addWidget(cb_checked)
        left_layout.addWidget(cb_disabled)

        left_layout.addSpacing(10)
        rb_1 = QRadioButton("单选框 A")
        rb_2 = QRadioButton("单选框 B (选中)")
        rb_2.setChecked(True)
        rb_disabled = QRadioButton("单选框 C (禁用)")
        rb_disabled.setEnabled(False)
        left_layout.addWidget(rb_1)
        left_layout.addWidget(rb_2)
        left_layout.addWidget(rb_disabled)

        left_layout.addStretch()

        # 右侧: 表单输入控件
        right_box = QGroupBox("表单与数值控件")
        form_layout = QFormLayout(right_box)

        form_layout.addRow("文本输入框:", QLineEdit("默认文本"))
        form_layout.addRow("占位符输入框:", QLineEdit(placeholderText="请输入..."))

        pwd_edit = QLineEdit("123456")
        pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("密码输入框:", pwd_edit)

        disabled_edit = QLineEdit("禁用的输入框")
        disabled_edit.setEnabled(False)
        form_layout.addRow("禁用输入框:", disabled_edit)

        form_layout.addRow("整数微调框:", QSpinBox())
        form_layout.addRow("浮点微调框:", QDoubleSpinBox())

        combo = QComboBox()
        combo.addItems(["选项 A", "选项 B", "选项 C"])
        form_layout.addRow("下拉选择框:", combo)

        date_edit = QDateTimeEdit()
        date_edit.setCalendarPopup(True)
        form_layout.addRow("日期时间框:", date_edit)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(60)
        form_layout.addRow("滑动条:", slider)

        dial = QDial()
        dial.setNotchesVisible(True)
        dial.setValue(40)
        form_layout.addRow("旋钮控件:", dial)

        layout.addWidget(left_box)
        layout.addWidget(right_box)
        return widget

    def create_views_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # 1. QTableWidget (开启交替背景色以测试 AlternateBase)
        table_box = QGroupBox("表格视图 (QTableWidget - AlternateBase)")
        table_layout = QVBoxLayout(table_box)
        table = QTableWidget(5, 3)
        table.setHorizontalHeaderLabels(["列 1", "列 2", "列 3"])
        table.setAlternatingRowColors(True)  # 开启隔行变色
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row in range(5):
            for col in range(3):
                table.setItem(row, col, QTableWidgetItem(f"单元格 ({row}, {col})"))

        table_layout.addWidget(table)

        # 2. QTreeWidget
        tree_box = QGroupBox("树状视图 (QTreeWidget)")
        tree_layout = QVBoxLayout(tree_box)
        tree = QTreeWidget()
        tree.setHeaderLabels(["结构", "状态"])
        root1 = QTreeWidgetItem(tree, ["节点 1", "正常"])
        QTreeWidgetItem(root1, ["子节点 1-1", "激活"])
        QTreeWidgetItem(root1, ["子节点 1-2", "禁用"])
        root2 = QTreeWidgetItem(tree, ["节点 2", "悬停"])
        tree.expandAll()
        tree_layout.addWidget(tree)

        # 3. QListWidget
        list_box = QGroupBox("列表视图 (QListWidget)")
        list_layout = QVBoxLayout(list_box)
        list_widget = QListWidget()
        for i in range(1, 10):
            list_widget.addItem(QListWidgetItem(f"列表项 Item {i}"))
        list_layout.addWidget(list_widget)

        layout.addWidget(table_box, stretch=2)
        layout.addWidget(tree_box, stretch=1)
        layout.addWidget(list_box, stretch=1)
        return widget

    def create_containers_tab(self):
        widget = QWidget()
        layout = QGridLayout(widget)

        # 文本编辑器
        text_box = QGroupBox("多行文本框 (QTextEdit)")
        text_layout = QVBoxLayout(text_box)
        text_edit = QTextEdit()
        text_edit.setPlainText(
            "这里是多行文本框内容...\n"
            "可以用来测试 Text, Base, Selection, Highlight 等颜色的渲染效果.\n"
            "试试在此选中文本观察选中文本背景色."
        )
        text_layout.addWidget(text_edit)

        # 进度条与日历
        right_box = QGroupBox("复合控件与进度条")
        right_layout = QVBoxLayout(right_box)

        progress = QProgressBar()
        progress.setValue(75)
        right_layout.addWidget(QLabel("进度条 (75%):"))
        right_layout.addWidget(progress)

        progress_ind = QProgressBar()
        progress_ind.setRange(0, 0)  # 繁忙指示器
        right_layout.addWidget(QLabel("忙碌状态进度条:"))
        right_layout.addWidget(progress_ind)

        right_layout.addWidget(QLabel("日历控件 (QCalendarWidget):"))
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        right_layout.addWidget(calendar)

        layout.addWidget(text_box, 0, 0)
        layout.addWidget(right_box, 0, 1)
        return widget

    def create_dialogs_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        btn_grid = QGridLayout()

        btn_dialog = QPushButton("打开自定义 QDialog")
        btn_dialog.clicked.connect(lambda: TestDialog(self).exec())

        btn_info = QPushButton("QMessageBox - 信息 (Information)")
        btn_info.clicked.connect(
            lambda: QMessageBox.information(self, "信息", "这是一个信息提示框.")
        )

        btn_warn = QPushButton("QMessageBox - 警告 (Warning)")
        btn_warn.clicked.connect(
            lambda: QMessageBox.warning(self, "警告", "这是一个警告提示框!")
        )

        btn_critical = QPushButton("QMessageBox - 错误 (Critical)")
        btn_critical.clicked.connect(
            lambda: QMessageBox.critical(self, "错误", "这是一个关键错误提示框!")
        )

        btn_file = QPushButton("打开 QFileDialog (文件选择)")
        btn_file.clicked.connect(
            lambda: QFileDialog.getOpenFileName(self, "选择文件", "")
        )

        btn_color = QPushButton("打开 QColorDialog (颜色选择)")
        btn_color.clicked.connect(lambda: QColorDialog.getColor(parent=self))

        btn_grid.addWidget(btn_dialog, 0, 0)
        btn_grid.addWidget(btn_info, 0, 1)
        btn_grid.addWidget(btn_warn, 1, 0)
        btn_grid.addWidget(btn_critical, 1, 1)
        btn_grid.addWidget(btn_file, 2, 0)
        btn_grid.addWidget(btn_color, 2, 1)

        layout.addLayout(btn_grid)
        layout.addStretch()
        return widget

    def change_style(self, style_name):
        QApplication.setStyle(style_name)
        self.statusBar().showMessage(f"当前 Style 已切换为: {style_name}")

    def toggle_theme_mode(self):
        setting.theme = ThemeMode.light if setting.theme == ThemeMode.dark else ThemeMode.dark

        color_schema = {
            ThemeMode.light: Qt.ColorScheme.Light,
            ThemeMode.dark: Qt.ColorScheme.Dark,
        }

        QApplication.styleHints().setColorScheme(color_schema[setting.theme])
        self.update_palette()

    def toggle_palette(self):
        self.is_default_palette = not self.is_default_palette
        self.update_palette()

    def update_palette(self):
        if self.is_default_palette:
            QApplication.setPalette(QPalette())

        else:
            QApplication.setPalette(palette())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
