from kivymd.app import MDApp
from mainwidget import MainWidget
from kivy.lang import Builder
from kivy.core.window import Window

class MainApp(MDApp):
    """
    Classe com a aplicação principal.
    """
    def build(self):
        """
        Constrói a aplicação.
        """
        Window.fullscreen = 'auto'
        self._widget = MainWidget()
        return self._widget
    
if __name__ == "__main__":
    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(),rulesonly=True)
    MainApp().run()