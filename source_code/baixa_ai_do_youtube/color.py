def get_color_hex(color_name: str) -> str:
    """
    Obtém o hexadecimal de uma cor
    """
    colors = {
        "black": "#000000",
        "white": "#FFFFFF",
        "red": "#FF0000",
        "green": "#00FF00",
        "blue": "#0000FF",
        "yellow": "#FFFF00",
        "cyan": "#00FFFF",
        "magenta": "#FF00FF",
        "gray": "#808080",
        "dark_gray": "#A9A9A9",
        "light_gray": "#D3D3D3",
        "dark_red": "#8B0000",
        "dark_green": "#006400",
        "dark_blue": "#00008B",
        "dark_yellow": "#BDB76B",
        "dark_cyan": "#008B8B",
        "dark_magenta": "#8B008B",
        "light_red": "#FFA07A",
        "light_green": "#90EE90",
        "light_blue": "#ADD8E6",
        "light_yellow": "#FFFFE0",
        "light_cyan": "#E0FFFF",
        "light_magenta": "#FFB6C1",        
    }
    if not color_name in colors.keys():
        return colors["light_gray"]
    return colors[color_name]

