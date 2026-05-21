from manim import *

class Scene3(Scene):
    def construct(self):
        # 1. Setup the Hub and connected devices
        hub_box = Rectangle(height=1.2, width=2.0, color=BLUE, fill_opacity=0.2)
        hub_label = Text("HUB", font_size=24, color=WHITE).move_to(hub_box.get_center())
        hub = VGroup(hub_box, hub_label)

        pc1 = Square(side_length=0.7, color=TEAL).shift(LEFT * 3 + UP * 2)
        pc1_label = Text("PC A", font_size=20).next_to(pc1, UP)
        
        pc2 = Square(side_length=0.7, color=TEAL).shift(RIGHT * 3 + UP * 2)
        pc2_label = Text("PC B", font_size=20).next_to(pc2, UP)
        
        pc3 = Square(side_length=0.7, color=TEAL).shift(LEFT * 3 + DOWN * 2)
        pc4 = Square(side_length=0.7, color=TEAL).shift(RIGHT * 3 + DOWN * 2)

        line1 = Line(pc1.get_center(), hub.get_center(), color=GRAY)
        line2 = Line(pc2.get_center(), hub.get_center(), color=GRAY)
        line3 = Line(pc3.get_center(), hub.get_center(), color=GRAY)
        line4 = Line(pc4.get_center(), hub.get_center(), color=GRAY)

        network_elements = VGroup(hub, pc1, pc1_label, pc2, pc2_label, pc3, pc4, line1, line2, line3, line4)

        # 2. Collision Domain Visual
        collision_domain = Circle(radius=3.8, color=YELLOW, fill_opacity=0.1).move_to(hub.get_center())
        domain_label = Text("Single Collision Domain", color=YELLOW, font_size=32).to_edge(UP)

        # 3. Animation Sequence
        self.play(Create(network_elements))
        self.wait(1)
        
        self.play(
            Create(collision_domain),
            Write(domain_label)
        )
        self.wait(1.5)

        # 4. Collision Animation
        packet_a = Dot(color=RED, radius=0.15).move_to(pc1.get_center())
        packet_b = Dot(color=GREEN, radius=0.15).move_to(pc2.get_center())

        collision_text = Text("COLLISION!", color=RED, font_size=40).move_to(hub.get_center() + UP * 0.8)
        flash_circle = Circle(radius=0.1, color=RED, fill_opacity=0.8).move_to(hub.get_center())

        self.play(
            packet_a.animate.move_to(hub.get_center()),
            packet_b.animate.move_to(hub.get_center()),
            run_time=2,
            rate_func=linear
        )

        # The moment of collision
        self.play(
            flash_circle.animate.set_style(stroke_width=0).scale(15).set_opacity(0),
            Write(collision_text),
            packet_a.animate.scale(0.5).set_opacity(0),
            packet_b.animate.scale(0.5).set_opacity(0),
            run_time=0.8
        )
        
        self.wait(2)

        # Final cleanup
        self.play(
            FadeOut(collision_text),
            FadeOut(collision_domain),
            FadeOut(domain_label),
            FadeOut(network_elements)
        )
        self.wait(1)