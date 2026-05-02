
import math

def rotate_x(x, y, z, angle):
    rad = math.radians(angle)
    ny = y * math.cos(rad) - z * math.sin(rad)
    nz = y * math.sin(rad) + z * math.cos(rad)
    return x, ny, nz

def rotate_y(x, y, z, angle):
    rad = math.radians(angle)
    nx = x * math.cos(rad) + z * math.sin(rad)
    nz = -x * math.sin(rad) + z * math.cos(rad)
    return nx, y, nz

def rotate_z(x, y, z, angle):
    rad = math.radians(angle)
    nx = x * math.cos(rad) - y * math.sin(rad)
    ny = x * math.sin(rad) + y * math.cos(rad)
    return nx, ny, z

def project(x, y, z, fov, viewer_distance):
    factor = fov / (viewer_distance + z)
    return x * factor, y * factor

def main():
    cube_vertices = [
        (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
        (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
    ]

    cube_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
        (0, 4), (1, 5), (2, 6), (3, 7)  # Connecting edges
    ]

    screen_width = 80
    screen_height = 40
    fov = 10  # Field of view / scaling factor
    viewer_distance = 5 # Distance from the viewer to the projection plane
    angle_x, angle_y, angle_z = 30, 45, 0  # Rotation angles

    frame_buffer = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]

    projected_points_raw = []
    for x, y, z in cube_vertices:
        # Rotate
        x, y, z = rotate_x(x, y, z, angle_x)
        x, y, z = rotate_y(x, y, z, angle_y)
        x, y, z = rotate_z(x, y, z, angle_z)

        # Project to 2D plane
        px, py = project(x, y, z, fov, viewer_distance)
        projected_points_raw.append((px, py, z)) # Store raw projected for calculating min/max

    # Calculate min/max projected coordinates for dynamic scaling
    min_px = min(p[0] for p in projected_points_raw)
    max_px = max(p[0] for p in projected_points_raw)
    min_py = min(p[1] for p in projected_points_raw)
    max_py = max(p[1] for p in projected_points_raw)

    # Add a small padding to min/max to ensure points at edges are not clipped
    padding_x = (max_px - min_px) * 0.1
    padding_y = (max_py - min_py) * 0.1
    min_px -= padding_x
    max_px += padding_x
    min_py -= padding_y
    max_py += padding_y

    # Determine scaling factors to fit within screen dimensions
    # We use a common scale factor to maintain aspect ratio
    range_px = max_px - min_px
    range_py = max_py - min_py

    scale_x = (screen_width - 1) / range_px if range_px > 0 else 0
    scale_y = (screen_height - 1) / range_py if range_py > 0 else 0
    
    # Use the smaller scale factor to ensure the entire cube fits on screen
    scale = min(scale_x, scale_y) if scale_x > 0 and scale_y > 0 else (scale_x or scale_y)

    projected_points_screen = []
    for px, py, z in projected_points_raw:
        # Scale and translate to screen coordinates
        sx = int((px - min_px) * scale)
        sy = int((py - min_py) * scale)

        projected_points_screen.append((sx, sy, z)) # Store z for depth sorting/drawing order if needed

        # Draw vertices with 'O'
        if 0 <= sx < screen_width and 0 <= sy < screen_height:
            frame_buffer[sy][sx] = 'O'

    # Draw edges with '.'
    for start_idx, end_idx in cube_edges:
        p1 = projected_points_screen[start_idx]
        p2 = projected_points_screen[end_idx]

        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx_step = 1 if x1 < x2 else -1
        sy_step = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if 0 <= x1 < screen_width and 0 <= y1 < screen_height:
                if frame_buffer[y1][x1] == ' ': # Only draw if not already a vertex
                    frame_buffer[y1][x1] = '.' # Changed edge character to '.'

            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx_step
            if e2 < dx:
                err += dx
                y1 += sy_step

    # Print frame buffer
    for row in frame_buffer:
        print("".join(row))

if __name__ == "__main__":
    main()
