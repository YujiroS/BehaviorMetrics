"""
    Robot: F1
    Framework: keras
    Number of networks: 1
    Network type: Classification
    Predicionts:
        angular speed(w)

    This brain uses a classification network based on Keras framework to predict the angular velocity
    of the F1 car. For that task it uses a classification convolutional neural networks for w (with 7 classes) leaving
    the linear speed (v) constant
"""
from behaviorlib.keraslib.keras_predict import KerasPredictor


class Brain:

    def __init__(self, sensors, actuators, handler=None):
        self.motors = actuators.get_motor('motors_0')
        self.camera = sensors.get_camera('camera_0')
        self.handler = handler
        self.cont = 0
        self.net_w = KerasPredictor('path_to_w')
        self.k_v = 5

    def update_frame(self, frame_id, data):
        self.handler.update_frame(frame_id, data)

    def calculate_w(self, predicted_class):
        """
        Method that calculates the linear speed of the robot (v) based on the predicted class

        The class-speed label conversion for v is as follows:
            class 0 = radically left
            class 1 = moderate left
            class 2 = slightly left
            class 3 = slight
            class 4 = slightly right
            class 5 = moderate right
            class 6 = radically right
        """
        if predicted_class == 0:
            self.motors.sendW(1.7)
        elif predicted_class == 1:
            self.motors.sendW(0.75)
        elif predicted_class == 2:
            self.motors.sendW(0.25)
        elif predicted_class == 3:
            self.motors.sendW(0)
        elif predicted_class == 4:
            self.motors.sendW(-0.25)
        elif predicted_class == 5:
            self.motors.sendW(-0.75)
        elif predicted_class == 6:
            self.motors.sendW(-1.7)

    def execute(self):

        if self.cont > 0:
            print("Runing...")
            self.cont += 1

        image = self.camera.getImage().data
        prediction_w = self.net_w.predict(image)

        if prediction_w != '' and prediction_w != '':
            self.calculate_w(prediction_w)
            self.motors.sendV(self.k_v)

        self.update_frame('frame_0', image)