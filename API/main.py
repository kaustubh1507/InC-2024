import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import tensorflow as tf
from flask_cors import CORS
import matplotlib.pyplot as plt
import matplotlib.image as img




app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": [
    "http://localhost",
    "http://localhost:3000",
]}})

def predictm(model, img, class_names):
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class, confidence




@app.route('/predict', methods=['POST'])
def predict():

    if 'image' not in request.files:
        print("abcd")
        return "No image file found"

    image_file= request.files['image']
    keywords = request.form['keywords']


    image = Image.open(image_file)
    # image_array = np.array(image.resize((256, 256))) / 255.0
    # image_batch = np.expand_dims(image_array, axis=0)

    if keywords == "1":
        potato_m = tf.keras.models.load_model("../Models/potato_f")
        # potato_names = ['Early Blight', 'Late Blight', 'Healthy']
        class_names = ['Potato Early Blight', 'Potato Late Blight', 'Potato Healthy']

        # print(image_batch.size)
        # prediction = potato_m.predict(image_batch)
        # print(prediction)
        # predicted_class = potato_names[np.argmax(prediction[0])]
        # print("1")
        # print(predicted_class)

        predicted_class, confidence = predictm(potato_m, image, class_names= class_names)
        print(predicted_class, confidence)
        # plt.figure(figsize=(10, 10))
        # for image in image_batch:
        #     plt.imshow(image)
        #     #plt.title(class_names[label_batch[i]])
        #     plt.axis("off")
        #     plt.show()

        print(predicted_class, " ", confidence)
        return jsonify({

            'class': predicted_class,
            'confidence': confidence
        })

    elif keywords == "2":
        bell_pepper_m = tf.keras.models.load_model("../Models/bell_pepper")
        class_names = ['Bacterial Spot', 'Healthy']

        # prediction = bell_pepper_m.predict(image_batch)
        # print(prediction)
        # predicted_class = bell_pepper_names[np.argmax(prediction[0])]
        # print("2")
        # print(predicted_class)

        # plt.figure(figsize=(10, 10))
        #
        # plt.imshow(image)
        # plt.axis("off")
        # plt.show()  # PRINTING RANDOMLY SELECTED IMAGES FROM 1ST BATCH OF THE DATA SET
        predicted_class, confidence = predictm(bell_pepper_m, image, class_names=class_names)
        print(predicted_class, confidence)
        print(predicted_class, " ", confidence)
        answer = {
            'class': predicted_class,
            'confidence': confidence
        }
        return jsonify(answer)

    elif keywords == "3":
        tomato_m = tf.keras.models.load_model("../Models/tomato2")
        class_names = ['Early Blight', 'Late Blight', 'Healthy']

        # prediction = tomato_m.predict(image_batch)
        # print(prediction)
        # predicted_class = tomato_names[np.argmax(prediction[0])]
        # print("3")
        # print(predicted_class)



        # plt.figure(figsize=(10, 10))
        # plt.imshow(image)
        # plt.axis("off")
        # plt.show()  # PRINTING RANDOMLY SELECTED IMAGES FROM 1ST BATCH OF THE DATA SET
        predicted_class, confidence = predictm(tomato_m, image, class_names=class_names)
        print(predicted_class, confidence)

        print(predicted_class, " ", confidence)
        # formdata = {}
        # formdata['class']= selectedFile
        # formdata.append("keywords", selectedOption);
        return jsonify({
            'class': predicted_class,
            'confidence': confidence
        })

    else:
        return "Select Plant!"

    # confidence = float(np.max(prediction[0]))



if __name__ == '__main__':
    app.run(debug=True)
