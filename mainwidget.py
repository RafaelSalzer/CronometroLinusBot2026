from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
import Equipes
import Cronometro
from websocket import WebSocketApp
import threading

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
        # Cronômetro para o tempo total
        self.cronometroTempoTotal = Cronometro.Cronometro()
        # Cronômetro para o tempo da volta
        self.cronometroTempoVolta = Cronometro.Cronometro()

    def configurar_interface(self, dt=None):
        """
        Configura a interface após estar totalmente carregada
        """
        self.ids.tituloEquipe.text = self.equipes[self.selecionar].exibeTitulo()

    def formatar_tempo(self, tempo_total):
        """
        Formata um tempo em segundos para MM:SS.mmm.
        """
        minutos = int(tempo_total // 60)
        segundos = int(tempo_total % 60)
        milissegundos = int((tempo_total % 1) * 1000)
        return f"{minutos:02d}:{segundos:02d}.{milissegundos:03d}"

    def imprimir_voltas_ordenadas(self):
        """
        Imprime as voltas da equipe atual da mais rápida para a mais lenta.
        """
        voltas_ordenadas = sorted(self.equipes[self.selecionar].voltas)
        print(f"Voltas da equipe {self.equipes[self.selecionar].nome}:")
        for indice, tempo in enumerate(voltas_ordenadas, start=1):
            print(f"{indice}: {self.formatar_tempo(tempo)}")

    def atualizar_voltas_interface(self):
        """
        Atualiza os labels da interface com as voltas mais rápidas primeiro.
        """
        voltas_ordenadas = sorted(self.equipes[self.selecionar].voltas)
        labels_voltas = [self.ids.volta1, self.ids.volta2, self.ids.volta3, self.ids.volta4, self.ids.volta5]

        for indice, label in enumerate(labels_voltas, start=1):
            if indice <= len(voltas_ordenadas):
                label.text = f"volta {indice}: {self.formatar_tempo(voltas_ordenadas[indice - 1])}"
            else:
                label.text = f"volta {indice}: 00:00.000"

    def iniciar_websocket(self, dt=None):
        """Inicializa a conexão WebSocket com o ESP32"""
        
        def on_message(ws, message):
            #print(f"Mensagem recebida: {message}")
            if message == "Passou" and self.inicio and not self.ultimaVolta:
                self.inicio = False
                self.cronometroTempoVolta.iniciar()
                self.eventoTextoTempoVolta = Clock.schedule_interval(self.altera_texto_tempo_volta, 0.01)
                self.iniciar_cronometro()
            elif message == "Passou" and not self.inicio:
                tempo_volta = self.cronometroTempoVolta.obter_tempo_atual()
                tempo_volta_formatado = self.formatar_tempo(tempo_volta)

                if self.volta == 1:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta1.opacity = 1
                
                elif self.volta == 2:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta2.opacity = 1

                elif self.volta == 3:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta3.opacity = 1

                elif self.volta == 4:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta4.opacity = 1

                elif self.volta == 5:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta5.opacity = 1
                
                elif self.volta == 6:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta1.opacity = 1
                
                elif self.volta == 7:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta2.opacity = 1
                    
                elif self.volta == 8:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta3.opacity = 1
                    
                elif self.volta == 9:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta4.opacity = 1
                    
                elif self.volta == 10:
                    self.equipes[self.selecionar].voltas.append(tempo_volta)
                    self.volta += 1
                    #self.ids.volta5.opacity = 1

                self.atualizar_voltas_interface()
                
                if self.ultimaVolta:
                    """Essa é a última parte da corrida de cada equipe
                    """
                    if self.eventoTextoTempoVolta is not None:
                        self.zerar_cronometro_volta()
                        self.inicio = False
                    self.imprimir_voltas_ordenadas()
                    #self.ultimaVolta = False
                    #self.inicio = True
                    #self.volta = 1
                    self.ids.botaoEsquerda.disabled = False
                    self.ids.botaoDireita.disabled = False
                    #self.ids.botaoCasa.disabled = False
                else:
                    # Para o cronômetro da volta
                    self.cronometroTempoVolta.zerar_cronometro()
                    self.cronometroTempoVolta.iniciar()
                    self.eventoTextoTempoVolta = Clock.schedule_interval(self.altera_texto_tempo_volta, 0.01)

        def on_error(ws, error):
            print(f"Erro WebSocket: {error}")

        def on_close(ws, close_status_code, close_msg):
            print("Conexão WebSocket encerrada")

        def on_open(ws):
            print("Conectado ao WebSocket do ESP32")
            
        try:
            ws_url = "ws://192.168.4.1:81"
            self.ws = WebSocketApp(ws_url,
                                   on_message=on_message,
                                   on_error=on_error,
                                   on_close=on_close,
                                   on_open=on_open)

            # Executar WebSocket em thread separada
            def run_websocket():
                self.ws.run_forever()
                
            thread = threading.Thread(target=run_websocket)
            thread.daemon = True
            thread.start()
            print("WebSocket iniciado em thread separada")
            
        except Exception as e:
            print(f"Erro ao iniciar WebSocket: {e}")
                
            
    def selecionar_equipe_direita(self):
        self.zerar_cronometro()
        self.ultimaVolta = False
        self.inicio = True
        self.volta = 1
        self.selecionar += 1
        if self.selecionar >= len(self.equipes):
            self.selecionar = 0
        self.ids.tituloEquipe.text = self.equipes[self.selecionar].exibeTitulo()
        self.ids.volta1.text = "volta 1: 00:00.000"
        self.ids.volta2.text = "volta 2: 00:00.000"
        self.ids.volta3.text = "volta 3: 00:00.000"
        self.ids.volta4.text = "volta 4: 00:00.000"
        self.ids.volta5.text = "volta 5: 00:00.000"

    def selecionar_equipe_esquerda(self):
        self.zerar_cronometro()
        self.ultimaVolta = False
        self.inicio = True
        self.volta = 1
        self.selecionar -= 1
        if self.selecionar < 0:
            self.selecionar = len(self.equipes) - 1
        self.ids.tituloEquipe.text = self.equipes[self.selecionar].exibeTitulo()
        self.ids.volta1.text = "volta 1: 00:00.000"
        self.ids.volta2.text = "volta 2: 00:00.000"
        self.ids.volta3.text = "volta 3: 00:00.000"
        self.ids.volta4.text = "volta 4: 00:00.000"
        self.ids.volta5.text = "volta 5: 00:00.000"

    def iniciar_cronometro(self):
        self.cronometroTempoTotal.iniciar()
        self.eventoTextoTempoTotal = Clock.schedule_interval(self.altera_texto_tempo_total, 0.01)
        self.ids.botaoEsquerda.disabled = True
        self.ids.botaoDireita.disabled = True
        #self.ids.botaoCasa.disabled = True

    def altera_texto_tempo_total(self, dt):
        tempo = self.cronometroTempoTotal.obter_tempo_atual()

        self.ids.tempoTotal.text = self.cronometroTempoTotal.obter_tempo_formatado()

        if tempo >= 60:  ## ta dando um erreinho de alguns milisegundos, mas a logica funciona
            self.cronometroTempoTotal.pausar_cronometro()
            self.ultimaVolta = True
            if getattr(self, 'eventoTextoTempoTotal', None):
                self.eventoTextoTempoTotal.cancel()
                self.eventoTextoTempoTotal = None
            self.ids.tempoTotal.text = "01:00.000"

    
                
    def altera_texto_tempo_volta(self, dt):
        self.ids.tempoVolta.text = self.cronometroTempoVolta.obter_tempo_formatado()
        
    def zerar_cronometro(self):
        self.cronometroTempoTotal.zerar_cronometro()
        self.ids.tempoTotal.text = "00:00.000"
        self.ids.volta1.text = "volta 1: 00:00.000"
        self.ids.volta2.text = "volta 2: 00:00.000"
        self.ids.volta3.text = "volta 3: 00:00.000"
        self.ids.volta4.text = "volta 4: 00:00.000"
        self.ids.volta5.text = "volta 5: 00:00.000"
        self.equipes[self.selecionar].voltas = []
        self.inicio = True
        self.volta = 1
        self.ultimaVolta = False
        if self.eventoTextoTempoTotal:
            self.eventoTextoTempoTotal.cancel()
            self.eventoTextoTempoTotal = None
        self.ids.botaoEsquerda.disabled = False
        self.ids.botaoDireita.disabled = False
        #self.ids.botaoCasa.disabled = False
        if self.eventoTextoTempoVolta is not None:
            self.zerar_cronometro_volta()

    def zerar_cronometro_volta(self):
        self.cronometroTempoVolta.zerar_cronometro()
        self.ids.tempoVolta.text = "00:00.000"
        if self.eventoTextoTempoVolta:    
            self.eventoTextoTempoVolta.cancel()
            self.eventoTextoTempoVolta = None
        self.inicio = True