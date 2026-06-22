# -*- coding: utf-8 -*-
import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform

# Formula text
FORMULA_P = "[b]单项覆盖系数[/b]  p = mnd√(1 + π²D²/L²) / (πD)"
FORMULA_P2 = "[b]编织密度[/b]  P = (2p − p²) × 100%"


class CalculatorApp(App):
    def build(self):
        self.title = "公式计算器"
        if platform() == "android":
            from kivy.core.window import Window
            Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        sm = ScreenManager()
        sm.add_widget(TabCoverage(name="coverage"))
        sm.add_widget(TabPitch(name="pitch"))
        return sm


class TabCoverage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))

        # Formula
        root.add_widget(Label(
            text=FORMULA_P, markup=True,
            size_hint_y=None, height=dp(28),
            font_size=dp(15), color=(0, 0, 0, 1)))
        root.add_widget(Label(
            text=FORMULA_P2, markup=True,
            size_hint_y=None, height=dp(26),
            font_size=dp(14), color=(0, 0, 0, 1)))

        # Input grid
        grid = GridLayout(cols=2, spacing=dp(4), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        self.inputs = {}
        labels = ["m：", "n：", "d：", "D：", "L："]
        hints = ["同方向锭子数", "每锭根数", "单线直径", "编织后直径 mm", "编织节距 mm"]
        for lbl, hint in zip(labels, hints):
            grid.add_widget(Label(text=lbl, halign="right", size_hint_y=None, height=dp(36), font_size=dp(14)))
            inp = TextInput(hint_text=hint, multiline=False, size_hint_y=None, height=dp(36), font_size=dp(14))
            inp.bind(on_text_validate=lambda _: self.do_calc())
            grid.add_widget(inp)
            self.inputs[lbl[0]] = inp
        root.add_widget(grid)

        # Buttons
        btn_row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        btn_calc = Button(text="计算", on_press=lambda _: self.do_calc())
        btn_reset = Button(text="重置", on_press=lambda _: self.do_reset())
        btn_row.add_widget(btn_calc)
        btn_row.add_widget(btn_reset)
        root.add_widget(btn_row)

        # Result
        self.result_lbl = Label(
            text="", size_hint_y=None, height=dp(30),
            font_size=dp(15), bold=True, color=(0.7, 0, 0, 1))
        root.add_widget(self.result_lbl)

        # Steps
        self.steps_area = ScrollView(size_hint=(1, 1))
        self.steps_label = Label(
            text="", size_hint_y=None, font_size=dp(12),
            halign="left", valign="top", padding=(dp(4), dp(4)))
        self.steps_label.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))
        self.steps_area.add_widget(self.steps_label)
        root.add_widget(self.steps_area)

        self.add_widget(root)

    def get_val(self, key):
        v = self.inputs[key].text.strip()
        return v if v else None

    def do_calc(self):
        try:
            raw = {k: self.get_val(k) for k in "mndDL"}
            if not all(raw.values()):
                self.result_lbl.text = "错误：请填写所有输入框"
                return
            m = float(raw["m"]);
            n = float(raw["n"]);
            d = float(raw["d"])
            D = float(raw["D"]);
            L = float(raw["L"])
            if any(v <= 0 for v in [m, n, d, D, L]):
                raise ValueError("所有输入必须大于 0")
            pi = math.pi
            steps = []
            steps.append("pi = {:.6f}".format(pi))
            steps.append("pi^2 = {:.6f}".format(pi * pi))
            steps.append("D = {},  D^2 = {:.6f}".format(D, D * D))
            steps.append("L = {},  L^2 = {:.6f}".format(L, L * L))
            steps.append("pi^2 x D^2 = {:.6f}".format((pi * pi) * (D * D)))
            steps.append("pi^2 x D^2 / L^2 = {:.6f}".format((pi * pi * D * D) / (L * L)))
            a = 1 + (pi * pi * D * D) / (L * L)
            steps.append("1 + pi^2 x D^2 / L^2 = {:.6f}".format(a))
            b = math.sqrt(a)
            steps.append("sqrt(1 + pi^2 x D^2 / L^2) = {:.6f}".format(b))
            c = m * n * d
            steps.append("m x n x d = {:.6f}".format(c))
            d_step = c * b
            steps.append("(m x n x d) x sqrt(...) = {:.6f}".format(d_step))
            e = pi * D
            steps.append("pi x D = {:.6f}".format(e))
            p = d_step / e
            steps.append("p = {:.6f} / {:.6f} = {:.6f}".format(d_step, e, p))
            p_pct = p * 100
            steps.append("p x 100% = {:.4f}%".format(p_pct))
            P = (2 * p - p * p) * 100
            steps.append("")
            steps.append("P = (2 x {:.6f} - {:.6f}^2) x 100%".format(p, p))
            steps.append("  = ({:.6f} - {:.6f}) x 100%".format(2 * p, p * p))
            steps.append("  = {:.6f} x 100%".format(2 * p - p * p))
            steps.append("  = {:.4f}%".format(P))
            self.steps_label.text = "【计算过程】\n\n  " + "\n  ".join(steps)
            self.result_lbl.text = "p = {:.4f}%    P = {:.4f}%".format(p_pct, P)
        except ValueError as e:
            self.result_lbl.text = "错误：" + (str(e) if str(e) else "请输入有效数字")
        except Exception as e:
            self.result_lbl.text = "错误：" + str(e)

    def do_reset(self):
        for inp in self.inputs.values():
            inp.text = ""
        self.result_lbl.text = ""
        self.steps_label.text = ""


