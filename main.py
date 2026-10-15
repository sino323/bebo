"""Mark-LV mobile (Kivy). Android entry point for buildozer; also runs on desktop."""
import os, re, math, random, threading
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.utils import escape_markup

Window.clearcolor = (0.03, 0.04, 0.08, 1)
EMO = re.compile("([\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\uFE0F\u200D]+)")
EMOJI_FONT = "assets/NotoEmoji-Regular.ttf"  # optional; without it emojis are hidden

def mk(s):
    s = escape_markup(s)
    return EMO.sub(r"[font=%s]\1[/font]" % EMOJI_FONT, s) if os.path.exists(EMOJI_FONT) else EMO.sub("", s)

class Ring(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.state, self.level, self.t = "idle", 0.0, 0.0
        Clock.schedule_interval(self.tick, 1 / 60)

    def tick(self, dt):
        self.t += dt
        tg = {"speaking": .3 + .7 * abs(math.sin(self.t * 9) * math.sin(self.t * 2.3)) + random.random() * .15,
              "thinking": .35, "idle": .1 + .05 * math.sin(self.t * 2)}[self.state]
        self.level += (tg - self.level) * .2
        self.canvas.clear()
        cx, cy = self.center; R = min(self.width, self.height) * .3
        with self.canvas:
            Color(0, .9, 1, .12 + .3 * self.level)
            Ellipse(pos=(cx - R * .6, cy - R * .6), size=(R * 1.2, R * 1.2))
            for i in range(3):
                r = R * (1 + .18 * i) * (1 + .12 * self.level * (i + 1))
                Color(*((0, .9, 1, .9 - i * .2) if i % 2 == 0 else (.49, .3, 1, .9 - i * .2)))
                if self.state == "thinking":
                    a = (self.t * (200 + 80 * i)) % 360
                    Line(circle=(cx, cy, r, a, a + 100), width=2)
                else:
                    Line(circle=(cx, cy, r), width=1.5 + self.level * 3)

class MarkApp(App):
    title = "Mark-LV"

    def build(self):
        os.environ["MARKLV_HOME"] = self.user_data_dir
        from core import config
        from core.engine import MarkLV
        self.cfg, self.ai = config, MarkLV()
        root = BoxLayout(orientation="vertical", padding=10, spacing=8)
        head = BoxLayout(size_hint_y=None, height=44)
        head.add_widget(Label(text="[b]MARK-LV[/b]", markup=True, color=(0, .9, 1, 1), font_size="20sp"))
        head.add_widget(Button(text="Settings", size_hint_x=.35, on_release=lambda *_: self.ask_key()))
        root.add_widget(head)
        self.ring = Ring(size_hint_y=.38); root.add_widget(self.ring)
        self.log = Label(markup=True, size_hint_y=None, halign="left", valign="top")
        self.log.bind(width=lambda *_: setattr(self.log, "text_size", (self.log.width, None)),
                      texture_size=lambda *_: setattr(self.log, "height", self.log.texture_size[1]))
        self.sv = ScrollView(); self.sv.add_widget(self.log); root.add_widget(self.sv)
        row = BoxLayout(size_hint_y=None, height=52, spacing=6)
        self.inp = TextInput(hint_text="Ask Mark-LV anything...", multiline=False, on_text_validate=self.send)
        row.add_widget(self.inp); row.add_widget(Button(text="Send", size_hint_x=.25, on_release=self.send))
        root.add_widget(row)
        self.add("Mark-LV", "Hey, I'm Mark-LV 🤖✨ Your AI companion is online. What's on your mind? 🚀", "00e5ff")
        return root

    def on_start(self):
        if not self.cfg.get_key():
            self.ask_key(first=True)

    def add(self, who, text, col):
        self.log.text += f"[color={col}][b]{who}[/b][/color]\n{mk(text)}\n\n"
        Clock.schedule_once(lambda dt: setattr(self.sv, "scroll_y", 0), .1)

    def ask_key(self, first=False):
        ti = TextInput(text="" if first else self.cfg.get_key(), password=True, multiline=False,
                       hint_text="Please enter your Gemini API Key", size_hint_y=None, height=48)
        def ok(*_):
            if ti.text.strip():
                self.cfg.set_key(ti.text); pop.dismiss()
        box = BoxLayout(orientation="vertical", spacing=8, padding=10)
        box.add_widget(ti); box.add_widget(Button(text="Save changes", size_hint_y=None, height=48, on_release=ok))
        pop = Popup(title="Mark-LV Setup" if first else "Settings", content=box,
                    size_hint=(.92, .4), auto_dismiss=not first)
        pop.open()

    def send(self, *_):
        t = self.inp.text.strip()
        if not t: return
        self.inp.text = ""; self.add("You", t, "9d7bff"); self.ring.state = "thinking"
        threading.Thread(target=self.work, args=(t,), daemon=True).start()

    def work(self, t):
        try: r, ok = self.ai.ask(t), True
        except Exception as e: r, ok = str(e), False
        Clock.schedule_once(lambda dt: self.done(r, ok))

    def done(self, r, ok):
        self.add("Mark-LV", r, "00e5ff")
        self.ring.state = "speaking" if ok else "idle"
        if ok:
            try:
                from plyer import tts
                tts.speak(EMO.sub("", r))
            except Exception:
                pass
            Clock.schedule_once(lambda dt: setattr(self.ring, "state", "idle"), min(len(r) / 14, 10))

if __name__ == "__main__":
    MarkApp().run()
