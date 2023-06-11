from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
import time
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from kivy.clock import Clock
class CircleWidget(Widget):
    def __init__(self, **kwargs):
        super(CircleWidget, self).__init__(**kwargs)
        self.rsrp_label = Label(text='-', pos=(self.center_x, self.center_y+20))
        self.rsrq_label = Label(text='-', pos=(self.center_x, self.center_y))
        self.rssi_label = Label(text='-', pos=(self.center_x, self.center_y-20))
        self.sinr_label = Label(text='-', pos=(self.center_x, self.center_y-40))
        self.add_widget(self.rsrp_label)
        self.add_widget(self.rsrq_label)
        self.add_widget(self.rssi_label)
        self.add_widget(self.sinr_label)
        
    def update_labels(self, rsrp, rsrq, rssi, sinr):
        self.rsrp_label.text = "RSRP: {} dBm".format(rsrp)
        self.rsrq_label.text = "RSRQ: {} dB".format(rsrq)
        self.rssi_label.text = "RSSI: {} dBm".format(rssi)
        self.sinr_label.text = "SINR: {} dB".format(sinr)
class MainApp(App):
    def update_information(self, *args):
        information = self.getsignalinformation()
        self.circle1.update_labels(information['rsrp'], information['rsrq'], information['rssi'], information['sinr'])
        self.circle2.update_labels(information['rsrp'], information['rsrq'], information['rssi'], information['sinr'])
        self.circle3.update_labels(information['rsrp'], information['rsrq'], information['rssi'], information['sinr'])
        self.circle4.update_labels(information['rsrp'], information['rsrq'], information['rssi'], information['sinr'])
        print(information)
        
    def getsignalinformation(self):
        with Connection('http://admin:admin@192.168.8.1/') as connection:
            client = Client(connection)
            device_signal = client.device.signal()
            rsrq = float(device_signal['rsrq'].split('dB')[0])
            rsrp = float(device_signal['rsrp'].split('dB')[0])
            rssi = float(device_signal['rssi'].split('dB')[0])
            sinr = float(device_signal['sinr'].split('dB')[0])
            information = {'rsrq': rsrq, 'rsrp': rsrp, 'rssi': rssi, 'sinr': sinr}
        return information
    
    def build(self):
        self.circle1 = CircleWidget(center=self.root.center, size_hint=(None, None), size=(100, 100))
        self.circle2 = CircleWidget(center=self.root.center, size_hint=(None, None), size=(200, 200))
        self.circle3 = CircleWidget(center=self.root.center, size_hint=(None, None), size=(300, 300))
        self.circle4 = CircleWidget(center=self.root.center, size_hint=(None, None), size=(400, 400))
        self.root.add_widget(self.circle1)
        self.root.add_widget(self.circle2)
        self.root.add_widget(self.circle3)
        self.root.add_widget(self.circle4)
        
        with self.circle1.canvas:
            Color(1, 0, 0)
            Ellipse(pos=self.circle1.pos, size=self.circle1.size)
        with self.circle2.canvas:
            Color(0, 1, 0)
            Ellipse(pos=self.circle2.pos, size=self.circle2.size)
        with self.circle3.canvas:
            Color(0, 0, 1)
            Ellipse(pos=self.circle3.pos, size=self.circle3.size)
        with self.circle4.canvas:
            Color(1, 1, 0)
            Ellipse(pos=self.circle4.pos, size=self.circle4.size)
        
        self.update_information() # Update once on launch
        self.event = Clock.schedule_interval(self.update_information, 0.5) # Schedule updates every 1 second
        return self.root
if __name__ == '__main__':
    app = MainApp()
    app.run()
