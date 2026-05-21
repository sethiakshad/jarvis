from manim import *

class Scene1(Scene):
    def construct(self):
        # Title and Concept
        title = Text("Hub as a Multi-Port Repeater", font_size=32, color=WHITE).to_edge(UP)
        explanation = Text("Regenerates and broadcasts signals", font_size=24, color=GOLD).next_to(title, DOWN)
        
        # Central Hub
        hub_box = Rectangle(height=1.2, width=2.0, color=BLUE, fill_opacity=0.3)
        hub_label = Text("Hub", font_size=24).move_to(hub_box.get_center())
        hub = VGroup(hub_box, hub_label).move_to(ORIGIN)

        # Peripheral Stations (Computers)
        comp_top = Square(side_length=0.7, color=TEAL, fill_opacity=0.5).move_to(2.5 * UP)
        comp_bottom = Square(side_length=0.7, color=TEAL, fill_opacity=0.5).move_to(2.5 * DOWN)
        comp_left = Square(side_length=0.7, color=TEAL, fill_opacity=0.5).move_to(4.0 * LEFT)
        comp_right = Square(side_length=0.7, color=TEAL, fill_opacity=0.5).move_to(4.0 * RIGHT)
        
        stations = VGroup(comp_top, comp_bottom, comp_left, comp_right)
        
        # Connection Lines
        l1 = Line(hub_box.get_top(), comp_top.get_bottom(), color=WHITE)
        l2 = Line(hub_box.get_bottom(), comp_bottom.get_top(), color=WHITE)
        l3 = Line(hub_box.get_left(), comp_left.get_right(), color=WHITE)
        l4 = Line(hub_box.get_right(), comp_right.get_left(), color=WHITE)
        
        lines = VGroup(l1, l2, l3, l4)

        # Initial Setup Animation
        self.add(title)
        self.play(Write(explanation))
        self.play(Create(hub), Create(stations), Create(lines))
        self.wait(1)

        # Signal Entering Hub (Weak Signal)
        weak_pulse = Dot(point=comp_left.get_center(), radius=0.08, color=YELLOW)
        self.add(weak_pulse)
        self.play(
            weak_pulse.animate.move_to(hub.get_center()),
            weak_pulse.animate.set_opacity(0.3),
            run_time=2,
            rate_func=linear
        )
        self.remove(weak_pulse)

        # Regeneration Effect
        flash = Circle(radius=0.1, color=GOLD, fill_opacity=0.8).move_to(hub.get_center())
        self.play(
            flash.animate.scale(8).set_opacity(0),
            hub_box.animate.set_color(GOLD),
            run_time=0.8
        )
        self.play(hub_box.animate.set_color(BLUE), run_time=0.2)

        # Broadcasted Signals (Regenerated/Strong)
        p1 = Dot(point=hub.get_center(), radius=0.15, color=GOLD)
        p2 = Dot(point=hub.get_center(), radius=0.15, color=GOLD)
        p3 = Dot(point=hub.get_center(), radius=0.15, color=GOLD)
        
        self.play(
            p1.animate.move_to(comp_top.get_center()),
            p2.animate.move_to(comp_bottom.get_center()),
            p3.animate.move_to(comp_right.get_center()),
            run_time=2,
            rate_func=smooth
        )
        
        # Cleanup
        self.play(FadeOut(p1, p2, p3))
        self.wait(2)