from manim import *

class Scene3(Scene):
    def construct(self):
        # 1. Background elements
        hub = Rectangle(width=2.2, height=1.4, color=TEAL, fill_opacity=0.3)
        hub_label = Text("Hub", color=TEAL, font_size=28).move_to(hub.get_center())
        hub_group = VGroup(hub, hub_label)

        pc1 = Square(side_length=1.2, color=BLUE, fill_opacity=0.4).move_to([-4, 0, 0])
        pc1_label = Text("PC 1", font_size=20).next_to(pc1, UP)
        
        pc2 = Square(side_length=1.2, color=BLUE, fill_opacity=0.4).move_to([4, 0, 0])
        pc2_label = Text("PC 2", font_size=20).next_to(pc2, UP)

        line1 = Line(pc1.get_right(), hub.get_left(), color=WHITE)
        line2 = Line(pc2.get_left(), hub.get_right(), color=WHITE)

        # Labels for the domain
        domain_text = Text("Single Collision Domain", color=YELLOW, font_size=24).to_edge(DOWN, buff=1)

        # Display structure
        self.play(
            Create(hub_group),
            Create(pc1),
            Create(pc1_label),
            Create(pc2),
            Create(pc2_label),
            Create(line1),
            Create(line2),
            Write(domain_text),
            run_time=2
        )
        self.wait(1)

        # 2. Packet Generation
        p1 = Dot(color=GOLD, radius=0.15).move_to(pc1.get_center())
        p2 = Dot(color=GOLD, radius=0.15).move_to(pc2.get_center())

        # 3. Collision Animation
        # Packets move toward the hub simultaneously
        self.play(
            p1.animate.move_to(hub.get_center()),
            p2.animate.move_to(hub.get_center()),
            run_time=1.5,
            rate_func=linear
        )

        # Collision effect: Red flash and Text
        collision_flash = Circle(radius=0.1, color=RED, fill_opacity=1).move_to(hub.get_center())
        collision_msg = Text("COLLISION!", color=RED, font_size=36, weight=BOLD).next_to(hub, UP, buff=0.5)
        
        self.play(
            collision_flash.animate.scale(10).set_fill(opacity=0),
            Write(collision_msg),
            run_time=0.8
        )
        self.remove(p1, p2, collision_flash)

        # 4. Shared Bandwidth Concept
        shared_label = Text("Shared Bandwidth", color=GOLD, font_size=32).move_to([0, -1, 0])
        bus_arrow = Arrow(start=[-3.5, -1.8, 0], end=[3.5, -1.8, 0], color=TEAL, buff=0)
        bus_label = Text("Logical Bus Topology", color=WHITE, font_size=22).next_to(bus_arrow, DOWN, buff=0.2)

        self.play(
            Write(shared_label),
            Create(bus_arrow),
            Write(bus_label),
            run_time=2
        )
        
        self.wait(2)

        # 5. Outro fade
        self.play(
            FadeOut(hub_group),
            FadeOut(pc1),
            FadeOut(pc1_label),
            FadeOut(pc2),
            FadeOut(pc2_label),
            FadeOut(line1),
            FadeOut(line2),
            FadeOut(domain_text),
            FadeOut(collision_msg),
            FadeOut(shared_label),
            FadeOut(bus_arrow),
            FadeOut(bus_label),
            run_time=1.5
        )