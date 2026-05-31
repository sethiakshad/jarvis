from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Title and Explanation text
        title = Text("Hub as a Central Connector", font_size=36, color=GOLD).to_edge(UP)
        explanation = Text("Star Topology: Multi-port Repeater", font_size=24, color=WHITE).next_to(title, DOWN)
        
        # 2. Central Hub
        hub_rect = Rectangle(width=2.4, height=1.4, color=BLUE, fill_opacity=0.7)
        hub_label = Text("HUB", font_size=32, color=WHITE).move_to(hub_rect.get_center())
        
        # Create 5 ports (Dots) on the hub
        ports = VGroup()
        for i in range(5):
            port = Dot(radius=0.06, color=YELLOW)
            port.move_to(hub_rect.get_top() + DOWN * 0.3 + LEFT * 0.8 + RIGHT * (i * 0.4))
            ports.add(port)
            
        hub_group = VGroup(hub_rect, hub_label, ports)
        hub_group.move_to(ORIGIN)

        # 3. Create 5 Stations (PCs) in a circular star layout
        pcs = VGroup()
        lines = VGroup()
        
        # Angles for 5 nodes (starting from top)
        angles = [90, 162, 234, 306, 378]
        radius = 3.0
        
        for i, angle in enumerate(angles):
            # Define PC position using trigonometry
            angle_rad = angle * PI / 180
            pc_pos = [radius * np.cos(angle_rad), radius * np.sin(angle_rad), 0]
            
            # PC visual: Square + Text
            pc_box = Square(side_length=0.8, color=TEAL, fill_opacity=0.5)
            pc_text = Text(f"PC {i+1}", font_size=18, color=WHITE)
            pc = VGroup(pc_box, pc_text).move_to(pc_pos)
            pcs.add(pc)
            
            # Connection line from a specific hub port to the PC
            # Using port index for connection
            line = Line(ports[i].get_center(), pc.get_center(), color=WHITE, stroke_width=2)
            lines.add(line)

        # 4. Animation Sequence
        # Intro
        self.play(Write(title))
        self.play(Write(explanation))
        self.wait(1)
        
        # Show Hub
        self.play(Create(hub_rect), Write(hub_label))
        self.play(Create(ports))
        self.wait(0.5)
        
        # Draw connections and nodes (Star Formation)
        self.play(
            Create(lines),
            Create(pcs),
            run_time=3
        )
        self.wait(1.5)
        
        # Final Highlight: Focus on the physical star layout
        final_note = Text("Direct connection to individual ports", font_size=22, color=YELLOW).to_edge(DOWN)
        self.play(Write(final_note))
        self.wait(2.5)
        
        # Outro - Grouping all to avoid self.mobjects
        all_elements = VGroup(title, explanation, hub_group, pcs, lines, final_note)
        self.play(FadeOut(all_elements))