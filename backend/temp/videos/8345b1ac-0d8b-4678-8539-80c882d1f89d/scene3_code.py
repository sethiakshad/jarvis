from manim import *

class Scene3(Scene):
    def construct(self):
        # Title of the scene
        title = Text("Quantitative Data and Scales", color=YELLOW).scale(0.8)
        title.to_edge(UP)

        # Digital Calculator Construction
        calc_body = Rectangle(height=2.8, width=2.0, color=BLUE, fill_opacity=0.2)
        calc_screen = Rectangle(height=0.7, width=1.6, color=WHITE, fill_opacity=0.3).move_to(calc_body.get_top() + DOWN * 0.6)
        calc_text = MathTex("542.80", color=WHITE).scale(0.8).move_to(calc_screen.get_center())
        
        # Calculator buttons using small rectangles
        btn_grid = VGroup()
        for i in range(3):
            for j in range(3):
                btn = Rectangle(height=0.3, width=0.4, color=WHITE, fill_opacity=0.5)
                btn.move_to(calc_body.get_center() + RIGHT * (j - 1) * 0.5 + DOWN * (i * 0.5 + 0.3))
                btn_grid.add(btn)
        
        calculator = VGroup(calc_body, calc_screen, calc_text, btn_grid).shift(RIGHT * 2.5)

        # Bar Chart Construction
        axis_h = Line(LEFT * 1.5, RIGHT * 1.5, color=WHITE).shift(LEFT * 3 + DOWN * 1.5)
        axis_v = Line(DOWN * 1.5, UP * 1.5, color=WHITE).shift(LEFT * 4.5 + DOWN * 1.5)
        
        bar1 = Rectangle(height=1.0, width=0.5, color=TEAL, fill_opacity=0.8)
        bar1.move_to(LEFT * 4.0 + DOWN * 1.0)
        
        bar2 = Rectangle(height=2.2, width=0.5, color=GOLD, fill_opacity=0.8)
        bar2.move_to(LEFT * 3.3 + DOWN * 0.4)
        
        bar3 = Rectangle(height=1.6, width=0.5, color=RED, fill_opacity=0.8)
        bar3.move_to(LEFT * 2.6 + DOWN * 0.7)
        
        chart = VGroup(axis_h, axis_v, bar1, bar2, bar3)

        # Mathematical Symbols
        sym1 = MathTex("+", color=GREEN).scale(1.2).next_to(calculator, UP, buff=0.5)
        sym2 = MathTex("-", color=RED).scale(1.2).next_to(calculator, DOWN, buff=0.5)
        sym3 = MathTex("\\times", color=TEAL).scale(1.2).next_to(calculator, LEFT, buff=0.5)
        sym4 = MathTex("\\div", color=GOLD).scale(1.2).next_to(calculator, RIGHT, buff=0.5)
        symbols = VGroup(sym1, sym2, sym3, sym4)

        # Bottom Labels (Scales)
        l1 = Text("Nominal", color=WHITE).scale(0.5)
        l2 = Text("Ordinal", color=WHITE).scale(0.5)
        l3 = Text("Interval", color=WHITE).scale(0.5)
        l4 = Text("Ratio", color=WHITE).scale(0.5)
        
        labels = VGroup(l1, l2, l3, l4).arrange(RIGHT, buff=0.7)
        labels.to_edge(DOWN).shift(DOWN * 2) 

        # --- Animations ---

        # 1. Appear Title and visuals
        self.play(Write(title))
        self.play(Create(calculator), Create(chart), run_time=2)
        
        # 2. Symbols Appear and Rotate
        self.play(Write(symbols))
        self.play(
            Rotate(symbols, angle=TAU, about_point=calculator.get_center()),
            run_time=3,
            rate_func=linear
        )
        
        # 3. Labels slide into view
        self.play(labels.animate.shift(UP * 2.5), run_time=1.5)
        
        # 4. Final hold
        self.wait(2)