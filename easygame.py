def degrees(d):
    """Convert degrees to radians.

    Arguments:
    d -- Angle in degrees.
    """
    import math
    return d / 180 * math.pi

def rotate(vector, angle):
    """Rotate a vector (x, y) by an angle in radians."""
    import math
    x, y = vector
    sin, cos = math.sin(angle), math.cos(angle)
    return (
        cos * x - sin * y,
        sin * x + cos * y,
    )

class EasyGameError(Exception):
    """All exceptions raised from this module are of this type."""
    pass

class _Camera:
    def __init__(self, center, position, rotation, zoom):
        self.center = center
        self.position = position
        self.rotation = rotation
        self.zoom = zoom

class _Context:
    _win = None
    _fps = 60
    _events = []
    _camera = _Camera((0, 0), (0, 0), 0, 1)
    _saved_cameras = []
    _channels = {}
    _fonts = {}

_ctx = _Context()

class CloseEvent:
    """Happens when user clicks the X button on the window."""
    pass

_symbol_dict = None

def _symbol_to_string(key):
    global _symbol_dict
    import pyglet
    if _symbol_dict is None:
        _symbol_dict = {
            pyglet.window.key.A: 'A',
            pyglet.window.key.B: 'B',
            pyglet.window.key.C: 'C',
            pyglet.window.key.D: 'D',
            pyglet.window.key.E: 'E',
            pyglet.window.key.F: 'F',
            pyglet.window.key.G: 'G',
            pyglet.window.key.H: 'H',
            pyglet.window.key.I: 'I',
            pyglet.window.key.J: 'J',
            pyglet.window.key.K: 'K',
            pyglet.window.key.L: 'L',
            pyglet.window.key.M: 'M',
            pyglet.window.key.N: 'N',
            pyglet.window.key.O: 'O',
            pyglet.window.key.P: 'P',
            pyglet.window.key.Q: 'Q',
            pyglet.window.key.R: 'R',
            pyglet.window.key.S: 'S',
            pyglet.window.key.T: 'T',
            pyglet.window.key.U: 'U',
            pyglet.window.key.V: 'V',
            pyglet.window.key.W: 'W',
            pyglet.window.key.X: 'X',
            pyglet.window.key.Y: 'Y',
            pyglet.window.key.Z: 'Z',
            pyglet.window.key._0: '0',
            pyglet.window.key._1: '1',
            pyglet.window.key._2: '2',
            pyglet.window.key._3: '3',
            pyglet.window.key._4: '4',
            pyglet.window.key._5: '5',
            pyglet.window.key._6: '6',
            pyglet.window.key._7: '7',
            pyglet.window.key._8: '8',
            pyglet.window.key._9: '9',

            pyglet.window.key.SPACE: 'SPACE',
            pyglet.window.key.ENTER: 'ENTER',
            pyglet.window.key.BACKSPACE: 'BACKSPACE',
            pyglet.window.key.ESCAPE: 'ESCAPE',
            pyglet.window.key.LEFT: 'LEFT',
            pyglet.window.key.RIGHT: 'RIGHT',
            pyglet.window.key.UP: 'UP',
            pyglet.window.key.DOWN: 'DOWN',

            pyglet.window.mouse.LEFT: 'LEFT',
            pyglet.window.mouse.RIGHT: 'RIGHT',
            pyglet.window.mouse.MIDDLE: 'MIDDLE',
        }
    if key not in _symbol_dict:
        return None
    return _symbol_dict[key]

class KeyDownEvent:
    """Happens when user pressed a key on the keyboard.

    Fields:
    key -- String representation of the pressed key.
           These are: 'A' ... 'Z',
                      '0' ... '9',
                      'SPACE', 'ENTER', 'BACKSPACE', 'ESCAPE',
                      'LEFT', 'RIGHT', 'UP, 'DOWN'.
    """
    def __init__(self, key):
        self.key = key

class KeyUpEvent:
    """Happens when user releases a key on the keyboard.

    Fields:
    key -- String representation of the released key.
           These are: 'A' ... 'Z',
                      '0' ... '9',
                      'SPACE', 'ENTER', 'BACKSPACE', 'ESCAPE',
                      'LEFT', 'RIGHT', 'UP, 'DOWN'.
    """
    def __init__(self, key):
        self.key = key

