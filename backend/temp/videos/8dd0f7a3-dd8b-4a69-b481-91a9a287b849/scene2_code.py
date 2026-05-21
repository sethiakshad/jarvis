from manim import *

class Scene2(Scene):
    def construct(self):
        # 1. Background elements
        title = Text("Hub vs. Switch: Collision Domains", color=WHITE).scale(0.8).to_edge(UP)
        divider = Line(UP * 2, DOWN * 3, color=WHITE)
        hub_title = Text("Hub", color=RED).scale(0.7).shift(LEFT * 3.5 + UP * 2.2)
        switch_title = Text("Switch", color=GREEN).scale(0.7).shift(RIGHT * 3.5 + UP * 2.2)
        
        self.play(Write(title))
        self.play(Create(divider), Write(hub_title), Write(switch_title))

        # 2. Hub Setup (Left Side)
        hub_box = Square(color=RED, fill_opacity=0.3).scale(0.4).shift(LEFT * 3.5)
        h_node1 = Circle(radius=0.2, color=WHITE).shift(LEFT * 5 + UP * 1)
        h_node2 = Circle(radius=0.2, color=WHITE).shift(LEFT * 2 + UP * 1)
        h_node3 = Circle(radius=0.2, color=WHITE).shift(LEFT * 3.5 + DOWN * 1.5)
        
        h_lines = VGroup(
            Line(h_node1.get_center(), hub_box.get_center()),
            Line(h_node2.get_center(), hub_box.get_center()),
            Line(h_node3.get_center(), hub_box.get_center())
        )
        
        hub_group = VGroup(hub_box, h_node1, h_node2, h_node3, h_lines)
        self.play(Create(hub_group))

        # 3. Switch Setup (Right Side)
        switch_box = Square(color=GREEN, fill_opacity=0.3).scale(0.4).shift(RIGHT * 3.5)
        s_node1 = Circle(radius=0.2, color=WHITE).shift(RIGHT * 2 + UP * 1)
        s_node2 = Circle(radius=0.2, color=WHITE).shift(RIGHT * 5 + UP * 1)
        s_node3 = Circle(radius=0.2, color=WHITE).shift(RIGHT * 2 + DOWN * 1.5)
        s_node4 = Circle(radius=0.2, color=WHITE).shift(RIGHT * 5 + DOWN * 1.5)
        
        s_lines = VGroup(
            Line(s_node1.get_center(), switch_box.get_center()),
            Line(s_node2.get_center(), switch_box.get_center()),
            Line(s_node3.get_center(), switch_box.get_center()),
            Line(s_node4.get_center(), switch_box.get_center())
        )
        
        switch_group = VGroup(switch_box, s_node1, s_node2, s_node3, s_node4, s_lines)
        self.play(Create(switch_group))

        # 4. Hub Animation: Signal Broadcast
        packet_h = Dot(color=YELLOW).move_to(h_node1.get_center())
        self.play(packet_h.animate.move_to(hub_box.get_center()), run_time=1)
        
        packet_h2 = packet_h.copy()
        packet_h3 = packet_h.copy()
        
        broadcast_text = Text("Broadcasts to all", color=RED).scale(0.4).next_to(hub_box, DOWN)
        self.play(
            packet_h.animate.move_to(h_node2.get_center()),
            packet_h2.animate.move_to(h_node3.get_center()),
            Write(broadcast_text),
            run_time=1.5
        )
        self.play(FadeOut(packet_h), FadeOut(packet_h2), FadeOut(broadcast_text))

        # 5. Switch Animation: Simultaneous Dedicated Paths
        packet_s1 = Dot(color=GOLD).move_to(s_node1.get_center())
        packet_s3 = Dot(color=TEAL).move_to(s_node3.get_center())
        
        dedicated_text = Text("Dedicated Paths", color=GREEN).scale(0.4).next_to(switch_box, DOWN)
        
        # Step 1: To Switch
        self.play(
            packet_s1.animate.move_to(switch_box.get_center()),
            packet_s3.animate.move_to(switch_box.get_center()),
            Write(dedicated_text),
            run_time=1
        )
        # Step 2: To specific destinations
        self.play(
            packet_s1.animate.move_to(s_node2.get_center()),
            packet_s3.animate.move_to(s_node4.get_center()),
            run_time=1.5
        )
        
        # 6. Conclusion Text
        comparison = Text("1 Collision Domain vs. Many", color=YELLOW).scale(0.6).to_edge(DOWN)
        self.play(Write(comparison))
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(hub_group), 
            FadeOut(switch_group), 
            FadeOut(title), 
            FadeOut(divider), 
            FadeOut(hub_title), 
            FadeOut(switch_title),
            FadeOut(comparison),
            FadeOut(packet_s1),
            FadeOut(packet_s3),
            FadeOut(dedicated_text)
        )