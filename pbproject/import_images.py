# import os
# from django.core.files import File
# # Import your model where you want to store the images
# from yourapp.models import YourModel


# def import_images():
#     # Specify the directory where your images are located
#     image_dir = '/path/to/your/images'

#     # Iterate through the files in the directory
#     for filename in os.listdir(image_dir):
#         # Construct the full path to the image file
#         filepath = os.path.join(image_dir, filename)

#         # Open the image file
#         with open(filepath, 'rb') as f:
#             # Create a new instance of your model
#             instance = YourModel()

#             # Set any additional attributes of the model instance
#             instance.attribute1 = value1
#             instance.attribute2 = value2
#             # Set the image field using Django's File object
#             instance.image_field.save(filename, File(f), save=False)

#             # Save the instance to the database
#             instance.save()


# if __name__ == '__main__':
#     import_images()

# In this script:

# Replace 'yourapp.models' with the appropriate import path to your Django model where you want to store the images.
# Replace 'YourModel' with the name of your Django model.
# Replace 'image_field' with the name of the image field in your model.
# Replace attribute1, attribute2, etc., with any additional attributes of your model that you want to set.
# Modify the image_dir variable to point to the directory where your images are located.
# Ensure that the images in the directory correspond to the model instances you're creating.
# You can then run this script from the command line using python import_images.py to import the images into your Django project.

# Make sure to test the script thoroughly before running it in a production environment, and always make backups of your data before performing bulk imports.