class TabPitch(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))

        root.add_widget(Label(
            text=FORMULA_P, markup=True,
            size_hint_y=None, height=dp(28),
            font_size=dp(15), color=(0, 0, 0, 1)))
        root.add_widget(Label(
            text=FORMULA_P2, markup=True,
            size_hint_y=None, height=dp(26),
            font_size=dp(14), color=(0, 0, 0, 1)))
        root.add_widget(Label(
            text="↓ 给定 P 范围，反求 L 范围 ↓",
            size_hint_y=None, height=dp(22),
            font_size=dp(12), color=(0.5, 0.5, 0.5, 1)))

        grid = GridLayout(cols=2, spacing=dp(4), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        self.inputs = {}
        labels = ["m：", "n：", "d：", "D："]
        hints = ["同方向锭子数", "每锭根数", "单线直径", "编织后直径 mm"]
        for lbl, hint in zip(labels, hints):
            grid.add_widget(Label(text=lbl, halign="right", size_hint_y=None, height=dp(36), font_size=dp(14)))
            inp = TextInput(hint_text=hint, multiline=False, size_hint_y=None, height=dp(36), font_size=dp(14))
            inp.bind(on_text_validate=lambda _: self.do_calc())
            grid.add_widget(inp)
            self.inputs[lbl[0]] = inp
        root.add_widget(grid)

        # P range inputs
        grid2 = GridLayout(cols=2, spacing=dp(4), size_hint_y=None)
        grid2.bind(minimum_height=grid2.setter("height"))
        grid2.add_widget(Label(text="P 最小值（%）：", halign="right", size_hint_y=None, height=dp(36), font_size=dp(14)))
        self.pmin_inp = TextInput(text="80.5", multiline=False, size_hint_y=None, height=dp(36), font_size=dp(14))
        self.pmin_inp.bind(on_text_validate=lambda _: self.do_calc())
        grid2.add_widget(self.pmin_inp)
        grid2.add_widget(Label(text="P 最大值（%）：", halign="right", size_hint_y=None, height=dp(36), font_size=dp(14)))
        self.pmax_inp = TextInput(text="84.0", multiline=False, size_hint_y=None, height=dp(36), font_size=dp(14))
        self.pmax_inp.bind(on_text_validate=lambda _: self.do_calc())
        grid2.add_widget(self.pmax_inp)
        root.add_widget(grid2)

        btn_row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        btn_calc = Button(text="计算 L 范围", on_press=lambda _: self.do_calc())
        btn_reset = Button(text="重置", on_press=lambda _: self.do_reset())
        btn_row.add_widget(btn_calc)
        btn_row.add_widget(btn_reset)
        root.add_widget(btn_row)

        self.result_lbl = Label(
            text="", size_hint_y=None, height=dp(30),
            font_size=dp(15), bold=True, color=(0, 0.5, 0.7, 1))
        root.add_widget(self.result_lbl)

        self.steps_area = ScrollView(size_hint=(1, 1))
        self.steps_label = Label(
            text="", size_hint_y=None, font_size=dp(12),
            halign="left", valign="top", padding=(dp(4), dp(4)))
        self.steps_label.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))
        self.steps_area.add_widget(self.steps_label)
        root.add_widget(self.steps_area)

        self.add_widget(root)

    def get_val(self, key):
        v = self.inputs[key].text.strip()
        return v if v else None

    def do_calc(self):
        try:
            raw = {k: self.get_val(k) for k in "mndD"}
            if not all(raw.values()):
                self.result_lbl.text = "错误：请填写 m, n, d, D"
                return
            m = float(raw["m"]);
            n = float(raw["n"]);
            d = float(raw["d"]);
            D = float(raw["D"])
            Pmin_s = self.pmin_inp.text.strip()
            Pmax_s = self.pmax_inp.text.strip()
            if not Pmin_s or not Pmax_s:
                self.result_lbl.text = "错误：请填写 P 范围"
                return
            Pmin = float(Pmin_s);
            Pmax = float(Pmax_s)
            if any(v <= 0 for v in [m, n, d, D]):
                raise ValueError("m, n, d, D 必须大于 0")
            if Pmin <= 0 or Pmax <= 0 or Pmax <= Pmin:
                raise ValueError("P 范围无效")
            if Pmin >= 100 or Pmax >= 100:
                raise ValueError("P 必须小于 100%")

            pi = math.pi;
            k = m * n * d

            def p_from_P(v):
                return 1 - math.sqrt(1 - v / 100.0)

            def L_from_p(pv):
                A = pv * pi * D / k
                return pi * D / math.sqrt(A * A - 1)

            p_low = p_from_P(Pmin)
            p_high = p_from_P(Pmax)
            L_max = L_from_p(p_low)
            L_min = L_from_p(p_high)

            steps = []
            steps.append("m={}, n={}, d={}, D={}, pi={:.6f}".format(m, n, d, D, pi))
            steps.append("k = m x n x d = {:.6f}".format(k))
            steps.append("")
            steps.append("Pmin={:.2f}% -> p_low={:.6f}".format(Pmin, p_low))
            steps.append("Pmax={:.2f}% -> p_high={:.6f}".format(Pmax, p_high))
            steps.append("")
            steps.append("L_max (对应Pmin) = {:.6f}".format(L_max))
            steps.append("L_min (对应Pmax) = {:.6f}".format(L_min))
            steps.append("")
            steps.append("验证：")
            for label, Lv, pv in [("L_min", L_min, p_high), ("L_max", L_max, p_low)]:
                sv = math.sqrt(1 + pi * pi * D * D / (Lv * Lv))
                pc = k * sv / (pi * D)
                Pc = (2 * pc - pc * pc) * 100
                steps.append("  {}={:.4f} -> P={:.4f}%".format(label, Lv, Pc))

            self.steps_label.text = "【计算过程】\n\n  " + "\n  ".join(steps)
            self.result_lbl.text = "L ∈ [{:.4f}, {:.4f}]".format(L_min, L_max)
        except ValueError as e:
            self.result_lbl.text = "错误：" + (str(e) if str(e) else "输入无效")
        except Exception as e:
            self.result_lbl.text = "错误：" + str(e)

    def do_reset(self):
        for inp in self.inputs.values():
            inp.text = ""
        self.pmin_inp.text = "80.5"
        self.pmax_inp.text = "84.0"
        self.result_lbl.text = ""
        self.steps_label.text = ""


if __name__ == "__main__":
    CalculatorApp().run()