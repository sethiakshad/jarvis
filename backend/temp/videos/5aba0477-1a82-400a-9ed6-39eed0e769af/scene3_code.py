from manim import *

class Scene3(Scene):
    def construct(self):
        # Title
        title = Text("Routers vs Gateways", color=WHITE).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # --- Router Section (Top Half) ---
        router_box = Rectangle(height=1.0, width=2.0, color=BLUE, fill_opacity=0.2).shift(UP * 1)
        router_text = Text("Router", font_size=24).move_to(router_box)
        
        lan_node = Circle(radius=0.5, color=GREEN).next_to(router_box, LEFT, buff=1.5)
        lan_label = Text("LAN", font_size=20).next_to(lan_node, DOWN)
        
        wan_node = Circle(radius=0.5, color=TEAL).next_to(router_box, RIGHT, buff=1.5)
        wan_label = Text("WAN", font_size=20).next_to(wan_node, DOWN)
        
        path_l = Line(lan_node.get_right(), router_box.get_left())
        path_r = Line(router_box.get_right(), wan_node.get_left())
        
        router_group = VGroup(router_box, router_text, lan_node, lan_label, wan_node, wan_label, path_l, path_r)
        self.play(Create(router_group))

        # Routing Packet Animation
        packet_r = Square(side_length=0.2, fill_opacity=1, color=YELLOW).move_to(lan_node)
        routing_info = Text("IP Path Found", font_size=18, color=YELLOW).next_to(router_box, UP, buff=0.2)
        
        self.play(packet_r.animate.move_to(router_box))
        self.play(Write(routing_info))
        self.play(packet_r.animate.move_to(wan_node))
        self.play(FadeOut(packet_r), FadeOut(routing_info))
        
        self.wait(1)

        # --- Gateway Section (Bottom Half) ---
        gateway_box = Rectangle(height=1.0, width=2.0, color=RED, fill_opacity=0.2).shift(DOWN * 1.5)
        gateway_text = Text("Gateway", font_size=24).move_to(gateway_box)
        
        sys_a = Text("Protocol A", font_size=20, color=GOLD).next_to(gateway_box, LEFT, buff=1.2)
        sys_b = Text("Protocol B", font_size=20, color=WHITE).next_to(gateway_box, RIGHT, buff=1.2)
        
        arrow_a = Arrow(sys_a.get_right(), gateway_box.get_left(), buff=0.1)
        arrow_b = Arrow(gateway_box.get_right(), sys_b.get_left(), buff=0.1)
        
        gateway_group = VGroup(gateway_box, gateway_text, sys_a, sys_b, arrow_a, arrow_b)
        self.play(Create(gateway_group))

        # Gateway Conversion Animation
        packet_g = Square(side_length=0.2, fill_opacity=1, color=GOLD).move_to(sys_a)
        conversion_text = Text("Translating...", font_size=18, color=RED).next_to(gateway_box, DOWN, buff=0.2)
        
        self.play(packet_g.animate.move_to(gateway_box))
        self.play(Write(conversion_text))
        # Change appearance to show translation
        self.play(packet_g.animate.set_color(WHITE).scale(1.2))
        self.play(packet_g.animate.move_to(sys_b))
        
        self.play(FadeOut(packet_g), FadeOut(conversion_text))
        
        # Summary Labels
        label_router = Text("Layer 3: IP Forwarding", font_size=16, color=BLUE).next_to(router_group, UP, buff=0.1)
        label_gateway = Text("Protocol Conversion", font_size=16, color=RED).next_to(gateway_group, DOWN, buff=0.1)
        
        self.play(Write(label_router), Write(label_gateway))
        self.wait(2)