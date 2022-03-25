import PIL

from controllers import photo_controller

# To run, open cmd in folder and type:
    # All tests:        pytest -v --durations=0
    # Specif file:      pytest test_photo_controller.py -v --durations=0
    # Specific test:    pytest -v --durations=0 -k "method name"
    # Ref: https://docs.pytest.org/en/latest/usage.html

c = photo_controller.PhotoController()

# Person methods:
def test_10_encode():
    pass

def test_20_decode():
    pass

def test_30_get_image():

    received_data = c.get_image('Alexandre16.jpg')

    assert type(received_data) == PIL.JpegImagePlugin.JpegImageFile

def test_31_get_image_not_found():

    received_data_1, received_data_2 = c.get_image('Alexandre16')

    if 'Photo not found:' in received_data_2:
        received_data_3 = True

    received_data = (received_data_1, received_data_3)

    expected_data = (None, True)
    
    assert received_data == expected_data

def test_32_get_image_error():
    received_data_1, received_data_2 = c.get_image()
    received_data = (received_data_1, received_data_2)

    expected_data = (False, "Error in method PhotoController.get_image. Error message: join() argument must be str, bytes, or os.PathLike object, not 'NoneType'")
    
    assert received_data == expected_data

def test_40_save_image():

    name_1 = 'Alexandre16.jpg'
    name_2 = 'Alexandre16_2.jpg'

    # Getting 1st image.
    image_1 = c.get_image(name_1)
    received_data_1 = type(image_1)

    # Saving as 2nd image.
    received_data_2 = c.save_image(image_1, name_2)

    # Openingn 2nd image.
    image_2 = c.get_image(name_2)
    received_data_3 = type(image_2)

    received_data = (received_data_1, received_data_2, received_data_3)
    expected_data = (PIL.JpegImagePlugin.JpegImageFile, True, PIL.JpegImagePlugin.JpegImageFile)
    
    assert received_data == expected_data

def test_50_delete_image():
    name_1 = 'Alexandre16.jpg'
    name_2 = 'Alexandre16_2.jpg'

    # Getting 1st image.
    image_1 = c.get_image(name_1)
    received_data_1 = type(image_1)

    # Saving as 2nd image.
    received_data_2 = c.save_image(image_1, name_2)

    # Opening 2nd image.
    image_2 = c.get_image(name_2)
    received_data_3 = type(image_2)
    image_2.close()

    # Deleting 2nd image:
    received_data_4 = c.delete_image(name_2)

    # Trying to Open 2nd image.
    received_data_5, received_data_6 = c.get_image(name_2)

    if 'Photo not found:' in received_data_6:
        received_data_6 = True

    received_data = (
        received_data_1,
        received_data_2,
        received_data_3,
        received_data_4,
        received_data_5,
        received_data_6,
        )

    expected_data = (
        PIL.JpegImagePlugin.JpegImageFile,
        True,
        PIL.JpegImagePlugin.JpegImageFile,
        True,
        None,
        True,
        )
    
    assert received_data == expected_data

def test_61_get_path_test():
    c.test = True
    received_data = c.get_path()
    c.test = False
    expected_data = 'C:\Repos\GlobalAccess_Python\ControleAcesso_Python_Solution\Middleware\static'
    assert received_data == expected_data

def test_62_get_path_windows():
    received_data = c.get_path()
    expected_data = 'C:\\Photos'
    assert received_data == expected_data
