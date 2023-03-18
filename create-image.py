#

from PIL import Image
from time import time

def open_conscript_images_and_get_merged_image(romanized_parts, other_arg_list=[100000, "LTR"]):# TODO: implement writing_dir
    # https://www.tutorialspoint.com/python_pillow/Python_pillow_merging_images.htm
    #Read the two images
    imageList = []
    for i in range(0, len(romanized_parts)):
        imageList.append(Image.open(f'{imagePath}/{romanized_parts[i]}.png'))

    calculate_and_create_final_image(imageList, other_arg_list[0], other_arg_list[1])
#********************************** end **********************************#

def calculate_and_create_final_image(images, max_pixels_in_writing_dir=100000, writing_dir="LTR"):
    full_image_size = [0 ,images[0].size[1]] #TODO: use the biggest image height for initialization instead of the first one, if ever required by a conscript being added
    current_writing_dir_pixels = 0
    i = 0
    auto_created_linebreak_positsions = []

    for image in images:

        if current_writing_dir_pixels >= max_pixels_in_writing_dir:# TODO: if an image has a larger Y than the current line's Y space, just add that extra space [remove both copys of comment]
            full_image_size[1] += image.size[1]
            current_writing_dir_pixels = 0

            auto_created_linebreak_positsions.append(i)
    
        current_writing_dir_pixels += image.size[0]
        print(max_pixels_in_writing_dir)

        i+=1
    if auto_created_linebreak_positsions == []: # if there weren't any linebreaks, make the image as big as how many pixels were used
        full_image_size[0] = current_writing_dir_pixels
    else: # else, if there were linebreaks, then use the max image width for the width
        full_image_size[0] = max_pixels_in_writing_dir

    #print(f"full image size calculated to: {full_image_size[0]}x by {full_image_size[1]}y")

# ********************************** create image **********************************
# I know this isn't the best, most DRY code, but I can't put this code into the above loop because it finds the total image size
# of the combined image and this loop concats the smaller images into the large image
    new_image = Image.new('RGB',(full_image_size[0], full_image_size[1]), (250,250,250))
    current_y = 0
    current_linebreak = 0
    current_x_multiplier = 0

    for i in range(0, len(images)):
        if len(auto_created_linebreak_positsions) != current_linebreak and i == auto_created_linebreak_positsions[current_linebreak]:# TODO: if an image has a larger Y than the current line's Y space, just add that extra space [remove both copys of comment]
            current_y += images[i].size[1]# TODO: make this a function that both loops use
            current_linebreak += 1
            current_x_multiplier = 0

        new_image.paste(images[i],(images[i].size[0]*current_x_multiplier, current_y))
        current_x_multiplier += 1
    
    new_image.save(f"{imagePath}/../merged_image_{time()}.png","PNG")
#********************************** end **********************************#

def split_romanization(text, conscript):
    split_romanization_list = []
    romanization_token = ""
    letter_num = 0
    not_done = True

    match conscript:
        case "`hu`iewata-v1":
            while not_done:
                # **start main part of code**
                if text[letter_num] == "`": # if there is a dipthong next
                    romanization_token = (text[letter_num+1] + text[letter_num+2])
                    letter_num += 2

                elif text[letter_num] == "\\":
                    romanization_token = "unquote"
                elif text[letter_num] == "/":
                    romanization_token = "quote"
                else:
                    romanization_token = text[letter_num]
                
                split_romanization_list.append(romanization_token)
                letter_num += 1
                if letter_num >= len(text):
                    not_done = False # end the loop
        case _:
            raise ValueError(f"the script \"{conscript}\" is not supported.")

    return split_romanization_list
#********************************** end **********************************#

if __name__ == "__main__":
    imagePath = ("`hu`iewata")+"-images" # TODO: look at using a function for the folder name after I've made more than 1 con script
    romanized = input(r"romanized text (note: spaces are replaced with underscores): ").replace(" ", "_")
    print(romanized)
    split_romanized = split_romanization(romanized, input("what conscript? (supported scripts: `hu`iewata-v1):"))
    pixelsPerLineBreak = int(input("how many pixels per line break? (keep in mind how large the images for each character are) "))
    #TextDir_and_settings = input("what text direction/settings do you want to use? (not supported yet, ignore this)")
    print(split_romanized)
    open_conscript_images_and_get_merged_image(split_romanized, [pixelsPerLineBreak, """TextDir_and_settings"""])
    input("press enter to exit")
#********************************** end **********************************#