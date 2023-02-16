#!/usr/bin/python3

from reportlab.pdfbase import pdfmetrics   # 注册字体
from reportlab.pdfbase.ttfonts import TTFont # 字体类
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image # 报告内容相关类
from reportlab.lib.pagesizes import letter, landscape # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # 文本样式
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors  # 颜色模块
from reportlab.graphics.charts.barcharts import VerticalBarChart  # 图表类
from reportlab.graphics.charts.legends import Legend  # 图例类
from reportlab.graphics.shapes import Drawing  # 绘图工具
from reportlab.lib.units import cm  # 单位：cm
 
# 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)
pdfmetrics.registerFont(TTFont('SimSun', "./NotoSansSCRegular.ttf"))


class PdfMaker:
    # 绘制标题
    content_style = ParagraphStyle(name="ContentStyle", fontName="ping", fontSize=18, leading=25, spaceAfter=20,
                                            underlineWidth=1, alignment=TA_LEFT, )
    @staticmethod
    def draw_title(title, size=20):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'      # 字体名
        ct.fontSize = size           # 字体大小
        ct.leading = 50             # 行间距
        ct.textColor = colors.black     # 字体颜色
        ct.alignment = 1    # 居中
        ct.bold = True
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)
      
  # 绘制小标题
    @staticmethod
    def draw_little_title(title, size=20 , color=colors.black):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = size  # 字体大小
        ct.leading = 30  # 行间距
        ct.textColor = color   # 字体颜色
        ct.bold = True
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)
 
    # 绘制普通段落内容
    @staticmethod
    def draw_text(text, size):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 获取普通样式
        ct = style['Normal']
        ct.fontName = 'SimSun'
        ct.fontSize = size
        ct.wordWrap = 'CJK'     # 设置自动换行
        ct.alignment = 0        # 左对齐
        ct.firstLineIndent = 32     # 第一行开头空格
        ct.leading = 25
        return Paragraph(text, ct)
 
    # 绘制表格
    @staticmethod
    def draw_table(style, *args, totalWidth, rowHeight=30, rates):
        total_rate = 0
        for rate in rates:
            total_rate += rate
        
        col_rate = []
        for rate in rates:
            col_rate.append((rate/total_rate) * totalWidth)

        table = Table(args, colWidths=col_rate,  style=style, rowHeights=rowHeight)
        return table

    #跨页合并需求
    @staticmethod
    def draw_mul_table(style, *args, totalWidth, rates):
        total_rate = 0
        for rate in rates:
            total_rate += rate
        
        col_rate = []
        for rate in rates:
            col_rate.append((rate/total_rate) * totalWidth)
            
        i = 0
        begin = 0
        end = 0
        while i < len(args)-1:
            if args[i+1][0] == args[i][0] :
                if i +1 == len(args)-1:
                    end = len(args)-1
                    style = style + [
                        ('SPAN', (0, begin), (0, end))  
                    ]
            else:
                end = i
                style = style + [
                        ('SPAN', (0, begin), (0, end))  
                    ] 

                begin = end + 1
        
            i += 1

        table = Table(args, colWidths=col_rate,  style=style, rowHeights=30)
            # i += 15
        return table
 
    # 创建图表
    @staticmethod
    def draw_bar(bar_data: list, ax: list, items: list):
        drawing = Drawing(500, 250)
        bc = VerticalBarChart()
        bc.x = 45       # 整个图表的x坐标
        bc.y = 45      # 整个图表的y坐标
        bc.height = 200     # 图表的高度
        bc.width = 350      # 图表的宽度
        bc.data = bar_data
        bc.strokeColor = colors.black         # 顶部和右边轴线的颜色
        bc.valueAxis.valueMin = 5000          # 设置y坐标的最小值
        bc.valueAxis.valueMax = 26000         # 设置y坐标的最大值
        bc.valueAxis.valueStep = 2000         # 设置y坐标的步长
        bc.categoryAxis.labels.dx = 2
        bc.categoryAxis.labels.dy = -8
        bc.categoryAxis.labels.angle = 20
        bc.categoryAxis.categoryNames = ax
 
        # 图示
        leg = Legend()
        leg.fontName = 'SimSun'
        leg.alignment = 'right'
        leg.boxAnchor = 'ne'
        leg.x = 475         # 图例的x坐标
        leg.y = 240
        leg.dxTextSpace = 10
        leg.columnMaximum = 3
        leg.colorNamePairs = items
        drawing.add(leg)
        drawing.add(bc)
        return drawing
 
    # 绘制图片
    @staticmethod
    def draw_img(path):
        img = Image(path)       # 读取指定路径下的图片
        img.drawWidth = 5*cm        # 设置图片的宽度
        img.drawHeight = 8*cm       # 设置图片的高度
        return img

    def create_pdf(filename, content):
        # 生成pdf文件
        doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
        doc.build(content)


