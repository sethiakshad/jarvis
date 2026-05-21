from manim import *

class Scene1(Scene):
    def construct(self):
        # --- PART 1: REPEATER (Signal Regeneration) ---
        title = Text("Layer 1: Repeater & Hub", color=BLUE).to_edge(UP)
        self.play(Write(title))

        repeater_box = Rectangle(height=1.5, width=3, color=TEAL, fill_opacity=0.2)
        repeater_label = Text("REPEATER", font_size=24).move_to(repeater_box.get_center())
        repeater = VGroup(repeater_box, repeater_label).shift(UP * 0.5)

        # Signal lines
        weak_signal = Line(LEFT * 6, LEFT * 1.5, color=WHITE, stroke_width=2).set_opacity(0.3)
        weak_label = Text("Weak Signal", font_size=20, color=RED).next_to(weak_signal, UP)
        
        strong_signal = Line(RIGHT * 1.5, RIGHT * 6, color=GREEN, stroke_width=8)
        strong_label = Text("Regenerated Signal", font_size=20, color=GREEN).next_to(strong_signal, UP)

        self.play(Create(repeater))
        self.play(Create(weak_signal), Write(weak_label))
        self.wait(1)
        
        # Regeneration animation
        pulse = Dot(color=YELLOW).move_to(weak_signal.get_start())
        self.play(pulse.animate.move_to(repeater_box.get_left()), run_time=1.5)
        self.play(Create(strong_signal), Write(strong_label), pulse.animate.move_to(strong_signal.get_end()))
        self.play(FadeOut(pulse))
        self.wait(1)

        # Clear Repeater section
        self.play(FadeOut(repeater), FadeOut(weak_signal), FadeOut(weak_label), FadeOut(strong_signal), FadeOut(strong_label))

        # --- PART 2: HUB (Broadcasting) ---
        hub_box = Square(side_length=1.5, color=GOLD, fill_opacity=0.2).shift(DOWN * 0.5)
        hub_label = Text("HUB", font_size=24).move_to(hub_box.get_center())
        hub = VGroup(hub_box, hub_label)

        # Connected PCs
        pc_tl = Circle(radius=0.4, color=WHITE).shift(UP * 1.5 + LEFT * 3)
        pc_tr = Circle(radius=0.4, color=WHITE).shift(UP * 1.5 + RIGHT * 3)
        pc_bl = Circle(radius=0.4, color=WHITE).shift(DOWN * 2.5 + LEFT * 3)
        pc_br = Circle(radius=0.4, color=WHITE).shift(DOWN * 2.5 + RIGHT * 3)
        
        pcs = VGroup(pc_tl, pc_tr, pc_bl, pc_br)
        
        # Connections
        l1 = Line(hub_box.get_corner(UL), pc_tl.get_center(), color=GRAY)
        l2 = Line(hub_box.get_corner(UR), pc_tr.get_center(), color=GRAY)
        l3 = Line(hub_box.get_corner(DL), pc_bl.get_center(), color=GRAY)
        l4 = Line(hub_box.get_corner(DR), pc_br.get_center(), color=GRAY)
        lines = VGroup(l1, l2, l3, l4)

        self.play(Create(hub), Create(pcs), Create(lines))
        
        # Broadcasting Packet
        packet_start = Dot(color=YELLOW).move_to(pc_tl.get_center())
        self.play(FadeIn(packet_start))
        
        # Packet to Hub
        self.play(packet_start.animate.move_to(hub_box.get_center()), run_time=1)
        
        # Hub broadcasts to all others (copies)
        p1 = Dot(color=YELLOW).move_to(hub_box.get_center())
        p2 = Dot(color=YELLOW).move_to(hub_box.get_center())
        p3 = Dot(color=YELLOW).move_to(hub_box.get_center())
        
        self.play(
            p1.animate.move_to(pc_tr.get_center()),
            p2.animate.move_to(pc_bl.get_center()),
            p3.animate.move_to(pc_br.get_center()),
            packet_start.animate.set_opacity(0),
            run_time=1.5
        )
        
        no_filter = Text("Broadcasting: No Filtering", font_size=24, color=RED).next_to(hub_box, DOWN)
        self.play(Write(no_filter))
        self.wait(2)

        # Final Cleanup
        self.play(FadeOut(hub), FadeOut(pcs), FadeOut(lines), FadeOut(p1), FadeOut(p2), FadeOut(p3), FadeOut(no_filter), FadeOut(title))