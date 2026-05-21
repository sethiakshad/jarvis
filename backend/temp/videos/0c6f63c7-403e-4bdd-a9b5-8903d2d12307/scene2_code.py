from manim import *

class Scene2(Scene):
    def construct(self):
        # Title and Hub Setup
        title = Text("Hub Broadcasting Mechanism", font_size=32, color=WHITE).to_edge(UP)
        hub = Square(side_length=1.8, color=GOLD, fill_opacity=0.4)
        hub_label = Text("HUB", font_size=24, color=WHITE).move_to(hub.get_center())
        hub_group = VGroup(hub, hub_label)
        
        # Connected Devices (using Circles)
        d1 = Circle(radius=0.5, color=BLUE, fill_opacity=0.5).move_to(3*LEFT + 2*UP)
        d2 = Circle(radius=0.5, color=BLUE, fill_opacity=0.5).move_to(3*RIGHT + 2*UP)
        d3 = Circle(radius=0.5, color=BLUE, fill_opacity=0.5).move_to(3*LEFT + 2*DOWN)
        d4 = Circle(radius=0.5, color=BLUE, fill_opacity=0.5).move_to(3*RIGHT + 2*DOWN)
        
        l1 = Line(d1.get_center(), hub.get_center(), color=GRAY)
        l2 = Line(d2.get_center(), hub.get_center(), color=GRAY)
        l3 = Line(d3.get_center(), hub.get_center(), color=GRAY)
        l4 = Line(d4.get_center(), hub.get_center(), color=GRAY)
        
        devices = VGroup(d1, d2, d3, d4)
        lines = VGroup(l1, l2, l3, l4)
        
        # Explanation Text
        explanation = Text("Hubs cannot filter data", font_size=24, color=YELLOW).to_edge(DOWN)

        self.add(title, hub_group, devices, lines)
        self.play(Write(explanation))
        self.wait(1)

        # Incoming Data Packet from Device 1
        packet_rect = Rectangle(width=0.8, height=0.4, color=WHITE, fill_opacity=1)
        packet_text = Text("Data", font_size=18, color=BLACK).move_to(packet_rect.get_center())
        packet = VGroup(packet_rect, packet_text).move_to(d1.get_center())

        self.play(packet.animate.move_to(hub.get_center()), run_time=1.5)
        
        # Splitting/Broadcasting
        p2 = packet.copy()
        p3 = packet.copy()
        p4 = packet.copy()
        
        broadcast_label = Text("Broadcasting to all ports...", font_size=24, color=RED).to_edge(DOWN)
        self.play(Transform(explanation, broadcast_label))

        self.play(
            p2.animate.move_to(d2.get_center()),
            p3.animate.move_to(d3.get_center()),
            p4.animate.move_to(d4.get_center()),
            packet.animate.set_fill(opacity=0),
            run_time=2
        )
        
        self.wait(2)
        
        # Conclusion of Scene
        final_note = Text("Intelligence Lack: No destination filtering", font_size=20, color=WHITE).to_edge(DOWN)
        self.play(Transform(explanation, final_note))
        self.wait(2)

        # Cleanup for 25s limit
        self.play(FadeOut(VGroup(hub_group, devices, lines, p2, p3, p4, title, explanation, packet)))

if __name__ == "__main__":
    pass