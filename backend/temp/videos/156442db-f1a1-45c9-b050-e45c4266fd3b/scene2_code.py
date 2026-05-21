from manim import *

class Scene2(Scene):
    def construct(self):
        # Title and Labels
        title = Text("Broadcasting and Lack of Intelligence", font_size=32, color=YELLOW).to_edge(UP)
        explanation = Text("Hubs broadcast data to every device.", font_size=20).next_to(title, DOWN)

        # Network Infrastructure
        hub = Square(color=GOLD, fill_opacity=0.6).scale(0.8)
        hub_label = Text("HUB", font_size=24).move_to(hub.get_center())
        hub_v = VGroup(hub, hub_label)

        # Devices
        c_a = Circle(color=BLUE, fill_opacity=0.4).scale(0.5).move_to([-4, 2, 0])
        c_b = Circle(color=BLUE, fill_opacity=0.4).scale(0.5).move_to([4, 2, 0])
        c_c = Circle(color=BLUE, fill_opacity=0.4).scale(0.5).move_to([-4, -2, 0])
        c_d = Circle(color=BLUE, fill_opacity=0.4).scale(0.5).move_to([4, -2, 0])

        # Connections
        l_a = Line(c_a.get_center(), hub.get_center(), color=WHITE, stroke_width=2)
        l_b = Line(c_b.get_center(), hub.get_center(), color=WHITE, stroke_width=2)
        l_c = Line(c_c.get_center(), hub.get_center(), color=WHITE, stroke_width=2)
        l_d = Line(c_d.get_center(), hub.get_center(), color=WHITE, stroke_width=2)

        names = VGroup(
            Text("Comp A", font_size=18).next_to(c_a, UP),
            Text("Comp B", font_size=18).next_to(c_b, UP),
            Text("Comp C", font_size=18).next_to(c_c, DOWN),
            Text("Comp D", font_size=18).next_to(c_d, DOWN)
        )

        network_group = VGroup(hub_v, c_a, c_b, c_c, c_d, l_a, l_b, l_c, l_d, names)
        self.play(Create(network_group), Write(title), Write(explanation))

        # Data Packet
        p_rect = Rectangle(height=0.4, width=1.1, color=TEAL, fill_opacity=1)
        p_text = Text("To Comp D", font_size=12, color=BLACK).move_to(p_rect.get_center())
        packet = VGroup(p_rect, p_text).move_to(c_a.get_center())

        # Animation: A to Hub
        self.play(packet.animate.move_to(hub.get_center()), run_time=1.5)
        self.wait(0.5)

        # Broadcast: Hub to B, C, and D
        p_b = packet.copy()
        p_c = packet.copy()
        p_d = packet.copy()

        self.play(
            p_b.animate.move_to(c_b.get_center()),
            p_c.animate.move_to(c_c.get_center()),
            p_d.animate.move_to(c_d.get_center()),
            FadeOut(packet),
            run_time=2
        )

        # Rejection/Acceptance Indicators
        reject_b = Text("Not for me", font_size=16, color=RED).next_to(c_b, RIGHT)
        reject_c = Text("Not for me", font_size=16, color=RED).next_to(c_c, LEFT)
        accept_d = Text("Target Found!", font_size=16, color=GREEN).next_to(c_d, RIGHT)

        self.play(
            Write(reject_b),
            Write(reject_c),
            Write(accept_d)
        )

        self.wait(3)