from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
import Equipes

class MainWidget(MDBoxLayout):
    """
    Classe com o widget principal.
    """
    def __init__(self, **kwargs):
        """
        Inicializa o widget.
        """
        super().__init__(**kwargs)
        self.equipes = [Equipes.Equipe("Cavaleiros das Trevas", "Preta"), Equipes.Equipe("Droga, é o Brian", "Cinza"),
                        Equipes.Equipe("RUST-EZE", "Vermelha"), Equipes.Equipe("Laranja Mecânica", "Laranja"),
                        Equipes.Equipe("Os Vigaristas", "Roxa"), Equipes.Equipe("S. C. O. O. B. Y", "Verde"), 
                        Equipes.Equipe("Charmbots", "Rosa")]
        # Inicia o Websocket
        Clock.schedule_once(self.iniciar_websocket, 0.1)
        # Configura a interface
        Clock.schedule_once(self.configurar_interface, 0.05)
        # Seleção da equipe (0 a 6)
        self.selecionar = 0
        # Volta Inicial
        self.volta = 1
        # Flag para o início da corrida
        self.inicio = True
        # Websocket
        self.ws = None
        # Flag para última volta
        self.ultimaVolta = False
        # Eventos para atualizar os textos dos cronômetros
        self.eventoTextoTempoTotal = None
        self.eventoTextoTempoVolta = None

    def configurar_interface(self, dt=None):
        """
        Configura a interface após estar totalmente carregada
        """
        self.ids.tituloEquipe.text = self.equipes[self.selecionar].exibeTitulo()