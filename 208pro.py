
import tkinter as tk
import heapq
from tkinter import ttk

class GraphVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Algorithm Visualizer")
        
        # Start in fullscreen mode
        self.root.attributes('-fullscreen', True)
        
        # Configure colors - more vibrant palette
        self.bg_color = "#1E1E2E"  # Dark blue-gray
        self.panel_color = "#2A2A3A"  # Slightly lighter than bg
        self.button_color = "#414868"  # Muted purple
        self.text_color = "#F8F8F2"  # Off-white
        self.highlight_color = "#F38BA8"  # Pink
        self.node_color = "#89B4FA"  # Light blue
        self.edge_color = "#CDD6F4"  # Light gray
        self.path_color = "#A6E3A1"  # Mint green
        self.error_color = "#F38BA8"  # Pink (same as highlight for consistency)
        self.visited_color = "#CBA6F7"  # Lavender
        self.queue_color = "#F9E2AF"  # Light yellow
        
        # Additional colors for variety
        self.bfs_color = "#94E2D5"  # Teal
        self.dfs_color = "#FAB387"  # Peach
        self.dijkstra_color = "#A6E3A1"  # Mint green
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles for buttons with our colors
        self.style.configure("TButton", 
                           background=self.button_color,
                           foreground=self.text_color,
                           padding=6,
                           font=('Helvetica', 10))
        
        self.style.configure("Toolbutton", 
                           background=self.button_color,
                           foreground=self.text_color,
                           padding=6)
        
        self.style.configure("Accent.TButton", 
                           background=self.highlight_color,
                           foreground="#1E1E2E",  # Dark background color
                           padding=6,
                           font=('Helvetica', 10, 'bold'))
        
        self.style.map("Accent.TButton",
                      background=[('active', self.path_color)],
                      foreground=[('active', self.text_color)])
        
        # Main frame for canvas and control panel
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for graph drawing (takes 70% of width)
        self.canvas = tk.Canvas(self.main_frame, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Control panel on the right (30% of width)
        self.control_panel = tk.Frame(self.main_frame, width=400, bg=self.panel_color)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # Message panel with scrollbar
        self.message_frame = tk.Frame(self.control_panel, bg=self.panel_color)
        self.message_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.message_label = tk.Label(self.message_frame, text="Messages:", 
                                    bg=self.panel_color, fg=self.highlight_color,
                                    font=('Helvetica', 12, 'bold'))
        self.message_label.pack(anchor=tk.W)

        self.message_scroll = tk.Scrollbar(self.message_frame)
        self.message_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_text = tk.Text(self.message_frame, height=20, width=35, 
                                  bg=self.panel_color, fg=self.text_color,
                                  insertbackground=self.text_color,
                                  yscrollcommand=self.message_scroll.set,
                                  font=('Courier', 10),
                                  padx=10, pady=10)
        self.message_text.pack(fill=tk.BOTH, expand=True)
        self.message_scroll.config(command=self.message_text.yview)

        # Weight input panel
        self.weight_panel = tk.LabelFrame(self.control_panel, text="Edge Weight", 
                                        bg=self.panel_color, fg=self.highlight_color,
                                        font=('Helvetica', 10, 'bold'))
        self.weight_panel.pack(fill=tk.X, pady=5, padx=5)

        self.weight_entry = ttk.Entry(self.weight_panel, font=('Helvetica', 12))
        self.weight_entry.pack(fill=tk.X, padx=5, pady=5)
        self.weight_entry.insert(0, "1")

        self.weight_submit = ttk.Button(self.weight_panel, text="Set Weight", 
                                      command=self.set_weight,
                                      style="Accent.TButton")
        self.weight_submit.pack(fill=tk.X, padx=5, pady=2)

        # Node input panel for algorithms
        self.node_input_panel = tk.LabelFrame(self.control_panel, text="Algorithm Parameters", 
                                            bg=self.panel_color, fg=self.highlight_color,
                                            font=('Helvetica', 10, 'bold'))
        self.node_input_panel.pack(fill=tk.X, pady=5, padx=5)

        self.start_node_label = tk.Label(self.node_input_panel, text="Start Node:", 
                                       bg=self.panel_color, fg=self.text_color,
                                       font=('Helvetica', 10))
        self.start_node_label.pack(anchor=tk.W, padx=5)

        self.start_node_entry = ttk.Entry(self.node_input_panel, font=('Helvetica', 12))
        self.start_node_entry.pack(fill=tk.X, padx=5, pady=2)

        self.end_node_label = tk.Label(self.node_input_panel, text="End Node (Dijkstra):", 
                                    bg=self.panel_color, fg=self.text_color,
                                    font=('Helvetica', 10))
        self.end_node_label.pack(anchor=tk.W, padx=5)

        self.end_node_entry = ttk.Entry(self.node_input_panel, font=('Helvetica', 12))
        self.end_node_entry.pack(fill=tk.X, padx=5, pady=2)

        # Improved Actions Panel with clear grouping
        self.button_panel = tk.LabelFrame(self.control_panel, text="Actions", 
                                        bg=self.panel_color, fg=self.highlight_color,
                                        font=('Helvetica', 10, 'bold'))
        self.button_panel.pack(fill=tk.X, pady=5, padx=5)

        # Graph Editing Buttons Panel
        self.edit_panel = tk.Frame(self.button_panel, bg=self.panel_color)
        self.edit_panel.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(self.edit_panel, text="Graph Editing:", background=self.panel_color,
                 foreground=self.text_color, font=('Helvetica', 10, 'bold')).pack(anchor=tk.W, padx=5)

        self.edit_buttons_frame = tk.Frame(self.edit_panel, bg=self.panel_color)
        self.edit_buttons_frame.pack(fill=tk.X, pady=2)

        edit_buttons = [
            ("Add Node", self.add_node_mode, self.node_color),
            ("Add Edge", self.add_edge_mode, self.edge_color),
            ("Delete Node", self.delete_node_mode, self.error_color),
            ("Delete Edge", self.delete_edge_mode, self.error_color),
            ("Clear Graph", self.clear_graph, self.highlight_color)
        ]

        for text, command, color in edit_buttons:
            btn = tk.Button(self.edit_buttons_frame, text=text, command=command,
                          bg=color, fg="#1E1E2E", activebackground=self.path_color,
                          font=('Helvetica', 10), relief=tk.RAISED, bd=2)
            btn.pack(side=tk.LEFT, padx=2, pady=2, expand=True, fill=tk.X)

        # Algorithm Buttons Panel
        self.algo_panel = tk.Frame(self.button_panel, bg=self.panel_color)
        self.algo_panel.pack(fill=tk.X, pady=(5, 0))

        ttk.Label(self.algo_panel, text="Algorithms:", background=self.panel_color,
                 foreground=self.text_color, font=('Helvetica', 10, 'bold')).pack(anchor=tk.W, padx=5)

        self.algo_buttons_frame = tk.Frame(self.algo_panel, bg=self.panel_color)
        self.algo_buttons_frame.pack(fill=tk.X, pady=2)

        algo_buttons = [
            ("BFS", self.run_bfs, self.bfs_color),
            ("DFS", self.run_dfs, self.dfs_color),
            ("Dijkstra", self.run_dijkstra, self.dijkstra_color)
        ]

        for text, command, color in algo_buttons:
            btn = tk.Button(self.algo_buttons_frame, text=text, command=command,
                          bg=color, fg="#1E1E2E", activebackground=self.highlight_color,
                          font=('Helvetica', 10, 'bold'), relief=tk.RAISED, bd=2)
            btn.pack(side=tk.LEFT, padx=2, pady=2, expand=True, fill=tk.X)

        # Add exit fullscreen button
        self.exit_fullscreen_btn = ttk.Button(self.control_panel, text="Exit Fullscreen (F11)",
                                            command=self.toggle_fullscreen,
                                            style="Accent.TButton")
        self.exit_fullscreen_btn.pack(fill=tk.X, padx=5, pady=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, 
                                 bg=self.button_color, fg=self.text_color,
                                 anchor=tk.W, font=('Helvetica', 10, 'bold'))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Graph data structures
        self.nodes = []
        self.edges = []
        self.node_positions = {}
        self.node_count = 0
        self.mode = "node"
        self.selected_nodes = []
        self.current_weight = 1
        self.edge_creation_pending = False

        # Store graph adjacency list: node -> list of (neighbor, weight)
        self.graph = {}

        # For storing canvas item IDs for edges and weights, to delete easily
        self.edge_lines = {}  # key: (node1,node2) tuple sorted, value: line id
        self.edge_weights_text = {}  # key: (node1,node2) tuple sorted, value: text id

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.root.bind("<F11>", lambda event: self.toggle_fullscreen())
        self.update_status("Welcome to Graph Algorithm Visualizer! Press F11 to toggle fullscreen.")

    def toggle_fullscreen(self):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()

    def log_message(self, message, color=None):
        if color is None:
            color = self.text_color
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, message + "\n", color)
        self.message_text.tag_config(color, foreground=color)
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
        self.update_status(message)

    # Mode setters
    def add_node_mode(self):
        self.mode = "node"
        self.selected_nodes = []
        self.log_message("Switched to Node Adding Mode", self.node_color)

    def add_edge_mode(self):
        self.mode = "edge"
        self.selected_nodes = []
        self.edge_creation_pending = False
        self.log_message("Switched to Edge Adding Mode", self.edge_color)

    def delete_node_mode(self):
        self.mode = "delete_node"
        self.selected_nodes = []
        self.log_message("Switched to Delete Node Mode", self.error_color)

    def delete_edge_mode(self):
        self.mode = "delete_edge"
        self.selected_nodes = []
        self.log_message("Switched to Delete Edge Mode", self.error_color)

    def clear_graph(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.edges.clear()
        self.node_positions.clear()
        self.graph.clear()
        self.node_count = 0
        self.edge_lines.clear()
        self.edge_weights_text.clear()
        self.selected_nodes.clear()
        self.log_message("Cleared the graph", self.highlight_color)

    def on_canvas_click(self, event):
        if self.mode == "node":
            self.create_node(event.x, event.y)
        elif self.mode == "edge":
            self.select_node_for_edge(event.x, event.y)
        elif self.mode == "delete_node":
            self.delete_node(event.x, event.y)
        elif self.mode == "delete_edge":
            self.select_edge_for_deletion(event.x, event.y)

    # Node creation
    def create_node(self, x, y):
        r = 25  # Larger nodes for better visibility
        node_id = self.node_count
        # Create node with gradient effect
        self.canvas.create_oval(x - r, y - r, x + r, y + r, 
                              fill=self.node_color, outline=self.highlight_color,
                              width=3, tags=f"node{node_id}")
        self.canvas.create_text(x, y, text=str(node_id), 
                              fill=self.text_color, font=('Helvetica', 12, 'bold'),
                              tags=f"node{node_id}")
        self.node_positions[node_id] = (x, y)
        self.nodes.append(node_id)
        self.graph[node_id] = []
        self.node_count += 1
        self.log_message(f"Node {node_id} added at ({x}, {y})", self.node_color)

    # Node deletion
    def delete_node(self, x, y):
        node_to_delete = None
        for node_id, (nx, ny) in self.node_positions.items():
            if abs(x - nx) < 30 and abs(y - ny) < 30:  # Larger click area
                node_to_delete = node_id
                break
        if node_to_delete is not None:
            # Remove node from canvas
            self.canvas.delete(f"node{node_to_delete}")
            # Remove edges connected to this node
            edges_to_remove = [edge for edge in self.edges if node_to_delete in edge]
            for edge in edges_to_remove:
                self.remove_edge_from_canvas(edge[0], edge[1])
                self.edges.remove(edge)
                # Remove from graph adjacency
                self.graph[edge[0]] = [(n, w) for (n, w) in self.graph[edge[0]] if n != edge[1]]
                self.graph[edge[1]] = [(n, w) for (n, w) in self.graph[edge[1]] if n != edge[0]]

            # Remove node from data structures
            self.nodes.remove(node_to_delete)
            del self.node_positions[node_to_delete]
            del self.graph[node_to_delete]
            self.log_message(f"Deleted node {node_to_delete} and its connected edges", self.error_color)

    # Edge creation
    def select_node_for_edge(self, x, y):
        for node_id, (nx, ny) in self.node_positions.items():
            if abs(x - nx) < 30 and abs(y - ny) < 30:  # Larger click area
                if node_id not in self.selected_nodes:
                    self.selected_nodes.append(node_id)
                    self.log_message(f"Node {node_id} selected", self.highlight_color)
                    
                    # Highlight selected node with animation
                    self.animate_node(node_id, self.highlight_color)
                    
                    if len(self.selected_nodes) == 2:
                        self.create_edge(self.selected_nodes[0], self.selected_nodes[1])
                        # Reset node colors with animation
                        for n in self.selected_nodes:
                            self.animate_node(n, self.node_color)
                        self.selected_nodes = []
                break

    def animate_node(self, node_id, target_color):
        current_color = self.node_color
        steps = 10
        delay = 30  # ms
        
        r1, g1, b1 = self.hex_to_rgb(current_color)
        r2, g2, b2 = self.hex_to_rgb(target_color)
        
        for i in range(steps + 1):
            r = int(r1 + (r2 - r1) * i / steps)
            g = int(g1 + (g2 - g1) * i / steps)
            b = int(b1 + (b2 - b1) * i / steps)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.itemconfig(f"node{node_id}", fill=color)
            self.root.update()
            self.root.after(delay)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def set_weight(self):
        try:
            self.current_weight = int(self.weight_entry.get())
            self.log_message(f"Weight set to {self.current_weight}", self.highlight_color)
        except ValueError:
            self.current_weight = 1
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, "1")
            self.log_message("Invalid weight, using default value 1", self.error_color)

    def create_edge(self, node1, node2):
        if node1 == node2:
            self.log_message("Cannot connect node to itself", self.error_color)
            return

        # Check if edge already exists
        edge_key = tuple(sorted((node1, node2)))
        if edge_key in self.edge_lines:
            self.log_message("Edge already exists", self.error_color)
            return

        x1, y1 = self.node_positions[node1]
        x2, y2 = self.node_positions[node2]

        # Create arrow with style
        line_id = self.canvas.create_line(x1, y1, x2, y2, 
                                        fill=self.edge_color, width=3,
                                        arrow=tk.LAST, arrowshape=(12, 15, 6),
                                        dash=(4, 2) if node1 > node2 else None)  # Different style for reverse edges
        self.edges.append((node1, node2))
        self.edge_lines[edge_key] = line_id

        # Add weight text above the edge line midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        offset = -15  # Move weight label slightly above the line
        weight_text_id = self.canvas.create_text(mid_x, mid_y + offset, 
                                              text=str(self.current_weight), 
                                              fill=self.text_color, 
                                              font=("Helvetica", 12, "bold"),
                                              tags=f"weight{edge_key}")
        self.edge_weights_text[edge_key] = weight_text_id

        self.graph[node1].append((node2, self.current_weight))
        self.graph[node2].append((node1, self.current_weight))

        self.log_message(f"Edge added between {node1} and {node2} with weight {self.current_weight}", self.edge_color)

    # Remove edge helper
    def remove_edge_from_canvas(self, node1, node2):
        edge_key = tuple(sorted((node1, node2)))
        if edge_key in self.edge_lines:
            self.canvas.delete(self.edge_lines[edge_key])
            del self.edge_lines[edge_key]
        if edge_key in self.edge_weights_text:
            self.canvas.delete(self.edge_weights_text[edge_key])
            del self.edge_weights_text[edge_key]

    # Delete edge mode
    def select_edge_for_deletion(self, x, y):
        # Detect which edge line is near clicked point
        # We'll approximate by checking distance to line segments
        for (node1, node2) in self.edges:
            x1, y1 = self.node_positions[node1]
            x2, y2 = self.node_positions[node2]

            if self.point_near_line(x, y, x1, y1, x2, y2):
                # Delete edge line and weight text
                self.remove_edge_from_canvas(node1, node2)
                self.edges.remove((node1, node2))
                # Remove from graph adjacency list
                self.graph[node1] = [(n, w) for (n, w) in self.graph[node1] if n != node2]
                self.graph[node2] = [(n, w) for (n, w) in self.graph[node2] if n != node1]
                self.log_message(f"Deleted edge between {node1} and {node2}", self.error_color)
                break

    # Helper to check if point (px,py) near line segment (x1,y1)-(x2,y2)
    def point_near_line(self, px, py, x1, y1, x2, y2, threshold=15):  # Larger threshold
        # Calculate distance from point to line segment
        line_mag = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        if line_mag < 0.000001:
            return False

        u = ((px - x1)*(x2 - x1) + (py - y1)*(y2 - y1)) / (line_mag**2)
        if u < 0 or u > 1:
            return False

        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        dist = ((px - ix)**2 + (py - iy)**2)**0.5
        return dist <= threshold

    # BFS
    def run_bfs(self):
        try:
            start_node = int(self.start_node_entry.get())
        except ValueError:
            self.log_message("Invalid start node", self.error_color)
            return
            
        if start_node not in self.graph:
            self.log_message("Start node does not exist.", self.error_color)
            return

        visited = []
        queue = []

        visited.append(start_node)
        queue.append(start_node)

        self.log_message("\nBFS Traversal:", self.bfs_color)

        while queue:
            current = queue.pop(0)
            self.log_message(f"Visited {current}")
            self.highlight_node(current, self.bfs_color)
            self.root.update()
            self.root.after(500)  # Pause for visualization

            for neighbor, _ in self.graph[current]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
                    self.highlight_edge(current, neighbor, self.bfs_color)
                    self.root.update()
                    self.root.after(300)

        # Reset colors after traversal
        self.reset_colors()

    # DFS
    def run_dfs(self):
        try:
            start_node = int(self.start_node_entry.get())
        except ValueError:
            self.log_message("Invalid start node", self.error_color)
            return
            
        if start_node not in self.graph:
            self.log_message("Start node does not exist.", self.error_color)
            return
            
        visited = []
        self.log_message("\nDFS Traversal:", self.dfs_color)
        self.dfs_helper(start_node, visited)
        self.reset_colors()

    def dfs_helper(self, node, visited):
        if node not in visited:
            visited.append(node)
            self.log_message(f"Visited {node}")
            self.highlight_node(node, self.dfs_color)
            self.root.update()
            self.root.after(500)  # Pause for visualization

            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    self.highlight_edge(node, neighbor, self.dfs_color)
                    self.root.update()
                    self.root.after(300)
                    self.dfs_helper(neighbor, visited)

    # Dijkstra
    def run_dijkstra(self):
        try:
            start_node = int(self.start_node_entry.get())
            end_node = int(self.end_node_entry.get())
        except ValueError:
            self.log_message("Invalid node numbers", self.error_color)
            return
            
        if start_node not in self.graph:
            self.log_message("Start node does not exist.", self.error_color)
            return
        if end_node not in self.graph:
            self.log_message("End node does not exist.", self.error_color)
            return
            
        distances = {node: float('inf') for node in self.graph}
        distances[start_node] = 0
        visited = set()
        previous_nodes = {node: None for node in self.graph}

        min_heap = [(0, start_node)]

        self.log_message("\nDijkstra's Shortest Path:", self.dijkstra_color)

        while min_heap:
            current_dist, current_node = heapq.heappop(min_heap)

            if current_node in visited:
                continue

            visited.add(current_node)
            self.highlight_node(current_node, self.dijkstra_color)
            self.root.update()
            self.root.after(300)
            
            if current_node == end_node:
                break

            for neighbor, weight in self.graph[current_node]:
                if neighbor not in visited:
                    new_dist = current_dist + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        previous_nodes[neighbor] = current_node
                        heapq.heappush(min_heap, (new_dist, neighbor))
                        self.highlight_edge(current_node, neighbor, self.dijkstra_color)
                        self.root.update()
                        self.root.after(200)

        # Reconstruct path
        path = []
        current = end_node
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()

        if distances[end_node] != float('inf'):
            self.log_message(f"Shortest path from {start_node} to {end_node}: {path}")
            self.log_message(f"Total distance: {distances[end_node]}")
            
            # Highlight the final path
            self.highlight_path(path)
        else:
            self.log_message(f"No path exists from {start_node} to {end_node}", self.error_color)

    def highlight_node(self, node, color):
        self.canvas.itemconfig(f"node{node}", fill=color)

    def highlight_edge(self, node1, node2, color):
        edge_key = tuple(sorted((node1, node2)))
        if edge_key in self.edge_lines:
            self.canvas.itemconfig(self.edge_lines[edge_key], fill=color, width=4)

    def highlight_path(self, path):
        # Reset all colors first
        self.reset_colors()
        
        # Color nodes in path
        for node in path:
            self.highlight_node(node, self.path_color)
            
        # Color edges in path
        for i in range(len(path)-1):
            self.highlight_edge(path[i], path[i+1], self.path_color)

    def reset_colors(self):
        for node in self.nodes:
            self.canvas.itemconfig(f"node{node}", fill=self.node_color)
            
        for edge in self.edge_lines.values():
            self.canvas.itemconfig(edge, fill=self.edge_color, width=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()

