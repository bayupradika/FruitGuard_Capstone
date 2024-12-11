# ml-FruitGuard-Classification

![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
[![Google Colab](https://img.shields.io/badge/open_in_colab-blue?style=for-the-badge&logo=googlecolab&color=blue&labelColor=525252)](https://colab.research.google.com/github/MamMates/ml-food-classification/blob/main/MamMates_Food_Classification.ipynb)
![LICENSE](https://img.shields.io/github/license/MamMates/ml-food-classification?style=for-the-badge)

FruitGuard Classification using Convolutional Neural Network (CNN).

## FruitGuard Classification

- **Notebook:** [FruitGuard Classification](https://colab.research.google.com/drive/1eWbNPGPvpQmxhaxegwuJDD2fQsf2C3ka?usp=sharing)
- **Dataset:** [FruitGuard Dataset](https://drive.google.com/file/d/16YAwpBp0thfyoHIQLi_s6dOTVSCJpGwf/view?usp=sharing)

## Features 💡

Using Mammates fruits Classification, you can categorize fruits images into 2 classes.

| Class | Label        |
| ----- | ------------ |
| 0     | Fresh_Fruits  |
| 1     | Rotten_Fruits |

## Prerequisites 📋

- [TensorFlow](https://www.tensorflow.org/) 2.17.1 or higher


## Development 💻

If you want to develop this model, you can follow the steps below:

- Clone this repository:

```bash
git clone https://github.com/MamMates/ml-food-classification.git
```

- Update the model by changing the saved model in the [model](model/) folder.

- Build the Docker image:

```bash
docker build -t mammates-food-classification .
```

- Run the image:

```bash
docker run -p 8501:8501 --name ml-clf mammates-food-classification
```

- You can check that the model is already running by opening browser and go to http://localhost:8501/v1/models/food_clf

- To do prediction, you can use the following command:

```bash
curl -d @example.json -X POST http://localhost:8501/v1/models/food_clf:predict
```

- To stop the container:

```bash
docker stop ml-clf
```

> [!NOTE]  
> If you want to learn more about TensorFlow Serving, you can read the REST API documentation [here](https://www.tensorflow.org/tfx/serving/api_rest).

## Acknowledgements 🙏

Our sincere gratitude goes to the creators and maintainers of these datasets. Their generosity in sharing these resources has been instrumental in driving the progress and success of this project.

- [Deteksi Makanan Daerah Dataset](https://universe.roboflow.com/fusion-qvvyj)
- [Indonesian Food Dataset](https://universe.roboflow.com/bangkit)
- [Food 101 Dataset](https://www.kaggle.com/datasets/dansbecker/food-101)
- [Food-5K Dataset](https://www.epfl.ch/labs/mmspg/downloads/food-image-datasets/)
- [Food-11 Dataset](https://www.kaggle.com/datasets/trolukovich/food11-image-dataset)

## License 📝

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
