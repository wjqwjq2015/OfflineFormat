#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
离线 JSON 格式化工具
功能：JSON 美化、排序、复制、清空、验证
作者：wangjunqi
版本：1.0
"""

import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QMessageBox, QSplitter,
    QFrame, QStatusBar, QTabWidget, QSpinBox,
    QFormLayout, QGroupBox, QLineEdit, QCheckBox, QShortcut,
    QTreeWidget, QTreeWidgetItem, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtGui import QFont, QKeySequence, QTextCursor, QTextCharFormat, QColor, QTextDocument


class JSONTreeWidget(QTreeWidget):
    """
    自定义JSON树形视图组件
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_tree()

    def setup_tree(self):
        """
        设置树形视图的基本属性
        """
        # 设置列标题
        self.setHeaderLabels(["键/索引", "值", "类型"])

        # 设置列宽
        header = self.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # 设置选择模式
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        # 设置样式
        self.setStyleSheet("""
            QTreeWidget {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 24px;
                alternate-background-color: #f8f9fa;
            }
            QTreeWidget::item {
                padding: 6px;
                border-bottom: 1px solid #ecf0f1;
                height: 24px;
            }
            QTreeWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTreeWidget::item:hover {
                background-color: #e8f4fd;
            }
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {
                border-image: none;
                image: none;
                background-color: #27ae60;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: 1px;
                border: 2px solid #2ecc71;
            }
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {
                border-image: none;
                image: none;
                background-color: #e74c3c;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: 1px;
                border: 2px solid #c0392b;
            }
            QTreeWidget::branch:has-children:!has-siblings:closed:hover,
            QTreeWidget::branch:closed:has-children:has-siblings:hover {
                background-color: #229954;
                border: 2px solid #27ae60;
            }
            QTreeWidget::branch:open:has-children:!has-siblings:hover,
            QTreeWidget::branch:open:has-children:has-siblings:hover {
                background-color: #cb4335;
                border: 2px solid #e74c3c;
            }
        """)

        # 启用交替行颜色
        self.setAlternatingRowColors(True)

        # 设置根节点装饰
        self.setRootIsDecorated(True)

        # 设置动画效果
        self.setAnimated(True)

    def populate_tree(self, json_data):
        """
        填充树形视图数据
        """
        self.clear()

        if json_data is None:
            return

        # 创建根节点
        if isinstance(json_data, dict):
            root_item = QTreeWidgetItem(["JSON Object", f"{len(json_data)} 项", "Object"])
            self.addTopLevelItem(root_item)
            self._add_dict_items(root_item, json_data)
        elif isinstance(json_data, list):
            root_item = QTreeWidgetItem(["JSON Array", f"{len(json_data)} 项", "Array"])
            self.addTopLevelItem(root_item)
            self._add_list_items(root_item, json_data)
        else:
            # 单个值
            root_item = QTreeWidgetItem(["JSON Value", str(json_data), type(json_data).__name__])
            self.addTopLevelItem(root_item)

        # 展开根节点
        self.expandToDepth(0)

    def _add_dict_items(self, parent_item, data_dict):
        """
        添加字典项到树中
        """
        for key, value in data_dict.items():
            if isinstance(value, dict):
                item = QTreeWidgetItem([str(key), f"{len(value)} 项", "Object"])
                parent_item.addChild(item)
                self._add_dict_items(item, value)
            elif isinstance(value, list):
                item = QTreeWidgetItem([str(key), f"{len(value)} 项", "Array"])
                parent_item.addChild(item)
                self._add_list_items(item, value)
            else:
                # 处理值的显示
                value_str = self._format_value(value)
                value_type = type(value).__name__
                item = QTreeWidgetItem([str(key), value_str, value_type])
                parent_item.addChild(item)

    def _add_list_items(self, parent_item, data_list):
        """
        添加列表项到树中
        """
        for index, value in enumerate(data_list):
            if isinstance(value, dict):
                item = QTreeWidgetItem([f"[{index}]", f"{len(value)} 项", "Object"])
                parent_item.addChild(item)
                self._add_dict_items(item, value)
            elif isinstance(value, list):
                item = QTreeWidgetItem([f"[{index}]", f"{len(value)} 项", "Array"])
                parent_item.addChild(item)
                self._add_list_items(item, value)
            else:
                # 处理值的显示
                value_str = self._format_value(value)
                value_type = type(value).__name__
                item = QTreeWidgetItem([f"[{index}]", value_str, value_type])
                parent_item.addChild(item)

    def _format_value(self, value):
        """
        格式化值的显示
        """
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, str):
            # 限制字符串长度显示
            if len(value) > 100:
                return f'"{value[:97]}..."'
            return f'"{value}"'
        else:
            return str(value)

    def get_selected_path(self):
        """
        获取选中项的路径
        """
        current_item = self.currentItem()
        if not current_item:
            return []

        path = []
        item = current_item
        while item and item.parent():
            path.insert(0, item.text(0))
            item = item.parent()

        return path


