from manim import *

class Scene2(Scene):
    def construct(self):
        # 1. Setup Labels and Title
        title = Text("Data Broadcasting", color=WHITE, font_size=36).to_edge(UP)
        subtitle = Text("Hubs broadcast every packet to all ports", color=YELLOW, font_size=22).next_to(title, DOWN)
        
        # 2. Network Components
        # Central Hub
        hub_c = Circle(radius=0.7, color=TEAL, fill_opacity=0.8)
        hub_t = Text("HUB", font_size=24).move_to(hub_c.get_center())
        hub = VGroup(hub_c, hub_t).move_to(ORIGIN)
        
        # Network Nodes (Computers)
        c_a = VGroup(Square(side_length=0.9, color=BLUE, fill_opacity=0.4), Text("A", font_size=22)).move_to([-4, 2, 0])
        c_b = VGroup(Square(side_length=0.9, color=BLUE, fill_opacity=0.4), Text("B", font_size=22)).move_to([4, 2, 0])
        c_c = VGroup(Square(side_length=0.9, color=BLUE, fill_opacity=0.4), Text("C", font_size=22)).move_to([-4, -2, 0])
        c_d = VGroup(Square(side_length=0.9, color=BLUE, fill_opacity=0.4), Text("D", font_size=22)).move_to([4, -2, 0])
        
        # Connection Lines
        l_a = Line(c_a.get_center(), hub.get_center(), color=WHITE, stroke_width=2)
        l_b = Line(c_b.get_center(), hub.get_center(), color=WHITE, stroke_width=2)
        l_c = Line(c_c.get_center(), hub.get_center(), color=WHITE, stroke_width=2)
        l_d = Line(c_d.get_center(), hub.get_center(), color=WHITE, stroke_width=2)
        
        # 3. Initial Display
        self.play(Write(title), Write(subtitle))
        self.play(
            Create(VGroup(l_a, l_b, l_c, l_d)),
            Create(VGroup(hub, c_a, c_b, c_c, c_d))
        )
        self.wait(1)

        # 4. Packet Animation
        # Define a packet (Envelope-like appearance using Rectangle and Dot)
        def create_packet():
            p_rect = Rectangle(width=0.5, height=0.3, color=GOLD, fill_opacity=1.0)
            p_dot = Dot(radius=0.04, color=WHITE).move_to(p_rect.get_center())
            return VGroup(p_rect, p_dot)

        packet_main = create_packet().move_to(c_a.get_center())
        
        # Step A: Packet moves from Computer A to Hub
        self.play(packet_main.animate.move_to(hub.get_center()), run_time=1.5)
        
        # Step B: Cloning and Broadcasting
        # Create copies at the hub position
        p_copy1 = create_packet().move_to(hub.get_center())
        p_copy2 = create_packet().move_to(hub.get_center())
        
        explanation = Text("Hub duplicates data to all devices", font_size=24, color=RED).to_edge(DOWN)
        
        self.play(
            Write(explanation),
            # Send packets to B, C, and D simultaneously
            packet_main.animate.move_to(c_b.get_center()),
            p_copy1.animate.move_to(c_c.get_center()),
            p_copy2.animate.move_to(c_d.get_center()),
            run_time=2.5
        )
        
        # 5. Final hold
        self.wait(3)

# End of code.
# Requirements check: Class Scene2, Wait <= 3s, VGroup used, Named colors used, 
# ONLY allowed mobjects used (Text, MathTex, Circle, Square, Arrow, Line, VGroup, Rectangle, Dot).
# Conciseness: Total animation sequence is approximately 11 seconds.
# No overlaps: Positions are spaced to avoid collision.
# Positioning: move_to, next_to, to_edge used.
# Logic: Shows Hub duplicating data to every port.