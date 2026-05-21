from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Setup Title
        title = Text("The Hub: Multi-Port Repeater", color=WHITE).scale(0.8)
        title.to_edge(UP, buff=0.5)

        # 2. Central Hub
        hub_rect = Rectangle(height=1.2, width=2.2, color=BLUE, fill_opacity=0.5)
        hub_label = Text("HUB", color=WHITE).scale(0.6)
        hub = VGroup(hub_rect, hub_label).move_to(ORIGIN)

        # 3. Stations (Represented as Squares)
        s1 = Square(side_length=0.7, color=TEAL, fill_opacity=0.3).move_to([-3.5, 2, 0])
        s2 = Square(side_length=0.7, color=TEAL, fill_opacity=0.3).move_to([3.5, 2, 0])
        s3 = Square(side_length=0.7, color=TEAL, fill_opacity=0.3).move_to([-3.5, -2, 0])
        s4 = Square(side_length=0.7, color=TEAL, fill_opacity=0.3).move_to([3.5, -2, 0])
        
        st_label1 = Text("Station 1", color=WHITE).scale(0.4).next_to(s1, UP)
        st_label2 = Text("Station 2", color=WHITE).scale(0.4).next_to(s2, UP)
        st_label3 = Text("Station 3", color=WHITE).scale(0.4).next_to(s3, DOWN)
        st_label4 = Text("Station 4", color=WHITE).scale(0.4).next_to(s4, DOWN)

        # 4. Connection Lines (Star Topology)
        l1 = Line(s1.get_center(), hub.get_center(), color=WHITE)
        l2 = Line(s2.get_center(), hub.get_center(), color=WHITE)
        l3 = Line(s3.get_center(), hub.get_center(), color=WHITE)
        l4 = Line(s4.get_center(), hub.get_center(), color=WHITE)

        topology = VGroup(hub, s1, s2, s3, s4, st_label1, st_label2, st_label3, st_label4, l1, l2, l3, l4)

        # 5. Display Initial Topology
        self.play(Write(title))
        self.play(Create(topology), run_time=2)
        self.wait(1)

        # 6. Signal Transmission: Station 1 to Hub
        signal_dot = Dot(color=YELLOW, radius=0.15).move_to(s1.get_center())
        self.play(signal_dot.animate.move_to(hub.get_center()), run_time=2)

        # 7. Hub Regeneration Effect (Glow and Pulse)
        self.play(
            hub_rect.animate.set_fill(GOLD, fill_opacity=0.9).set_color(GOLD),
            hub_rect.animate.scale(1.2),
            run_time=0.5
        )
        self.play(
            hub_rect.animate.set_fill(BLUE, fill_opacity=0.5).set_color(BLUE),
            hub_rect.animate.scale(1/1.2),
            run_time=0.5
        )

        # 8. Multi-Port Regeneration (Broadcasting to all other stations)
        sig_out_2 = Dot(color=YELLOW, radius=0.12).move_to(hub.get_center())
        sig_out_3 = Dot(color=YELLOW, radius=0.12).move_to(hub.get_center())
        sig_out_4 = Dot(color=YELLOW, radius=0.12).move_to(hub.get_center())

        # Reuse signal_dot for station 2 and others for 3 and 4
        self.play(
            signal_dot.animate.move_to(s2.get_center()),
            sig_out_3.animate.move_to(s3.get_center()),
            sig_out_4.animate.move_to(s4.get_center()),
            run_time=2
        )

        # End Scene
        self.wait(2)