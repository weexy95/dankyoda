# Feel free to add more colors
red = 0xFF0000
l_red = 0xEC5858
orange = 0xFF4500
yellow = 0xFFFF00
l_yellow = 0xF2CB7D

green = 0x00FF00
l_green = 0x55AA5B
blue = 0x0000FF
l_blue = 0x60C1E8
cyan = 0x00FFFF

t_red = '\33[91m'
t_yellow = '\33[93m'
t_green = '\33[92m'
t_blue = '\33[96m'
t_white = '\33[0m'

colors = [
    0xFF0000,
    0xEC5858,
    0x00FF00,
    0x55AA5B,
    0xFFFF00,
    0xF2CB7D,
    0x0000FF,
    0x60C1E8,
    0x00FFFF,
    0xFF4500
]

colors_but_dict = {
    'red': 0xFF0000,
    'l_red': 0xEC5858,
    'green': 0x00FF00,
    'l_green': 0x55AA5B,
    'yellow ': 0xFFFF00,
    'l_yellow': 0xF2CB7D,
    'blue': 0x0000FF,
    'l_blue': 0x60C1E8,
    'cyan': 0x00FFFF,
    'orange': 0xFF4500
}

def get_color(color: str):
    try:
        return colors_but_dict[color]
    except KeyError:
        return colors_but_dict['l_yellow']

def colored(r, g, b, text):
    """
    Function to print colored text in terminal
    """
    print(f"\33[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m")