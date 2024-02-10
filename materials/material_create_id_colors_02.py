import bpy
import colorsys

def generate_colors(num_colors):
    colors = []
    # shift HSL value
    step = 360.0 / num_colors

    for i in range(num_colors):
        hue = i * step
        rgb = colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
        colors.append(rgb)

    return colors


if __name__ == "__main__":
    num_colors = 12  # Change this to the desired number of colors
    color_list = generate_colors(num_colors)
    print("Generated colors:")
    for i, color in enumerate(color_list):
        material = bpy.data.materials.new(name=f"ID_{i+1}")
        material.diffuse_color = (color[0], color[1], color[2],1.0)
        print(f"Color {i+1}: RGB({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})")
