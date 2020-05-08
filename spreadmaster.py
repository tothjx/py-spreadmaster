import wx
import time
import os
from PIL import Image as img
# import sys
# import string

title = 'SpreadMaster'


class SpreadFrame(wx.Frame):
    ################################
    # CONFIG
    ################################
    title = 'SpreadMaster'
    version = '1.0.2'
    description = 'Oldalpárok vágása JPG formátumú képekből...'
    author = 'Tóth József'
    email = 'tothjx@gmail.com'
    separator = '----------------------------------------------------------------'
    label_source_dir = 'Eredeti file-ok útvonala a file-rendszerben (forráskönyvtár):'
    label_target_dir = 'Vágott file-ok útvonala a file-rendszerben (célkönyvtár):'
    label_log_box = 'Elvégzett műveletek naplózása:'
    label_about = 'névjegy...'
    label_clipboard = 'napló másolása...'
    label_help = 'súgó...'
    label_close = 'bezárás...'
    label_crop = 'vágás...'.upper()
    label_version_number = 'verziószám'
    label_further_info = 'további információ'
    label_author = 'szerző'
    source_dir_default = 'C:\\out\\original\\'
    target_dir_default = 'C:\\out\\crop\\'
    msg_dir_src = 'Eredeti file-okat tartalmazó könyvtár kiválasztása...'
    msg_dir_tar = 'Vágott file-okat tartalmazó könyvtár kiválasztása...'
    msg_set_source_dir = 'Eredeti file-ok könyvtára beállítva:'
    msg_set_target_dir = 'Vágott file-ok könyvtára beállítva:'
    msg_all_images_num = 'A könyvtárban összesen %s file található...'
    msg_no_images = 'A választott forráskönyvtárban nem találhatóak file-ok. Kérem válasszon másik könyvtárat!'
    msg_target_not_empty = 'Figyelem, a kiválasztott célkönyvtár nem üres! Célszerű vágás előtt törölni a benne lévő file-okat. Ha a törlés elmarad, a program, a már létező file-okat kérdés nélkül felülírja.'
    msg_target_empty = 'A kiválasztott célkönyvtár üres, tárolásra alkalmas.'
    msg_orig_spread = 'Eredeti oldalpár'
    msg_left_saved = 'Bal oldal mentve'
    msg_right_saved = 'Jobb oldal mentve'
    msg_final_success = 'A képek vágása befejeződött, a darabolt oldalak a %s könyvtárban elérhetőek.'
    msg_clipboard_success = 'A napló tartalmának vágólapra másolása sikerült.'
    msg_clipboard_error = 'A napló tartalmának vágólapra másolása NEM sikerült.'
    log_txt_default = 'Napló indítása...\n'
    files = []
    help_text = 'A program használatához ki kell választani a forrás- és célkönyvtárakat. A forráskönyvtárban kell elhelyezni az oldalpárokat tartalmazó JPG formátumú képeket. Nagyon fontos: a program jelenleg csak ezt a formátumot támogatja.' + \
            '\n' + 'A könyvtár-választó szövegmezők mögött van egy gomb, amivel ki lehet tallózni a kívánt könyvtárakat. Ha a forráskönyvtár üres, azt a program jelzi a nagy mezőben, ahol naplóz minden műveletet (ezeket érdemes figyelemmel követni). Ha a kiválasztott célkönyvtárban vannak file-ok, arra a program a napló szövegében figyelmeztet, de a vágás elvégezhető. A már létező file-ok automatikusan felülírásra kerülnek.' + \
            '\n\n' + 'Ha a könyvtárak rendben vannak, a művelet a VÁGÁS... feliratú gombbal indítható. A sikeres futásról a naplóban lehet tájékozódni. A vágás és mentés után a vágott képek file-neve megegyezik az eredeti file-névvel, annyi kitétellel, hogy a bal oldalt tartalmazó kép neve kiegészül egy 1-essel, míg a jobb oldali egy 2-essel.' + \
            '\n\n' + 'És végül: a napló másolása gomb használata akkor lehet hasznos, ha valami hiba történik a futtatás során. A napló tartalma a vágólapra másolódik, és levélben elküldhető. Ennek segítségével tudom a hibát lokalizálni majd javítani.'

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self,*args, **kw)
        if title in vars():
            self.title = title
        ################################
        # PANEL
        ################################
        self.set_dirs()
        self.set_panel()
        self.log_init()

        # Set event handlers
        # self.button.Bind(wx.EVT_BUTTON, self.OnButton)

    def set_dirs(self):
        sd = self.source_dir_default
        td = self.target_dir_default
        source_dir_exists = os.path.isdir(sd)
        target_dir_exists = os.path.isdir(td)
        if source_dir_exists == False:
            os.makedirs(sd)

        if target_dir_exists == False:
            os.makedirs(td)

    # SET PANEL
    def set_panel(self):
        self.panel = wx.Panel(self)

        ################################
        # LABELS
        ################################
        self.label_source = wx.StaticText(self.panel, label=self.label_source_dir, pos=(15, 15))
        self.label_target = wx.StaticText(self.panel, label=self.label_target_dir, pos=(15, 45))
        self.label_log_box = wx.StaticText(self.panel, label=self.label_log_box, pos=(15, 75))

        # self.txt_source = wx.TextCtrl(self.panel, value=self.source_dir, size=(250, -1), pos=(250, 10))
        # self.txt_target = wx.TextCtrl(self.panel, value=self.target_dir, size=(250, -1), pos=(250, 40))

        ################################
        # DIRECTORY PICKER CONTROLS
        ################################
        self.source_dir = wx.DirPickerCtrl(self.panel, style=wx.DIRP_USE_TEXTCTRL, path=self.source_dir_default,
            message=self.msg_dir_src, size=(400, -1), pos=(350, 10))
        self.target_dir = wx.DirPickerCtrl(self.panel, style=wx.DIRP_USE_TEXTCTRL, path=self.target_dir_default,
            message=self.msg_dir_tar, size=(400, -1), pos=(350, 40))

        ################################
        # LOG FIELD
        ################################
        init_log_msg = self.ts() + ': ' + self.log_txt_default
        self.console = wx.TextCtrl(self.panel, value = init_log_msg,
            size=(750, 390), pos=(15, 100), style= wx.TE_MULTILINE)

        ################################
        # BUTTONS
        ################################
        self.button_help = wx.Button(self.panel, label=self.label_help, size=(120, 40), pos=(15, 505))
        self.button_about = wx.Button(self.panel, label=self.label_about, size=(120, 40), pos=(150, 505))
        self.button_clipboard = wx.Button(self.panel, label=self.label_clipboard, size=(120, 40), pos=(285, 505))
        self.button_close = wx.Button(self.panel, label=self.label_close, size=(120, 40), pos=(420, 505))
        self.button_crop = wx.Button(self.panel, label=self.label_crop, size=(160, 40), pos=(605, 505))

        ################################
        # SIZER
        ################################
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
        self.sizer = wx.wxEVT_SIZE
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizerAndFit(self.border)

        ################################
        # FONT
        ################################
        self.button_crop.SetForegroundColour(wx.RED)
        cfont = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        #self.label_source.SetFont(cfont)
        #self.label_target.SetFont(cfont)
        #self.label_log_box.SetFont(cfont)
        self.button_crop.SetFont(cfont)
        self.button_about.SetFont(cfont)
        self.button_help.SetFont(cfont)
        self.button_close.SetFont(cfont)
        self.button_clipboard.SetFont(cfont)

        ################################
        # BIND
        ################################
        self.source_dir.Bind(wx.EVT_DIRPICKER_CHANGED, lambda evt: self.on_source_dir(evt))
        self.target_dir.Bind(wx.EVT_DIRPICKER_CHANGED, lambda evt: self.on_target_dir(evt))
        self.button_about.Bind(wx.EVT_BUTTON, self.on_about)
        self.button_clipboard.Bind(wx.EVT_BUTTON, self.on_clipboard)
        self.button_help.Bind(wx.EVT_BUTTON, self.on_help)
        self.button_close.Bind(wx.EVT_BUTTON, self.on_close)
        self.button_crop.Bind(wx.EVT_BUTTON, self.on_crop)

    # SIMPLE LINE FOR LOG
    def log(self, str):
        self.console.AppendText(self.ts() + ': ' + str + '\n')

    # SEPARATOR FOR LOG
    def log_separator(self):
        self.console.AppendText(self.separator + '\n')

    # TIMESTAMP FOR LOG
    def ts(self):
        return time.strftime('%Y.%m.%d %H:%M:%S')

    # LOG INIT
    def log_init(self):
        self.log_separator()
        self.on_source_dir()
        self.on_target_dir()

    # GET SOURCE DIRECTORY
    def get_source_dir(self):
        return self.get_correct_path(self.source_dir.GetPath())

    # GET TARGET DIRECTORY
    def get_target_dir(self):
        return self.get_correct_path(self.target_dir.GetPath())

    # CHANGE SOURCE DIRECTORY
    def on_source_dir(self, evt = None):
        self.files = []
        self.files = self.get_files(self.get_source_dir())
        self.log(self.msg_set_source_dir + ' ' + self.get_source_dir())
        self.log_source_dir()
        self.log_separator()

    # CHANGE TARGET DIRECTORY
    def on_target_dir(self, evt = None):
        self.log(self.msg_set_target_dir + ' ' + self.get_target_dir())
        self.log_target_dir()
        self.log_separator()

    # ABOUT BUTTON EVENT
    def on_about(self, e):
        version = self.label_version_number + ': ' + self.version
        info = self.title + \
            '\n' + self.description + \
            '\n' + self.label_author + ': ' + self.author + \
            '\n' + version + \
            '\n\n' + self.label_further_info + ': ' + self.email
        wx.MessageBox(info, self.title, wx.OK | wx.ICON_INFORMATION)

    def on_help(self, evt):
        wx.MessageBox(self.help_text, self.label_help, wx.OK | wx.ICON_INFORMATION)

    # CLIPBOARD BUTTON EVENT
    def on_clipboard(self, e):
        text = self.console.GetValue()
        clipdata = wx.TextDataObject()
        clipdata.SetText(text)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipdata)
            wx.TheClipboard.Close()
            self.log(self.msg_clipboard_success)
        else:
            self.log(self.msg_clipboard_error)
        self.log_separator()

    # CLOSE BUTTON EVENT
    def on_close(self, e):
        self.Destroy()

    # CROP BUTTON EVENT
    def on_crop(self, e):
        self.files = self.get_files(self.get_source_dir())
        if len(self.files) <= 0:
           self.log(self.msg_no_images)
        else:
            for image in self.files:
                image_actual = img.open(self.get_source_dir() + image)
                self.crop_image(image_actual)

            self.log(self.msg_final_success % self.get_target_dir())
        self.log_separator()

    # GET CORRECT PATH WITH 2 BACKSLASHES IN END OF PATH
    def get_correct_path(self, cstr):
        end_of_str = cstr[-2:]
        if '\\' not in end_of_str:
            return cstr + '\\'
        else:
            return cstr

    # GET SOURCE FILENAMES
    def get_files(self, path):
        files = []
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                files.append(name)

        return files

    # SET FONT COLOR
    def sfc(self, err = 0):
        if err == 1:
            # ERROR -> RED
            self.console.SetForegroundColour(wx.RED)
        else:
            # NORMAL - BLACK
            self.console.SetForegroundColour(wx.BLACK)

    # LOG CAHNGE SOURCE DIR
    def log_source_dir(self):
        if len(self.files) > 0:
            self.log(self.msg_all_images_num % len(self.files))
        else:
            self.log(self.msg_no_images)

    # LOG CHANGE TARGET DIR
    def log_target_dir(self):
        target_files = self.get_files(self.get_target_dir())

        if len(target_files) > 0:
            self.log(self.msg_target_not_empty)
        else:
            self.log(self.msg_target_empty)

    # REAL CROPPING
    def crop_image(self, image):
        # LOG
        self.log(self.msg_orig_spread + ': ' + str(image.filename) + ' (' + str(image.width) + 'x' + str(image.height) + ')')

        # ATTRIBUTES
        w = image.width
        h = image.height
        w2 = abs(w / 2)
        filename = image.filename.replace(self.get_source_dir(), '')
        filename_left = filename.replace('.jpg', '_1.jpg')
        filename_right = filename.replace('.jpg', '_2.jpg')

        # crop(left, upper, right, lower)
        # NEW IMAGES
        img_left = image.crop((0, 0, w2, h))
        img_right = image.crop((w2, 0, w, h))

        # SAVING
        img_left.save(self.get_target_dir() + filename_left)
        img_right.save(self.get_target_dir() + filename_right)

        # LOG
        self.log(self.msg_left_saved + ': ' + self.get_target_dir() + filename_left + ' (' + str(img_left.width) + 'x' + str(img_left.height) + ' pixel)')
        self.log(self.msg_right_saved + ': ' + self.get_target_dir() + filename_right + ' (' + str(img_right.width) + 'x' + str(img_right.height) + ' pixel)')
        self.log_separator()


if __name__ == '__main__':
    app = wx.App(False)
    frame = SpreadFrame(None, title = title, size=(800, 600))
    frame.Show()
    app.MainLoop()
