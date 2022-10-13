from os import walk
import pygame


#Convert image file into the list
def import_folder(path):
    export_file = []

    for _,__,image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            export_file.append(image_surface)

    return export_file
