import efl.elementary as elm
from efl.elementary.window import StandardWindow
from efl.elementary.image  import Image
from efl.elementary.progressbar import Progressbar
from efl.elementary.box    import Box

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL

import resource

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
FILL_BOTH   = EVAS_HINT_FILL, EVAS_HINT_FILL

class MainWindow(StandardWindow):
  def __init__(self):
    StandardWindow.__init__(self, "fbUi", "Robot Framebuffer UI", size=(320, 240))
    self.callback_delete_request_add(lambda o: elm.exit())
    
    testButton1 = Progressbar(self)
    testButton1.size_hint_weight = (0, 0)
    testButton1.size_hint_align = FILL_BOTH
    testButton1.horizontal_set(False)
    #testButton1.text = "A Button"
    testButton1.show()
    
    background = Image(self)
    background.size_hint_weight = FILL_BOTH
    background.file_set("images/background.jpg")
    background.tooltip_text_set("background")
    background.show()
    self.resize_object_add(background)

    testButton2 = Progressbar(self)
    testButton2.size_hint_weight = (0, 0.5)
    testButton2.size_hint_align = FILL_BOTH
   # testButton2.text = "Button"
    testButton2.horizontal_set(False)
    testButton2.show()
    
    mainBox = Box(self)
    mainBox.size_hint_weight = EXPAND_BOTH
    mainBox.horizontal_set(True)
    
    mainBox.pack_end(testButton1)
    mainBox.pack_end(testButton2)
    
    mainBox.show()
    
    
    self.resize_object_add(mainBox)
    
    
if __name__ == "__main__":
  
  # Limit resouces
  rsrc = resource.RLIMIT_DATA
  soft, hard = resource.getrlimit(rsrc)
  
  resource.setrlimit(rsrc, (1001001024, hard))
  
  soft, hard = resource.getrlimit(rsrc)
  
  elm.init()
  GUI = MainWindow()
  GUI.show()
  elm.run()
  elm.shutdown()