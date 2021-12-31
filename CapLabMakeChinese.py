import json
from os import sep, getcwd
from os.path import isfile, isdir

import wx


class CapLabMakeChinese(wx.Frame):
    saveFileName = 'Trans_CapLabMakeChinese.txt'
    saveFolderPath = ''
    cache_Translation = {}
    namespace = 'CAPLAB'

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"CapLab简易中文编辑助手", pos=wx.DefaultPosition,
                          size=wx.Size(328, 244),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE | wx.MINIMIZE_BOX | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.SelectMainExecutePathButton = wx.Button(self, wx.ID_ANY, u"选择CapMain.exe路径", wx.DefaultPosition,
                                                     wx.DefaultSize, 0)
        self.SelectMainExecutePathButton.SetFont(
            wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        self.SelectMainExecutePathButton.SetToolTip(u"选择CapMain.exe（金融帝国实验室的主程序）的所在路径，或者直接把本程序放在游戏目录下即可。")

        bSizer1.Add(self.SelectMainExecutePathButton, 0, wx.ALL | wx.EXPAND, 5)

        self.SaveTranslationButton = wx.Button(self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0)
        self.SaveTranslationButton.SetFont(
            wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        self.SaveTranslationButton.Enable(False)
        self.SaveTranslationButton.SetToolTip(u"保存结果。")

        bSizer1.Add(self.SaveTranslationButton, 0, wx.ALL | wx.EXPAND, 5)

        SelectChineseUnitChoiceChoices = []
        self.SelectChineseUnitChoice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                 SelectChineseUnitChoiceChoices, wx.CB_SORT)
        self.SelectChineseUnitChoice.SetSelection(0)
        self.SelectChineseUnitChoice.Enable(False)

        bSizer1.Add(self.SelectChineseUnitChoice, 0, wx.ALL | wx.EXPAND, 5)

        gSizer1 = wx.GridSizer(0, 3, 0, 0)

        self.AddNewUnitButton = wx.Button(self, wx.ID_ANY, u"新增", wx.DefaultPosition, wx.DefaultSize, 0)
        self.AddNewUnitButton.SetFont(
            wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        self.AddNewUnitButton.Enable(False)

        gSizer1.Add(self.AddNewUnitButton, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"汉化名称-->", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        gSizer1.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.InputChineseTextEntry = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, -1),
                                                 0)
        self.InputChineseTextEntry.Enable(False)

        gSizer1.Add(self.InputChineseTextEntry, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

        self.DeleteThisUnitButton = wx.Button(self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0)
        self.DeleteThisUnitButton.SetFont(
            wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        self.DeleteThisUnitButton.Enable(False)
        self.DeleteThisUnitButton.SetToolTip(u"删除当前记录")

        gSizer1.Add(self.DeleteThisUnitButton, 0, wx.ALL | wx.EXPAND, 5)

        self.m_static2 = wx.StaticText(self, wx.ID_ANY, u"输入代号-->", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_static2.Wrap(-1)

        gSizer1.Add(self.m_static2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.InputCodeTextEntry = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                              wx.TE_READONLY)
        self.InputCodeTextEntry.Enable(False)

        gSizer1.Add(self.InputCodeTextEntry, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.SelectMainExecutePathButton.Bind(wx.EVT_BUTTON, self.SelectMainExecutePathButtonOnButtonClick)
        self.SaveTranslationButton.Bind(wx.EVT_BUTTON, self.SaveTranslationButtonOnButtonClick)
        self.SelectChineseUnitChoice.Bind(wx.EVT_CHOICE, self.SelectChineseUnitChoiceOnChoice)
        self.AddNewUnitButton.Bind(wx.EVT_BUTTON, self.AddNewUnitButtonOnButtonClick)
        self.InputChineseTextEntry.Bind(wx.EVT_KILL_FOCUS, self.InputChineseTextEntryOnKillFocus)
        self.DeleteThisUnitButton.Bind(wx.EVT_BUTTON, self.DeleteThisUnitButtonOnButtonClick)

        # Init
        if isfile('CLMC.json'):
            try:
                tF = open('CLMC.json', 'r', encoding='UTF-8')
                tD: dict = json.load(tF)
                tF.close()
                self.saveFolderPath = tD.get('folder')
            finally:
                pass
        elif isfile('CapMain.exe') and isdir('./Translate'):
            self.saveFolderPath = getcwd() + sep + 'Translate' + sep
        else:
            self.selectCapMainEXEPath()
        if isdir(self.saveFolderPath):
            self.enableAllButton()
            self.saveConfigFile()
            self.loadTranslateFile()

    # Virtual event handlers, override them in your derived class
    def SelectMainExecutePathButtonOnButtonClick(self, event):
        if self.selectCapMainEXEPath():
            self.enableAllButton()
            self.saveConfigFile()
        event.Skip()

    def SaveTranslationButtonOnButtonClick(self, event):
        if self.saveTranslateFile():
            wx.MessageDialog(self, '保存成功！下一次启动游戏后输入对应代号生效！', '保存', wx.OK | wx.ICON_INFORMATION).ShowModal()
        else:
            wx.MessageDialog(self, '保存失败！请检查磁盘空间或文件是否被占用！', '失败', wx.OK | wx.ICON_ERROR).ShowModal()
        event.Skip()

    def SelectChineseUnitChoiceOnChoice(self, event):
        tVar: str = self.SelectChineseUnitChoice.GetStringSelection()
        if tVar in self.cache_Translation.keys():
            self.InputChineseTextEntry.SetValue(tVar)
            self.InputCodeTextEntry.SetValue(self.cache_Translation.get(tVar))
        else:
            self.updateChoiceList()
        event.Skip()

    def AddNewUnitButtonOnButtonClick(self, event):
        cache_order = []
        for unitKey in self.cache_Translation.values():
            if isinstance(unitKey, str) and unitKey.startswith(self.namespace) and unitKey[6:].isdigit():
                cache_order.append(int(unitKey[6:]))
        cache_order.sort()
        if len(cache_order) == 0:
            self.InputCodeTextEntry.SetValue(self.namespace + '1')
        else:
            self.InputCodeTextEntry.SetValue(self.namespace + '%d' % (cache_order[-1] + 1))
        self.InputChineseTextEntry.Clear()
        self.InputChineseTextEntry.SetFocus()
        event.Skip()

    def InputChineseTextEntryOnKillFocus(self, event):
        tStr: str = self.InputChineseTextEntry.GetValue().strip()
        if len(tStr) > 0:
            self.cache_Translation[tStr] = self.InputCodeTextEntry.GetValue()
            self.InputChineseTextEntry.SetValue(tStr)
            self.updateChoiceList()
        else:
            self.InputCodeTextEntry.Clear()
            self.InputChineseTextEntry.Clear()
        event.Skip()

    def DeleteThisUnitButtonOnButtonClick(self, event):
        tVar: str = self.InputChineseTextEntry.GetValue().strip()
        if tVar in self.cache_Translation.keys():
            self.cache_Translation.pop(tVar)
            self.InputChineseTextEntry.Clear()
            self.InputCodeTextEntry.Clear()
            self.updateChoiceList()
        event.Skip()

    # 内部规程
    def selectCapMainEXEPath(self):
        fileDialog = wx.FileDialog(self, '指定CapMain.exe路径', defaultFile='CapMain.exe',
                                   wildcard='金融帝国实验室主程序（CapMain.exe）|*.exe',
                                   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        fileDialog.ShowModal()
        capMain_path: str = fileDialog.GetPath()
        fileDialog.Destroy()
        if isfile(capMain_path):
            capMain_folder_path = sep.join(capMain_path.split(sep)[:-1]) + sep + 'Translate' + sep
            if isdir(capMain_folder_path):
                self.saveFolderPath = capMain_folder_path
                return True
        return False

    def loadTranslateFile(self):
        """加载已有的翻译文件"""
        filePath = self.saveFolderPath + self.saveFileName
        if isfile(filePath):
            tF = open(filePath, 'r', encoding='UTF-8')
            for unit in ''.join(tF.read().splitlines()).split('|~')[:-1]:
                slice_unit = unit.split('|')
                self.cache_Translation[slice_unit[1]] = slice_unit[0]
            tF.close()
        self.updateChoiceList()

    def saveTranslateFile(self):
        """保存翻译文件"""
        filePath = self.saveFolderPath + self.saveFileName
        cache_text = ''
        LF = '\n'
        for unit in self.cache_Translation.keys():
            cache_text += self.cache_Translation.get(unit) + '|' + LF + \
                          unit + '|' + LF + '~' + LF
        try:
            tF = open(filePath, 'w', encoding='UTF-8')
            tF.write(cache_text)
            tF.close()
            return True
        except:
            return False

    def saveConfigFile(self):
        if isdir(self.saveFolderPath):
            try:
                tF = open('CLMC.json', 'w', encoding='UTF-8')
                json.dump({'folder': self.saveFolderPath}, tF)
                tF.close()
            finally:
                pass

    def enableAllButton(self):
        self.SelectMainExecutePathButton.Disable()
        self.AddNewUnitButton.Enable()
        self.DeleteThisUnitButton.Enable()
        self.SaveTranslationButton.Enable()
        self.InputChineseTextEntry.Enable()
        self.InputCodeTextEntry.Enable()
        self.SelectChineseUnitChoice.Enable()

    def updateChoiceList(self):
        tVar = list(self.cache_Translation.keys())
        self.SelectChineseUnitChoice.SetItems(tVar)
        self.SelectChineseUnitChoice.SetSelection(len(tVar) - 1)


if __name__ == '__main__':
    mainAPP = wx.App()
    mainWin = CapLabMakeChinese(None)
    mainWin.Show()
    mainAPP.MainLoop()