class TextEvent:
    """Happens when user types a text on the keyboard.

    Fields:
    text -- A string containing the typed text.
    """
    def __init__(self, text):
        self.text = text

class MouseMoveEvent:
    """Happens when user moves the mouse.

    Fields:
    x  -- The current X coordinate of the mouse.
    y  -- The current Y coordinate of the mouse.
    dx -- Difference from the previous X coordinate.
    dy -- Difference from the previous Y coordinate.
    """
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

class MouseDownEvent:
    """Happens when user presses a mouse button.

    Fields:
    x      -- The current X coordinate of the mouse.
    y      -- The current Y coordinate of the mouse.
    button -- String representation of the pressed button.
              These are: 'LEFT', 'RIGHT', 'MIDDLE'.
    """
    def __init__(self, x, y, button):
        self.x = x
        self.y = y
        self.button = button

class MouseUpEvent:
    """Happens when user releases a mouse button.

    Fields:
    x      -- The current X coordinate of the mouse.
    y      -- The current Y coordinate of the mouse.
    button -- String representation of the released button.
              These are: 'LEFT', 'RIGHT', 'MIDDLE'.
    """
    def __init__(self, x, y, button):
        self.x = x
        self.y = y
        self.button = button

def _update_camera():
    global _ctx
    import pyglet, math
    pyglet.gl.glViewport(0, 0, _ctx._win.width, _ctx._win.height)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glOrtho(0, _ctx._win.width, 0, _ctx._win.height, -1, 1)
    pyglet.gl.glTranslatef(_ctx._camera.center[0], _ctx._camera.center[1], 0)
    pyglet.gl.glRotatef(-_ctx._camera.rotation/math.pi*180, 0, 0, 1)
    pyglet.gl.glScalef(_ctx._camera.zoom, _ctx._camera.zoom, 1)
    pyglet.gl.glTranslatef(-_ctx._camera.position[0], -_ctx._camera.position[1], 0)

def open_window(title, width, height, fps=60):
    """Open a window with the specified parameters. Only one window can be open at any time.

    Arguments:
    title  -- Text at the top of the window.
    width  -- Width of the window in pixels.
    height -- Height of the window in pixels.
    fps    -- Maximum number of frames per second. (Defaults to 60.)
    """
    global _ctx
    import pyglet
    if _ctx._win is not None:
        raise EasyGameError('window already open')
    pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
    _ctx._win = pyglet.window.Window(caption=title, width=width, height=height)
    _ctx._fps = fps
    _ctx._win.switch_to()
    _ctx._camera = _Camera((0, 0), (0, 0), 0, 1)
    _ctx._saved_cameras = []
    _ctx._channels = {}
    _ctx._fonts = {}

    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    _update_camera()
    _ctx._win.dispatch_events()

    @_ctx._win.event
    def on_close():
        global _ctx
        _ctx._events.append(CloseEvent())

    @_ctx._win.event
    def on_key_press(symbol, modifiers):
        global _ctx
        key = _symbol_to_string(symbol)
        if key is None:
            return
        _ctx._events.append(KeyDownEvent(key))

    @_ctx._win.event
    def on_key_release(symbol, modifiers):
        global _ctx
        key = _symbol_to_string(symbol)
        if key is None:
            return
        _ctx._events.append(KeyUpEvent(key))

    @_ctx._win.event
    def on_text(text):
        global _ctx
        _ctx._events.append(TextEvent(text))

    @_ctx._win.event
    def on_mouse_motion(x, y, dx, dy):
        global _ctx
        _ctx._events.append(MouseMoveEvent(x, y, dx, dy))

    @_ctx._win.event
    def on_mouse_press(x, y, symbol, modifiers):
        global _ctx
        button = _symbol_to_string(symbol)
        if button is None:
            return
        _ctx._events.append(MouseDownEvent(x, y, button))

    @_ctx._win.event
    def on_mouse_release(x, y, symbol, modifiers):
        global _ctx
        button = _symbol_to_string(symbol)
        if button is None:
            return
        _ctx._events.append(MouseUpEvent(x, y, button))

def close_window():
    """Close the window. Raises an exception if no window is open."""
    global _ctx
    if _ctx._win is None:
        raise EasyGameError('window not open')
    _ctx._win.close()
    _ctx._win = None

