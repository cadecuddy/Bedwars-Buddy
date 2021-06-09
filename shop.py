from PIL import Image
import os

# Quickly made this to resize all icons I found to a common size, not used in actual bot
def rescale():
    files = os.listdir("./resources/")

    for file in files:
        if file.endswith('.png'):
            im = Image.open(f"./resources/{file}")
            width, height = im.size
            im1 = im.resize((30,30))
            im1.save(os.path.join("./resources/rescaled/", file))
        else:
            continue

# Creates and saves the user's custom Bedwars shop layout
def createShopImage(shop_data):
    position = [47,100]
    count = 1
    items = shop_data.split(',')
    shop_background = Image.open('shop_template.png')
    
    for item in items:
        if item == "null":
            count += 1
            position[0] += 36
            continue

        if ((count - 1) % 7 == 0) and count != 1:
            position[0] = 47
            position[1] += 35

        # All need common color depth value to avoid transparency error
        test = Image.open(f'resources/{item}.png').convert("RGBA")
        shop_background.paste(test,(position[0],position[1]),test)
        count += 1
        position[0] += 36
    shop_background.save('shop.png')
