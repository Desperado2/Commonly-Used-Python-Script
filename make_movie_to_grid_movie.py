import PySimpleGUI as sg
import os
import time
import shutil
import queue
import threading
from PIL import Image
from moviepy.editor import *


def sort_strings_with_emb_numbers(image_paths):
    """
    排序图片，防止乱序
    :param image_paths: 图片路径列表
    :return: 排序后的图片路径列表
    """
    return image_paths.sort()


def mkdir_folder(file_path):
    """
    创建一个文件夹，如果不存在就创建；否则不做处理
    :param file_path:
    :return:
    """
    if os.path.exists(file_path):
        return

    os.mkdir(file_path)


def get_audio_from_video(video_raw_clip, output_path):
    """
    从视频中提取音频
    :param video_raw_clip: 视频Clip对象
    :param output_path: 输出音频文件完整路径
    :return:
    """
    audio = video_raw_clip.audio
    audio.write_audiofile(output_path)

    return output_path


def pics_to_video(pics_path, output_path, fps):
    """
    图片转为视频
    pics_to_video('./../gif_temp/', './../video_temp/temp1.mp4', 20)
    :param pics_path:
    :param output_path:
    :return:
    """
    image_paths = list(map(lambda x: pics_path + x, os.listdir(pics_path)))

    # 注意：这里必须进行一次排序，保证所有帧的顺序是一致
    image_paths = sort_strings_with_emb_numbers(image_paths)

    # 过滤掉非图片
    image_paths = list(filter(lambda image_path: image_path.endswith('.jpg'), image_paths))

    # 图片剪辑类
    clip = ImageSequenceClip(image_paths,
                             fps=fps)

    clip.write_videofile(output_path)


def video_with_audio(path_video_raw, path_bgm_raw, output):
    """
    视频合成音频
    :return:
    """
    videoclip = VideoFileClip(path_video_raw)
    audioclip = AudioFileClip(path_bgm_raw)

    # 设置视频音频，并写入到文件中去
    videoclip.set_audio(audioclip).write_videofile(output,
                                                   codec='libx264',
                                                   audio_codec='aac',
                                                   temp_audiofile='temp-audio.m4a',
                                                   remove_temp=True
                                                   )


def remove_folder(file_path):
    """
    删除文件夹
    :param file_path:
    :return:
    """
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    elif os.path.isfile(file_path):
        os.remove(file_path)
    else:
        pass


def create_video(file_path, file_name):
    path_temp = os.getcwd() + '/temp/'
    path_output = os.getcwd() + '/out/'
    item_space = 10

    # 新建临时文件夹和输出文件夹
    mkdir_folder(path_temp)
    mkdir_folder(path_output)

    video_raw_clip = VideoFileClip(file_path)

    # 宽、高
    video_width, video_height = video_raw_clip.w, video_raw_clip.h

    # 帧率
    fps = video_raw_clip.fps

    # 视频时长
    during = video_raw_clip.duration

    get_audio_from_video(video_raw_clip, path_output + "/temp.mp3")

    index = 1
    for frame in video_raw_clip.iter_frames():
        image = Image.fromarray(frame)

        # 视频帧图片保存的临时路径（完整路径）
        frame_file_complete_path = path_temp + "%04d.jpg" % index

        index += 1
        # 1、剪成9张图片，计算每张图片的宽、高
        item_width = int(video_width / 3)
        item_height = int(video_height / 3)

        # 2、新的宽、高
        item_width_new = video_width + item_space * 2
        item_height_new = video_height + item_space * 2

        # 3、重新建一个画布背景
        new_image = Image.new(image.mode, (item_width_new, item_height_new),
                              color='white')

        # 4、裁剪图片，然后粘贴到新的画布中去
        # i:横向、j：纵向
        for i in range(0, 3):
            for j in range(0, 3):
                # 裁剪区域
                box = (j * item_width, i * item_height, (j + 1) * item_width, (i + 1) * item_height)

                # 根据区域，裁剪图片
                crop_image = image.crop(box)

                # 横向、纵向第2块和第3块，要加上偏移距离
                x = 0 if j == 0 else (item_width + item_space) * j
                y = 0 if i == 0 else (item_height + item_space) * i

                # 将9张图片，按照上面计算的坐标值，粘贴到背景中去
                new_image.paste(crop_image, (int(x), int(y)))

                # 保存图片到本地
                new_image.save(frame_file_complete_path)

    pics_to_video(path_temp, path_output + "/temp.mp4", fps)
    video_with_audio(path_output + "temp.mp4", path_output + "temp.mp3", path_output + file_name + ".mp4")
    # 删除临时文件
    remove_folder(path_temp)
    remove_folder(path_output + "temp.mp4")
    remove_folder(path_output + "temp.mp3")


gui_queue = queue.Queue()
sg.ChangeLookAndFeel('GreenTan')  # 更换主题
menu_def = [['&使用说明', ['&注意']]]
layout = [
    [sg.Menu(menu_def, tearoff=True)],
    [sg.Text('原视频位置', size=(8, 1), auto_size_text=False, justification='right'),
     sg.InputText(enable_events=True, key="lujing"), sg.FileBrowse()],
    [sg.Text('新视频名字', size=(8, 1), justification='right'),
     sg.InputText(enable_events=True, key="wenjian")],
    [sg.Submit(tooltip='文件'), sg.Cancel()]]

window = sg.Window('视频转换器', layout, default_element_size=(40, 1), grab_anywhere=False)
while True:
    event, values = window.read()
    if event == "Submit":
        if values["lujing"] is None:
            sg.Popup("文件不能为空")
        else:
            filename = values['wenjian']
            if values['wenjian'] is None:
                filename = time.strftime("%Y%m%d%H%m%s", time.localtime())
            threading.Thread(target=create_video, args=(values["lujing"], filename), daemon=True).start()
            sg.Popup("开始转换，请稍后，转换成功文件地址:" + os.getcwd() + '/out/')
    if event == "Cancel" or event == sg.WIN_CLOSED:
        break
    if event == "注意":
        sg.Popup("作用讲解：",
                 "将视频转换为九宫格视频",
                 "转换后的视频位置，当前目录下面的out文件夹中")
window.close()
