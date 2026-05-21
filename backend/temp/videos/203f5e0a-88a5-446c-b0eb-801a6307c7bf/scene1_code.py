from manim import *

class Scene1(Scene):
    def construct(self):
        # Title
        title = Text("Star Topology: The Hub", font_size=36, color=WHITE).to_edge(UP)
        
        # Central Hub
        hub_rect = Rectangle(width=2.5, height=1.5, color=BLUE, fill_opacity=0.5)
        hub_text = Text("Hub", font_size=28).move_to(hub_rect.get_center())
        hub = VGroup(hub_rect, hub_text).move_to(ORIGIN)

        # Peripheral PCs
        pc_positions = [
            [-4, 2, 0],  # Top Left
            [4, 2, 0],   # Top Right
            [-4, -2, 0], # Bottom Left
            [4, -2, 0]   # Bottom Right
        ]
        
        pcs = VGroup()
        lines = VGroup()
        
        for i, pos in enumerate(pc_positions):
            pc_box = Square(side_length=1.0, color=TEAL, fill_opacity=0.3)
            pc_label = Text(f"PC {i+1}", font_size=20).move_to(pc_box.get_center())
            pc_group = VGroup(pc_box, pc_label).move_to(pos)
            pcs.add(pc_group)
            
            # Lines from Hub to PC
            conn_line = Line(hub.get_center(), pc_group.get_center(), color=WHITE, stroke_width=2)
            lines.add(conn_line)

        # Explanation Text
        explanation = Text("Multi-port Repeater", font_size=24, color=YELLOW).to_edge(DOWN)

        # Animations
        self.play(Write(title))
        self.play(Create(hub))
        self.wait(1)

        # Create PCs and connections
        self.play(
            Create(pcs),
            Create(lines),
            run_time=2
        )
        self.play(Write(explanation))
        self.wait(1)

        # Signal Pulse Animation
        # Pulse enters from PC 1 to Hub
        pulse = Dot(point=pcs[0].get_center(), color=GREEN, radius=0.15)
        
        self.play(pulse.animate.move_to(hub.get_center()), run_time=1.5)
        
        # Hub "Glows" as it receives signal
        glow_rect = Rectangle(width=2.7, height=1.7, color=GREEN, stroke_width=8).move_to(hub.get_center())
        self.play(
            Create(glow_rect),
            hub_rect.animate.set_fill(GREEN, fill_opacity=0.8),
            run_time=0.5
        )
        self.play(FadeOut(glow_rect), hub_rect.animate.set_fill(BLUE, fill_opacity=0.5))

        # Pulse repeats to all other ports
        pulse2 = Dot(point=hub.get_center(), color=GREEN)
        pulse3 = Dot(point=hub.get_center(), color=GREEN)
        pulse4 = Dot(point=hub.get_center(), color=GREEN)
        
        self.play(
            pulse.animate.move_to(pcs[1].get_center()),
            pulse2.animate.move_to(pcs[2].get_center()),
            pulse3.animate.move_to(pcs[3].get_center()),
            run_time=1.5
        )
        
        self.play(FadeOut(pulse), FadeOut(pulse2), FadeOut(pulse3))
        self.wait(2)

        # Final cleanup/Closing
        self.play(
            FadeOut(title),
            FadeOut(hub),
            FadeOut(pcs),
            FadeOut(lines),
            FadeOut(explanation)
        )