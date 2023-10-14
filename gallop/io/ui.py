import os

import wx


def get_path(wildcard: str = "") -> str:
    """Simply gui to get file path

    Args:
        wildcard (str, optional): can be a filter to only display specific file types. Examples: "*.csv", "*.json", "*.py". Defaults to "".

    Returns:
        str: path to file
    """
    current_dir = os.getcwd()
    app = wx.App(redirect=False)

    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.STAY_ON_TOP
    dialog = wx.FileDialog(
        None, "Select", defaultDir=current_dir, wildcard=wildcard, style=style
    )
    if dialog.ShowModal() == wx.ID_OK:
        path: str = dialog.GetPath()
    else:
        path: str = ""
    dialog.Destroy()
    app.Destroy()
    return path
