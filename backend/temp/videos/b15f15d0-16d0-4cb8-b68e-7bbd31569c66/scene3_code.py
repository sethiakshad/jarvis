from manim import *

class Scene3(Scene):
    def construct(self):
        # Title
        title = Text("Router and Gateway: Connectivity", color=WHITE, font_size=32).to_edge(UP)
        self.add(title)

        # --- ROUTER SECTION ---
        lan_box = Rectangle(height=2, width=3, color=BLUE, fill_opacity=0.2).shift(LEFT * 4)
        wan_box = Rectangle(height=2, width=3, color=TEAL, fill_opacity=0.2).shift(RIGHT * 4)
        router_sq = Square(side_length=1.2, color=GOLD, fill_opacity=0.5).move_to(ORIGIN)
        
        lan_label = Text("LAN", font_size=24, color=BLUE).next_to(lan_box, UP)
        wan_label = Text("WAN", font_size=24, color=TEAL).next_to(wan_box, UP)
        router_label = Text("Router", font_size=24, color=GOLD).next_to(router_sq, UP)
        
        router_group = VGroup(lan_box, wan_box, router_sq, lan_label, wan_label, router_label)
        self.play(Create(router_group), run_time=2)

        # Packet movement (Router)
        pkt_rect = Rectangle(height=0.4, width=0.6, color=WHITE, fill_opacity=1)
        pkt_text = MathTex("IP", font_size=18, color=BLACK).move_to(pkt_rect.get_center())
        packet = VGroup(pkt_rect, pkt_text).move_to(lan_box.get_center())

        self.play(packet.animate.move_to(router_sq.get_center()))
        self.wait(0.5)
        self.play(packet.animate.move_to(wan_box.get_center()))
        self.play(FadeOut(packet))
        
        # Transition to Gateway
        self.play(FadeOut(router_group))

        # --- GATEWAY SECTION ---
        net_a = Circle(radius=1.2, color=RED, fill_opacity=0.2).shift(LEFT * 4)
        net_b = Square(side_length=2.4, color=BLUE, fill_opacity=0.2).shift(RIGHT * 4)
        gateway_rect = Rectangle(height=1.5, width=2.5, color=YELLOW, fill_opacity=0.5).move_to(ORIGIN)
        
        a_label = Text("Network A (Model 1)", font_size=20, color=RED).next_to(net_a, UP)
        b_label = Text("Network B (Model 2)", font_size=20, color=BLUE).next_to(net_b, UP)
        gw_label = Text("Gateway (Converter)", font_size=24, color=YELLOW).next_to(gateway_rect, UP)
        
        gateway_scene = VGroup(net_a, net_b, gateway_rect, a_label, b_label, gw_label)
        self.play(Create(gateway_scene), run_time=2)

        # Protocol Conversion Animation
        # Packet starts as a Circle in Net A
        p_in = Circle(radius=0.2, color=WHITE, fill_opacity=1).move_to(net_a.get_center())
        p_mid = Rectangle(height=0.4, width=0.4, color=WHITE, fill_opacity=1).move_to(gateway_rect.get_center())
        p_out = Square(side_length=0.4, color=WHITE, fill_opacity=1).move_to(net_b.get_center())

        self.play(Create(p_in))
        self.play(p_in.animate.move_to(gateway_rect.get_center()))
        
        # Transform inside Gateway (Protocol conversion)
        self.play(ReplacementTransform(p_in, p_mid))
        conversion_text = Text("Converting Protocol...", font_size=16, color=YELLOW).next_to(gateway_rect, DOWN)
        self.play(Write(conversion_text))
        self.wait(1)
        
        # Move out as Square to Net B
        self.play(ReplacementTransform(p_mid, p_out))
        self.play(p_out.animate.scale(1.2), FadeOut(conversion_text))
        
        self.wait(2)