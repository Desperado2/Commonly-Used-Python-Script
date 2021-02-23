import xlwt
import xlrd


def set_style(name, height, color_index, bold=False, center=False, border=False, bg=False, bgcolor=2):
    """
    设置表格样式
    :param name: 字体名称
    :param height: 字体大小
    :param color_index:  字体颜色
    :param bold: 是否加粗
    :param center: 是否居中
    :param border: 是否设置边框
    :param bg: 是否设置背景颜色
    :param bgcolor: 背景颜色
    :return: 表格样式
    """
    style = xlwt.XFStyle()
    # 设置字体
    font = xlwt.Font()
    # 字体名称
    font.name = name
    # 加粗
    font.bold = bold
    # 字体颜色
    font.colour_index = color_index
    # 字体高度
    font.height = height
    style.font = font
    # 居中
    if center:
        alm = xlwt.Alignment()
        alm.horz = xlwt.Alignment.HORZ_CENTER
        style.alignment = alm
        # 边框
    if border:
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.bottom = 1
        borders.top = 1
        style.borders = borders
    # 设置背景颜色
    if bg:
        pattern = xlwt.Pattern()
        # 设置背景颜色的模式
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        # 背景颜色
        pattern.pattern_fore_colour = bgcolor
        style.pattern = pattern
    return style


def write_single_sheet_excel(data_list: list, sheet_name: str = "new_sheet", excel_name: str = "excel.xls"):
    """
    写单sheet的excel文件
    :param excel_name: 生成的excel文件名称，默认excel.xls
    :param data_list: 数据列表，类似于[(),(),()]这种结构
    :param sheet_name: sheet的名称,默认为new_sheet
    :return: 无返回
    """
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(sheetname=sheet_name)
    row_number = 0
    for datas in data_list:
        col_number = 0
        for data in datas:
            worksheet.write(row_number, col_number, data, set_style('Arial', 200, 4))
            col_number += 1
        row_number += 1
    workbook.save(excel_name)


def write_many_sheet_excel(data_sheet_list: list,  excel_name: str = "excel.xls"):
    """
    写多sheet的excel文件
    :param excel_name: 生成的excel文件名称，默认excel.xls
    :param data_sheet_list: 数据和sheet名称的列表，类似于[(sheet_name,[(),(),()]),(sheet_name,[(),(),()])]这种结构
    :return: 无返回
    """
    workbook = xlwt.Workbook(encoding='ascii')
    for sheet_name, data_list in data_sheet_list:
        worksheet = workbook.add_sheet(sheetname=sheet_name)
        row_number = 0
        for datas in data_list:
            col_number = 0
            for data in datas:
                worksheet.write(row_number, col_number, data, set_style('Arial', 200, 4))
                col_number += 1
            row_number += 1
    workbook.save(excel_name)


def read_excel(excel_name: str):
    """
    读取excel文件内容
    :param excel_name: 要读取的excel文件名称
    :return: excel文件内容
    """
    result_list = []
    workbook = xlrd.open_workbook(filename=excel_name)
    sheet_names = workbook.sheet_names()
    for sheet_name in sheet_names:
        sheet = workbook.sheet_by_name(sheet_name=sheet_name)
        rows = sheet.nrows
        cols = sheet.ncols
        sheet_data_list = []
        for row_number in range(0, rows):
            row_data_list = []
            for col_number in range(0, cols):
                cell_data = sheet.cell_value(row_number, col_number)
                row_data_list.append(cell_data)
            sheet_data_list.append(tuple(row_data_list))
        result_list.append((sheet_name, sheet_data_list))
    return result_list


if __name__ == '__main__':
    # 测试单个sheet写入
    data_list = [("jack", 22, "男"), ("Tom", 20, "男"), ("Alice", 22, "女"), ("Jerry", 22, "男")]
    write_single_sheet_excel(data_list=data_list, sheet_name="user", excel_name="single_sheet_user.xls")

    # 测试excel读取
    result_data = read_excel(excel_name='single_sheet_user.xls')
    print(result_data)

    # 测试多个sheet写入
    data_list = [
        ("user1",  [("jack", 22, "男"), ("Tom", 20, "男"), ("Alice", 22, "女"), ("Jerry", 22, "男")]),
        ("user2",  [("jack", 22, "男"), ("Tom", 20, "男"), ("Alice", 22, "女"), ("Jerry", 22, "男")]),
        ("user3",  [("jack", 22, "男"), ("Tom", 20, "男"), ("Alice", 22, "女"), ("Jerry", 22, "男")]),
    ]
    write_many_sheet_excel(data_sheet_list=data_list, excel_name="many_sheet_user.xls")

    # 测试excel读取
    result_data = read_excel(excel_name='many_sheet_user.xls')
    print(result_data)
