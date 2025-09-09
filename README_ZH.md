# 🔹 离线 JSON 格式化工具

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

一个功能强大的离线 JSON 格式化桌面应用程序，基于 Python + PyQt5 开发，提供类似 Postman Beautify 的功能，并支持 JSON
排序、压缩、验证等扩展功能。

## 🌟 特色功能

- 🚀 **完全离线**：无需网络连接，保护数据隐私
- 🎨 **现代化界面**：美观的 GUI 设计，支持搜索和替换功能
- ⚡ **高性能处理**：基于 PyQt5，响应迅速
- 🔧 **多种格式化选项**：美化、排序、压缩、验证一应俱全
- 📋 **便捷操作**：一键复制、清空，支持快捷键
- 🎯 **精准搜索**：支持大小写敏感、全字匹配的搜索替换
- 🌳 **树形视图**：可展开/折叠的JSON结构树，直观显示层级关系
- 🔄 **双视图模式**：文本视图和树形视图实时同步，满足不同使用需求

## 📋 需求文档总结

### 🎯 软件目标

开发一个**离线 JSON 格式化工具**，功能类似 **Postman 的 Beautify 功能**，并额外提供 JSON 排序功能。

### 📌 核心功能

1. **输入输出界面**
    - 左侧：JSON 输入区（多行文本框，可编辑）
    - 右侧：JSON 输出区（多行文本框，只读）
    - 等宽字体显示（Consolas）
    - 支持自动换行和滚动条

2. **功能按钮**
    - **🎨 Beautify**：格式化 JSON（缩进 4 空格）
    - **🔤 Sort**：按 JSON key 字母顺序排序并美化
    - **📦 Minify**：压缩 JSON 为单行（扩展功能）
    - **✅ Validate**：验证 JSON 格式合法性（扩展功能）
    - **📋 Copy**：复制输出结果到剪贴板
    - **📂 展开全部**：展开树形视图中的所有节点
    - **📁 折叠全部**：折叠树形视图中的所有节点
    - **🗑️ Clear**：清空输入和输出内容

3. **双视图显示**
    - **文本视图**：传统的文本格式显示，支持搜索和替换
    - **树形视图**：可交互的JSON结构树，支持节点展开/折叠
    - **选项卡切换**：在两种视图间自由切换，实时同步数据

3. **错误处理**
    - 输入非法 JSON 时弹窗提示
    - 程序不会因错误而中断
    - 详细的错误信息显示

## 🚀 功能特性

- ✅ **离线运行**：无需网络连接，完全本地处理
- ✅ **美观界面**：现代化 GUI 设计，支持深浅色主题
- ✅ **高性能**：基于 PyQt5，响应迅速
- ✅ **跨平台**：支持 Windows 7/10/11/Server
- ✅ **易用性**：直观的操作界面，一键格式化
- ✅ **扩展功能**：除基本格式化外，还支持排序、压缩、验证

## 📦 安装说明

### 环境要求

- **Python 版本**：3.12.3（推荐）或 Python 3.8+
- **操作系统**：Windows 7/10/11/Windows Server
- **内存**：建议 2GB 以上

### 方式一：直接运行源码

1. **克隆或下载项目**
   ```bash
   git clone <项目地址>
   cd OfflineFormat
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python main.py
   ```

### 方式二：使用打包后的 EXE（推荐）

1. 下载 `dist/main.exe`
2. 双击运行即可，无需安装 Python 环境

## 🛠️ 打包说明

### 打包为 EXE 文件

