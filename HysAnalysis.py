"""
HysAnalysis - Force-Displacement Hysteresis Curve Analysis Tool
================================================================

A Python application for analyzing force-displacement hysteresis curves,
extracting skeleton curves, and calculating various mechanical performance indices.

GitHub Repository: https://github.com/GarGarfie/HysAnalysis
License: MIT (or your chosen license)
Author: GarGarfie
Version: 1.0.0

For bug reports, feature requests, and contributions, please visit:
https://github.com/GarGarfie/HysAnalysis/issues
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

# PySide6 imports
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QRadioButton, QCheckBox,
    QGroupBox, QSplitter, QTabWidget, QTextEdit, QFileDialog,
    QMessageBox, QButtonGroup, QDoubleSpinBox, QSlider, QComboBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QScreen, QIcon
import webbrowser

# Matplotlib imports
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

# Scipy for interpolation
from scipy.interpolate import (
    make_interp_spline, UnivariateSpline, 
    PchipInterpolator, Akima1DInterpolator,
    BSpline, splrep
)
from scipy.signal import savgol_filter

# 配置 matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10


class MplCanvas(FigureCanvasQTAgg):
    """自定义 Matplotlib 画布，支持鼠标滚轮缩放"""
    
    def __init__(self, parent=None, width=12, height=9, dpi=100):
        self.analyzer = parent
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
        # 初始化图形
        self.ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, which='both')
        self.ax.minorticks_on()
        self.ax.grid(True, which='minor', alpha=0.15, linestyle=':', linewidth=0.3)
        self.update_labels()
        
        # 连接滚轮事件
        self.mpl_connect('scroll_event', self.on_scroll)
        
        # 记录初始视图范围
        self.original_xlim = None
        self.original_ylim = None
    
    def update_labels(self):
        if self.analyzer:
            self.ax.set_xlabel(self.analyzer.tr('Displacement (mm)'), 
                             fontsize=11, fontweight='bold')
            self.ax.set_ylabel(self.analyzer.tr('Force (N)'), 
                             fontsize=11, fontweight='bold')
            self.ax.set_title(self.analyzer.tr('Force-Displacement Hysteresis Curve'),
                            fontsize=13, fontweight='bold')
        
    def on_scroll(self, event):
        """鼠标滚轮缩放"""
        if event.inaxes != self.ax:
            return
        
        # 获取当前坐标范围
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        
        # 获取鼠标位置
        xdata = event.xdata
        ydata = event.ydata
        
        # 缩放因子
        if event.button == 'up':
            scale_factor = 0.9  # 放大
        elif event.button == 'down':
            scale_factor = 1.1  # 缩小
        else:
            return
        
        # 计算新的范围（以鼠标位置为中心缩放）
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
        
        self.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        self.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        
        self.draw()


class HysteresisAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        # 语言支持
        self.current_language = 'en'  # 默认英语
        self.translations = {
            'en': {
                'language': 'Language',
                'window_title': 'Force-Displacement Curve Analysis',
                'File Management': 'File Management',
                'Import': 'Import',
                'Clear': 'Clear',
                'Keyboard shortcut: Delete': 'Keyboard shortcut: "Delete" - Delete selected file',
                'Plot Style': 'Plot Style',
                'Dot-Line Graph': 'Dot-Line Graph',
                'Spline Connected Graph': 'Spline Connected Graph',
                'Skeleton curve extraction method': 'Skeleton curve extraction method',
                'Method 1: Outer Envelope': 'Method 1: Outer Envelope',
                'Method 2: Peak Points': 'Method 2: Peak Points',
                'Skeleton curve analysis direction': 'Skeleton curve analysis direction',
                'All directions': 'All directions',
                'Positive direction only': 'Positive direction only',
                'Negative direction only': 'Negative direction only',
                'Ductility coefficient calculation method': 'Ductility coefficient calculation method',
                'geometric': 'Geometric Method',
                'energy': 'Energy Method',
                'park': 'Park Method',
                'farthest': 'Farthest Point',
                'asce': 'ASCE Method',
                'eeep': 'EEEP Method',
                'elastic_yield': 'Elastic Yield',
                'Data filtering options': 'Data filtering options',
                'Only retain the first loop of the same displacement level': 'Only retain the first loop of the same displacement level',
                'language': 'Language',
                'Smoothness parameter': 'Smoothness parameter',
                'Preset': 'Preset',
                'Show original data points': 'Show original data points',
                'Number of interpolation points': 'Number of interpolation points',
                'Smoothing algorithm': 'Smoothing algorithm:',
                'PCHIP - Shape-preserving interpolation (no overshoot)': 'PCHIP - Shape-preserving interpolation (no overshoot)',
                'Akima - Akima interpolation (naturally smooth)': 'Akima - Akima interpolation (naturally smooth)',
                'Bezier - Bézier curve (ultra smooth)': 'Bezier - Bézier curve (ultra smooth)',
                'BSpline - B-spline (super smooth)': 'BSpline - B-spline (super smooth)',
                'SG filter - Savitzky-Golay filter (feature-preserving)': 'SG filter - Savitzky-Golay filter (feature-preserving)',
                'UnivariateSpline - General-purpose spline (adjustable smoothness)': 'UnivariateSpline - General-purpose spline (adjustable smoothness)',
                'CubicSpline - Cubic spline (exactly passes through points)': 'CubicSpline - Cubic spline (exactly passes through points)',
                'Control point density (%)': 'Control point density (%)',
                'Value': 'Value',
                'Adjustment': 'Adjustment',
                'Current value': 'Current value',
                'Current value {}': 'Current value {}',
                'Current value {:.2f}': 'Current value {:.2f}',
                'None': 'None',
                'Low': 'Low',
                'Medium': 'Medium',
                'High': 'High',
                'Very high': 'Very high',
                'Shape‑preserving piecewise cubic interpolation. Preserves data monotonicity and avoids overshoot and oscillations. Suitable for preserving data trends.': 'Shape‑preserving piecewise cubic interpolation. Preserves data monotonicity and avoids overshoot and oscillations. Suitable for preserving data trends.',
                'Akima interpolation method. Reduces oscillations in the curve and is more natural than cubic splines. Suitable for scenarios where you want to reduce fluctuations.': 'Akima interpolation method. Reduces oscillations in the curve and is more natural than cubic splines. Suitable for scenarios where you want to reduce fluctuations.',
                'Bézier curve. Generates an extremely smooth curve, suitable for presentation/visualization. The parameter controls control‑point density: 10% = smoothest, 100% = closest to the original data. Recommended 20–40%.': 'Bézier curve. Generates an extremely smooth curve, suitable for presentation/visualization. The parameter controls control‑point density: 10% = smoothest, 100% = closest to the original data. Recommended 20–40%.',
                'B‑spline interpolation. Produces a very smooth curve, but may deviate from the original data points. The parameter s controls the smoothness.': 'B‑spline interpolation. Produces a very smooth curve, but may deviate from the original data points. The parameter s controls the smoothness.',
                'Savitzky–Golay filtering. Smooths the data while preserving its features (such as peaks). The parameter is the window size.': 'Savitzky–Golay filtering. Smooths the data while preserving its features (such as peaks). The parameter is the window size.',
                'General‑purpose spline interpolation with adjustable smoothness. The parameter s controls the level of smoothing: s = 0 forces the spline to pass exactly through the points; the larger s is, the smoother the curve. Suitable for most cases.': 'General‑purpose spline interpolation with adjustable smoothness. The parameter s controls the level of smoothing: s = 0 forces the spline to pass exactly through the points; the larger s is, the smoother the curve. Suitable for most cases.',
                'Cubic spline interpolation that passes exactly through all data points. The resulting curve has a continuous second derivative at the knots.': 'Cubic spline interpolation that passes exactly through all data points. The resulting curve has a continuous second derivative at the knots.',
                'Smoothing interpolation failed': 'Smoothing interpolation failed',            
                'Failed to generate Bézier curve': 'Failed to generate Bézier curve',
                'Smoothing failed': 'Smoothing failed',
                'Displacement (mm)': 'Displacement (mm)',
                'Force (N)': 'Force (N)',
                'Force-Displacement Hysteresis Curve': 'Force-Displacement Hysteresis Curve',
                'Hysteresis Curve': 'Hysteresis Curve',
                'Positive Skeleton Curve': 'Positive Skeleton Curve',
                'Negative Skeleton Curve': 'Negative Skeleton Curve',
                'Skeleton Data Points': 'Skeleton Data Points',
                'Positive Skeleton Curve Start Point': 'Positive Curve Start Point',
                'Negative Skeleton Curve Start Point': 'Negative Skeleton Curve Start Point',
                'Positive Peak': 'Positive Peak',
                'Negative Peak': 'Negative Peak',
                'Filtered Label': '[Filtered Label]',
                'Smooth Label': '[Smooth Label]',
                'Hysteresis curve and backbone curve': 'Hysteresis curve and backbone curve',
                'Evaluation metrics and analysis results': 'Evaluation metrics and analysis results',
                'Detailed information on hysteresis loops': 'Detailed information on hysteresis loops',
                'No analysis results': 'No analysis results',
                'Force-Displacement Curve Analysis Report': 'Force-Displacement Curve Analysis Report',
                'Select force-displacement data files (multiple selections possible)': 'Select force-displacement data files (multiple selections possible)',
                'All supported formats (*.txt *.csv *.xls *.xlsx); text files (*.txt); CSV files (*.csv); Excel files (*.xls *.xlsx); all files (*.*)': 'All supported formats (*.txt *.csv *.xls *.xlsx); text files (*.txt); CSV files (*.csv); Excel files (*.xls *.xlsx); all files (*.*)',
                'Successfully imported {} files': 'Successfully imported {} files',
                'Success': 'Success',
                'Confirm': 'Confirm',
                'Are you sure you want to clear all files?': 'Are you sure you want to clear all files?',
                'Error': 'Error',
                'Unsported file format: {}': 'Unsported file format: {}',
                'Incorrect data format! The file must contain at least 2 columns:\nColumn 1 - Displacement\nColumn 2 - Force': 'Incorrect data format! The file must contain at least 2 columns:\nColumn 1 - Displacement\nColumn 2 - Force',
                'Fail to read file:\n{}': 'Fail to read file:\n{}',
                'Deleted': 'Deleted',
                'Deleted {} files': 'Deleted {} files',
                'Open Source Project | Contributions Welcome': 'Open Source Project | Contributions Welcome',
                
                 # 分析结果页面翻译
                'File Information': 'File Information',
                'File name': 'File name',
                'Number of data points': 'Number of data points',
                'Number of hysteresis loops': 'Number of hysteresis loops',
                'Enabled (Only retain the first loop of the same displacement level)': 'Enabled (Only retain the first loop of the same displacement level)',
                'Skeleton Curve Starting Points': 'Skeleton Curve Starting Points',
                'Note: Common starting point crossing y-axis between first negative peak and second positive peak': 'Note: Common starting point crossing y-axis between first negative peak and second positive peak',
                'Evaluation Metrics': 'Evaluation Metrics',
                'Displacement-related': 'Displacement-related',
                'Mechanical properties': 'Mechanical properties',
                'Energy metrics': 'Energy metrics',
                'Coefficient metrics': 'Coefficient metrics',
                'Degradation metrics': 'Degradation metrics',
                'Ductility coefficient': 'Ductility coefficient',
    
                # 指标名称
                'Peak displacement': 'Peak displacement',
                'Residual deformation (mm)': 'Residual deformation (mm)',
                'Peak load': 'Peak load',
                'Initial stiffness (N/mm)': 'Initial stiffness (N/mm)',
                'Secant stiffness (N/mm)': 'Secant stiffness (N/mm)',
                'Total hysteresis loop area (kN·mm)': 'Total hysteresis loop area (kN·mm)',
                'Cumulative energy dissipation (kN·mm)': 'Cumulative energy dissipation (kN·mm)',
                'Average loop energy (kN·mm)': 'Average loop energy (kN·mm)',
                'Maximum loop energy (kN·mm)': 'Maximum loop energy (kN·mm)',
                'Equivalent viscous damping coefficient': 'Equivalent viscous damping coefficient',
                'Positive strength degradation (%)': 'Positive strength degradation (%)',
                'Negative strength degradation (%)': 'Negative strength degradation (%)',
                'Stiffness degradation (%)': 'Stiffness degradation (%)',
                'Positive (mm)': 'Positive (mm)',
                'Negative (mm)': 'Negative (mm)',
                'Positive (N)': 'Positive (N)',
                'Negative (N)': 'Negative (N)',
                
                # 滞回环详细信息翻译
                'No hysteresis loop information': 'No hysteresis loop information',
                'Detailed Hysteresis Loop Information': 'Detailed Hysteresis Loop Information',
                'No.': 'No.',
                'Type': 'Type',
                'Peak Disp.': 'Peak Disp.',
                'Peak Force': 'Peak Force',
                'Loop Area': 'Loop Area',
                'Positive': 'Positive',
                'Negative': 'Negative',
                'Statistical Information': 'Statistical Information',
                'Total loops': 'Total loops',
                'Total energy dissipation': 'Total energy dissipation',
                'Average energy dissipation': 'Average energy dissipation',
                'Maximum energy dissipation': 'Maximum energy dissipation',
                'Minimum energy dissipation': 'Minimum energy dissipation',
                'Positive loops': 'Positive loops',
                'Negative loops': 'Negative loops',
                
            },
            
            
            'ru': {
                'language': 'Язык',
                'window_title': 'Анализ кривой сила-перемещение',
                'File Management': 'Управление файлами',
                'Import': 'Импорт',
                'Clear': 'Очистить',
                'Keyboard shortcut: Delete': 'Сочетание клавиш: "Delete" - удалить выбранный файл',
                'Plot Style': 'Стиль графика',
                'Dot-Line Graph': 'Точечный линейный график',
                'Spline Connected Graph': 'Сплайн-связанный график',
                'Skeleton curve extraction method': 'Метод извлечения скелетной кривой',
                'Method 1: Outer Envelope': 'Метод 1: Внешняя огибающая',
                'Method 2: Peak Points': 'Метод 2: Пиковые точки',
                'Skeleton curve analysis direction': 'Skeleton curve analysis direction',
                'All directions': 'Все направления',
                'Positive direction only': 'Только положительное',
                'Negative direction only': 'Только отрицательное',
                'Ductility coefficient calculation method': 'Метод расчета коэффициента пластичности',
                'geometric': 'Геометрический',
                'energy': 'Энергетический',
                'park': 'Метод Парка',
                'farthest': 'Дальняя точка',
                'asce': 'Метод ASCE',
                'eeep': 'Метод EEEP',
                'elastic_yield': 'Упругая текучесть',
                'Data filtering options': 'Фильтр данных',
                'Only retain the first loop of the same displacement level': 'Сохраните только первый круг того же уровня рабочего объема',
                'language': 'Язык',
                'Smoothness parameter': 'Параметр сглаживания:',
                'Show original data points': 'Показать исходные точки',
                'Number of interpolation points': 'Число точек интерполяции:',
                'Smoothing algorithm': 'Алгоритм сглаживания:',
                'Preset': 'Пресет',
                'PCHIP - Shape-preserving interpolation (no overshoot)': 'PCHIP — формосохраняющая интерполяция (без выбросов)',
                'Akima - Akima interpolation (naturally smooth)': 'Akima — интерполяция Акимы (естественное сглаживание)',
                'Bezier - Bézier curve (ultra smooth)': 'Bezier — кривая Безье (максимальная гладкость)',
                'BSpline - B-spline (super smooth)': 'BSpline — B-сплайн (сверхгладкое сглаживание)',
                'SG filter - Savitzky-Golay filter (feature-preserving)': 'SG filter — фильтр Савицкого–Голея (с сохранением особенностей сигнала)',
                'UnivariateSpline - General-purpose spline (adjustable smoothness)': 'UnivariateSpline — универсальный сплайн (настраиваемая степень сглаживания)',
                'CubicSpline - Cubic spline (exactly passes through points)': 'CubicSpline — кубический сплайн (строго проходит через точки)',
                'Control point density (%)': 'Плотность контрольных точек (%):',
                'Value': 'Значение',
                'Adjustment': 'Регулировка',
                'Current value': 'Текущее значение',
                'Current value {}': 'Текущее значение {}',
                'Current value {:.2f}': 'Текущее значение {:.2f}',
                'None': 'Нет',
                'Low': 'Низкий',
                'Medium': 'Средний',
                'High': 'Высокий',
                'Very high': 'Очень высокий',
                'Shape‑preserving piecewise cubic interpolation. Preserves data monotonicity and avoids overshoot and oscillations. Suitable for preserving data trends.': 'Формосохраняющая кусочно‑кубическая интерполяция. Сохраняет монотонность данных и избегает выбросов и колебаний. Подходит для сохранения тренда данных.',
                'Akima interpolation method. Reduces oscillations in the curve and is more natural than cubic splines. Suitable for scenarios where you want to reduce fluctuations.': 'Метод интерполяции Акимы. Уменьшает колебания кривой и даёт более естественный результат, чем кубический сплайн. Подходит для задач, где нужно снизить флуктуации.',
                'Bézier curve. Generates an extremely smooth curve, suitable for presentation/visualization. The parameter controls control‑point density: 10% = smoothest, 100% = closest to the original data. Recommended 20–40%.': 'Кривая Безье. Генерирует предельно гладкую кривую, подходит для наглядного отображения. Параметр задаёт плотность контрольных точек: 10% — максимальная гладкость, 100% — наибольшее соответствие исходным данным. Рекомендуется 20–40%.',
                'B‑spline interpolation. Produces a very smooth curve, but may deviate from the original data points. The parameter s controls the smoothness.': 'Интерполяция B‑сплайном. Даёт очень гладкую кривую, но она может отклоняться от исходных точек данных. Параметр s управляет степенью сглаживания.',
                'Savitzky–Golay filtering. Smooths the data while preserving its features (such as peaks). The parameter is the window size.': 'Фильтрация Савицкого–Голея. Выполняет сглаживание, сохраняя особенности данных (например, пики). Параметр задаёт размер окна.',
                'General‑purpose spline interpolation with adjustable smoothness. The parameter s controls the level of smoothing: s = 0 forces the spline to pass exactly through the points; the larger s is, the smoother the curve. Suitable for most cases.': 'Универсальная сплайн‑интерполяция с настраиваемой степенью сглаживания. Параметр s определяет уровень сглаживания: при s = 0 сплайн строго проходит через точки; чем больше s, тем сильнее сглаживание. Подходит для большинства задач.',
                'Cubic spline interpolation that passes exactly through all data points. The resulting curve has a continuous second derivative at the knots.': 'Кубическая сплайн‑интерполяция, строго проходящая через все точки данных. Получающаяся кривая имеет непрерывную вторую производную в узлах.',
                'Smoothing interpolation failed': 'Сглаживающая интерполяция не удалась',
                'Failed to generate Bézier curve': 'Не удалось сгенерировать кривую Безье',
                'Smoothing failed': 'Сглаживание не удалось',
                'Displacement (mm)': 'Перемещение (мм)',
                'Force (N)': 'Сила (Н)',
                'Force-Displacement Hysteresis Curve': 'Кривая гистерезиса сила-перемещение',
                'Hysteresis Curve': 'Кривая гистерезиса',
                'Positive Skeleton Curve': 'Положительная скелетная кривая',
                'Negative Skeleton Curve': 'Отрицательная скелетная кривая',
                'Skeleton Data Points': 'Точки данных скелета',
                'Positive Skeleton Curve Start Point': 'Положительное начало',
                'Negative Skeleton Curve Start Point': 'Отрицательное начало',
                'Positive Peak': 'Положительный пик',
                'Negative Peak': 'Отрицательный пик',               
                'Filtered Label': 'Отфильтровано',
                'Smooth Label': 'Сглаживание',                
                'Hysteresis curve and backbone curve': 'Гистерезисная кривая и скелетная (огибающая) кривая',
                'Evaluation metrics and analysis results': 'Показатели оценки и результаты анализа',
                'Detailed information on hysteresis loops': 'Подробная информация о петлях гистерезиса',                
                'No analysis results': 'Результаты анализа отсутствуют.',
                'Force-Displacement Curve Analysis Report': 'Отчет по анализу кривой «сила-смещение»',
                'Select force-displacement data files (multiple selections possible)': 'Выберите файлы данных «сила-смещение» (возможен выбор нескольких вариантов)',
                'All supported formats (*.txt *.csv *.xls *.xlsx); text files (*.txt); CSV files (*.csv); Excel files (*.xls *.xlsx); all files (*.*)': 'Все поддерживаемые форматы (*.txt *.csv *.xls *.xlsx); текстовые файлы (*.txt); файлы CSV (*.csv); файлы Excel (*.xls *.xlsx); все файлы (*.*)',
                'Successfully imported {} files': 'Успешно импортировано {} файлов.',
                'Success': 'Успех',
                'Confirm': 'Потвердить',
                'Are you sure you want to clear all files?': 'Очистить все файлы?',
                'Error': 'Ошибка',
                'Unsported file format: {}': 'Неподдерживаемый формат файла: {}',
                'Incorrect data format! The file must contain at least 2 columns:\nColumn 1 - Displacement\nColumn 2 - Force': 'Неверный формат данных! Файл должен содержать как минимум два столбца данных: \nСтолбец 1 - Перемещение \nСтолбец 2 - Сила',
                'Fail to read file:\n{}': 'Не удалось прочитать файл: \n{}',
                'Deleted': 'Удалено',
                'Deleted {} files': 'Удалено {} файлов',
                'Open Source Project | Contributions Welcome': 'Проект с открытым исходным кодом | Приветствуются вклады',
                
                # Перевод страницы результатов анализа
                'File Information': 'Информация о файле',
                'File name': 'Имя файла',
                'Number of data points': 'Количество точек данных',
                'Number of hysteresis loops': 'Количество петель гистерезиса',
                'Enabled (Only retain the first loop of the same displacement level)': 'Включено (сохранять только первую петлю для одного и того же уровня перемещения)',
                'Skeleton Curve Starting Points': 'Начальные точки скелетной кривой',
                'Note: Common starting point crossing y-axis between first negative peak and second positive peak': 'Примечание: типичная начальная точка — пересечение с осью Y между первым отрицательным пиком и вторым положительным пиком',
                'Evaluation Metrics': 'Оценочные показатели',
                'Displacement-related': 'Показатели, связанные с перемещением',
                'Mechanical properties': 'Механические характеристики',
                'Energy metrics': 'Энергетические показатели',
                'Coefficient metrics': 'Коэффициентные показатели',
                'Degradation metrics': 'Показатели деградации',
                'Ductility coefficient': 'Коэффициент пластичности',

                # Названия показателей
                'Peak displacement': 'Пиковое перемещение',
                'Residual deformation (mm)': 'Остаточная деформация (мм)',
                'Peak load': 'Пиковая нагрузка',
                'Initial stiffness (N/mm)': 'Начальная жёсткость (Н/мм)',
                'Secant stiffness (k/mm)': 'Секущая жёсткость (Н/мм)',
                'Total hysteresis loop area (kN·mm)': 'Общая площадь петель гистерезиса (кН·мм)',
                'Cumulative energy dissipation (kN·mm)': 'Суммарное рассеяние энергии (кН·мм)',
                'Average loop energy (kN·mm)': 'Средняя энергия петли (кН·мм)',
                'Maximum loop energy (kN·mm)': 'Максимальная энергия петли (кН·мм)',
                'Equivalent viscous damping coefficient': 'Эквивалентный коэффициент вязкого демпфирования',
                'Positive strength degradation (%)': 'Деградация прочности в положительном направлении (%)',
                'Negative strength degradation (%)': 'Деградация прочности в отрицательном направлении (%)',
                'Stiffness degradation (%)': 'Деградация жёсткости (%)',
                'Positive (mm)': 'Положительное (мм)',
                'Negative (mm)': 'Отрицательное (мм)',
                'Positive (N)': 'Положительное (Н)',
                'Negative (N)': 'Отрицательное (Н)',

                # Подробная информация о петлях гистерезиса
                'No hysteresis loop information': 'Нет данных о петлях гистерезиса',
                'Detailed Hysteresis Loop Information': 'Подробная информация о петлях гистерезиса',
                'No.': '№',
                'Type': 'Тип',
                'Peak Disp.': 'Пиковое перемещение',
                'Peak Force': 'Пиковое усилие',
                'Loop Area': 'Площадь петли',
                'Positive': 'Положительная',
                'Negative': 'Отрицательная',
                'Statistical Information': 'Статистическая информация',
                'Total loops': 'Общее число петель',
                'Total energy dissipation': 'Общее рассеяние энергии',
                'Average energy dissipation': 'Среднее рассеяние энергии',
                'Maximum energy dissipation': 'Максимальное рассеяние энергии',
                'Minimum energy dissipation': 'Минимальное рассеяние энергии',
                'Positive loops': 'Положительные петли',
                'Negative loops': 'Отрицательные петли',
                
            },
            
            'zh': {
                'language': '语言',
                'window_title': '力-位移曲线数据处理与分析程序',
                'File Management': '文件管理',
                'Import': '导入文件',
                'Clear': '清空列表',
                'Keyboard shortcut: Delete': '快捷键: "Delete" - 删除选定文件',
                'Plot Style': '绘图样式',
                'Dot-Line Graph': '点线连接图',
                'Spline Connected Graph': '平滑曲线图',
                'Skeleton curve extraction method': '骨架曲线提取方法',
                'Method 1: Outer Envelope': '方法1: 最外层包络线描边',
                'Method 2: Peak Points': '方法2: 峰值点连接法',
                'Skeleton curve analysis direction': '骨架曲线分析方向',
                'All directions': '全部方向',
                'Positive direction only': '仅正向',
                'Negative direction only': '仅负向',
                'Ductility coefficient calculation method': '延性系数计算方法',
                'geometric': '几何作图法',
                'energy': '能量法',
                'park': 'Park法',
                'farthest': '最远点法',
                'asce': 'ASCE法',
                'eeep': 'EEEP法',
                'elastic_yield': '弹性屈服法',
                'Data filtering options': '数据过滤选项',
                'Only retain the first loop of the same displacement level': '仅保留同级位移首圈',
                'language': '语言',
                'Smoothness parameter': '平滑度参数:',
                'Preset': '预设',
                'Show original data points': '显示原始数据点',
                'Number of interpolation points': '插值点数:',
                'Smoothing algorithm': '平滑算法:',
                'PCHIP - Shape-preserving interpolation (no overshoot)': 'PCHIP - 保形插值（无过冲）',
                'Akima - Akima interpolation (naturally smooth)': 'Akima - Akima插值（自然平滑）',
                'Bezier - Bézier curve (ultra smooth)': 'Bezier - 贝塞尔曲线（极致平滑）',
                'BSpline - B-spline (super smooth)': 'BSpline - B样条（超平滑）',
                'SG filter - Savitzky-Golay filter (feature-preserving)': 'Savitzky-Golay - SG滤波（保特征）',
                'UnivariateSpline - General-purpose spline (adjustable smoothness)': 'UnivariateSpline - 通用样条（可调平滑度）',
                'CubicSpline - Cubic spline (exactly passes through points)': 'CubicSpline - 三次样条（严格通过点）',
                'Control point density (%)': '控制点密度 (%):',
                'Value': '数值',
                'Adjustment': '调节',
                'Current value': '当前值',
                'Current value {}': '当前值: {}',
                'Current value {:.2f}': '当前值: {:.2f}',
                'None': '无',
                'Low': '低',
                'Medium': '中',
                'High': '高',
                'Very high': '极高',
                'Shape‑preserving piecewise cubic interpolation. Preserves data monotonicity and avoids overshoot and oscillations. Suitable for preserving data trends.': '保形分段三次插值。保持数据的单调性，避免过冲和振荡。适合保持数据趋势。',
                'Akima interpolation method. Reduces oscillations in the curve and is more natural than cubic splines. Suitable for scenarios where you want to reduce fluctuations.': 'Akima插值方法。减少曲线振荡，比三次样条更自然。适合减少波动的场景。',
                'Bézier curve. Generates an extremely smooth curve, suitable for presentation/visualization. The parameter controls control‑point density: 10% = smoothest, 100% = closest to the original data. Recommended 20–40%.': '贝塞尔曲线。生成极致平滑的曲线，适合展示用途。参数控制控制点密度：10% = 最平滑，100% = 最贴合原始数据。推荐20–40%。',
                'B‑spline interpolation. Produces a very smooth curve, but may deviate from the original data points. The parameter s controls the smoothness.': 'B样条插值。生成最平滑的曲线，但可能偏离原始数据点。参数s控制平滑度。',
                'Savitzky–Golay filtering. Smooths the data while preserving its features (such as peaks). The parameter is the window size.': 'Savitzky-Golay滤波。在平滑的同时保持数据特征（如峰值）。参数为窗口大小。',
                'General‑purpose spline interpolation with adjustable smoothness. The parameter s controls the level of smoothing: s = 0 forces the spline to pass exactly through the points; the larger s is, the smoother the curve. Suitable for most cases.': '通用样条插值，支持平滑度调节。参数s控制平滑程度：s = 0严格通过点，s越大越平滑。适合大多数情况。',
                'Cubic spline interpolation that passes exactly through all data points. The resulting curve has a continuous second derivative at the knots.': '三次样条插值，严格通过所有数据点。生成的曲线在连接点处二阶导数连续。',
                'Smoothing interpolation failed': '平滑插值失败',
                'Failed to generate Bézier curve': '贝塞尔曲线生成失败',
                'Smoothing failed': '平滑失败',
                'Displacement (mm)': '位移 (mm)',
                'Force (N)': '力 (N)',
                'Force-Displacement Hysteresis Curve': '力-位移滞回曲线',
                'Hysteresis Curve': '滞回曲线',
                'Positive Skeleton Curve': '正向骨架曲线',
                'Negative Skeleton Curve': '负向骨架曲线',
                'Skeleton Data Points': '骨架曲线数据点',
                'Positive Skeleton Curve Start Point': '正向骨架曲线起点',
                'Negative Skeleton Curve Start Point': '负向骨架曲线起点',
                'Positive Peak': '正向峰值',
                'Negative Peak': '负向峰值',
                'Filtered Label': '[已过滤]',
                'Smooth Label': '[平滑]',
                'Hysteresis curve and backbone curve': '滞回曲线与骨架曲线',
                'Evaluation metrics and analysis results': '评价指标与分析结果',
                'Detailed information on hysteresis loops': '滞回环详细信息',                   
                'No analysis results': '无分析结果',
                'Force-Displacement Curve Analysis Report': '力-位移滞回曲线分析报告',
                'Select force-displacement data files (multiple selections possible)': '选择力-位移数据文件（可多选）',
                'All supported formats (*.txt *.csv *.xls *.xlsx); text files (*.txt); CSV files (*.csv); Excel files (*.xls *.xlsx); all files (*.*)': '所有支持的格式 (*.txt *.csv *.xls *.xlsx); 文本文件 (*.txt); CSV文件 (*.csv); Excel文件 (*.xls *.xlsx); 所有文件 (*.*)',
                'Successfully imported {} files': '成功导入 {} 个文件。',
                'Success': '成功',
                'Confirm': '确认',
                'Are you sure you want to clear all files?': ' 确定要清空所有文件吗？',
                'Error': '错误',
                'Unsported file format: {}': '不支持的文件格式: {}',
                'Incorrect data format! The file must contain at least 2 columns:\nColumn 1 - Displacement\nColumn 2 - Force': '数据格式不正确！文件需要至少包含两列数据：\n第1列 - 位移 \n第2列 - 力',
                'Fail to read file:\n{}': '读取文件失败: \n{}',
                'Deleted': '已删除',
                'Deleted {} files': '已删除 {} 个文件',
                'Open Source Project | Contributions Welcome': '免费开源项目 | 欢迎贡献',
                  
                # 分析结果页面翻译
                'File Information': '文件信息',
                'File name': '文件名',
                'Number of data points': '数据点数量',
                'Number of hysteresis loops': '滞回环数量',
                'Enabled (Only retain the first loop of the same displacement level)': '启用（仅保留相同位移水平的首个滞回环）',
                'Skeleton Curve Starting Points': '骨架曲线起始点',
                'Note: Common starting point crossing y-axis between first negative peak and second positive peak': '注：常用起点为第一次负峰与第二次正峰之间穿过 y 轴的点',
                'Evaluation Metrics': '评价指标',
                'Displacement-related': '位移相关',
                'Mechanical properties': '力学性能',
                'Energy metrics': '能量指标',
                'Coefficient metrics': '系数指标',
                'Degradation metrics': '退化指标',
                'Ductility coefficient': '延性系数',

                # 指标名称
                'Peak displacement': '峰值位移',
                'Residual deformation (mm)': '残余变形 (mm)',
                'Peak load': '峰值荷载',
                'Initial stiffness (N/mm)': '初始刚度 (k/mm)',
                'Secant stiffness (N/mm)': '割线刚度 (N/mm)',
                'Total hysteresis loop area (kN·mm)': '滞回环总面积 (kN·mm)',
                'Cumulative energy dissipation (kN·mm)': '累积耗能 (kN·mm)',
                'Average loop energy (kN·mm)': '平均单环耗能 (kN·mm)',
                'Maximum loop energy (kN·mm)': '最大单环耗能 (kN·mm)',
                'Equivalent viscous damping coefficient': '等效粘滞阻尼系数',
                'Positive strength degradation (%)': '正向强度退化 (%)',
                'Negative strength degradation (%)': '负向强度退化 (%)',
                'Stiffness degradation (%)': '刚度退化 (%)',
                'Positive (mm)': '正向 (mm)',
                'Negative (mm)': '负向 (mm)',
                'Positive (N)': '正向 (N)',
                'Negative (N)': '负向 (N)',

                # 滞回环详细信息翻译
                'No hysteresis loop information': '无滞回环信息',
                'Detailed Hysteresis Loop Information': '滞回环详细信息',
                'No.': '序号',
                'Type': '类型',
                'Peak Disp.': '峰值位移',
                'Peak Force': '峰值力',
                'Loop Area': '滞回环面积',
                'Positive': '正向',
                'Negative': '负向',
                'Statistical Information': '统计信息',
                'Total loops': '滞回环总数',
                'Total energy dissipation': '总耗能',
                'Average energy dissipation': '平均耗能',
                'Maximum energy dissipation': '最大耗能',
                'Minimum energy dissipation': '最小耗能',
                'Positive loops': '正向滞回环',
                'Negative loops': '负向滞回环',           
                                         
            }
        }
        
        self.setWindowTitle("Force-Displacement Curve Analyzer")

        # 设置窗口图标
        def get_resource_path(relative_path):
            """获取资源文件的绝对路径（支持打包后的exe）"""
            try:
                # PyInstaller创建临时文件夹，路径存储在_MEIPASS中
                base_path = sys._MEIPASS
            except Exception:
                base_path = Path(__file__).parent
            return Path(base_path) / relative_path

        icon_path = get_resource_path("icon.ico")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # 自适应屏幕尺寸
        self.setup_window_geometry()
        
        # 数据存储
        self.data_files = []
        self.current_data = None
        self.hysteresis_loops = []
        self.skeleton_curve = None
        self.history = []
        self.indices = {}
        
        # 创建界面
        self.init_ui()
        
        # 设置快捷键
        self.setup_shortcuts()
    
    def setup_window_geometry(self):
        """设置窗口几何尺寸，自适应屏幕"""
        # 获取主屏幕
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
            
            # 设置窗口为屏幕的85%大小
            window_width = int(screen_width * 0.85)
            window_height = int(screen_height * 0.85)
            
            # 计算居中位置
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            # 设置窗口位置和大小
            self.setGeometry(x, y, window_width, window_height)
        else:
            # 如果无法获取屏幕信息，使用默认值
            self.setGeometry(100, 100, 1400, 800)
        
    def init_ui(self):
        """初始化UI"""
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧控制面板
        left_widget = self.create_left_panel()
        splitter.addWidget(left_widget)
        
        # 右侧显示面板
        right_widget = self.create_right_panel()
        splitter.addWidget(right_widget)
        
        # 设置分割器比例
        splitter.setSizes([350, 1250])
        
        
    def create_left_panel(self):
        """创建左侧控制面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        # 语言选择
        self.lang_group = QGroupBox(self.tr('language'))
        lang_layout = QHBoxLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['English', 'Русскии', '中文'])
        self.lang_combo.setCurrentIndex(0) # 默认英语
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_combo)
        self.lang_group.setLayout(lang_layout)
        layout.addWidget(self.lang_group)
        
        # 文件管理区域
        self.file_group = QGroupBox("File Management")
        file_layout = QVBoxLayout()
        
        # 按钮行
        btn_layout = QHBoxLayout()
        self.import_btn = QPushButton("Import")
        self.import_btn.clicked.connect(self.import_files)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_files)
        btn_layout.addWidget(self.import_btn)
        btn_layout.addWidget(self.clear_btn)
        file_layout.addLayout(btn_layout)
        
        # 文件列表
        self.file_list = QListWidget()
        self.file_list.currentRowChanged.connect(self.on_file_select)
        file_layout.addWidget(self.file_list)
        
        # 提示标签
        self.hint_label = QLabel("Keyboard shortcut: Delete")
        self.hint_label.setStyleSheet("color: gray; font-size: 8pt;")
        file_layout.addWidget(self.hint_label)
        
        self.file_group.setLayout(file_layout)
        layout.addWidget(self.file_group)
        
        # 绘图样式选择
        self.plot_style_group = QGroupBox("Plot Style")
        plot_style_layout = QVBoxLayout()
        
        self.plot_style_group_func = QButtonGroup()
        self.rb_line = QRadioButton("Dot-Line Graph")
        self.rb_smooth = QRadioButton("Spline Connected Graph")
        self.rb_line.setChecked(True)
        
        self.plot_style_group_func.addButton(self.rb_line, 0)
        self.plot_style_group_func.addButton(self.rb_smooth, 1)
        
        self.rb_line.toggled.connect(self.on_plot_style_changed)
        self.rb_smooth.toggled.connect(self.on_plot_style_changed)
        
        plot_style_layout.addWidget(self.rb_line)
        plot_style_layout.addWidget(self.rb_smooth)
        
        # 平滑曲线选项容器
        smooth_container = QWidget()
        smooth_layout = QVBoxLayout(smooth_container)
        smooth_layout.setContentsMargins(15, 5, 5, 5)
        
        # 平滑算法选择
        self.algo_label = QLabel("Smoothing algorithm")
        self.algo_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        smooth_layout.addWidget(self.algo_label)
        
        self.smooth_algorithm = QComboBox()
        self.smooth_algorithm.addItems([
            self.tr('PCHIP - Shape-preserving interpolation (no overshoot)'),
            self.tr('Akima - Akima interpolation (naturally smooth)'),
            self.tr('Bezier - Bézier curve (ultra smooth)'),
            self.tr('BSpline - B-spline (super smooth)'),
            self.tr('SG filter - Savitzky-Golay filter (feature-preserving)'),
            self.tr('UnivariateSpline - General-purpose spline (adjustable smoothness)'),
            self.tr('CubicSpline - Cubic spline (exactly passes through points)')
        ])
        self.smooth_algorithm.currentIndexChanged.connect(self.on_algorithm_changed)
        smooth_layout.addWidget(self.smooth_algorithm)
        
        # 算法说明
        self.algo_description = QLabel()
        self.algo_description.setWordWrap(True)
        self.algo_description.setStyleSheet(
            "color: #34495e; font-size: 8pt; "
            "padding: 8px; background-color: #ecf0f1; "
            "border-radius: 4px; margin: 5px 0px;"
        )
        smooth_layout.addWidget(self.algo_description)
        
        # 参数调节区域
        param_container = QWidget()
        param_layout = QVBoxLayout(param_container)
        param_layout.setContentsMargins(0, 5, 0, 5)
        
        # 参数标签
        self.param_title = QLabel("Smoothness parameter")
        self.param_title.setStyleSheet("font-weight: bold; color: #2c3e50;")
        param_layout.addWidget(self.param_title)
        
        # 数字输入框
        spinbox_layout = QHBoxLayout()
        self.spinbox_label = QLabel("Value")
        self.smoothness_spinbox = QDoubleSpinBox()
        self.smoothness_spinbox.setRange(0.0, 10.0)
        self.smoothness_spinbox.setSingleStep(0.1)
        self.smoothness_spinbox.setValue(1.0)
        self.smoothness_spinbox.setDecimals(2)
        self.smoothness_spinbox.valueChanged.connect(self.on_smoothness_changed)
        spinbox_layout.addWidget(self.spinbox_label)
        spinbox_layout.addWidget(self.smoothness_spinbox)
        param_layout.addLayout(spinbox_layout)
        
        # 滑块控制
        slider_layout = QVBoxLayout()
        self.slider_label = QLabel("Adjustment")
        self.smoothness_slider = QSlider(Qt.Horizontal)
        self.smoothness_slider.setRange(0, 100)
        self.smoothness_slider.setValue(10)
        self.smoothness_slider.setTickPosition(QSlider.TicksBelow)
        self.smoothness_slider.setTickInterval(10)
        self.smoothness_slider.valueChanged.connect(self.on_slider_changed)
        slider_layout.addWidget(self.slider_label)
        slider_layout.addWidget(self.smoothness_slider)
        param_layout.addLayout(slider_layout)
        
        # 当前值显示
        self.smoothness_value_label = QLabel(self.tr('Current value').format("1.00"))
        self.smoothness_value_label.setStyleSheet("color: #16a085; font-weight: bold;")
        param_layout.addWidget(self.smoothness_value_label)
        
        # 预设按钮
        preset_layout = QHBoxLayout()
        self.preset_label = QLabel("Preset")
        preset_layout.addWidget(self.preset_label)
        
        for value, name in [(0.0, self.tr('None')), (2.5, self.tr('Low')), (5.0, self.tr('Medium')), (7.5, self.tr('High')), (10, self.tr('Very High'))]:
            btn = QPushButton(name)
            btn.setProperty("smoothness_value", value)
            btn.clicked.connect(self.on_preset_clicked)
            btn.setMaximumWidth(100)
            preset_layout.addWidget(btn)
        
        param_layout.addLayout(preset_layout)
        
        self.param_container = param_container
        smooth_layout.addWidget(param_container)
        
        # 插值点数控制
        points_layout = QHBoxLayout()
        self.points_label = QLabel("Number of interpolation points")
        self.interp_points = QComboBox()
        self.interp_points.addItems(["100", "200", "300", "500", "1000"])
        self.interp_points.setCurrentText("300")
        self.interp_points.currentTextChanged.connect(self.update_plot_only)
        points_layout.addWidget(self.points_label)
        points_layout.addWidget(self.interp_points)
        smooth_layout.addLayout(points_layout)
        
        # 显示原始数据点
        self.show_original_points = QCheckBox("Show original data points")
        self.show_original_points.setChecked(True)
        self.show_original_points.stateChanged.connect(self.update_plot_only)
        smooth_layout.addWidget(self.show_original_points)
        
        self.smooth_container = smooth_container
        plot_style_layout.addWidget(smooth_container)
        
        # 初始状态：隐藏平滑选项
        self.smooth_container.setVisible(False)
        
        self.plot_style_group.setLayout(plot_style_layout)
        layout.addWidget(self.plot_style_group)
        
        # 骨架曲线提取方法
        self.skeleton_group = QGroupBox("Skeleton curve extraction method")
        skeleton_layout = QVBoxLayout()
        
        self.skeleton_method_group = QButtonGroup()
        self.rb_outer = QRadioButton("Method 1: Outer Envelope")
        self.rb_peak = QRadioButton("Method 2: Peak Points")
        self.rb_outer.setChecked(True)
        
        self.skeleton_method_group.addButton(self.rb_outer, 0)
        self.skeleton_method_group.addButton(self.rb_peak, 1)
        
        self.rb_outer.toggled.connect(self.update_analysis)
        self.rb_peak.toggled.connect(self.update_analysis)
        
        skeleton_layout.addWidget(self.rb_outer)
        skeleton_layout.addWidget(self.rb_peak)
        self.skeleton_group.setLayout(skeleton_layout)
        layout.addWidget(self.skeleton_group)
        
        # 分析方向选择
        self.direction_group = QGroupBox("Skeleton curve analysis direction")
        direction_layout = QVBoxLayout()
        
        self.direction_group_button = QButtonGroup()
        self.rb_both = QRadioButton("All directions")
        self.rb_positive = QRadioButton("Positive direction only")
        self.rb_negative = QRadioButton("Negative direction only")
        self.rb_both.setChecked(True)
        
        self.direction_group_button.addButton(self.rb_both, 0)
        self.direction_group_button.addButton(self.rb_positive, 1)
        self.direction_group_button.addButton(self.rb_negative, 2)
        
        self.rb_both.toggled.connect(self.update_analysis)
        self.rb_positive.toggled.connect(self.update_analysis)
        self.rb_negative.toggled.connect(self.update_analysis)
        
        direction_layout.addWidget(self.rb_both)
        direction_layout.addWidget(self.rb_positive)
        direction_layout.addWidget(self.rb_negative)
        self.direction_group.setLayout(direction_layout)
        layout.addWidget(self.direction_group)
        
        # 延性系数计算方法
        self.ductility_group = QGroupBox("Ductility coefficient calculation method")
        ductility_layout = QVBoxLayout()
        
        self.ductility_method_group = QButtonGroup()
        methods = [
            ("Geometric Method", "geometric"),      #几何作图法
            ("Energy Method", "energy"),                   #能量法
            ("Park Method", "park"),                     #Park法
            ("Farthest Point", "farthest"),               #最远点法
            ("ASCE Method", "asce"),                    #ASCE法
            ("EEEP Method", "eeep"),                    #EEEP法
            ("Elastic Yield", "elastic_yield")        #弹性屈服法
        ]
        
        
        self.ductility_radios = {}
        for i, (text, value) in enumerate(methods):
            rb = QRadioButton(text)
            rb.setProperty("method_value", value)
            if i == 0:
                rb.setChecked(True)
            rb.toggled.connect(self.update_analysis)
            self.ductility_method_group.addButton(rb, i)
            self.ductility_radios[value] = rb
            ductility_layout.addWidget(rb)
        
        self.ductility_group.setLayout(ductility_layout)
        layout.addWidget(self.ductility_group)
        
        # 数据过滤选项
        self.filter_group = QGroupBox("Data filtering options")
        filter_layout = QVBoxLayout()
        
        self.filter_first_loop = QCheckBox("Only retain the first loop of the same displacement level")
        self.filter_first_loop.stateChanged.connect(self.update_analysis)
        filter_layout.addWidget(self.filter_first_loop)
        
        self.filter_group.setLayout(filter_layout)
        layout.addWidget(self.filter_group)
        
        # GitHub 开源项目链接
        github_group = QGroupBox()
        github_layout = QVBoxLayout()

        # 项目信息标签
        self.project_label = QLabel(self.tr('Open Source Project | Contributions Welcome'))
        self.project_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.project_label.setAlignment(Qt.AlignCenter)
        github_layout.addWidget(self.project_label)

        # GitHub 链接
        github_link = QLabel()
        github_link.setText('<a href="https://github.com/GarGarfie/HysAnalysis" style="color: #3498db; text-decoration: none;">📂 github.com/GarGarfie/HysAnalysis</a>')
        github_link.setOpenExternalLinks(True)
        github_link.setAlignment(Qt.AlignCenter)
        github_link.setStyleSheet("""
            QLabel {
                padding: 8px;
                background-color: #ecf0f1;
                border-radius: 4px;
                font-size: 9pt;
            }
            QLabel:hover {
                background-color: #d5dbdb;
            }
        """)
        github_layout.addWidget(github_link)

        github_group.setLayout(github_layout)
        layout.addWidget(github_group)
        
        # 添加弹簧
        layout.addStretch()
        
        # 初始化算法描述
        self.update_algorithm_description()
        
        return widget
    
    def tr(self, key):
        """获取翻译文本"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def change_language(self, index):
        """切换语言"""
        languages = ['en', 'ru', 'zh']
        self.current_language = languages[index]
        self.update_ui_language()
        
        # matplotlib配置，根据语言调整
        if self.current_language == 'zh':
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
        elif self.current_language == 'ru':
            plt.rcParams['font.sans-serif'] = ['Arial', 'Liberation Sans', 'DejaVu Sans', 'Tahoma']
            plt.rcParams['axes.unicode_minus'] = True
        else:
            plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
            plt.rcParams['axes.unicode_minus'] = True
        
        self.canvas.update_labels()
            
        if self.current_data:
            self.update_plot()
            self.update_results()
            self.update_loop_info()
            
    def update_ui_language(self):
        """更新UI所有文本"""
        self.setWindowTitle(self.tr('window_title'))
        self.lang_group.setTitle(self.tr('language'))
        self.file_group.setTitle(self.tr('File Management'))
        self.import_btn.setText(self.tr('Import'))
        self.clear_btn.setText(self.tr('Clear'))
        self.hint_label.setText(self.tr('Keyboard shortcut: Delete'))
        self.plot_style_group.setTitle(self.tr('Plot Style'))
        self.rb_line.setText(self.tr('Dot-Line Graph'))
        self.rb_smooth.setText(self.tr('Spline Connected Graph'))
        self.skeleton_group.setTitle(self.tr('Skeleton curve extraction method'))
        self.rb_outer.setText(self.tr('Method 1: Outer Envelope'))
        self.rb_peak.setText(self.tr('Method 2: Peak Points'))
        self.direction_group.setTitle(self.tr('Skeleton curve analysis direction'))
        self.rb_both.setText(self.tr('All directions'))
        self.rb_positive.setText(self.tr('Positive direction only'))
        self.rb_negative.setText(self.tr('Negative direction only'))
        self.ductility_group.setTitle(self.tr('Ductility coefficient calculation method'))
        self.filter_group.setTitle(self.tr('Data filtering options'))
        self.filter_first_loop.setText(self.tr('Only retain the first loop of the same displacement level'))
        self.algo_label.setText(self.tr('Smoothing algorithm'))
        self.points_label.setText(self.tr('Number of interpolation points'))
        self.preset_label.setText(self.tr('Preset'))
        self.show_original_points.setText(self.tr('Show original data points'))
        self.spinbox_label.setText(self.tr('Value'))
        self.slider_label.setText(self.tr('Adjustment'))
        self.tab_widget.setTabText(0, self.tr('Hysteresis curve and backbone curve'))
        self.tab_widget.setTabText(1, self.tr('Evaluation metrics and analysis results'))
        self.tab_widget.setTabText(2, self.tr('Detailed information on hysteresis loops'))
        self.project_label.setText(self.tr('Open Source Project | Contributions Welcome'))
        
        # 更新ComboBox - 保存当前选择
        current_algo = self.smooth_algorithm.currentIndex()
        self.smooth_algorithm.clear()
        self.smooth_algorithm.addItems([
            self.tr('PCHIP - Shape-preserving interpolation (no overshoot)'),
            self.tr('Akima - Akima interpolation (naturally smooth)'),
            self.tr('Bezier - Bézier curve (ultra smooth)'),
            self.tr('BSpline - B-spline (super smooth)'),
            self.tr('SG filter - Savitzky-Golay filter (feature-preserving)'),
            self.tr('UnivariateSpline - General-purpose spline (adjustable smoothness)'),
            self.tr('CubicSpline - Cubic spline (exactly passes through points)')
        ])
        self.smooth_algorithm.setCurrentIndex(current_algo)  # 恢复选择

        
        
    def create_right_panel(self):
        """创建右侧显示面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 图形显示页面
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        
        # 创建matplotlib画布
        self.canvas = MplCanvas(self, width=12, height=9, dpi=100)
        
        # 添加工具栏
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        
        self.tab_widget.addTab(plot_widget, self.tr("Hysteresis curve and backbone curve"))
        
        # 分析结果页面
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Courier New", 10))
        result_layout.addWidget(self.result_text)
        
        self.tab_widget.addTab(result_widget, self.tr("Evaluation metrics and analysis results"))
        
        # 滞回环详细信息页面
        loop_widget = QWidget()
        loop_layout = QVBoxLayout(loop_widget)
        
        self.loop_text = QTextEdit()
        self.loop_text.setReadOnly(True)
        self.loop_text.setFont(QFont("Courier New", 9))
        loop_layout.addWidget(self.loop_text)
        
        self.tab_widget.addTab(loop_widget, self.tr("Detailed information on hysteresis loops"))
        
        return widget
    
    def setup_shortcuts(self):
        """设置快捷键"""
        # Ctrl+Z 撤销
        undo_shortcut = QShortcut(QKeySequence.Undo, self)
        undo_shortcut.activated.connect(self.undo)
        
        # Delete 删除
        delete_shortcut = QShortcut(QKeySequence.Delete, self)
        delete_shortcut.activated.connect(self.delete_selected)
    
    def on_plot_style_changed(self):
        """绘图样式改变时的处理"""
        is_smooth = self.rb_smooth.isChecked()
        self.smooth_container.setVisible(is_smooth)
        
        if is_smooth:
            self.update_algorithm_description()
        
        self.update_plot_only()
    
    def on_algorithm_changed(self):
        """算法改变时的处理"""
        self.update_algorithm_description()
        self.update_smoothness_range()
        self.update_plot_only()
    
    def update_algorithm_description(self):
        """更新算法描述"""
        algo_index = self.smooth_algorithm.currentIndex()
        
        descriptions = [
            "Shape‑preserving piecewise cubic interpolation. Preserves data monotonicity and avoids overshoot and oscillations. Suitable for preserving data trends.",
            "Akima interpolation method. Reduces oscillations in the curve and is more natural than cubic splines. Suitable for scenarios where you want to reduce fluctuations.",
            "Bézier curve. Generates an extremely smooth curve, suitable for presentation/visualization. The parameter controls control‑point density: 10% = smoothest, 100% = closest to the original data. Recommended 20–40%.",
            "B‑spline interpolation. Produces a very smooth curve, but may deviate from the original data points. The parameter s controls the smoothness.",
            "Savitzky–Golay filtering. Smooths the data while preserving its features (such as peaks). The parameter is the window size.",
            "General‑purpose spline interpolation with adjustable smoothness. The parameter s controls the level of smoothing: s = 0 forces the spline to pass exactly through the points; the larger s is, the smoother the curve. Suitable for most cases.",
            "Cubic spline interpolation that passes exactly through all data points. The resulting curve has a continuous second derivative at the knots."
        ]
        
        self.algo_description.setText(self.tr(descriptions[algo_index]))

    def update_smoothness_range(self):
        """根据算法更新平滑度参数范围"""
        algo_index = self.smooth_algorithm.currentIndex()
        
        # PCHIP (0), Akima (1), CubicSpline (6) 不需要参数
        if algo_index in [0, 1, 6]:
            self.param_container.setVisible(False)
        
        # Bezier (2) 使用控制点密度
        elif algo_index == 2:
            self.param_container.setVisible(True)
            self.param_title.setText(self.tr('Control point density (%)'))
            self.smoothness_spinbox.setRange(10, 100)
            self.smoothness_spinbox.setSingleStep(5)
            self.smoothness_spinbox.setValue(30)
            self.smoothness_spinbox.setDecimals(0)
        
        # BSpline (3) 支持平滑度参数
        elif algo_index == 3:
            self.param_container.setVisible(True)
            self.param_title.setText("Smoothness parameter (s):")
            self.smoothness_spinbox.setRange(0.0, 10.0)
            self.smoothness_spinbox.setSingleStep(0.1)
            self.smoothness_spinbox.setValue(2.0)
            self.smoothness_spinbox.setDecimals(2)
        
        # Savitzky-Golay (4) 使用窗口大小
        elif algo_index == 4:
            self.param_container.setVisible(True)
            self.param_title.setText("窗口大小:")
            self.smoothness_spinbox.setRange(3, 51)
            self.smoothness_spinbox.setSingleStep(2)
            self.smoothness_spinbox.setValue(7)
            self.smoothness_spinbox.setDecimals(0)
        
        # UnivariateSpline (5) 支持平滑度参数
        elif algo_index == 5:
            self.param_container.setVisible(True)
            self.param_title.setText("Smoothness parameter (s):")
            self.smoothness_spinbox.setRange(0.0, 10.0)
            self.smoothness_spinbox.setSingleStep(0.1)
            self.smoothness_spinbox.setValue(1.0)
            self.smoothness_spinbox.setDecimals(2)

    def on_smoothness_changed(self, value):
        """平滑度数值改变时的处理"""
        algo_index = self.smooth_algorithm.currentIndex()
        
        # Savitzky-Golay 确保窗口大小为奇数
        if algo_index == 4:
            if int(value) % 2 == 0:
                value = int(value) + 1
                self.smoothness_spinbox.blockSignals(True)
                self.smoothness_spinbox.setValue(value)
                self.smoothness_spinbox.blockSignals(False)
        
        # Bezier 确保是整数
        if algo_index == 2:
            value = int(value)
        
        # 同步更新滑块
        self.smoothness_slider.blockSignals(True)
        if algo_index == 4:  # SG滤波
            self.smoothness_slider.setValue(int((value - 3) / 48 * 100))
        elif algo_index == 2:  # Bezier
            self.smoothness_slider.setValue(int((value - 10) / 90 * 100))
        else:
            self.smoothness_slider.setValue(int(value * 10))
        self.smoothness_slider.blockSignals(False)
        
        # 更新显示标签
        if algo_index in [2, 4]:
            self.smoothness_value_label.setText(self.tr('Current value').format(int(value)))
        else:
            self.smoothness_value_label.setText(self.tr('Current value').format(f"{value:.2f}"))
        
        # 更新图形
        self.update_plot_only()
    
    def on_slider_changed(self, value):
        """滑块改变时的处理"""
        algo_index = self.smooth_algorithm.currentIndex()
        
        # 转换值
        if algo_index == 4:  # SG滤波：3-51
            smooth_value = int(3 + (value / 100) * 48)
            if smooth_value % 2 == 0:
                smooth_value += 1
        elif algo_index == 2:  # Bezier：10-100
            smooth_value = int(10 + (value / 100) * 90)
        else:  # 其他：0-10.0
            smooth_value = value / 10.0
        
        # 同步更新数字输入框
        self.smoothness_spinbox.blockSignals(True)
        self.smoothness_spinbox.setValue(smooth_value)
        self.smoothness_spinbox.blockSignals(False)
        
        # 更新显示标签
        if algo_index in [2, 4]:
            self.smoothness_value_label.setText(self.tr('Current value {}').format(int(smooth_value)))
        else:
            self.smoothness_value_label.setText(self.tr('Current value {:.2f}').format(smooth_value))
        
        # 更新图形
        self.update_plot_only()
    
    def on_preset_clicked(self):
        """预设按钮点击处理"""
        sender = self.sender()
        value = sender.property("smoothness_value")
        if value is not None:
            self.smoothness_spinbox.setValue(value)
    
    def get_plot_style(self):
        """获取绘图样式"""
        if self.rb_smooth.isChecked():
            return "smooth"
        else:
            return "line"
    
    def get_smooth_algorithm(self):
        """获取平滑算法"""
        algo_names = [
            "PCHIP",
            "Akima",
            "Bezier",
            "BSpline",
            "SavitzkyGolay",
            "UnivariateSpline",
            "CubicSpline"
        ]
        return algo_names[self.smooth_algorithm.currentIndex()]
    
    def interpolate_smooth(self, x, y, num_points=300):
        """使用选定的算法平滑曲线"""
        try:
            # 确保数据点足够多
            if len(x) < 4:
                return x, y
            
            # 移除重复的x值并排序
            unique_indices = []
            seen_x = {}
            for i, xi in enumerate(x):
                if xi not in seen_x:
                    unique_indices.append(i)
                    seen_x[xi] = i
            
            if len(unique_indices) < 4:
                return x, y
            
            x_unique = x[unique_indices]
            y_unique = y[unique_indices]
            
            # 排序
            sort_indices = np.argsort(x_unique)
            x_sorted = x_unique[sort_indices]
            y_sorted = y_unique[sort_indices]
            
            # 获取算法和参数
            algorithm = self.get_smooth_algorithm()
            num_points = int(self.interp_points.currentText())
            smoothness = self.smoothness_spinbox.value()
            
            # 生成插值点
            x_smooth = np.linspace(x_sorted[0], x_sorted[-1], num_points)
            
            # 根据算法选择插值方法
            if algorithm == "PCHIP":
                pchip = PchipInterpolator(x_sorted, y_sorted)
                y_smooth = pchip(x_smooth)
            
            elif algorithm == "Akima":
                akima = Akima1DInterpolator(x_sorted, y_sorted)
                y_smooth = akima(x_smooth)
            
            elif algorithm == "Bezier":
                # 使用控制点密度参数
                control_ratio = smoothness / 100.0  # 将百分比转换为0-1范围
                y_smooth = self.bezier_curve(x_sorted, y_sorted, x_smooth, control_ratio)
            
            elif algorithm == "BSpline":
                s_param = smoothness * len(x_sorted)
                tck = splrep(x_sorted, y_sorted, s=s_param, k=3)
                from scipy.interpolate import splev
                y_smooth = splev(x_smooth, tck)
            
            elif algorithm == "SavitzkyGolay":
                # 首先进行初步插值以获得均匀采样
                spline = make_interp_spline(x_sorted, y_sorted, k=3)
                y_temp = spline(x_smooth)
                # 然后应用SG滤波
                window_length = int(smoothness)
                if window_length % 2 == 0:
                    window_length += 1
                window_length = min(window_length, len(x_smooth) - 1)
                if window_length < 3:
                    window_length = 3
                polyorder = min(3, window_length - 1)
                y_smooth = savgol_filter(y_temp, window_length, polyorder)
            
            elif algorithm == "UnivariateSpline":
                if smoothness == 0:
                    spline = make_interp_spline(x_sorted, y_sorted, k=3)
                else:
                    s_param = smoothness * len(x_sorted)
                    spline = UnivariateSpline(x_sorted, y_sorted, s=s_param, k=3)
                y_smooth = spline(x_smooth)
            
            elif algorithm == "CubicSpline":
                spline = make_interp_spline(x_sorted, y_sorted, k=3)
                y_smooth = spline(x_smooth)
            
            else:
                return x, y
            
            return x_smooth, y_smooth
            
        except Exception as e:
            error_msg = self.tr('Smoothing interpolation failed').format(str(e))
            print(error_msg)
            self.statusBar().showMessage(error_msg, 3000)
            import traceback
            traceback.print_exc()
            return x, y
    
    def bezier_curve(self, x, y, x_new, control_point_ratio=0.3):
        """生成贝塞尔曲线
        
        Args:
            x: 原始x坐标数组
            y: 原始y坐标数组
            x_new: 新的x坐标数组（插值目标）
            control_point_ratio: 控制点密度（0-1之间，默认0.3即30%）
        """
        try:
            # 根据控制点密度选择控制点
            n_points = len(x)
            n_control = max(4, int(n_points * control_point_ratio))  # 至少4个控制点
            
            if n_control >= n_points:
                # 使用所有点
                control_x = x
                control_y = y
            else:
                # 均匀选择控制点，但始终包含首尾点
                indices = np.linspace(0, n_points - 1, n_control, dtype=int)
                indices = np.unique(indices)  # 去重
                control_x = x[indices]
                control_y = y[indices]
            
            n = len(control_x) - 1
            t = np.linspace(0, 1, len(x_new))
            
            # 贝塞尔曲线的伯恩斯坦基函数
            def bernstein(n, k, t):
                """计算伯恩斯坦多项式"""
                from scipy.special import comb
                return comb(n, k) * (t ** k) * ((1 - t) ** (n - k))
            
            # 计算贝塞尔曲线上的点
            curve_x = np.zeros(len(t))
            curve_y = np.zeros(len(t))
            
            for k in range(n + 1):
                B = bernstein(n, k, t)
                curve_x += control_x[k] * B
                curve_y += control_y[k] * B
            
            # 由于贝塞尔曲线的参数化，curve_x 可能不是单调的
            # 需要重新映射到目标x坐标
            try:
                # 尝试直接插值
                if len(np.unique(curve_x)) > 3:  # 确保有足够的唯一点
                    # 对curve_x排序并去重
                    sort_idx = np.argsort(curve_x)
                    curve_x_sorted = curve_x[sort_idx]
                    curve_y_sorted = curve_y[sort_idx]
                    
                    # 去除重复的x值
                    unique_mask = np.concatenate([[True], np.diff(curve_x_sorted) > 1e-10])
                    curve_x_unique = curve_x_sorted[unique_mask]
                    curve_y_unique = curve_y_sorted[unique_mask]
                    
                    if len(curve_x_unique) > 3:
                        # 使用PCHIP插值（保持单调性）
                        from scipy.interpolate import PchipInterpolator
                        interp = PchipInterpolator(curve_x_unique, curve_y_unique)
                        y_new = interp(x_new)
                        return y_new
            except:
                pass
            
            # 如果上述方法失败，使用替代方法：
            # 将贝塞尔曲线视为参数曲线，找到每个x_new对应的t值
            y_new = np.zeros(len(x_new))
            for i, xi in enumerate(x_new):
                # 找到最接近xi的curve_x的索引
                idx = np.argmin(np.abs(curve_x - xi))
                y_new[i] = curve_y[idx]
            
            return y_new
            
        except Exception as e:
            error_msg = self.tr('Failed to generate Bézier curve').format(str(e))
            print(error_msg)
            self.statusBar().showMessage(error_msg, 3000)
            # 回退到三次样条
            try:
                spline = make_interp_spline(x, y, k=3)
                return spline(x_new)
            except:
                return np.interp(x_new, x, y)
    
    def import_files(self):
        """导入数据文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            self.tr("Select force-displacement data files (multiple selections possible)"),
            "",
            self.tr("All supported formats (*.txt *.csv *.xls *.xlsx);;Text files (*.txt);;CSV files (*.csv);;Excel files (*.xls *.xlsx);;All files (*.*)")
        )
        
        if files:
            for file in files:
                if file not in [f['path'] for f in self.data_files]:
                    self.data_files.append({
                        'path': file,
                        'name': Path(file).name
                    })
                    self.file_list.addItem(Path(file).name)
            
            self.save_state()
            QMessageBox.information(self, self.tr("Success"), self.tr("Successfully imported {} files").format(len(files)))
    
    def clear_files(self):
        """清空文件列表"""
        if self.data_files:
            reply = QMessageBox.question(
                self, self.tr("Confirm"), self.tr("Are you sure you want to clear all files?"),
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.data_files.clear()
                self.file_list.clear()
                self.current_data = None
                self.clear_plot()
                self.result_text.clear()
                self.loop_text.clear()
                self.save_state()
    
    def on_file_select(self, index):
        """文件选择事件"""
        if index >= 0 and index < len(self.data_files):
            file_path = self.data_files[index]['path']
            self.load_data(file_path)
            self.update_analysis()
    
    def load_data(self, file_path):
        """加载数据文件"""
        try:
            ext = Path(file_path).suffix.lower()
            
            if ext == '.txt':
                df = pd.read_csv(file_path, sep=r'\s+', header=None, engine='python')
            elif ext == '.csv':
                df = pd.read_csv(file_path, header=None)
            elif ext in ['.xls', '.xlsx']:
                df = pd.read_excel(file_path, header=None)
            else:
                QMessageBox.critical(self, self.tr("Error"), self.tr("Unsupported file format: {}").format(ext))
                return
            
            if df.shape[1] < 2:
                QMessageBox.critical(self, self.tr("Error"), 
                    self.tr("Incorrect data format! The file must contain at least 2 columns:\nColumn 1 - Displacement\nColumn 2 - Force"))
                return
            
            displacement = df.iloc[:, 0].values.astype(float)
            force = df.iloc[:, 1].values.astype(float)
            
            displacement, force = self.preprocess_data(displacement, force)
            
            self.current_data = {
                'displacement': displacement,
                'force': force,
                'file_name': Path(file_path).name,
                'file_path': file_path
            }
            
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to read file:\n{}").format(str(e)))
    
    def is_near_zero(self, value, threshold=1e-3):
        """判断一个值是否接近零"""
        return abs(value) < threshold
    
    def preprocess_data(self, displacement, force):
        """预处理数据"""
        disp_range = np.max(np.abs(displacement)) - np.min(np.abs(displacement))
        disp_threshold = max(0.001, disp_range * 0.001)
        
        force_range = np.max(np.abs(force)) - np.min(np.abs(force))
        force_threshold = max(0.01, force_range * 0.001)
        
        displacement_cleaned = displacement.copy()
        force_cleaned = force.copy()
        
        for i in range(len(displacement)):
            if self.is_near_zero(displacement[i], disp_threshold):
                displacement_cleaned[i] = 0.0
            if self.is_near_zero(force[i], force_threshold):
                force_cleaned[i] = 0.0
        
        disp_to_max_force_idx = {}
        tolerance = disp_threshold * 0.5
        
        for i in range(len(displacement_cleaned)):
            current_disp = displacement_cleaned[i]
            current_force_abs = abs(force_cleaned[i])
            
            found_similar = False
            for stored_disp in list(disp_to_max_force_idx.keys()):
                if abs(current_disp - stored_disp) <= tolerance:
                    found_similar = True
                    stored_idx = disp_to_max_force_idx[stored_disp]
                    stored_force_abs = abs(force_cleaned[stored_idx])
                    
                    if current_force_abs > stored_force_abs:
                        del disp_to_max_force_idx[stored_disp]
                        disp_to_max_force_idx[current_disp] = i
                    break
            
            if not found_similar:
                disp_to_max_force_idx[current_disp] = i
        
        unique_indices = sorted(disp_to_max_force_idx.values())
        displacement_cleaned = displacement_cleaned[unique_indices]
        force_cleaned = force_cleaned[unique_indices]
        
        loading_start_idx = 0
        for i in range(len(displacement_cleaned)):
            if (abs(displacement_cleaned[i]) > disp_threshold * 2 or 
                abs(force_cleaned[i]) > force_threshold * 2):
                loading_start_idx = i
                break
        
        if loading_start_idx > 0:
            offset = displacement_cleaned[loading_start_idx]
            displacement_cleaned = displacement_cleaned - offset
        
        return displacement_cleaned, force_cleaned

    def get_skeleton_method(self):
        """获取骨架曲线提取方法"""
        if self.rb_outer.isChecked():
            return "outer_envelope"
        else:
            return "peak_points"
    
    def get_direction(self):
        """获取分析方向"""
        if self.rb_both.isChecked():
            return "both"
        elif self.rb_positive.isChecked():
            return "positive"
        else:
            return "negative"
    
    def get_ductility_method(self):
        """获取延性系数计算方法"""
        checked_button = self.ductility_method_group.checkedButton()
        if checked_button:
            return checked_button.property("method_value")
        return "geometric"
    
    def update_plot_only(self):
        """仅更新图形显示（不重新计算分析）"""
        if self.current_data:
            self.update_plot()
    
    def update_analysis(self):
        """更新所有分析"""
        if self.current_data is None:
            return
        
        try:
            self.extract_hysteresis_loops()
            self.extract_skeleton_curve()
            self.calculate_indices()
            self.calculate_ductility()
            self.update_plot()
            self.update_results()
            self.update_loop_info()
            
        except Exception as e:
            QMessageBox.critical(self, "分析错误", f"分析过程中出现错误:\n{str(e)}")

    def extract_hysteresis_loops(self):
        """提取滞回环"""
        displacement = self.current_data['displacement'].copy()
        force = self.current_data['force'].copy()
        
        if self.filter_first_loop.isChecked():
            displacement, force = self.filter_first_loops(displacement, force)
            self.current_data['displacement_filtered'] = displacement
            self.current_data['force_filtered'] = force
        
        self.hysteresis_loops = []
        peaks = []
        
        for i in range(1, len(displacement) - 1):
            if displacement[i] > displacement[i-1] and displacement[i] > displacement[i+1]:
                if displacement[i] > 0:
                    peaks.append({'index': i, 'type': 'positive', 
                                'disp': displacement[i], 'force': force[i]})
            elif displacement[i] < displacement[i-1] and displacement[i] < displacement[i+1]:
                if displacement[i] < 0:
                    peaks.append({'index': i, 'type': 'negative', 
                                'disp': displacement[i], 'force': force[i]})
        
        for i in range(len(peaks) - 1):
            start_idx = peaks[i]['index']
            end_idx = peaks[i+1]['index']
            
            loop_disp = displacement[start_idx:end_idx+1]
            loop_force = force[start_idx:end_idx+1]
            
            if len(loop_disp) > 2:
                area = self.calculate_loop_area(loop_disp, loop_force)
                self.hysteresis_loops.append({
                    'displacement': loop_disp,
                    'force': loop_force,
                    'peak_disp': peaks[i]['disp'],
                    'peak_force': peaks[i]['force'],
                    'area': area,
                    'type': peaks[i]['type']
                })
    
    def filter_first_loops(self, displacement, force):
        """过滤同级位移，仅保留第一圈"""
        abs_disp = np.abs(displacement)
        tolerance = 0.08
        
        peaks_indices = []
        for i in range(1, len(displacement) - 1):
            if (abs_disp[i] > abs_disp[i-1] and abs_disp[i] > abs_disp[i+1]):
                peaks_indices.append(i)
        
        if not peaks_indices:
            return displacement, force
        
        peak_values = abs_disp[peaks_indices]
        groups = []
        used = set()
        
        for i, peak_idx in enumerate(peaks_indices):
            if i in used:
                continue
            
            group = [peak_idx]
            peak_val = peak_values[i]
            
            for j, other_idx in enumerate(peaks_indices[i+1:], i+1):
                if j in used:
                    continue
                if abs(peak_values[j] - peak_val) <= tolerance * peak_val:
                    group.append(other_idx)
                    used.add(j)
            
            groups.append(group)
        
        keep_indices = set()
        for group in groups:
            if group:
                first_peak = min(group)
                start = max(0, first_peak - 50)
                end = min(len(displacement), first_peak + 50)
                keep_indices.update(range(start, end))
        
        if not keep_indices:
            return displacement, force
        
        keep_list = sorted(keep_indices)
        return displacement[keep_list], force[keep_list]
    
    def extract_skeleton_curve(self):
        """提取骨架曲线"""
        if not self.current_data:
            return
        
        displacement = self.current_data.get('displacement_filtered', 
                                             self.current_data['displacement'])
        force = self.current_data.get('force_filtered', 
                                      self.current_data['force'])
        
        method = self.get_skeleton_method()
        
        if method == "outer_envelope":
            self.skeleton_curve = self.extract_outer_envelope(displacement, force)
        else:
            self.skeleton_curve = self.extract_peak_points(displacement, force)
    
    def extract_outer_envelope(self, displacement, force):
        """方法1: 最外层包络线"""
        pos_envelope = {'disp': [0], 'force': [0]}
        neg_envelope = {'disp': [0], 'force': [0]}
        
        disp_threshold = max(0.01, np.max(np.abs(displacement)) * 0.005)
        force_threshold = max(0.01, np.max(np.abs(force)) * 0.01)
        
        max_disp = 0
        for i in range(len(displacement)):
            if (displacement[i] > disp_threshold and 
                displacement[i] > max_disp + disp_threshold * 0.1 and
                abs(force[i]) > force_threshold):
                max_disp = displacement[i]
                pos_envelope['disp'].append(displacement[i])
                pos_envelope['force'].append(force[i])
        
        min_disp = 0
        for i in range(len(displacement)):
            if (displacement[i] < -disp_threshold and 
                displacement[i] < min_disp - disp_threshold * 0.1 and
                abs(force[i]) > force_threshold):
                min_disp = displacement[i]
                neg_envelope['disp'].append(displacement[i])
                neg_envelope['force'].append(force[i])
        
        return {'positive': pos_envelope, 'negative': neg_envelope}
    
    def extract_peak_points(self, displacement, force):
        """方法2: 峰值点连接法"""
        peaks_pos = {'disp': [], 'force': []}
        peaks_neg = {'disp': [], 'force': []}
        
        disp_threshold = max(0.01, np.max(np.abs(displacement)) * 0.01)
        
        all_peaks = []
        for i in range(1, len(displacement) - 1):
            if (displacement[i] > displacement[i-1] and 
                displacement[i] > displacement[i+1] and 
                displacement[i] > disp_threshold):
                all_peaks.append({'index': i, 'type': 'positive', 
                                'disp': displacement[i], 'force': force[i]})
            elif (displacement[i] < displacement[i-1] and 
                  displacement[i] < displacement[i+1] and 
                  displacement[i] < -disp_threshold):
                all_peaks.append({'index': i, 'type': 'negative', 
                                'disp': displacement[i], 'force': force[i]})
        
        first_neg_peak_idx = None
        for peak in all_peaks:
            if peak['type'] == 'negative':
                first_neg_peak_idx = peak['index']
                break
        
        pos_peak_count = 0
        second_pos_peak_idx = None
        for peak in all_peaks:
            if peak['type'] == 'positive':
                pos_peak_count += 1
                if pos_peak_count == 2:
                    second_pos_peak_idx = peak['index']
                    break
        
        common_y_intercept = None
        if first_neg_peak_idx is not None and second_pos_peak_idx is not None:
            start_search = first_neg_peak_idx
            end_search = second_pos_peak_idx
            
            for j in range(start_search, end_search):
                if displacement[j] <= 0 and displacement[j+1] > 0:
                    if displacement[j+1] != displacement[j]:
                        t = -displacement[j] / (displacement[j+1] - displacement[j])
                        y_force = force[j] + t * (force[j+1] - force[j])
                        common_y_intercept = y_force
                        break
        
        if common_y_intercept is not None:
            peaks_pos['disp'].append(0)
            peaks_pos['force'].append(common_y_intercept)
            peaks_neg['disp'].append(0)
            peaks_neg['force'].append(common_y_intercept)
        else:
            peaks_pos['disp'].append(0)
            peaks_pos['force'].append(0)
            peaks_neg['disp'].append(0)
            peaks_neg['force'].append(0)
        
        pos_peaks_list = [p for p in all_peaks if p['type'] == 'positive']
        pos_peaks_sorted = sorted(pos_peaks_list, key=lambda x: x['disp'])
        
        max_pos = 0
        for peak in pos_peaks_sorted:
            if peak['disp'] > max_pos + disp_threshold * 0.1:
                max_pos = peak['disp']
                peaks_pos['disp'].append(peak['disp'])
                peaks_pos['force'].append(peak['force'])
        
        neg_peaks_list = [p for p in all_peaks if p['type'] == 'negative']
        neg_peaks_sorted = sorted(neg_peaks_list, key=lambda x: abs(x['disp']))
        
        max_neg = 0
        for peak in neg_peaks_sorted:
            if abs(peak['disp']) > abs(max_neg) + disp_threshold * 0.1:
                max_neg = peak['disp']
                peaks_neg['disp'].append(peak['disp'])
                peaks_neg['force'].append(peak['force'])
        
        return {'positive': peaks_pos, 'negative': peaks_neg}
    
    def calculate_indices(self):
        """计算所有评价指标"""
        if not self.current_data:
            return
        
        displacement = self.current_data.get('displacement_filtered', 
                                             self.current_data['displacement'])
        force = self.current_data.get('force_filtered', 
                                      self.current_data['force'])
        
        self.indices = {}
        
        max_pos_idx = np.argmax(displacement)
        max_neg_idx = np.argmin(displacement)
        self.indices['峰值位移'] = {
            '正向 (mm)': float(displacement[max_pos_idx]),
            '负向 (mm)': float(displacement[max_neg_idx])
        }
        
        max_force_idx = np.argmax(force)
        min_force_idx = np.argmin(force)
        self.indices['峰值荷载'] = {
            '正向 (N)': float(force[max_force_idx]),
            '负向 (N)': float(force[min_force_idx])
        }
        
        self.indices['残余变形 (mm)'] = float(displacement[-1])
        
        total_area = sum([loop['area'] for loop in self.hysteresis_loops])
        self.indices['滞回环总面积 (kN·mm)'] = total_area
        self.indices['累计耗能 (kN·mm)'] = total_area
        
        if self.skeleton_curve:
            pos_curve = self.skeleton_curve['positive']
            if len(pos_curve['disp']) > 1 and pos_curve['disp'][-1] != 0:
                K_sec = pos_curve['force'][-1] / pos_curve['disp'][-1]
                self.indices['割线刚度 (N/mm)'] = float(K_sec)
        
        if len(displacement) > 10:
            disp_threshold = max(0.001, np.max(np.abs(displacement)) * 0.001)
            force_threshold = max(0.01, np.max(np.abs(force)) * 0.001)
            
            start_idx = 0
            for i in range(len(force)):
                if abs(force[i]) > force_threshold and abs(displacement[i]) > disp_threshold:
                    start_idx = i
                    break
            
            n = max(5, min(20, len(displacement) // 10))
            end_idx = min(start_idx + n, len(displacement))
            
            if end_idx > start_idx + 2:
                disp_range = displacement[start_idx:end_idx]
                force_range = force[start_idx:end_idx]
                if len(disp_range) > 1 and np.ptp(disp_range) > disp_threshold:
                    K_initial = np.polyfit(disp_range, force_range, 1)[0]
                    self.indices['初始刚度 (N/mm)'] = float(K_initial)
        
        if total_area > 0 and self.skeleton_curve:
            pos_curve = self.skeleton_curve['positive']
            if len(pos_curve['disp']) > 1:
                max_disp = pos_curve['disp'][-1]
                max_force = pos_curve['force'][-1]
                S_OBE = 0.5 * abs(max_disp * max_force) * 2
                if S_OBE > 0:
                    he = total_area / (2 * np.pi * S_OBE)
                    self.indices['等效粘滞系数'] = float(he)
        
        if self.hysteresis_loops:
            loop_areas = [loop['area'] for loop in self.hysteresis_loops if loop['area'] > 0]
            if loop_areas:
                self.indices['平均环路耗能 (kN·mm)'] = np.mean(loop_areas)
                self.indices['最大环路耗能 (kN·mm)'] = np.max(loop_areas)
        
        self.calculate_degradation()
    
    def calculate_degradation(self):
        """计算强度退化和刚度退化"""
        if not self.hysteresis_loops or len(self.hysteresis_loops) < 2:
            return
        
        pos_loops = [l for l in self.hysteresis_loops if l['type'] == 'positive']
        neg_loops = [l for l in self.hysteresis_loops if l['type'] == 'negative']
        
        if len(pos_loops) >= 2:
            forces = [abs(l['peak_force']) for l in pos_loops]
            if forces[0] != 0:
                strength_deg = (forces[0] - forces[-1]) / forces[0] * 100
                self.indices['正向强度退化 (%)'] = float(strength_deg)
        
        if len(neg_loops) >= 2:
            forces = [abs(l['peak_force']) for l in neg_loops]
            if forces[0] != 0:
                strength_deg = (forces[0] - forces[-1]) / forces[0] * 100
                self.indices['负向强度退化 (%)'] = float(strength_deg)
        
        if '初始刚度 (N/mm)' in self.indices and '割线刚度 (N/mm)' in self.indices:
            K0 = self.indices['初始刚度 (N/mm)']
            Ks = self.indices['割线刚度 (N/mm)']
            if K0 != 0:
                stiffness_deg = (K0 - Ks) / K0 * 100
                self.indices['刚度退化 (%)'] = float(stiffness_deg)
    
    def calculate_ductility(self):
        """计算延性系数"""
        if not self.skeleton_curve:
            return
        
        method = self.get_ductility_method()
        direction = self.get_direction()
        
        curves_to_analyze = []
        if direction in ["positive", "both"]:
            curves_to_analyze.append(('positive', self.skeleton_curve['positive']))
        if direction in ["negative", "both"]:
            curves_to_analyze.append(('negative', self.skeleton_curve['negative']))
        
        for dir_name, curve in curves_to_analyze:
            if not curve or len(curve['disp']) < 3:
                continue
            
            disp = np.array(curve['disp'])
            force = np.array(curve['force'])
            
            if method == "geometric":
                ductility = self.calc_geometric_ductility(disp, force)
            elif method == "energy":
                ductility = self.calc_energy_ductility(disp, force)
            elif method == "park":
                ductility = self.calc_park_ductility(disp, force)
            elif method == "farthest":
                ductility = self.calc_farthest_ductility(disp, force)
            elif method == "asce":
                ductility = self.calc_asce_ductility(disp, force)
            elif method == "eeep":
                ductility = self.calc_eeep_ductility(disp, force)
            else:
                ductility = self.calc_elastic_yield_ductility(disp, force)
            
            key = f'延性系数-{dir_name} ({method})'
            self.indices[key] = float(ductility)
    
    def calc_geometric_ductility(self, disp, force):
        """几何作图法"""
        abs_force = np.abs(force)
        max_idx = np.argmax(abs_force)
        max_force = abs_force[max_idx]
        max_disp = abs(disp[max_idx])
        
        yield_force = 0.75 * max_force
        yield_idx = np.argmin(np.abs(abs_force[:max_idx+1] - yield_force))
        yield_disp = abs(disp[yield_idx])
        
        return max_disp / yield_disp if yield_disp > 0 else 1.0
    
    def calc_energy_ductility(self, disp, force):
        """能量法"""
        total_energy = self.calculate_loop_area(disp, force)
        max_disp = abs(disp[np.argmax(np.abs(disp))])
        max_force = abs(force[np.argmax(np.abs(force))])
        
        if max_force > 0:
            yield_disp = 2 * total_energy / max_force
            return max_disp / yield_disp if yield_disp > 0 else 1.0
        return 1.0
    
    def calc_park_ductility(self, disp, force):
        """Park法"""
        if len(disp) < 3:
            return 1.0
        
        K0 = 0
        for i in range(1, min(5, len(disp))):
            if abs(disp[i]) > 1e-6:
                K_temp = abs(force[i] / disp[i])
                if K_temp > K0:
                    K0 = K_temp
        
        if K0 == 0:
            return 1.0
        
        Ky = K0 / 3
        
        for i in range(2, len(disp)):
            if abs(disp[i]) > 1e-6:
                K_current = abs(force[i] / disp[i])
                if K_current <= Ky:
                    yield_disp = abs(disp[i])
                    max_disp = abs(disp[-1])
                    return max_disp / yield_disp if yield_disp > 0 else 1.0
        
        return 1.0
    
    def calc_farthest_ductility(self, disp, force):
        """最远点法"""
        max_idx = np.argmax(np.abs(disp))
        max_disp = disp[max_idx]
        max_force = force[max_idx]
        
        if abs(max_disp) < 1e-6:
            return 1.0
        
        max_dist = 0
        yield_idx = 0
        
        for i in range(1, max_idx):
            dist = abs(max_force * disp[i] - max_disp * force[i]) / np.sqrt(max_force**2 + max_disp**2)
            if dist > max_dist:
                max_dist = dist
                yield_idx = i
        
        yield_disp = abs(disp[yield_idx])
        return abs(max_disp) / yield_disp if yield_disp > 0 else 1.0
    
    def calc_asce_ductility(self, disp, force):
        """ASCE法"""
        abs_force = np.abs(force)
        max_force = np.max(abs_force)
        yield_force = 0.6 * max_force
        
        yield_idx = np.argmin(np.abs(abs_force - yield_force))
        yield_disp = abs(disp[yield_idx])
        max_disp = abs(disp[np.argmax(np.abs(disp))])
        
        return max_disp / yield_disp if yield_disp > 0 else 1.0
    
    def calc_eeep_ductility(self, disp, force):
        """EEEP法"""
        area = self.calculate_loop_area(disp, force)
        max_force = abs(force[np.argmax(np.abs(force))])
        max_disp = abs(disp[np.argmax(np.abs(disp))])
        
        if max_force > 0:
            yield_disp = area / max_force
            return max_disp / yield_disp if yield_disp > 0 else 1.0
        return 1.0
    
    def calc_elastic_yield_ductility(self, disp, force):
        """弹性屈服法"""
        K0 = 0
        for i in range(1, min(5, len(disp))):
            if abs(disp[i]) > 1e-6:
                K_temp = abs(force[i] / disp[i])
                if K_temp > K0:
                    K0 = K_temp
        
        if K0 == 0:
            return 1.0
        
        max_force = abs(force[np.argmax(np.abs(force))])
        yield_disp = max_force / K0 if K0 > 0 else 0
        max_disp = abs(disp[np.argmax(np.abs(disp))])
        
        return max_disp / yield_disp if yield_disp > 0 else 1.0
    
    def calculate_loop_area(self, displacement, force):
        """计算环路面积"""
        area = 0
        for i in range(len(displacement) - 1):
            area += 0.5 * (force[i] + force[i+1]) * (displacement[i+1] - displacement[i])
        return abs(area)
    
    def update_plot(self):
        """更新图形显示"""
        self.canvas.ax.clear()
        
        self.canvas.ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, which='both')
        self.canvas.ax.minorticks_on()
        self.canvas.ax.grid(True, which='minor', alpha=0.15, linestyle=':', linewidth=0.3)
        
        self.canvas.ax.set_xlabel(self.tr('Displacement (mm)'), fontsize=11, fontweight='bold')
        self.canvas.ax.set_ylabel(self.tr('Force (N)'), fontsize=11, fontweight='bold')
        
        if not self.current_data:
            self.canvas.draw()
            return
        
        displacement = self.current_data.get('displacement_filtered', 
                                            self.current_data['displacement'])
        force = self.current_data.get('force_filtered', 
                                    self.current_data['force'])
        
        plot_style = self.get_plot_style()
        
        # 绘制滞回曲线
        self.canvas.ax.plot(displacement, force, 'b-', linewidth=1.2, 
                    label=self.tr('Hysteresis Curve'), alpha=0.7, zorder=1)
        
        # 绘制骨架曲线
        if self.skeleton_curve:
            direction = self.get_direction()
            
            if direction in ["both", "positive"]:
                pos_curve = self.skeleton_curve['positive']
                if len(pos_curve['disp']) > 1:
                    pos_disp = np.array(pos_curve['disp'])
                    pos_force = np.array(pos_curve['force'])
                    
                    if plot_style == "smooth" and len(pos_disp) >= 4:
                        try:
                            x_smooth, y_smooth = self.interpolate_smooth(pos_disp, pos_force)
                            algo_name = self.get_smooth_algorithm()
                            self.canvas.ax.plot(x_smooth, y_smooth, 'r-', linewidth=2.5, 
                                    label=f'{self.tr("Positive Skeleton Curve")} ({algo_name})', zorder=3)
                            if self.show_original_points.isChecked():
                                self.canvas.ax.plot(pos_disp, pos_force, 'ro', markersize=6,
                                        zorder=4, label=self.tr('Skeleton Data Points'))
                        except Exception as e:
                            error_msg = self.tr('Smoothing failed').format(str(e))
                            print(error_msg)
                            self.statusBar().showMessage(error_msg, 3000)
                            self.canvas.ax.plot(pos_disp, pos_force, 'r-', linewidth=2.5, 
                                    marker='o', markersize=6, label=self.tr('Positive Skeleton Curve'), zorder=3)
                    else:
                        self.canvas.ax.plot(pos_disp, pos_force, 'r-', linewidth=2.5, 
                                marker='o', markersize=6, label=self.tr('Positive Skeleton Curve'), zorder=3)
                    
                    self.canvas.ax.plot(pos_curve['disp'][0], pos_curve['force'][0],
                            'ro', markersize=12, markerfacecolor='yellow',
                            markeredgewidth=2.5, 
                            label=f'{self.tr("Positive Skeleton Curve Start Point")}(0, {pos_curve["force"][0]:.3f})', zorder=4)
            
            if direction in ["both", "negative"]:
                neg_curve = self.skeleton_curve['negative']
                if len(neg_curve['disp']) > 1:
                    neg_disp = np.array(neg_curve['disp'])
                    neg_force = np.array(neg_curve['force'])
                    
                    if plot_style == "smooth" and len(neg_disp) >= 4:
                        try:
                            x_smooth, y_smooth = self.interpolate_smooth(neg_disp, neg_force)
                            algo_name = self.get_smooth_algorithm()
                            self.canvas.ax.plot(x_smooth, y_smooth, 'g-', linewidth=2.5,
                                    label=f'{self.tr("Negative Skeleton Curve")} ({algo_name})', zorder=3)
                            if self.show_original_points.isChecked():
                                self.canvas.ax.plot(neg_disp, neg_force, 'gs', markersize=6,
                                        zorder=4, label=self.tr('Skeleton Data Points'))
                        except Exception as e:
                            error_msg = self.tr('Smoothing failed').format(str(e))
                            print(error_msg)
                            self.statusBar().showMessage(error_msg, 3000)
                            self.canvas.ax.plot(neg_disp, neg_force, 'g-', linewidth=2.5, 
                                    marker='s', markersize=6, label=self.tr('Negative Skeleton Curve'), zorder=3)
                    else:
                        self.canvas.ax.plot(neg_disp, neg_force, 'g-', linewidth=2.5, 
                                marker='s', markersize=6, label=self.tr('Negative Skeleton Curve'), zorder=3)
                    
                    self.canvas.ax.plot(neg_curve['disp'][0], neg_curve['force'][0],
                            'gs', markersize=12, markerfacecolor='yellow',
                            markeredgewidth=2.5, 
                            label=f'{self.tr("Negative Skeleton Curve Start Point")}(0, {pos_curve["force"][0]:.3f})', zorder=4)
        
        # 标注峰值点
        if self.indices:
            if '峰值位移' in self.indices and '峰值荷载' in self.indices:
                pos_disp = self.indices['峰值位移']['正向 (mm)']
                neg_disp = self.indices['峰值位移']['负向 (mm)']
                
                pos_idx = np.argmax(displacement)
                neg_idx = np.argmin(displacement)
                pos_force = force[pos_idx]
                neg_force = force[neg_idx]
                
                self.canvas.ax.plot(pos_disp, pos_force, 'r*', markersize=18, 
                        label=f'{self.tr("Positive Peak")} ({pos_disp:.2f}, {pos_force:.2f})', zorder=5)
                self.canvas.ax.plot(neg_disp, neg_force, 'g*', markersize=18, 
                        label=f'{self.tr("Negative Peak")} ({neg_disp:.2f}, {neg_force:.2f})', zorder=5)
        
        # 设置图例和标题
        self.canvas.ax.legend(loc='best', fontsize=9)
        title = f"{self.tr('Force-Displacement Hysteresis Curve')} - {self.current_data['file_name']}"
        if self.filter_first_loop.isChecked():
            title += f" {self.tr('Filtered Label')}"
        if plot_style == "smooth":
            algo_name = self.get_smooth_algorithm()
            title += f" {self.tr('Smooth Label')}: {algo_name}]"
        self.canvas.ax.set_title(title, fontsize=12, fontweight='bold')
        
        self.canvas.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
        self.canvas.ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()
        
        if self.canvas.original_xlim is None:
            self.canvas.original_xlim = self.canvas.ax.get_xlim()
            self.canvas.original_ylim = self.canvas.ax.get_ylim()
    
    def update_results(self):
        """更新分析结果显示"""
        self.result_text.clear()
        
        if not self.indices:
            self.result_text.append(self.tr('No analysis results') + "\n")
            return
        
        text = "=" * 80 + "\n"
        text += f"         {self.tr('Force-Displacement Curve Analysis Report')}\n"
        text += "=" * 80 + "\n\n"
        
        text += f"{self.tr('File Information')}\n"
        text += f"  {self.tr('File name')}: {self.current_data['file_name']}\n"
        text += f"  {self.tr('Number of data points')}: {len(self.current_data['displacement'])}\n"
        text += f"  {self.tr('Number of hysteresis loops')}: {len(self.hysteresis_loops)}\n"
        if self.filter_first_loop.isChecked():
            text += f"  {self.tr('Data filtering')}: {self.tr('Enabled (first loop only)')}\n"
        
        # 获取骨架曲线提取方法的翻译
        method = self.get_skeleton_method()
        method_text = self.tr(method)
        text += f"  {self.tr('Skeleton curve extraction method')}: {method_text}\n"
            
        # 获取绘图样式的翻译
        style = self.get_plot_style()
        style_text = self.tr(style)
        text += f"  {self.tr('Plot style')}: {style_text}\n"
        
        # 获取平滑方法
        if self.get_plot_style() == "smooth":
            algo_index = self.smooth_algorithm.currentIndex()
            algo_names = ['PCHIP', 'Akima', 'Bezier', 'BSpline', 'SavitzkyGolay', 'UnivariateSpline', 'CubicSpline']
            text += f"  {self.tr('Smoothing algorithm')}: {algo_names[algo_index]}\n"
            if algo_index in [2, 3, 4, 5]:
                text += f"  {self.tr('Smoothing parameter')}: {self.smoothness_spinbox.value()}\n"
        text += "\n"
        
        # 获取骨架曲线信息
        if self.skeleton_curve:
            text += f"{self.tr('Skeleton Curve Starting Points')}\n"
            if 'positive' in self.skeleton_curve and len(self.skeleton_curve['positive']['disp']) > 0:
                pos_start_d = self.skeleton_curve['positive']['disp'][0]
                pos_start_f = self.skeleton_curve['positive']['force'][0]
                text += f"  {self.tr('Positive starting point')}: ({pos_start_d:.6f}, {pos_start_f:.6f})\n"
            
            if 'negative' in self.skeleton_curve and len(self.skeleton_curve['negative']['disp']) > 0:
                neg_start_d = self.skeleton_curve['negative']['disp'][0]
                neg_start_f = self.skeleton_curve['negative']['force'][0]
                text += f"  {self.tr('Negative starting point')}: ({neg_start_d:.6f}, {neg_start_f:.6f})\n"
            
            if self.get_skeleton_method() == 'peak_points':
                text += f"  {self.tr('Note: Common starting point crossing y-axis between first negative peak and second positive peak')}\n"
            text += "\n"
        
        text += f"{self.tr('Evaluation Metrics')}\n"
        text += "-" * 80 + "\n"
        
        # 创建指标映射字典（中文key -> 翻译key）
        index_translation_map = {
            '峰值位移': 'Peak displacement',
            '残余变形 (mm)': 'Residual deformation (mm)',
            '峰值荷载': 'Peak load',
            '初始刚度 (N/mm)': 'Initial stiffness (N/mm)',
            '割线刚度 (N/mm)': 'Secant stiffness (N/mm)',
            '滞回环总面积 (kN·mm)': 'Total hysteresis loop area (kN·mm)',
            '累计耗能 (kN·mm)': 'Cumulative energy dissipation (kN·mm)',
            '平均环路耗能 (kN·mm)': 'Average loop energy (kN·mm)',
            '最大环路耗能 (kN·mm)': 'Maximum loop energy (kN·mm)',
            '等效粘滞系数': 'Equivalent viscous damping coefficient',
            '正向强度退化 (%)': 'Positive strength degradation (%)',
            '负向强度退化 (%)': 'Negative strength degradation (%)',
            '刚度退化 (%)': 'Stiffness degradation (%)',
            '正向 (mm)': 'Positive (mm)',
            '负向 (mm)': 'Negative (mm)',
            '正向 (N)': 'Positive (N)',
            '负向 (N)': 'Negative (N)',
        }
        
        categories = {
            'Displacement-related': ['峰值位移', '残余变形 (mm)'],
            'Mechanical properties': ['峰值荷载', '初始刚度 (N/mm)', '割线刚度 (N/mm)'],
            'Energy metrics': ['滞回环总面积 (kN·mm)', '累计耗能 (kN·mm)', 
                    '平均环路耗能 (kN·mm)', '最大环路耗能 (kN·mm)'],
            'Coefficient metrics': ['等效粘滞系数'],
            'Degradation metrics': ['正向强度退化 (%)', '负向强度退化 (%)', '刚度退化 (%)'],
            'Ductility coefficient': [k for k in self.indices.keys() if '延性系数' in k]
        }
        
        for category_key, keys in categories.items():
            has_data = any(k in self.indices for k in keys)
            if has_data:
                text += f"\n■ {self.tr(category_key)}\n"
                for key in keys:
                    if key in self.indices:
                        # 翻译指标名称
                        translated_key = self.tr(index_translation_map.get(key, key))
                        value = self.indices[key]
                        
                        if isinstance(value, dict):
                            text += f"  {translated_key}:\n"
                            for sub_key, sub_value in value.items():
                                # 翻译子键
                                translated_sub_key = self.tr(index_translation_map.get(sub_key, sub_key))
                                text += f"    {translated_sub_key:20s} = {sub_value:12.4f}\n"
                        else:
                            text += f"  {translated_key:30s} = {value:12.4f}\n"
        
        text += "\n" + "=" * 80 + "\n"
        self.result_text.setPlainText(text)
    
    def update_loop_info(self):
        """更新滞回环详细信息"""
        self.loop_text.clear()
        
        if not self.hysteresis_loops:
            self.loop_text.append(self.tr('No hysteresis loop information') + "\n")
            return
        
        text = "=" * 90 + "\n"
        text += f"                        {self.tr('Detailed Hysteresis Loop Information')}\n"
        text += "=" * 90 + "\n\n"
        
        # 表头
        text += f"{self.tr('No.'):^6} {self.tr('Type'):^8} {self.tr('Peak Disp.'):^12} "
        text += f"{self.tr('Peak Force'):^12} {self.tr('Loop Area'):^15} {self.tr('Data Points'):^10}\n"
        text += "-" * 90 + "\n"
        
        # 数据行
        for i, loop in enumerate(self.hysteresis_loops, 1):
            loop_type = self.tr('Positive') if loop['type'] == 'positive' else self.tr('Negative')
            text += (f"{i:^6d} {loop_type:^8s} "
                    f"{loop['peak_disp']:^12.4f} {loop['peak_force']:^12.4f} "
                    f"{loop['area']:^15.4f} {len(loop['displacement']):^10d}\n")
        
        text += "\n" + "=" * 90 + "\n"
        text += f"{self.tr('Statistical Information')}\n"
        
        total_area = sum(loop['area'] for loop in self.hysteresis_loops)
        avg_area = total_area / len(self.hysteresis_loops) if self.hysteresis_loops else 0
        max_area = max((loop['area'] for loop in self.hysteresis_loops), default=0)
        min_area = min((loop['area'] for loop in self.hysteresis_loops), default=0)
        
        text += f"  {self.tr('Total loops')}: {len(self.hysteresis_loops)}\n"
        text += f"  {self.tr('Total energy dissipation')}: {total_area:.4f} kN·mm\n"
        text += f"  {self.tr('Average energy dissipation')}: {avg_area:.4f} kN·mm\n"
        text += f"  {self.tr('Maximum energy dissipation')}: {max_area:.4f} kN·mm\n"
        text += f"  {self.tr('Minimum energy dissipation')}: {min_area:.4f} kN·mm\n"
        
        pos_loops = [l for l in self.hysteresis_loops if l['type'] == 'positive']
        neg_loops = [l for l in self.hysteresis_loops if l['type'] == 'negative']
        
        text += f"\n  {self.tr('Positive loops')}: {len(pos_loops)}\n"
        text += f"  {self.tr('Negative loops')}: {len(neg_loops)}\n"
        text += "=" * 90 + "\n"
        
        self.loop_text.setPlainText(text)
    
    def clear_plot(self):
        """清空图形"""
        self.canvas.ax.clear()
        self.canvas.ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, which='both')
        self.canvas.ax.minorticks_on()
        self.canvas.ax.grid(True, which='minor', alpha=0.15, linestyle=':', linewidth=0.3)
        self.canvas.ax.set_xlabel('位移 (mm)', fontsize=11)
        self.canvas.ax.set_ylabel('力 (N)', fontsize=11)
        self.canvas.ax.set_title('力-位移滞回曲线', fontsize=12)
        self.canvas.draw()
    
    def save_state(self):
        """保存状态用于撤销"""
        state = {
            'data_files': [f.copy() for f in self.data_files],
            'current_data': self.current_data
        }
        self.history.append(state)
        
        if len(self.history) > 30:
            self.history.pop(0)
    
    def undo(self):
        """撤销操作"""
        if len(self.history) > 1:
            self.history.pop()
            last_state = self.history[-1]
            
            self.data_files = [f.copy() for f in last_state['data_files']]
            self.current_data = last_state['current_data']
            
            self.file_list.clear()
            for file in self.data_files:
                self.file_list.addItem(file['name'])
            
            if self.current_data:
                self.update_analysis()
            else:
                self.clear_plot()
    
    def delete_selected(self):
        """删除选中文件"""
        current_row = self.file_list.currentRow()
        if current_row >= 0:
            deleted_file = self.data_files[current_row]['name']
            self.data_files.pop(current_row)
            self.file_list.takeItem(current_row)
            
            if self.current_data and self.current_data['file_name'] == deleted_file:
                self.current_data = None
                self.clear_plot()
                self.result_text.clear()
                self.loop_text.clear()
            
            self.save_state()
            QMessageBox.information(self, self.tr("Deleted"), f"{self.tr('Deleted')} {deleted_file}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = HysteresisAnalyzer()
    window.show()
    
    sys.exit(app.exec())