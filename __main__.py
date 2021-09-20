import pyglet
window = pyglet.window.Window()

label = pyglet.text.Label('Hello, world!',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

def draw_rect(x, y, z, width, height):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
        ('v3f', [x, y, z, x + width, y, z, x + width, y + height,z, x, y + height,z]))

window.set_exclusive_mouse(True)

@window.event
def on_draw():
    window.clear()
    label.draw()
    draw_rect(0,0,-10,20,20)
    
@window.event
def on_mouse_motion(x, y, dx, dy):
    print([x,y,dx,dy])

pyglet.app.run()