#### 方式一：标准打包（36MB）

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="JSON格式化工具" main.py
```

#### 方式二：优化打包（15-20MB）

```bash
# 使用优化脚本
build_optimized.bat
```

#### 方式三：极致优化（8-15MB）

```bash
# 使用 spec 配置文件
build_small.bat
```

#### 进一步压缩（可选）

1. **安装 UPX 压缩工具**
    - 下载：https://github.com/upx/upx/releases
    - 解压到系统 PATH 或项目目录

2. **手动压缩**
   ```bash
   upx --ultra-brute "dist\JSON格式化工具.exe"
   ```

#### 体积对比

- **标准打包**：~36MB
- **优化打包**：~15-20MB（减小 45%）
- **极致优化**：~8-15MB（减小 60-80%）
- **UPX 压缩后**：~5-10MB（额外减小 30%）

#### 打包参数说明

- `--onefile`：单文件打包
- `--windowed`：隐藏控制台
- `--exclude-module`：排除不需要的模块
- `--strip`：剥离调试符号
- `--optimize=2`：最高级别代码优化
- `--upx`：启用 UPX 压缩（需安装 UPX）

## 📖 使用方法

### 基本操作

1. **启动程序**
    - 双击 `main.exe` 或运行 `python main.py`

2. **输入 JSON**
    - 在左侧文本框中输入或粘贴需要格式化的 JSON 数据

3. **选择操作**
    - **Beautify**：美化格式，添加缩进和换行
    - **Sort**：按键名排序后美化
    - **Minify**：压缩为单行
    - **Validate**：仅验证格式，不修改内容

4. **查看结果**
    - 处理后的 JSON 显示在右侧文本框
    - 使用 Copy 按钮复制结果

### 示例操作

**输入 JSON：**

```json
{"name":"张三","age":25,"city":"北京","skills":["Python","JavaScript"]}
```

**Beautify 后：**

```json
{
    "name": "张三",
    "age": 25,
    "city": "北京",
    "skills": [
        "Python",
        "JavaScript"
    ]
}
```

**Sort 后：**

```json
{
    "age": 25,
    "city": "北京",
    "name": "张三",
    "skills": [
        "Python",
        "JavaScript"
    ]
}
```

## 🔧 技术架构

### 技术栈

- **语言**：Python 3.12.3
- **GUI 框架**：PyQt5 5.15.10
- **JSON 处理**：Python 标准库 `json`
- **打包工具**：PyInstaller 6.3.0

### 项目结构

```
OfflineFormat/
├── main.py              # 主程序文件
├── requirements.txt     # 依赖包列表
├── README.md           # 说明文档
├── .trae/
│   └── rules/
│       └── project_rules.md  # 项目规则
└── dist/               # 打包输出目录（生成后）
    └── main.exe        # 可执行文件
```

### 核心类说明

- **JSONFormatterApp**：主窗口类，继承自 QMainWindow
    - `init_ui()`：初始化用户界面
    - `create_text_area()`：创建文本输入输出区域
    - `create_button_area()`：创建功能按钮区域
    - `beautify_json()`：JSON 美化功能
    - `sort_json()`：JSON 排序功能
    - `minify_json()`：JSON 压缩功能
    - `validate_json()`：JSON 验证功能
    - `copy_output()`：复制到剪贴板功能
    - `clear_all()`：清空内容功能

## 🐛 常见问题

### Q1: 程序无法启动

**A**: 检查是否安装了 PyQt5，运行 `pip install PyQt5`

### Q2: JSON 格式化失败

**A**: 确保输入的是合法的 JSON 格式，程序会显示具体的错误信息

### Q3: 打包后的 EXE 文件过大

**A**: 这是正常现象，因为包含了 Python 运行时和 PyQt5 库

### Q4: 在 Windows 7 上运行报错

**A**: 确保系统已安装 Visual C++ Redistributable

## 📝 更新日志

### v1.3 (2025-01-XX)

- 🌳 **新增JSON树形视图**：实现可展开/折叠的JSON结构树显示
- 🔄 **双视图模式**：添加文本视图和树形视图选项卡，支持实时切换
- 📂 **树形操作**：新增"展开全部"和"折叠全部"按钮，便于快速操作
- 🎨 **视觉优化**：树形视图支持交替行颜色、现代化样式设计
- ⚡ **性能提升**：优化大型JSON数据的树形显示性能

### v1.2 (2025-01-XX)

- 🔍 **新增搜索替换功能**：支持嵌入式搜索框，现代化蓝色高亮显示
- 🎨 **界面优化**：改进搜索匹配文字的高亮样式，使用蓝色背景+白色文字+加粗效果
- 🐛 **修复问题**：解决 QTextDocument.find 参数类型错误
- ⚙️ **功能增强**：支持循环搜索、大小写敏感、全字匹配等选项

### v1.1 (2024-12-XX)

- 🔧 **功能扩展**：添加字体大小调节功能
- 📱 **界面改进**：优化布局和用户体验
- 🎯 **错误处理**：增强 JSON 验证和错误提示

### v1.0 (2024-01-XX)

- ✅ 实现基本的 JSON 格式化功能
- ✅ 添加 JSON 排序功能
- ✅ 实现复制到剪贴板功能
- ✅ 添加清空功能和错误处理
- ✅ 扩展功能：Minify 和 Validate
- ✅ 美观的 GUI 界面设计
- ✅ 完整的打包和分发方案

## 📄 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

### 开发环境设置

```bash
git clone https://github.com/your-username/offline-json-formatter.git
cd offline-json-formatter
pip install -r requirements.txt
python main.py
```

## 👨‍💻 开发者

- **作者**：wangjunqi
- **当前版本**：1.2
- **开发时间**：2024-2025

## ⭐ 支持项目

如果这个项目对您有帮助，请给它一个 ⭐ Star！

---

**🎉 感谢使用离线 JSON 格式化工具！如有问题或建议，欢迎反馈。**