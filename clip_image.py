# -*- coding: utf-8 -*-
"""
windows下，使用ctrl+C复制图片文件之后,在剪切板中保存的内容并非图片内容,而是图片文件的路径,导致picgo无法直接使用
本脚本获取剪切板中的图片文件路径,读取图片文件,将图片内容重新写入剪切板中。之后就可以使用picgo上传到图床了

"""

from io import BytesIO

from PIL import Image

import win32clipboard


def get_image_path():
    """
    从剪切板中获取文件路径

    Returns
    -------
    filenames: tuple
        选中的所有文件的路径
    """

    win32clipboard.OpenClipboard()
    filenames = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
    win32clipboard.CloseClipboard()
    for filename in filenames:
        print(filename)
    return filenames


def send_to_clipboard(clip_type, data):
    """
    将image data写入到clipboard中

    Parameters
    ----------
    clip_type : 剪切板支持的CF_DIB格式
    data : 字节流数据

    """

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


if __name__ == "__main__":

    if not win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
        filenames = get_image_path()
        for filepath in filenames:
            image = Image.open(filepath)

            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            send_to_clipboard(win32clipboard.CF_DIB, data)