class JSONFormatterApp(QMainWindow):
    """
    JSON 格式化工具主窗口类
    """

    def __init__(self):
        """
        初始化主窗口
        """
        super().__init__()
        # 初始化设置
        self.settings = QSettings('JSONFormatter', 'FontSettings')
        self.current_text_font_size = self.settings.value('text_font_size', 12, type=int)  # 文本编辑器字体
        self.current_ui_font_size = self.settings.value('ui_font_size', 14, type=int)  # UI元素字体
        self.temp_ui_font_size = self.current_ui_font_size  # 临时UI字体大小，用于保存前的预览

        # 初始化搜索相关变量
        self.input_search_widget = None
        self.output_search_widget = None
        self.input_replace_widget = None
        self.output_replace_widget = None
        self.current_search_text = ""
        self.last_search_position = 0
        self.search_results = []
        self.current_result_index = -1

        # 初始化JSON验证相关变量
        self.json_error_format = QTextCharFormat()
        self.json_error_format.setBackground(QColor(255, 200, 200))  # 浅红色背景
        self.json_normal_format = QTextCharFormat()
        self.json_normal_format.setBackground(QColor(255, 255, 255))  # 白色背景
        # 移除实时验证相关变量
        # self.validation_timer = QTimer()
        # self.validation_timer.setSingleShot(True)
        # self.validation_timer.timeout.connect(self.validate_json_input)
        # self.last_json_error = None

        self.init_ui()
        self.setup_connections()
        self.setup_shortcuts()
        self.apply_font_size()

    def init_ui(self):
        """
        初始化用户界面
        """
        # 设置窗口基本属性
        self.setWindowTitle('离线 JSON 格式化工具 v1.0')
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 创建标签页控件
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 创建主功能标签页
        main_tab = QWidget()
        self.tab_widget.addTab(main_tab, "JSON 格式化")

        # 创建选项标签页
        options_tab = QWidget()
        self.tab_widget.addTab(options_tab, "选项设置")

        # 设置主功能标签页布局
        main_tab_layout = QVBoxLayout(main_tab)
        main_tab_layout.setContentsMargins(10, 10, 10, 10)
        main_tab_layout.setSpacing(10)

        # 创建简化的标题标签（减少占用空间）
        self.title_label = QLabel('JSON 格式化工具')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px;
                background-color: #ecf0f1;
                border-radius: 3px;
                margin-bottom: 5px;
            }
        """)
        main_tab_layout.addWidget(self.title_label)

        # 创建文本区域布局（增加拉伸因子，占用更多空间）
        text_layout = self.create_text_area()
        main_tab_layout.addLayout(text_layout, 1)  # 拉伸因子为1，占用主要空间

        # 创建按钮区域（固定大小，不拉伸）
        button_layout = self.create_button_area()
        main_tab_layout.addLayout(button_layout, 0)  # 拉伸因子为0，保持固定大小

        # 设置选项标签页
        self.setup_options_tab(options_tab)

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('就绪')

        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                line-height: 1.4;
                background-color: white;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)

    def create_text_area(self):
        """
        创建文本输入输出区域
        """
        # 创建水平分割器
        splitter = QSplitter(Qt.Horizontal)

        # 创建左侧输入区域
        left_frame = QFrame()
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(0, 0, 5, 0)

        self.input_label = QLabel('输入 JSON：')
        self.input_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
        """)
        left_layout.addWidget(self.input_label)

        # 创建输入文本框容器（用于嵌入搜索组件）
        self.input_container = QFrame()
        self.input_container.setStyleSheet("QFrame { border: 1px solid #bdc3c7; }")
        input_container_layout = QVBoxLayout(self.input_container)
        input_container_layout.setContentsMargins(0, 0, 0, 0)
        input_container_layout.setSpacing(0)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('请在此处输入需要格式化的 JSON 数据...')
        self.input_text.setStyleSheet("QTextEdit { border: none; }")
        input_container_layout.addWidget(self.input_text)

        left_layout.addWidget(self.input_container)

        # 创建右侧输出区域
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(5, 0, 0, 0)

        self.output_label = QLabel('输出 JSON：')
        self.output_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
        """)
        right_layout.addWidget(self.output_label)

        # 创建输出区域选项卡
        self.output_tab_widget = QTabWidget()
        self.output_tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #d5dbdb;
            }
        """)

        # 创建文本视图标签页
        text_tab = QWidget()
        text_tab_layout = QVBoxLayout(text_tab)
        text_tab_layout.setContentsMargins(0, 0, 0, 0)
        text_tab_layout.setSpacing(0)

        # 创建输出文本框容器（用于嵌入搜索组件）
        self.output_container = QFrame()
        self.output_container.setStyleSheet("QFrame { border: none; }")
        output_container_layout = QVBoxLayout(self.output_container)
        output_container_layout.setContentsMargins(0, 0, 0, 0)
        output_container_layout.setSpacing(0)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText('格式化后的 JSON 将显示在此处...')
        self.output_text.setStyleSheet("QTextEdit { border: none; }")
        output_container_layout.addWidget(self.output_text)

        text_tab_layout.addWidget(self.output_container)

        # 创建树形视图标签页
        tree_tab = QWidget()
        tree_tab_layout = QVBoxLayout(tree_tab)
        tree_tab_layout.setContentsMargins(0, 0, 0, 0)

        self.json_tree = JSONTreeWidget()
        tree_tab_layout.addWidget(self.json_tree)

        # 添加标签页
        self.output_tab_widget.addTab(text_tab, "📄 文本视图")
        self.output_tab_widget.addTab(tree_tab, "🌳 树形视图")

        right_layout.addWidget(self.output_tab_widget)

        # 添加到分割器
        splitter.addWidget(left_frame)
        splitter.addWidget(right_frame)
        splitter.setSizes([600, 600])  # 设置初始比例

        # 创建布局并添加分割器
        layout = QVBoxLayout()
        layout.addWidget(splitter)

        return layout

    def setup_options_tab(self, options_tab):
        """
        设置选项标签页
        """
        options_layout = QVBoxLayout(options_tab)
        options_layout.setContentsMargins(20, 20, 20, 20)
        options_layout.setSpacing(15)

        # 字体设置组
        font_group = QGroupBox("字体设置")
        font_layout = QFormLayout(font_group)

        # 定义字体大小范围
        self.min_font_size = 8
        self.max_font_size = 32

        # 文本编辑器字体大小设置
        self.text_font_size_spinbox = QSpinBox()
        self.text_font_size_spinbox.setMinimum(1)
        self.text_font_size_spinbox.setMaximum(999)
        self.text_font_size_spinbox.setValue(self.current_text_font_size)
        self.text_font_size_spinbox.setSuffix(" px")
        self.text_font_size_spinbox.valueChanged.connect(self.on_text_font_size_changed)

        font_layout.addRow("文本编辑器字体大小：", self.text_font_size_spinbox)

        # UI元素字体大小设置
        self.ui_font_size_spinbox = QSpinBox()
        self.ui_font_size_spinbox.setMinimum(1)
        self.ui_font_size_spinbox.setMaximum(999)
        self.ui_font_size_spinbox.setValue(self.current_ui_font_size)
        self.ui_font_size_spinbox.setSuffix(" px")
        self.ui_font_size_spinbox.valueChanged.connect(self.on_ui_font_size_changed)

        font_layout.addRow("界面标签字体大小：", self.ui_font_size_spinbox)

        # 保存按钮
        self.save_font_button = QPushButton("保存字体设置")
        self.save_font_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.save_font_button.clicked.connect(self.save_font_settings_and_apply)
        font_layout.addRow(self.save_font_button)

        # 添加说明标签
        self.info_label = QLabel(
            "提示：\n• 使用 Ctrl + 鼠标滚轮 可快速调整文本编辑器字体大小\n• 界面标签字体需要点击保存按钮后生效")
        self.info_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
                padding: 15px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                line-height: 1.5;
            }
        """)
        font_layout.addRow(self.info_label)

        options_layout.addWidget(font_group)
        options_layout.addStretch()

    def create_button_area(self):
        """
        创建按钮区域
        """
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # 创建按钮（添加中文标签）
        self.beautify_btn = QPushButton('🎨 美化格式')
        self.beautify_btn.setToolTip('格式化 JSON（美化显示）')

        self.sort_btn = QPushButton('🔤 排序格式')
        self.sort_btn.setToolTip('按键名排序并格式化 JSON')

        self.minify_btn = QPushButton('📦 压缩格式')
        self.minify_btn.setToolTip('压缩 JSON 为单行')

        self.validate_btn = QPushButton('✅ 验证格式')
        self.validate_btn.setToolTip('验证 JSON 格式是否正确')

        self.copy_btn = QPushButton('📋 复制结果')
        self.copy_btn.setToolTip('复制输出结果到剪贴板')

        self.clear_btn = QPushButton('🗑️ 清空内容')
        self.clear_btn.setToolTip('清空输入和输出内容')

        self.expand_all_btn = QPushButton('📂 展开全部')
        self.expand_all_btn.setToolTip('展开树形视图中的所有节点')

        self.collapse_all_btn = QPushButton('📁 折叠全部')
        self.collapse_all_btn.setToolTip('折叠树形视图中的所有节点')

        # 设置按钮样式
        buttons = [self.beautify_btn, self.sort_btn, self.minify_btn,
                   self.validate_btn, self.copy_btn, self.expand_all_btn,
                   self.collapse_all_btn, self.clear_btn]

        for i, btn in enumerate(buttons):
            if i == len(buttons) - 1:  # 清空按钮使用不同颜色
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                    QPushButton:pressed {
                        background-color: #a93226;
                    }
                """)
            elif i == len(buttons) - 3 or i == len(buttons) - 2:  # 展开/折叠按钮使用绿色
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #27ae60;
                    }
                    QPushButton:hover {
                        background-color: #229954;
                    }
                    QPushButton:pressed {
                        background-color: #1e8449;
                    }
                """)
            button_layout.addWidget(btn)

        # 添加弹性空间
        button_layout.addStretch()

        return button_layout

    def setup_connections(self):
        """
        设置信号连接
        """
        self.beautify_btn.clicked.connect(self.beautify_json)
        self.sort_btn.clicked.connect(self.sort_json)
        self.minify_btn.clicked.connect(self.minify_json)
        self.validate_btn.clicked.connect(self.validate_json)
        self.copy_btn.clicked.connect(self.copy_output)
        self.expand_all_btn.clicked.connect(self.expand_all_tree)
        self.collapse_all_btn.clicked.connect(self.collapse_all_tree)
        self.clear_btn.clicked.connect(self.clear_all)

        # 为文本编辑器安装事件过滤器以处理滚轮事件
        self.input_text.installEventFilter(self)
        self.output_text.installEventFilter(self)

        # 移除实时JSON验证连接
        # self.input_text.textChanged.connect(self.on_input_text_changed)

    def setup_shortcuts(self):
        """
        设置快捷键
        """
        # Ctrl+F 搜索快捷键
        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(self.show_search_dialog)

        # Ctrl+R 搜索替换快捷键
        self.replace_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.replace_shortcut.activated.connect(self.show_replace_dialog)

    def eventFilter(self, obj, event):
        """
        事件过滤器，处理Ctrl+滚轮调整字体大小
        """
        if (obj == self.input_text or obj == self.output_text) and event.type() == event.Wheel:
            if event.modifiers() == Qt.ControlModifier:
                # Ctrl + 滚轮只调整文本编辑器字体大小
                delta = event.angleDelta().y()
                if delta > 0:  # 向上滚动，增大字体
                    self.increase_text_font_size()
                else:  # 向下滚动，减小字体
                    self.decrease_text_font_size()
                return True  # 事件已处理
        return super().eventFilter(obj, event)

    def on_text_font_size_changed(self, size):
        """
        文本编辑器字体大小改变时的处理（立即生效）
        """
        self.current_text_font_size = size
        self.apply_text_font_size()
        self.save_text_font_settings()
        self.status_bar.showMessage(f"文本编辑器字体大小已调整为 {size}px", 2000)

    def on_ui_font_size_changed(self, size):
        """
        UI元素字体大小改变时的处理（仅更新临时值，需要保存后生效）
        """
        self.temp_ui_font_size = size
        self.status_bar.showMessage(f"界面标签字体大小设置为 {size}px（点击保存按钮生效）", 2000)

    def increase_text_font_size(self):
        """
        增大文本编辑器字体大小
        """
        if self.current_text_font_size < 999:
            self.current_text_font_size += 1
            self.text_font_size_spinbox.setValue(self.current_text_font_size)

    def decrease_text_font_size(self):
        """
        减小文本编辑器字体大小
        """
        if self.current_text_font_size > 1:
            self.current_text_font_size -= 1
            self.text_font_size_spinbox.setValue(self.current_text_font_size)

    def increase_all_font_size(self):
        """
        增大所有字体大小
        """
        if self.current_text_font_size < self.max_font_size:
            self.current_text_font_size += 1
            self.text_font_size_spinbox.setValue(self.current_text_font_size)
        if self.current_ui_font_size < self.max_font_size:
            self.current_ui_font_size += 1
            self.ui_font_size_spinbox.setValue(self.current_ui_font_size)

    def decrease_all_font_size(self):
        """
        减小所有字体大小
        """
        if self.current_text_font_size > self.min_font_size:
            self.current_text_font_size -= 1
            self.text_font_size_spinbox.setValue(self.current_text_font_size)
        if self.current_ui_font_size > self.min_font_size:
            self.current_ui_font_size -= 1
            self.ui_font_size_spinbox.setValue(self.current_ui_font_size)

    def apply_text_font_size(self):
        """
        应用字体大小到文本编辑器
        """
        font = QFont('Consolas', self.current_text_font_size)
        if hasattr(self, 'input_text'):
            self.input_text.setFont(font)
        if hasattr(self, 'output_text'):
            self.output_text.setFont(font)

    def apply_ui_font_size(self):
        """
        应用字体大小到UI元素（包括选项设置页面内的元素）
        """
        # 更新标题标签字体
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {self.current_ui_font_size}px;
                    font-weight: bold;
                    color: #2c3e50;
                    padding: 5px;
                    background-color: #ecf0f1;
                    border-radius: 3px;
                    margin-bottom: 5px;
                }}
            """)

        # 更新输入输出标签字体
        if hasattr(self, 'input_label'):
            self.input_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {self.current_ui_font_size}px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 5px;
                }}
            """)

        if hasattr(self, 'output_label'):
            self.output_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {self.current_ui_font_size}px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 5px;
                }}
            """)

        # 更新选项设置页面内的字体
        if hasattr(self, 'info_label'):
            self.info_label.setStyleSheet(f"""
                QLabel {{
                    color: #7f8c8d;
                    font-size: {self.current_ui_font_size}px;
                    padding: 15px;
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                    line-height: 1.5;
                }}
            """)

        if hasattr(self, 'save_font_button'):
            self.save_font_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: {self.current_ui_font_size}px;
                }}
                QPushButton:hover {{
                    background-color: #0056b3;
                }}
                QPushButton:pressed {{
                    background-color: #004085;
                }}
            """)

    def apply_font_size(self):
        """
        应用所有字体大小设置
        """
        self.apply_text_font_size()
        self.apply_ui_font_size()

    def save_text_font_settings(self):
        """
        保存文本编辑器字体大小设置
        """
        self.settings.setValue('text_font_size', self.current_text_font_size)

    def save_font_settings_and_apply(self):
        """
        保存所有字体设置并应用UI字体
        """
        self.current_ui_font_size = self.temp_ui_font_size
        self.settings.setValue('text_font_size', self.current_text_font_size)
        self.settings.setValue('ui_font_size', self.current_ui_font_size)
        self.apply_ui_font_size()
        self.status_bar.showMessage(
            f'字体设置已保存：文本 {self.current_text_font_size}px，界面 {self.current_ui_font_size}px', 3000)

    def save_font_settings(self):
        """
        保存字体大小设置
        """
        self.settings.setValue('text_font_size', self.current_text_font_size)
        self.settings.setValue('ui_font_size', self.current_ui_font_size)
        self.status_bar.showMessage(
            f'字体大小已调整：文本 {self.current_text_font_size}px，界面 {self.current_ui_font_size}px')

    def get_input_json(self):
        """
        获取并解析输入的 JSON
        """
        try:
            input_text = self.input_text.toPlainText().strip()
            if not input_text:
                self.show_message('警告', '请先输入 JSON 数据！', QMessageBox.Warning)
                return None

            json_data = json.loads(input_text)
            return json_data
        except json.JSONDecodeError as e:
            self.show_message('JSON 格式错误', f'输入的 JSON 无效：\n{str(e)}', QMessageBox.Critical)
            return None
        except Exception as e:
            self.show_message('错误', f'处理 JSON 时发生错误：\n{str(e)}', QMessageBox.Critical)
            return None

    def beautify_json(self):
        """
        美化 JSON 格式
        """
        json_data = self.get_input_json()
        if json_data is not None:
            try:
                formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False, separators=(',', ': '))
                # 更新文本视图
                self.output_text.setPlainText(formatted_json)
                # 更新树形视图
                self.json_tree.populate_tree(json_data)
                self.status_bar.showMessage('JSON 格式化完成')
            except Exception as e:
                self.show_message('错误', f'格式化失败：\n{str(e)}', QMessageBox.Critical)

    def sort_json(self):
        """
        排序并美化 JSON
        """
        json_data = self.get_input_json()
        if json_data is not None:
            try:
                formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False,
                                            separators=(',', ': '), sort_keys=True)
                # 更新文本视图
                self.output_text.setPlainText(formatted_json)
                # 更新树形视图（排序后的数据）
                self.json_tree.populate_tree(json_data)
                self.status_bar.showMessage('JSON 排序并格式化完成')
            except Exception as e:
                self.show_message('错误', f'排序失败：\n{str(e)}', QMessageBox.Critical)

    def minify_json(self):
        """
        压缩 JSON 为单行
        """
        json_data = self.get_input_json()
        if json_data is not None:
            try:
                minified_json = json.dumps(json_data, ensure_ascii=False, separators=(',', ':'))
                self.output_text.setPlainText(minified_json)
                self.status_bar.showMessage('JSON 压缩完成')
            except Exception as e:
                self.show_message('错误', f'压缩失败：\n{str(e)}', QMessageBox.Critical)

    def validate_json(self):
        """
        验证 JSON 格式
        """
        input_text = self.input_text.toPlainText().strip()
        if not input_text:
            self.show_message('警告', '请先输入 JSON 数据！', QMessageBox.Warning)
            return

        try:
            json.loads(input_text)
            self.show_message('验证结果', 'JSON 格式正确！✅', QMessageBox.Information)
            self.status_bar.showMessage('JSON 格式验证通过')
        except json.JSONDecodeError as e:
            self.show_message('验证结果', f'JSON 格式错误：\n{str(e)}', QMessageBox.Critical)
            self.status_bar.showMessage('JSON 格式验证失败')
        except Exception as e:
            self.show_message('错误', f'验证时发生错误：\n{str(e)}', QMessageBox.Critical)

    def copy_output(self):
        """
        复制输出内容到剪贴板
        """
        output_text = self.output_text.toPlainText().strip()
        if not output_text:
            self.show_message('警告', '没有可复制的内容！', QMessageBox.Warning)
            return

        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(output_text)
            self.show_message('成功', '内容已复制到剪贴板！📋', QMessageBox.Information)
            self.status_bar.showMessage('内容已复制到剪贴板')
        except Exception as e:
            self.show_message('错误', f'复制失败：\n{str(e)}', QMessageBox.Critical)

    def clear_all(self):
        """
        清空所有内容
        """
        reply = QMessageBox.question(self, '确认清空', '确定要清空所有内容吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.input_text.clear()
            self.output_text.clear()
            self.json_tree.clear()
            self.status_bar.showMessage('内容已清空')

    def expand_all_tree(self):
        """
        展开树形视图中的所有节点
        """
        self.json_tree.expandAll()
        self.status_bar.showMessage('已展开所有节点')

    def collapse_all_tree(self):
        """
        折叠树形视图中的所有节点
        """
        self.json_tree.collapseAll()
        # 保持根节点展开
        if self.json_tree.topLevelItemCount() > 0:
            self.json_tree.expandToDepth(0)
        self.status_bar.showMessage('已折叠所有节点')

    def show_message(self, title, message, icon=QMessageBox.Information):
        """
        显示消息对话框
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()

    def show_search_dialog(self):
        """
        显示嵌入式搜索组件
        """
        # 确定当前焦点的文本框
        if self.input_text.hasFocus():
            self.show_embedded_search(self.input_text, self.input_container, 'input')
        elif self.output_text.hasFocus():
            self.show_embedded_search(self.output_text, self.output_container, 'output')
        else:
            # 默认使用输入框
            self.show_embedded_search(self.input_text, self.input_container, 'input')

    def show_replace_dialog(self):
        """
        显示嵌入式替换组件
        """
        # 确定当前焦点的文本框
        if self.input_text.hasFocus():
            self.show_embedded_replace(self.input_text, self.input_container, 'input')
        elif self.output_text.hasFocus():
            self.show_embedded_replace(self.output_text, self.output_container, 'output')
        else:
            # 默认使用输入框
            self.show_embedded_replace(self.input_text, self.input_container, 'input')

    def show_embedded_search(self, text_edit, container, widget_type):
        """
        显示嵌入式搜索组件
        """
        # 隐藏其他搜索组件
        self.hide_all_search_widgets()

        # 创建或显示对应的搜索组件
        if widget_type == 'input':
            if self.input_search_widget is None:
                self.input_search_widget = EmbeddedSearchWidget(text_edit, self)
                container.layout().insertWidget(0, self.input_search_widget)
            self.input_search_widget.show()
            self.input_search_widget.focus_search_input()
        else:
            if self.output_search_widget is None:
                self.output_search_widget = EmbeddedSearchWidget(text_edit, self)
                container.layout().insertWidget(0, self.output_search_widget)
            self.output_search_widget.show()
            self.output_search_widget.focus_search_input()

    def show_embedded_replace(self, text_edit, container, widget_type):
        """
        显示嵌入式替换组件
        """
        # 隐藏其他搜索组件
        self.hide_all_search_widgets()

        # 创建或显示对应的替换组件
        if widget_type == 'input':
            if self.input_replace_widget is None:
                self.input_replace_widget = EmbeddedReplaceWidget(text_edit, self)
                container.layout().insertWidget(0, self.input_replace_widget)
            self.input_replace_widget.show()
            self.input_replace_widget.focus_search_input()
        else:
            if self.output_replace_widget is None:
                self.output_replace_widget = EmbeddedReplaceWidget(text_edit, self)
                container.layout().insertWidget(0, self.output_replace_widget)
            self.output_replace_widget.show()
            self.output_replace_widget.focus_search_input()

    def hide_all_search_widgets(self):
        """
        隐藏所有搜索组件
        """
        widgets = [self.input_search_widget, self.output_search_widget,
                   self.input_replace_widget, self.output_replace_widget]
        for widget in widgets:
            if widget is not None:
                widget.hide()

    # 移除实时验证相关方法
    # def on_input_text_changed(self):
    #     pass
    # 
    # def validate_json_input(self):
    #     pass

    def highlight_json_error(self, error):
        """
        高亮显示JSON错误位置
        """
        try:
            # 保存当前光标位置
            current_cursor = self.input_text.textCursor()
            current_position = current_cursor.position()

            text = self.input_text.toPlainText()
            lines = text.split('\n')

            if error.lineno <= len(lines):
                # 计算错误位置的字符索引
                char_pos = 0
                for i in range(error.lineno - 1):
                    char_pos += len(lines[i]) + 1  # +1 for newline character

                error_char_pos = char_pos + error.colno - 1

                # 创建新的光标用于高亮，不影响用户当前光标位置
                highlight_cursor = self.input_text.textCursor()

                # 选择错误字符或单词
                if error_char_pos < len(text):
                    highlight_cursor.setPosition(error_char_pos)
                    highlight_cursor.setPosition(min(error_char_pos + 1, len(text)), QTextCursor.KeepAnchor)

                    # 应用错误格式
                    highlight_cursor.setCharFormat(self.json_error_format)

                    # 恢复用户原来的光标位置
                    current_cursor.setPosition(current_position)
                    self.input_text.setTextCursor(current_cursor)
        except Exception:
            # 如果高亮失败，不影响程序运行
            pass

    def clear_json_error_highlighting(self):
        """
        清除JSON错误高亮
        """
        try:
            # 保存当前光标位置
            current_cursor = self.input_text.textCursor()
            current_position = current_cursor.position()

            # 创建新光标用于清除格式
            clear_cursor = self.input_text.textCursor()
            clear_cursor.select(QTextCursor.Document)
            clear_cursor.setCharFormat(self.json_normal_format)
            clear_cursor.clearSelection()

            # 恢复用户原来的光标位置
            current_cursor.setPosition(current_position)
            self.input_text.setTextCursor(current_cursor)
        except Exception:
            # 如果清除失败，不影响程序运行
            pass