def poll_events():
    """Return a list of events that happened since the last call to this function.

    There are 7 types of events:
    CloseEvent, KeyDownEvent, KeyUpEvent, TextEvent, MouseMoveEvent, MouseDownEvent, MouseUpEvent.

    CloseEvent has no fields.

    Both KeyUpEvent and KeyDownEvent have a field called key, which contains a string representation
    of the pressed/released key. These are:
    - 'A' ... 'Z'
    - '0' ... '9'
    - 'SPACE', 'ENTER', 'BACKSPACE', 'ESCAPE'
    - 'LEFT', 'RIGHT', 'UP, 'DOWN'.

    TextEvent has one field: text. This field contains a string of text that has been typed
    on the keyboard.

    All mouse events have fields x and y, telling the current mouse position.

    MouseMoveEvent has additional dx, dy fields telling the difference of the current mouse
    position from the previous one.

    MouseDownEvent and MouseUpEvent have an additional button field, which contains a string
    representation of the pressed/released mouse button. These are:
    - 'LEFT', 'RIGHT', 'MIDDLE'.
    """
    global _ctx
    import pyglet
    if _ctx._win is None:
        raise EasyGameError('window not open')
    _ctx._events = []
    _ctx._win.dispatch_events()
    return list(_ctx._events)

def next_frame():
    """Show the content of the window and waits until it's time for the next frame."""
    global _ctx
    import time
    import pyglet
    if _ctx._win is None:
        raise EasyGameError('window not open')
    _ctx._win.flip()
    dt = pyglet.clock.tick()
    if dt < 1 / _ctx._fps:
        time.sleep(1/_ctx._fps - dt)

def fill(r, g, b):
    """Fill the whole window with a single color.

    The r, g, b components of the color should be between 0 and 1.
    """
    global _ctx
    import pyglet
    if _ctx._win is None:
        raise EasyGameError('window not open')
    pyglet.gl.glClearColor(r, g, b, 1)
    _ctx._win.clear()

