
from itertools import cycle

import pygame as pg
import prepare, tools
import string


LOADED_FONTS = {}

BUTTON_DEFAULTS = {"call"               : None,
                   "args"               : None,
                   "call_on_up"         : True,
                   "font"               : None,
                   "font_size"          : 36,
                   "text"               : None,
                   "hover_text"         : None,
                   "disable_text"       : None,
                   "text_color"         : pg.Color("white"),
                   "hover_text_color"   : None,
                   "disable_text_color" : None,
                   "fill_color"         : None,
                   "hover_fill_color"   : None,
                   "disable_fill_color" : None,
                   "idle_image"         : None,
                   "hover_image"        : None,
                   "disable_image"      : None,
                   "hover_sound"        : None,
                   "click_sound"        : None,
                   "visible"            : True,
                   "active"             : True,
                   "bindings"           : ()}

def _parse_color(color):
    if color is not None:
        try:
            return pg.Color(color)
        except ValueError:
            return pg.Color(*color)
    return color


class Label(object):
    """
    Parent class all labels inherit from. Color arguments can use color names
    or an RGB tuple. rect_attr should be a dict with keys of pygame.Rect
    attribute names (strings) and the relevant position(s) as values.

    Creates a surface with text blitted to it (self.image) and an associated
    rectangle (self.rect). Label will have a transparent bg if
    bg is not passed to __init__.
    """
    def __init__(self, path, size, text, color, rect_attr, bg=None):
        self.path, self.size = path, size
        if (path, size) not in LOADED_FONTS:
            LOADED_FONTS[(path, size)] = pg.font.Font(path, size)
        self.font = LOADED_FONTS[(path, size)]
        self.bg = _parse_color(bg)
        self.color = _parse_color(color)
        self.rect_attr = rect_attr
        self.set_text(text)

    def set_text(self, text):
        """Set the text to display."""
        self.text = text
        self.update_text()

    def update_text(self):
        """Update the surface using the current properties and text."""
        if self.bg:
            render_args = (self.text, True, self.color, self.bg)
        else:
            render_args = (self.text, True, self.color)
        self.image = self.font.render(*render_args)
        self.rect = self.image.get_rect(**self.rect_attr)

    def draw(self, surface):
        """Blit self.image to target surface."""
        surface.blit(self.image, self.rect)


class Blinker(Label):
    """
    A blinking label. frequency is the number of milliseconds between blinks.
    """
    def __init__(self, path, size, text, color, rect_attr, frequency, bg=None):
        super(Blinker, self).__init__(path, size, text, color, rect_attr, bg)
        self.frequency = frequency
        self.elapsed = 0.0
        self.on = False
        self.blinking = True

    def update(self, dt):
        self.elapsed += dt
        while self.elapsed >= self.frequency:
            self.elapsed -= self.frequency
            if self.blinking:
                self.on = not self.on

    def draw(self, surface):
        if self.on:
            surface.blit(self.image, self.rect)


class ButtonGroup(pg.sprite.Group):
    def get_event(self, event, *args, **kwargs):
        check = (s for s in self.sprites() if s.active and s.visible)
        for s in check:
            s.get_event(event, *args, **kwargs)


class Button(pg.sprite.Sprite, tools._KwargMixin):
    _invisible = pg.Surface((1,1)).convert_alpha()
    _invisible.fill((0,0,0,0))

    def __init__(self, rect_style, *groups, **kwargs):
        super(Button, self).__init__(*groups)
        self.process_kwargs("Button", BUTTON_DEFAULTS, kwargs)
        self.rect = pg.Rect(rect_style)
        rendered = self.render_text()
        self.idle_image = self.make_image(self.fill_color, self.idle_image,
                                          rendered["text"])
        self.hover_image = self.make_image(self.hover_fill_color,
                                           self.hover_image, rendered["hover"])
        self.disable_image = self.make_image(self.disable_fill_color,
                                             self.disable_image,
                                             rendered["disable"])
        self.image = self.idle_image
        self.clicked = False
        self.hover = False

    def render_text(self):
        font, size = self.font, self.font_size
        if (font, size) not in LOADED_FONTS:
            LOADED_FONTS[font, size] = pg.font.Font(font, size)
        self.font = LOADED_FONTS[font, size]
        text = self.text and self.font.render(self.text, 1, self.text_color)
        hover = self.hover_text and self.font.render(self.hover_text, 1,
                                                     self.hover_text_color)
        disable = self.disable_text and self.font.render(self.disable_text, 1,
                                                       self.disable_text_color)
        return {"text" : text, "hover" : hover, "disable": disable}

    def make_image(self, fill, image, text):
        if not any((fill, image, text)):
            return None
        final_image = pg.Surface(self.rect.size).convert_alpha()
        final_image.fill((0,0,0,0))
        rect = final_image.get_rect()
        fill and final_image.fill(fill, rect)
        image and final_image.blit(image, rect)
        text and final_image.blit(text, text.get_rect(center=rect.center))
        return final_image

    def get_event(self, event):
        if self.active and self.visible:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.on_up_event(event)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.on_down_event(event)
            elif event.type == pg.KEYDOWN and event.key in self.bindings:
                self.on_down_event(event, True)
            elif event.type == pg.KEYUP and event.key in self.bindings:
                self.on_up_event(event, True)

    def on_up_event(self, event, onkey=False):
        if self.clicked and self.call_on_up:
            self.click_sound and self.click_sound.play()
            self.call and self.call(self.args or self.text)
        self.clicked = False

    def on_down_event(self, event, onkey=False):
        if self.hover or onkey:
            self.clicked = True
            if not self.call_on_up:
                self.click_sound and self.click_sound.play()
                self.call and self.call(self.args or self.text)

    def update(self, prescaled_mouse_pos):
        hover = self.rect.collidepoint(prescaled_mouse_pos)
        pressed = pg.key.get_pressed()
        if any(pressed[key] for key in self.bindings):
            hover = True
        if not self.visible:
            self.image = Button._invisible
        elif self.active:
            self.image = (hover and self.hover_image) or self.idle_image
            if not self.hover and hover:
                self.hover_sound and self.hover_sound.play()
            self.hover = hover
        else:
            self.image = self.disable_image or self.idle_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)