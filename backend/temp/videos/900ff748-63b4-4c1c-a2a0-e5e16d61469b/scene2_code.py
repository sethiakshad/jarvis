from manim import *

class Scene2(Scene):
    def construct(self):
        # Title
        title = Text("Hub vs. Switch: Traffic Flow", font_size=32, color=WHITE).to_edge(UP)
        self.add(title)

        # Split Screen Line
        divider = Line(start=UP * 2, end=DOWN * 3, color=WHITE)
        self.add(divider)

        # Labels for Hub and Switch sides
        hub_title = Text("Hub (Single Collision Domain)", font_size=24, color=BLUE).move_to([-3.5, 2.5, 0])
        switch_title = Text("Switch (Dedicated Bandwidth)", font_size=24, color=GREEN).move_to([3.5, 2.5, 0])
        self.add(hub_title, switch_title)

        # --- HUB SIDE SETUP ---
        hub_box = Rectangle(width=1.5, height=1, color=BLUE, fill_opacity=0.2).move_to([-3.5, 0, 0])
        hub_label = Text("HUB", font_size=20).move_to(hub_box.get_center())
        
        # Hub Ports
        h_p1 = Dot(point=[-5.5, 1, 0], color=WHITE)
        h_p2 = Dot(point=[-1.5, 1, 0], color=WHITE)
        h_p3 = Dot(point=[-5.5, -1, 0], color=WHITE)
        h_p4 = Dot(point=[-1.5, -1, 0], color=WHITE)
        
        h_ports = VGroup(h_p1, h_p2, h_p3, h_p4)
        h_lines = VGroup(
            Line(h_p1.get_center(), hub_box.get_left()),
            Line(h_p2.get_center(), hub_box.get_right()),
            Line(h_p3.get_center(), hub_box.get_left()),
            Line(h_p4.get_center(), hub_box.get_right())
        )
        
        hub_group = VGroup(hub_box, hub_label, h_ports, h_lines)
        self.add(hub_group)

        # --- SWITCH SIDE SETUP ---
        switch_box = Rectangle(width=1.5, height=1, color=GREEN, fill_opacity=0.2).move_to([3.5, 0, 0])
        switch_label = Text("SWITCH", font_size=20).move_to(switch_box.get_center())
        
        # Switch Ports
        s_p1 = Dot(point=[1.5, 1, 0], color=WHITE)
        s_p2 = Dot(point=[5.5, 1, 0], color=WHITE)
        s_p3 = Dot(point=[1.5, -1, 0], color=WHITE)
        s_p4 = Dot(point=[5.5, -1, 0], color=WHITE)
        
        s_ports = VGroup(s_p1, s_p2, s_p3, s_p4)
        s_lines = VGroup(
            Line(s_p1.get_center(), switch_box.get_left()),
            Line(s_p2.get_center(), switch_box.get_right()),
            Line(s_p3.get_center(), switch_box.get_left()),
            Line(s_p4.get_center(), switch_box.get_right())
        )
        
        switch_group = VGroup(switch_box, switch_label, s_ports, s_lines)
        self.add(switch_group)

        # --- ANIMATION: HUB BROADCAST ---
        packet_h = Dot(point=h_p1.get_center(), color=YELLOW, radius=0.1)
        self.play(Create(packet_h))
        self.play(packet_h.animate.move_to(hub_box.get_center()), run_time=1)
        
        # Broadcast packets
        p_h2 = packet_h.copy()
        p_h3 = packet_h.copy()
        p_h4 = packet_h.copy()
        
        self.play(
            p_h2.animate.move_to(h_p2.get_center()),
            p_h3.animate.move_to(h_p3.get_center()),
            p_h4.animate.move_to(h_p4.get_center()),
            packet_h.animate.set_opacity(0),
            run_time=1.5
        )
        
        broadcast_text = Text("Broadcast Traffic", font_size=18, color=RED).next_to(hub_box, DOWN)
        self.play(Write(broadcast_text))
        self.wait(1)

        # --- ANIMATION: SWITCH DIRECT FLOW ---
        packet_s = Dot(point=s_p1.get_center(), color=BLUE, radius=0.1)
        self.play(Create(packet_s))
        self.play(packet_s.animate.move_to(switch_box.get_center()), run_time=1)
        
        # Only to Port 4
        dedicated_text = Text("Dedicated Bandwidth", font_size=18, color=YELLOW).next_to(switch_box, DOWN)
        self.play(
            packet_s.animate.move_to(s_p4.get_center()),
            Write(dedicated_text),
            run_time=1.5
        )
        
        # Indicate separate collision domains
        collision_label = Text("Separate Collision Domains", font_size=16, color=TEAL).next_to(switch_title, DOWN, buff=0.1)
        self.play(Write(collision_label))

        self.wait(2)
        
        # Cleanup
        self.play(
            FadeOut(hub_group), FadeOut(switch_group), FadeOut(packet_h), 
            FadeOut(p_h2), FadeOut(p_h3), FadeOut(p_h4), FadeOut(packet_s),
            FadeOut(broadcast_text), FadeOut(dedicated_text), FadeOut(collision_label),
            FadeOut(title), FadeOut(divider), FadeOut(hub_title), FadeOut(switch_title)
        )