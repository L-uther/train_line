import ezdxf

# 打开 DWG 文件
dwg = ezdxf.readfile("坐标系.dxf")

# 获取图形模型
modelspace = dwg.modelspace()

# 遍历图形模型中的所有图形
for entity in modelspace:
    # 判断是否是线段
    if entity.dxftype() == 'LINE':
        # 提取线段的起点坐标和终点坐标
        start_point = entity.dxf.start
        end_point = entity.dxf.end
        print("Start Point:", start_point)
        print("End Point:", end_point)