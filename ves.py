from PIL import Image, ImageDraw, ImageFilter

def hexColor(color):
    def hex2dec(hex_str):
        return int(hex_str, 16)
    r = hex2dec(color[1:3])
    g = hex2dec(color[3:5])
    b = hex2dec(color[5:7])
    return (r, g, b)

def platno(width, height, color):
    obr = Image.new('RGB', (width, height), color)
    return obr

def filled_circle(im, S, r, color):
    if r <= 0:
        return
    draw = ImageDraw.Draw(im)
    left_up = (S[0] - r, S[1] - r)
    right_down = (S[0] + r, S[1] + r)
    draw.ellipse([left_up, right_down], fill=color)

def filled_rectangle(im, x1, x2, y1, y2, color):
    for x in range(x1, x2):
        for y in range(y1, y2):
            im.putpixel((x, y), color)
    return im

def line1(im, A, B, color, thickness):
    draw = ImageDraw.Draw(im)
    draw.line([A, B], fill=color, width=thickness)

def simulate_protanopia(im):
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = im.getpixel((x, y))
            new_r = int(0.567 * r + 0.433 * g)
            new_g = int(0.558 * r + 0.442 * g)
            new_b = b
            im.putpixel((x, y), (new_r, new_g, new_b))
    return im

def greyscale(im):
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = im.getpixel((x, y))
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            im.putpixel((x, y), (gray, gray, gray))
    return im

def invert_colors(im):
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = im.getpixel((x, y))
            im.putpixel((x, y), (255 - r, 255 - g, 255 - b))
    return im

def blur_image(im):
    return im.filter(ImageFilter.GaussianBlur(radius=5))

def generate_image_from_ves_code(ves_code):
    obr = None

    for line in ves_code:
        line = line.strip()
        parts = line.split()

        if parts[0] == "VES":
            width = int(parts[2])
            height = int(parts[3])
            color = parts[4]
            rgb_color = hexColor(color)
            obr = platno(width, height, rgb_color)

        if parts[0] == "FILL_CIRCLEX":
            S = (int(parts[1]), int(parts[2]))
            r = int(parts[3])
            times = int(parts[4])
            color_keyword = parts[5]
            sunset_colors = ["#FFEB99", "#FFD170", "#FFB84D", "#FFAA3E", "#F99B72", "#F28A8B", "#E37F9E", "#D86F94", "#D15F8C", "#B9446E"]
            if color_keyword == "SUNSET":
                colors = sunset_colors
            for i in range(times):
                prvy_r = r - i * 15
                if prvy_r > 0:
                    color = colors[i]
                    rgb_color = hexColor(color)
                    filled_circle(obr, S, prvy_r, rgb_color)

        if parts[0] == "FILL_RECTANGLE":
            x1 = int(parts[1])
            x2 = int(parts[2])
            y1 = int(parts[3])
            y2 = int(parts[4])
            color = parts[5]
            rgb_color = hexColor(color)
            obr = filled_rectangle(obr, x1, x2, y1, y2, rgb_color)

        if parts[0] == "FILL_CIRCLE":
            S = (int(parts[1]), int(parts[2]))
            r = int(parts[3])
            color = parts[4]
            rgb_color = hexColor(color)
            filled_circle(obr, S, r, rgb_color)

        if parts[0] == "LINE":
            A = (int(parts[1]), int(parts[3]))
            B = (int(parts[2]), int(parts[4]))
            color = parts[6]
            rgb_color = hexColor(color)
            thickness = int(parts[5])
            line1(obr, A, B, rgb_color, thickness)

        if parts[0] == "CIRCLE":
            farba = hexColor(parts[5])
            S = [int(parts[1]), int(parts[2])]
            r = int(parts[3])
            thickness = int(parts[4])
            filled_circle(obr, S, r, farba)

        if parts[0] == "TRIANGLE":
            color = parts[8]
            rgb_color = hexColor(color)
            thickness = parts[7]
            pass

        if parts[0] == "GREYSCALE":
            obr = greyscale(obr)

        if parts[0] == "COLORBLIND":
            obr = simulate_protanopia(obr)

        if parts[0] == "INVERTED":
            obr = invert_colors(obr)

        if parts[0] == "BLUR":
            obr = blur_image(obr)

    return obr

def process_ves_file(file_name):
    with open(file_name, 'r') as f:
        ves_code = f.readlines()
    return ves_code
