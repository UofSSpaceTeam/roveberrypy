from object_renderer import ObjectRenderer

from kivy.core.window import Window  # noqa
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation

class BaseView(ObjectRenderer):

    def position(self, angle):
        Animation(
            cam_rotation=(0, 0, 0),
            cam_translation=(0, 0, -2),
            d=0).start(self)

    def update_lights(self, dt):
		for i in range(self.nb_lights):
			self.light_sources[i] = [self.light_radius, 5, self.light_radius, 1.0]
		for k in self.light_sources.keys():
			if k >= self.nb_lights:
				del(self.light_sources[k])
		return



class View(BaseView):
    pass


KV = '''

FloatLayout:
	Button:
		text: "Hello"
    View:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: (self.x, self.y)

        id: rendering
        scene: '../navball.obj'
        obj_scale: 1
        display_all: True
        ambiant: .8
        diffuse: 0.20
        specular: 0.4
        on_parent: self.position(0)
        mode: 'triangles'
        light_radius: 20
        nb_lights: 4
'''

if __name__ == '__main__':
    from kivy.app import App

    class App3D(App):
        def build(self):
            root = Builder.load_string(KV)
            Clock.schedule_once(root.ids.rendering.update_lights, 0)
            return root

    App3D().run()
