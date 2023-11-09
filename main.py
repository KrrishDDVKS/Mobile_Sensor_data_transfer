import socket

from kivy import platform
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from plyer import gps
from plyer import gravity
from plyer import gyroscope
from plyer import accelerometer
from kivymd.uix.dialog import MDDialog

class SayHello(App):
    w,x,y,z,k,l,m,n=0,0,0,0,0,0,0,0
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    a="hi"
    if platform == "Android":
        from android.permissions import Permission, request_permissions

        def callback(permission,results):
            if all([res for res in results]):
                print("PERMISSION ACCEPTED")
            else:
                print("PERMISSION DENIED")
        request_permissions([Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_EXTERNAL_STORAGE,
                             Permission.ACCESS_COARSE_LOCATION,Permission.ACCESS_FINE_LOCATION],callback)
    def update_blinker_position(self, *args, **kwargs):
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']
        SayHello.w = f"lat:{my_lat} lon:{my_lon}"

    def on_auth_status(self, stat, msg):
        if stat == 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        dialog=MDDialog(title="GPS Error",text="You need to enable GPS")
        dialog.size_hint=[0.8,0.8]
        dialog.pos_hint = {'center_x':0.5,'center_y':0.5}
        dialog.open()

    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 2
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # label widget
        self.greeting = Label(
                        text= "IPv4",
                        font_size= 32,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.greeting)

        # text input widget
        self.ip = TextInput(
                    text='192.168.1.91',
                    multiline= False,
                    padding_y= (20,20),
                    size_hint= (1, 0.5)
                    )
        self.window.add_widget(self.ip)
        SayHello.a = self.ip.text
        #sensor labels
        self.gps = Label(
            text="GPS",
            font_size=32,
            color='#00FFCE'
        )
        self.window.add_widget(self.gps)

        # checkbox widget


        def on_checkbox_active1(checkbox, value):
            SayHello.k=value

            if value:
                print('The checkbox', checkbox, 'is active')
                gps.configure(on_location=self.update_blinker_position(),on_status=self.on_auth_status)
                gps.start(minTime=1000,minDistance=0)
            else:
                print('The checkbox', checkbox, 'is inactive')
                gps.stop()


        self.checkbox1 = CheckBox()
        self.checkbox1.bind(active=on_checkbox_active1)
        self.window.add_widget(self.checkbox1)

        self.g = Label(
            text="Gravity",
            font_size=32,
            color='#00FFCE'
        )
        self.window.add_widget(self.g)
        def on_checkbox_active2(checkbox, value):
            SayHello.l = value
            if value:
                print('The checkbox', checkbox, 'is active')
                gravity.enable()
                SayHello.x=gravity.gravity
            else:
                print('The checkbox', checkbox, 'is inactive')
                gravity.disable()

        self.checkbox2 = CheckBox()
        self.checkbox2.bind(active=on_checkbox_active2)
        self.window.add_widget(self.checkbox2)

        self.acc = Label(
            text="Accelerometer",
            font_size=32,
            color='#00FFCE'
        )
        self.window.add_widget(self.acc)
        def on_checkbox_active3(checkbox, value):
            SayHello.m = value
            if value:
                print('The checkbox', checkbox, 'is active')
                accelerometer.enable()
                SayHello.y = accelerometer.acceleration
            else:
                print('The checkbox', checkbox, 'is inactive')
                accelerometer.disable()
        self.checkbox3 = CheckBox()
        self.checkbox3.bind(active=on_checkbox_active3)
        self.window.add_widget(self.checkbox3)

        self.gyr = Label(
            text="Gyroscope",
            font_size=32,
            color='#00FFCE'
        )
        self.window.add_widget(self.gyr)


        def on_checkbox_active4(checkbox, value):
            SayHello.z = value
            if value:
                print('The checkbox', checkbox, 'is active')
                gyroscope.enable()
                SayHello.n=gyroscope.rotation
            else:
                print('The checkbox', checkbox, 'is inactive')
                gyroscope.disable()
        self.checkbox4 = CheckBox()
        self.checkbox4.bind(active=on_checkbox_active4)
        self.window.add_widget(self.checkbox4)

        # button widget
        self.start = Button(
            text="Send",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE',

        )
        self.start.bind(on_press=self.runstuff)
        self.window.add_widget(self.start)

        # button widget
        self.exit = Button(
            text="Stop",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE',
            )
        self.exit.bind(on_press=self.exitstuff)
        self.window.add_widget(self.exit)

        return self.window

    def server(self,instance):
        if SayHello.l==True:
            SayHello.clientSock.sendto(str(SayHello.x).encode(), (SayHello.a, 8888))
        if SayHello.m == True:
            SayHello.clientSock.sendto(str(SayHello.y).encode(), (SayHello.a, 8888))
        if SayHello.n == True:
            SayHello.clientSock.sendto(str(SayHello.z).encode(), (SayHello.a, 8888))

    def runstuff(self,instance):

        self.f=Clock.schedule_interval(self.server,0.5)
    def exitstuff(self,instance):
        self.f.cancel()
# run Say Hello App Calss
if __name__ == "__main__":
    SayHello().run()