@echo off
chcp 65001 >nul
echo ========================================
echo     JSON 格式化工具 - 自动打包脚本
echo ========================================
echo.

echo [1/4] 检查 Python 环境...
python --version
if %errorlevel% neq 0 (
    echo 错误：未找到 Python 环境，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/4] 安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误：依赖包安装失败
    pause
    exit /b 1
)

echo.
echo [3/4] 清理旧的打包文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo.
echo [4/4] 开始打包程序...
echo 正在生成单文件 EXE，请稍候...
pyinstaller --onefile --windowed --name="JSON格式化工具" --distpath="dist" main.py

if %errorlevel% eq 0 (
    echo.
    echo ========================================
    echo          打包完成！
    echo ========================================
    echo 生成的文件位置：dist\JSON格式化工具.exe
    echo 文件大小：
    dir "dist\JSON格式化工具.exe" | findstr "JSON格式化工具.exe"
    echo.
    echo 您可以将 EXE 文件分发给其他用户使用
    echo 用户无需安装 Python 环境即可运行
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo          打包失败！
    echo ========================================
    echo 请检查错误信息并重试
    pause
    exit /b 1
)