from kivy.app import App
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
        BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.clock import Clock
from math import cos, sin
import time

Builder.load_string('''
<LinePlayground>:
    canvas:
        Color:
            rgba: .4, .4, 1, 1
        Line:
            points: self.points
            joint: self.joint
            cap: self.cap
            width: self.linewidth
            close: self.close
        Color:
            rgba: 1, .4, .4, 1
        Line:
            points: self.points2
            joint: self.joint
            cap: self.cap
            width: self.linewidth
            close: self.close
        Color:
            rgba: 0, 1, 0, 1
        Line:
            points: self.points3
            joint: self.joint
            cap: self.cap
            width: self.linewidth
            close: self.close

    GridLayout:
        cols: 2
        size_hint: 1, None
        height: 44 * 5

        GridLayout:
            cols: 2
            
            Label:
                text: 'Gx'
            Label:
                text: str(root.gx)

            Label:
                text: 'Gy'
            Label:
                text: str(root.gy)

            Label:
                text: 'Gz'
            Label:
                text: str(root.gz)
                
        AnchorLayout:
            GridLayout:
                cols: 1
                size_hint: None, None
                size: self.minimum_size
                ToggleButton:
                    size_hint: None, None
                    size: 100, 44
                    text: 'Start'
                    on_state: root.animate(self.state == 'down')

''')


class LinePlayground(FloatLayout):
    close = False #BooleanProperty(False)
    points = ListProperty([])
    points2 = ListProperty([])
    points3 = ListProperty([])
    joint = 'miter' #OptionProperty('none', options=('round', 'miter', 'bevel', 'none'))
    cap = 'round' #OptionProperty('none', options=('round', 'square', 'none'))
    linewidth = 1 #NumericProperty(1)
    dt = NumericProperty(0)

    x_pos = NumericProperty(0)

    current_width = NumericProperty(0)
    current_height = NumericProperty(0)


    gx = NumericProperty(0)
    gy = NumericProperty(0)
    gz = NumericProperty(0)
    

    def animate(self, do_animation):
        if do_animation:
            Clock.schedule_interval(self.update_points_animation, 0)
        else:
            Clock.unschedule(self.update_points_animation)

    def update_points_animation(self, dt):
        cy = self.height * 0.6
        cx = self.width * 0.1
        w = self.width * 0.8
        self.dt += dt
        data = {}
        time.sleep(.1)
        data.update(self.getData())
        self.gx = data["gx"]
        self.gy = data["gy"]
        self.gz = data["gz"]
        
        #check change in window size
        #d_width = self.width - self.current_width
        #d_higth = self.height - self.current_height
        
        self.points.append(cx + (self.x_pos) )
        self.points.append(cy + self.gx )

        self.points2.append(cx + (self.x_pos) )
        self.points2.append(cy + self.gy )
        
        self.points3.append(cx + (self.x_pos) )
        self.points3.append(cy + self.gz )

        self.current_width = self.width
        self.current_height = self.height
        
        self.x_pos += 1

        
        
        
    def getData(self):

        data = {}
        data["gx"] = 1 + self.gx 
        data["gy"] = 5 + self.gy
        data["gz"] = 10 + self.gz

        if self.gx > 200:
            data["gx"] = 0

        if self.gy > 200:
            data["gy"] = 0

        if self.gz > 200:
            data["gz"] = 0
        

        return data

class TestLineApp(App):
    def build(self):
        return LinePlayground()


if __name__ == '__main__':
    TestLineApp().run()
