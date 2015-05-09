from kivy.app import App
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
        BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.clock import Clock
import time

Builder.load_string('''
<LinePlayground>:
    canvas:
        Color:
            rgba: .4, .4, 1, 1
        Line:
            points: self.points
            joint: 'miter'
            cap: 'round'
            width: 1
            close: False
        Color:
            rgba: 1, .4, .4, 1
        Line:
            points: self.points2
            joint: 'miter'
            cap: 'round'
            width: 1
            close: False
        Color:
            rgba: 0, 1, 0, 1
        Line:
            points: self.points3
            joint: 'miter'
            cap: 'round'
            width: 1
            close: False

    GridLayout:
        cols: 2
        size_hint: 1, None
        #height: 44 * 5

        GridLayout:
            cols: 3

            Label:
                text: ''
            Label:
                text: 'data'
            Label:
                text: 'max'

            
            Label:
                text: 'Gx'
            Label:
                text: str(root.gx)
            Label:
                text: str(root.max_gx)
            
            Label:
                text: 'Gy'
            Label:
                text: str(root.gy)
            Label:
                text: str(root.max_gy)

            Label:
                text: 'Gz'
            Label:
                text: str(root.gz)
            Label:
                text: str(root.max_gz)
                
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

    points = ListProperty([])
    points2 = ListProperty([])
    points3 = ListProperty([])  
    dt = NumericProperty(0)

    x_pos = NumericProperty(0)

    old_width = NumericProperty(0)
    old_height = NumericProperty(0)


    gx = NumericProperty(0)
    gy = NumericProperty(0)
    gz = NumericProperty(0)

    max_gx = NumericProperty(0)
    max_gy = NumericProperty(0)
    max_gz = NumericProperty(0)


    def on_resize(window, width, height):
        print("resized")
        

    

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
        #time.sleep(.1)
        data.update(self.getData())
        self.gx = data["gx"]
        self.gy = data["gy"]
        self.gz = data["gz"]
        
        #check change in window size
        #d_width = self.width - self.current_width
        #d_higth = self.height - self.current_height

        if self.x_pos <= self.width * 0.8:
            
            self.points.append(cx + (self.x_pos) )
            self.points.append(cy + self.gx )

            self.points2.append(cx + (self.x_pos) )
            self.points2.append(cy + self.gy )
            
            self.points3.append(cx + (self.x_pos) )
            self.points3.append(cy + self.gz )

            
            self.x_pos += 1

        else:
            self.points.pop(0)
            self.points.pop(0)
            self.points2.pop(0)
            self.points2.pop(0)
            self.points3.pop(0)
            self.points3.pop(0)

            #self.points.append
            #self.points[0::2]

            for i in range(0, len(self.points)):
                if i % 2 == 0:
                    self.points[i] = self.points[i] - 1
                    self.points2[i] = self.points2[i] - 1
                    self.points3[i] = self.points3[i] - 1

            self.points[20] = self.points[20] + 1
            
            self.points.append(cx + (self.x_pos) )
            self.points.append(cy + self.gx )

            self.points2.append(cx + (self.x_pos) )
            self.points2.append(cy + self.gy )
            
            self.points3.append(cx + (self.x_pos) )
            self.points3.append(cy + self.gz )


        self.old_width = self.width
        self.old_height = self.height
        self.updateMax()
        
        
        
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

    def updateMax(self):
        if self.gx > self.max_gx:
            self.max_gx = self.gx

        if self.gy > self.max_gy:
            self.max_gy = self.gy

        if self.gz > self.max_gz:
            self.max_gz = self.gz
        
            

class TestLineApp(App):
    def build(self):
        return LinePlayground()


if __name__ == '__main__':
    TestLineApp().run()
