import unittest
import base64
import json
import cv2
from unittest.mock import patch

# Assuming your code is saved in a file named `card_detection.py`
from server.service.vision import from_b64, to_b64, detect

class TestCardDetection(unittest.TestCase):

    def setUp(self):
        # This method will be executed before each test
        self.img_b64 = self.encode_image_to_base64("test_image.jpg")
        self.sample_image = cv2.imread("test_image.jpg")  # Load a sample image for testing
        self.mock_card_model = patch('card_detection.YOLO').start()  # Mock YOLO model
        self.mock_card_model.names = {0: "card1", 1: "card2"}  # Mock card names

    def tearDown(self):
        # This method will be executed after each test
        patch.stopall()

    def encode_image_to_base64(self, image_path):
        """
        Helper function to encode an image file to base64.
        """
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    def test_from_b64(self):
        """Test the from_b64 function"""
        img = from_b64(f"data:image/jpg;base64,{self.img_b64}")
        self.assertIsInstance(img, np.ndarray)  # Check if the result is an OpenCV image (numpy array)
        self.assertEqual(img.shape[2], 3)  # Ensure it's a color image (3 channels)

    def test_to_b64(self):
        """Test the to_b64 function"""
        b64_img = to_b64(self.sample_image)
        self.assertTrue(b64_img.startswith('data:image/jpg;base64,'))  # Check if the result starts with correct prefix
        self.assertTrue(len(b64_img.split(',')[1]) > 0)  # Check if the base64 string is non-empty

    @patch('card_detection.YOLO.track')  # Mocking the track method of the YOLO model
    def test_detect(self, mock_track):
        """Test the detect function"""
        # Setup a mock response for the detection
        mock_track.return_value = [
            # Simulating the result from a YOLO model with detection boxes
            type('Result', (), {
                'boxes': [type('Box', (), {
                    'id': 1,
                    'xyxy': [[50, 50, 150, 150]],
                    'cls': 0,
                    'conf': 0.8
                })]
            })
        ]

        # Simulate a base64 image passed to detect()
        response = detect(f"data:image/jpg;base64,{self.img_b64}")

        # Assert the returned JSON format is as expected
        cards = json.loads(response)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][4], 'card1')  # The detected card class
        self.assertEqual(cards[0][5], 0.8)  # The confidence score

    def test_invalid_image(self):
        """Test the detect function with invalid image input"""
        response = detect("data:image/jpg;base64,invalid_data")
        self.assertEqual(response, '[]')  # If no valid detection occurs, an empty list is returned

if __name__ == '__main__':
    unittest.main()