class EmbeddedSearchWidget(QWidget):
    """
    嵌入式搜索组件
    """

    def __init__(self, target_widget, parent):
        super().__init__(parent)
        self.target_widget = target_widget
        self.parent_window = parent
        self.last_position = 0
        self.init_ui()

    def init_ui(self):
        """
        初始化嵌入式搜索界面
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        self.search_input.returnPressed.connect(self.find_next)
        layout.addWidget(self.search_input)

        # 选项
        self.case_sensitive = QCheckBox("Aa")
        self.case_sensitive.setToolTip("区分大小写")
        self.case_sensitive.setMaximumWidth(40)
        layout.addWidget(self.case_sensitive)

        self.whole_word = QCheckBox("W")
        self.whole_word.setToolTip("全字匹配")
        self.whole_word.setMaximumWidth(30)
        layout.addWidget(self.whole_word)

        # 按钮
        self.find_prev_btn = QPushButton("↑")
        self.find_prev_btn.setMaximumWidth(30)
        self.find_prev_btn.setToolTip("查找上一个")
        self.find_prev_btn.clicked.connect(self.find_previous)
        layout.addWidget(self.find_prev_btn)

        self.find_next_btn = QPushButton("↓")
        self.find_next_btn.setMaximumWidth(30)
        self.find_next_btn.setToolTip("查找下一个")
        self.find_next_btn.clicked.connect(self.find_next)
        layout.addWidget(self.find_next_btn)

        self.close_btn = QPushButton("×")
        self.close_btn.setMaximumWidth(30)
        self.close_btn.setToolTip("关闭搜索")
        self.close_btn.clicked.connect(self.hide)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

        # 设置样式
        self.setStyleSheet("""
            EmbeddedSearchWidget {
                background-color: #f0f0f0;
                border-bottom: 1px solid #ccc;
            }
            QLineEdit {
                padding: 3px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 3px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QCheckBox {
                font-size: 12px;
            }
        """)

        # 默认隐藏
        self.hide()

    def focus_search_input(self):
        """
        聚焦到搜索输入框
        """
        self.search_input.setFocus()
        self.search_input.selectAll()

    def on_search_text_changed(self):
        """
        搜索文本改变时重置搜索位置
        """
        self.last_position = 0

    def find_next(self):
        """
        查找下一个匹配项
        """
        search_text = self.search_input.text()
        if not search_text:
            return

        self._find_text(search_text, forward=True)

    def find_previous(self):
        """
        查找上一个匹配项
        """
        search_text = self.search_input.text()
        if not search_text:
            return

        self._find_text(search_text, forward=False)

    def _find_text(self, search_text, forward=True):
        """
        在文本中查找指定内容
        """
        if not self.target_widget:
            return

        document = self.target_widget.document()
        cursor = self.target_widget.textCursor()

        # 设置搜索选项
        flags = 0
        if not forward:
            flags |= QTextDocument.FindBackward
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_word.isChecked():
            flags |= QTextDocument.FindWholeWords

        # 从当前位置开始搜索
        if forward:
            start_cursor = cursor
        else:
            start_cursor = cursor
            start_cursor.setPosition(cursor.selectionStart())

        found_cursor = document.find(search_text, start_cursor, QTextDocument.FindFlags(flags))

        if found_cursor.isNull():
            # 如果没找到，从文档开头/结尾重新搜索
            if forward:
                start_position = 0
            else:
                start_position = document.characterCount() - 1
            start_cursor = QTextCursor(document)
            start_cursor.setPosition(start_position)
            found_cursor = document.find(search_text, start_cursor, QTextDocument.FindFlags(flags))

        if not found_cursor.isNull():
            # 找到了，设置红色高亮显示
            self.target_widget.setTextCursor(found_cursor)

            # 设置选中文本的现代化高亮样式
            format = QTextCharFormat()
            format.setBackground(QColor(52, 152, 219))  # 现代蓝色背景
            format.setForeground(QColor(255, 255, 255))  # 白色文字
            format.setFontWeight(QFont.Bold)  # 加粗字体
            found_cursor.setCharFormat(format)

            self.parent_window.status_bar.showMessage(f"找到匹配项", 2000)
        else:
            self.parent_window.status_bar.showMessage(f"未找到 '{search_text}'", 2000)


class EmbeddedReplaceWidget(QWidget):
    """
    嵌入式搜索替换组件
    """

    def __init__(self, target_widget, parent):
        super().__init__(parent)
        self.target_widget = target_widget
        self.parent_window = parent
        self.last_position = 0
        self.init_ui()

    def init_ui(self):
        """
        初始化嵌入式搜索替换界面
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)

        # 第一行：搜索输入框和选项
        search_layout = QHBoxLayout()
        search_layout.setSpacing(5)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        self.search_input.returnPressed.connect(self.find_next)
        search_layout.addWidget(self.search_input)

        # 选项
        self.case_sensitive = QCheckBox("Aa")
        self.case_sensitive.setToolTip("区分大小写")
        self.case_sensitive.setMaximumWidth(40)
        search_layout.addWidget(self.case_sensitive)

        self.whole_word = QCheckBox("W")
        self.whole_word.setToolTip("全字匹配")
        self.whole_word.setMaximumWidth(30)
        search_layout.addWidget(self.whole_word)

        # 按钮
        self.find_prev_btn = QPushButton("↑")
        self.find_prev_btn.setMaximumWidth(30)
        self.find_prev_btn.setToolTip("查找上一个")
        self.find_prev_btn.clicked.connect(self.find_previous)
        search_layout.addWidget(self.find_prev_btn)

        self.find_next_btn = QPushButton("↓")
        self.find_next_btn.setMaximumWidth(30)
        self.find_next_btn.setToolTip("查找下一个")
        self.find_next_btn.clicked.connect(self.find_next)
        search_layout.addWidget(self.find_next_btn)

        self.close_btn = QPushButton("×")
        self.close_btn.setMaximumWidth(30)
        self.close_btn.setToolTip("关闭搜索")
        self.close_btn.clicked.connect(self.hide)
        search_layout.addWidget(self.close_btn)

        layout.addLayout(search_layout)

        # 第二行：替换输入框和按钮
        replace_layout = QHBoxLayout()
        replace_layout.setSpacing(5)

        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("替换为...")
        replace_layout.addWidget(self.replace_input)

        self.replace_btn = QPushButton("替换")
        self.replace_btn.setMaximumWidth(60)
        self.replace_btn.clicked.connect(self.replace_current)
        replace_layout.addWidget(self.replace_btn)

        self.replace_all_btn = QPushButton("全部")
        self.replace_all_btn.setMaximumWidth(60)
        self.replace_all_btn.clicked.connect(self.replace_all)
        replace_layout.addWidget(self.replace_all_btn)

        layout.addLayout(replace_layout)

        self.setLayout(layout)

        # 设置样式
        self.setStyleSheet("""
            EmbeddedReplaceWidget {
                background-color: #f0f0f0;
                border-bottom: 1px solid #ccc;
            }
            QLineEdit {
                padding: 3px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 3px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QCheckBox {
                font-size: 12px;
            }
        """)

        # 默认隐藏
        self.hide()

    def focus_search_input(self):
        """
        聚焦到搜索输入框
        """
        self.search_input.setFocus()
        self.search_input.selectAll()

    def on_search_text_changed(self):
        """
        搜索文本改变时重置搜索位置
        """
        self.last_position = 0

    def find_next(self):
        """
        查找下一个匹配项
        """
        search_text = self.search_input.text()
        if not search_text:
            return

        self._find_text(search_text, forward=True)

    def find_previous(self):
        """
        查找上一个匹配项
        """
        search_text = self.search_input.text()
        if not search_text:
            return

        self._find_text(search_text, forward=False)

    def _find_text(self, search_text, forward=True):
        """
        在文本中查找指定内容
        """
        if not self.target_widget:
            return

        document = self.target_widget.document()
        cursor = self.target_widget.textCursor()

        # 设置搜索选项
        flags = 0
        if not forward:
            flags |= QTextDocument.FindBackward
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_word.isChecked():
            flags |= QTextDocument.FindWholeWords

        # 从当前位置开始搜索 - 修复参数类型
        found_cursor = document.find(search_text, cursor, QTextDocument.FindFlags(flags))

        if found_cursor.isNull():
            # 如果没找到，从文档开头/结尾重新搜索（循环搜索）
            if forward:
                start_position = 0
            else:
                start_position = document.characterCount() - 1
            start_cursor = QTextCursor(document)
            start_cursor.setPosition(start_position)
            found_cursor = document.find(search_text, start_cursor, QTextDocument.FindFlags(flags))

        if not found_cursor.isNull():
            # 找到了，设置红色字体和加深背景高亮显示
            self.target_widget.setTextCursor(found_cursor)

            # 设置选中文本的现代化高亮样式
            format = QTextCharFormat()
            format.setBackground(QColor(52, 152, 219))  # 现代蓝色背景
            format.setForeground(QColor(255, 255, 255))  # 白色文字
            format.setFontWeight(QFont.Bold)  # 加粗字体
            found_cursor.setCharFormat(format)

            self.parent_window.status_bar.showMessage(f"找到匹配项", 2000)
            return True
        else:
            self.parent_window.status_bar.showMessage(f"未找到 '{search_text}'", 2000)
            return False

    def replace_current(self):
        """
        替换当前选中的文本
        """
        if not self.target_widget or self.target_widget.isReadOnly():
            return

        search_text = self.search_input.text()
        replace_text = self.replace_input.text()

        if not search_text:
            return

        cursor = self.target_widget.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            # 检查选中的文本是否匹配搜索文本（简化匹配逻辑）
            match = False
            if self.case_sensitive.isChecked():
                match = (selected_text == search_text)
            else:
                match = (selected_text.lower() == search_text.lower())

            if match:
                cursor.insertText(replace_text)
                self.parent_window.status_bar.showMessage("已替换一处", 2000)
                # 查找下一个
                self.find_next()
            else:
                # 如果当前选中的不匹配，先查找
                self.find_next()
        else:
            # 如果没有选中文本，先查找
            self.find_next()

    def replace_all(self):
        """
        替换所有匹配项
        """
        if not self.target_widget or self.target_widget.isReadOnly():
            return

        search_text = self.search_input.text()
        replace_text = self.replace_input.text()

        if not search_text:
            return

        # 确认对话框
        reply = QMessageBox.question(self, "确认替换",
                                     f"确定要将所有 '{search_text}' 替换为 '{replace_text}' 吗？",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply != QMessageBox.Yes:
            return

        document = self.target_widget.document()
        cursor = QTextCursor(document)
        cursor.movePosition(QTextCursor.Start)

        # 设置搜索选项
        flags = 0
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_word.isChecked():
            flags |= QTextDocument.FindWholeWords

        replace_count = 0

        # 开始替换
        cursor.beginEditBlock()
        try:
            while True:
                found_cursor = document.find(search_text, cursor, QTextDocument.FindFlags(flags))
                if found_cursor.isNull():
                    break

                found_cursor.insertText(replace_text)
                replace_count += 1
                cursor = found_cursor
        finally:
            cursor.endEditBlock()

        self.parent_window.status_bar.showMessage(f"已替换 {replace_count} 处", 3000)

    def _text_matches(self, text1, text2):
        """
        检查两个文本是否匹配（考虑大小写敏感和全字匹配选项）
        """
        # 处理大小写敏感
        if not self.case_sensitive.isChecked():
            text1 = text1.lower()
            text2 = text2.lower()

        # 处理全字匹配
        if self.whole_word.isChecked():
            # 简单的全字匹配检查
            import re
            pattern = r'\b' + re.escape(text2) + r'\b'
            return bool(re.search(pattern, text1, re.IGNORECASE if not self.case_sensitive.isChecked() else 0))
        else:
            return text1 == text2


def main():
    """
    主函数
    """
    # 创建应用程序
    app = QApplication(sys.argv)

    # 设置应用程序属性
    app.setApplicationName('JSON 格式化工具')
    app.setApplicationVersion('1.0')
    app.setOrganizationName('wangjunqi')

    # 创建主窗口
    window = JSONFormatterApp()
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