class _Image:
    def __init__(self, img):
        import pyglet
        self._img = img
        self._sprite = pyglet.sprite.Sprite(img)

    @property
    def width(self):
        return self._img.width

    @property
    def height(self):
        return self._img.height

    @property
    def center(self):
        return (self._img.width//2, self._img.height//2)

def load_image(path):
    """Load an image from the specified path. PNG, JPEG, and many more formats are supported.

    Returns the loaded image.

    Arguments:
    path -- Path to the image file. (For example 'images/crying_baby.png'.)
    """
    import pyglet
    return _Image(pyglet.resource.image(path))

def load_sheet(path, frame_width, frame_height):
    """Load a sprite sheet from the specified path and slices it into frames of the specified size.

    Returns the list of images corresponding to the individual slices.

    Arguments:
    path         -- Path to the sprite sheet.
    frame_width  -- Width of a single frame.
    frame_height -- Height of a single frame.
    """
    import pyglet
    img = pyglet.resource.image(path)
    frames = []
    for x in map(lambda i: i * frame_width, range(img.width // frame_width)):
        for y in map(lambda i: i * frame_height, range(img.height // frame_height)):
            frames.append(img.get_region(x, y, frame_width, frame_height))
    return frames

def image_data(image):
    """Returns a list of RGBA values of pixels of the image.

    The pixels are listed row by row.
    """
    raw = image._img.get_image_data()
    pitch = raw.width * 4
    data = raw.get_data('RGBA', pitch)
    rows = []
    for y in range(raw.height):
        rows.append([])
        for x in range(raw.width):
            i = (y*raw.width + x) * 4
            r, g, b, a = int(data[i+0])/255, int(data[i+1])/255, int(data[i+2])/255, int(data[i+3])/255
            rows[y].append((r, g, b, a))
    return rows

def draw_image(image, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False):
    """Draw an image to the window, respecting the current camera settings.

    Arguments:
    image     -- The image to draw. (Obtained from load_image or load_sheet)
    position  -- Anchor's position on the screen. (Defaults to 0, 0.)
    anchor    -- Anchor's position relative to the bottom-left corner of the image. (Defaults to the center.)
    rotation  -- Rotation of the image around the anchor in radians. (Defaults to 0.)
    scale     -- Scale of the image around the anchor. (Defaults to 1.)
    scale_x   -- Additional scale along X axis.
    scale_y   -- Additional scale along Y axis.
    opacity   -- Use 0 for completely transparent, 1 for completely opaque.
    pixelated -- If True, image will be pixelated when scaled.
    """
    global _ctx
    import math, pyglet
    if _ctx._win is None:
        raise EasyGameError('window not open')

    if anchor is None:
        anchor = image.center

    image._img.anchor_x, image._img.anchor_y = anchor
    image._sprite.update(
        x=position[0],
        y=position[1],
        rotation=-rotation/math.pi*180,
        scale_x=scale*scale_x,
        scale_y=scale*scale_y,
    )
    image._sprite.opacity = int(opacity * 255)

    if pixelated:
        tex = image._img.get_texture()
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, tex.id)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    else:
        tex = image._img.get_texture()
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, tex.id)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_LINEAR)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_LINEAR)

    image._sprite.draw()

def draw_polygon(*points, color=(1, 1, 1, 1)):
    """Draw a convex polygon, respecting the current camera settings.

    Example:
      draw_polygon((0, 0), (100, 300), (200, 0), color=(0, 1, 1, 1))

    Arguments:
    points -- List of points of the polygon. (Is taken by variadic arguments.)
    color  -- Color of the polygon. Components are: red, green, blue, alpha.
    """
    global _ctx
    import pyglet
    if _ctx._win is None:
        raise EasyGameError('window not open')
    vertices = []
    for pt in points:
        vertices.append(pt[0])
        vertices.append(pt[1])
    pyglet.graphics.draw(len(points), pyglet.gl.GL_POLYGON,
        ('v2f', vertices),
        ('c4f', color * len(points)),
    )

def draw_line(*points, thickness=1, color=(1, 1, 1, 1)):
    """Draw a line between each two successive pair of points.

    Example:
      draw_line((0, 0), (100, 300), (200, 0), thickness=10 color=(0, 1, 1, 1))

    Arguments:
    points    -- List of points of the line. (Is taken by variadic arguments.)
    thickness -- Width of the line.
    color     -- Color of the line. Components are: red, green, blue, alpha.
    """
    import math
    for i in range(len(points)-1):
        x0, y0 = points[i]
        x1, y1 = points[i+1]
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        dx, dy = dx/length*thickness/2, dy/length*thickness/2
        draw_polygon(
            (x0 - dy, y0 + dx),
            (x0 + dy, y0 - dx),
            (x1 + dy, y1 - dx),
            (x1 - dy, y1 + dx),
            color=color,
        )

def draw_circle(center, radius, color=(1, 1, 1, 1)):
    """Draws a circle with the specified center and radius.

    Example:
      draw_circle((100, 100), 50, color=(1, 0, 0, 1))

    Arguments:
    center -- Coordinates of the center of the circle, in the form (x, y).
    radius -- Radius of the circle.
    color  -- Color of the line.
    """
    import math
    x, y = center
    pts = []
    for i in range(32):
        angle = i/32 * 2*math.pi
        pts.append((x + math.cos(angle)*radius, y + math.sin(angle)*radius))
    draw_polygon(*pts, color=color)

def draw_text(text, font, size, position=(0, 0), color=(1, 1, 1, 1), bold=False, italic=False):
    """Draw text using the selected font, respecting the current camera settings.

    Arguments:
    text     -- String to draw.
    font     -- Name of the font to use. (For example: 'Times New Roman' or 'Courier New'.)
    size     -- Size of the font in pixels.
    position -- Position of the bottom-left corner of the resulting text.
    color    -- Color of the text.
    bold     -- If True, the text will be bold.
    italic   -- If True, the text will be italic.
    """
    global _ctx
    import pyglet
    if _ctx._win is None:
        raise EasyGameError('window not open')
    if (font, size) not in _ctx._fonts:
        _ctx._fonts[(font, size)] = pyglet.text.Label(font_name=font, font_size=size)
    label = _ctx._fonts[(font, size)]
    label.text = text
    label.x, label.y = position
    label.color = tuple(map(lambda c: int(c*255), color))
    label.bold = bold
    label.italic = italic
    label.draw()

def set_camera(center=None, position=None, rotation=None, zoom=None):
    """Set properties of the camera. Only properties you set will be changed.

    Arguments:
    center   -- Position of the center of the camera on the screen.
    position -- The world position that the camera is looking at.
    rotation -- Rotation of the camera around its center.
    zoom     -- Zoom/scale of the camera. Value of 1 is no zoom, value of 2 is twice-scaled, etc.
    """
    global _ctx
    if _ctx._win is None:
        raise EasyGameError('window not open')
    if center is not None:
        _ctx._camera.center = center
    if position is not None:
        _ctx._camera.position = position
    if rotation is not None:
        _ctx._camera.rotation = rotation
    if zoom is not None:
        _ctx._camera.zoom = zoom
    _update_camera()

def move_camera(position=None, rotation=None, zoom=None):
    """Change properties of the camera relative to its current properties.

    Arguments:
    position  -- Vector to add to the current position.
    rotattion -- Angle to add to the current rotation.
    zoom      -- Number to multiply by the current zoom.
    """
    global _ctx
    import math
    if _ctx._win is None:
        raise EasyGameError('window not open')
    if position is not None:
        _ctx._camera.position = (
            _ctx._camera.position[0] + position[0],
            _ctx._camera.position[1] + position[1],
        )
    if rotation is not None:
        _ctx._camera.rotation += rotation
        while _ctx._camera.rotation >= 2*math.pi:
            _ctx._camera.rotation -= 2*math.pi
        while _ctx._camera.rotation < 0:
            _ctx._camera.rotation += 2*math.pi
    if zoom is not None:
        _ctx._camera.zoom *= zoom
    _update_camera()

def save_camera():
    """Save the current camera settings."""
    global _ctx
    if _ctx._win is None:
        raise EasyGameError('window not open')
    _ctx._saved_cameras.append(_Camera(
        _ctx._camera.center,
        _ctx._camera.position,
        _ctx._camera.rotation,
        _ctx._camera.zoom,
    ))

def restore_camera():
    """Restore the most recently saved and not yet restored camera settings."""
    global _ctx
    if _ctx._win is None:
        raise EasyGameError('window not open')
    if len(_ctx._saved_cameras) == 0:
        raise EasyGameError('no saved camera')
    _ctx._camera = _ctx._saved_cameras.pop(-1)
    _update_camera()

def reset_camera():
    """Reset camera to the original settings."""
    set_camera(center=(0, 0), position=(0, 0), rotation=0, zoom=1)

class _Audio:
    def __init__(self, snd):
        self._snd = snd

def load_audio(path, streaming=False):
    """Load an audio from the specified path.

    Returns the loaded audio.

    Arguments:
    path      -- Path to the audio file. (For example 'sounds/crying_baby.wav'.)
    streaming -- Whether to stream the file directly from the disk, or load it to the memory instead.
    """
    import pyglet
    snd = pyglet.resource.media(path, streaming=streaming)
    return _Audio(snd)

def play_audio(audio, channel=0, loop=False, volume=1):
    """Play an audio on the specified channel.

    There's infinite number of channels. Playing an audio on a channel stops previous playback
    on this channel. Therefore, at most one audio can play on one channel at any time.

    To stop playback on a channel, play a None audio:
      play_audio(None, channel=0)

    Arguments:
    audio   -- The audio to be played.
    channel -- The channel index.
    loop    -- If True, playback will repeat forever, or until stopped.
    volume  -- 0 for mute, 1 for normal volume.
    """
    global _ctx
    import pyglet
    if channel in _ctx._channels:
        _ctx._channels[channel].delete()
    if audio is None:
        return
    player = pyglet.media.Player()
    if loop:
        looper = pyglet.media.SourceGroup(audio._snd.audio_format, None)
        looper.loop = True
        looper.queue(audio._snd)
        player.queue(looper)
    else:
        player.queue(audio._snd)
    player.volume = volume
    _ctx._channels[channel] = player
    player.play()

def fix_rectangle_overlap(rect1, rect2):
    """Calculate the minimum vector required to move rect1 to fix the overlap between
    rect1 and rect2.

    Arguments:
    rect1 -- The first rectangle. Has form (x0, y0, x1, y1).
    rect2 -- The second rectangle. Has the same form as rect1.
    """
    ax0, ay0, ax1, ay1 = rect1
    bx0, by0, bx1, by1 = rect2
    left, right = max(0, ax1 - bx0), min(0, ax0 - bx1)
    down, up    = max(0, ay1 - by0), min(0, ay0 - by1)
    move_x = min(left, right, key=abs)
    move_y = min(down, up, key=abs)
    if abs(move_x) < abs(move_y):
        return (-move_x, 0)
    else:
        return (0, -move_y)
