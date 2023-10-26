# EyeDetector

![EyeDetector](https://github.com/benjiiross/EyeDetector/blob/main/public/background.jpg?raw=true)

_A Machine Learning project_

This project was made by [Julie Chen](https://github.com/juliele1), [Arthur Gagniare](https://github.com/AGagniare) and [Benjamin Rossignol](https://github.com/benjiiross). Its aim is to detect if an image contains eyes cancer or not.

The website is currently hosted on [Github Pages](https://benjiiross.github.io/EyeDetector/).

## Getting Started

You can download the project and run it locally using the following commands:

```bash
git clone https://github.com/benjiiross/EyeDetector.git
cd EyeDetector
conda create -y -n eyedetector
conda activate eyedetector
conda install -y python=3.8
python -m pip install -r requirements.txt
```

## Machine Learning

To run this project, you will need first to create a new project on [Azure Custom Vision](https://customvision.ai/).

Then, you will need to create a .env file at the root of the project with the following variables:

```
VISION_TRAINING_KEY
VISION_TRAINING_ENDPOINT
VISION_PREDICTION_KEY
VISION_PREDICTION_RESOURCE_ID
VISION_PROJECT_ID
VITE_PREDICTION_ENDPOINT
```

You will also need to copy the training photos in the root of the project in a folder named `images` (private data, not included in the repository)

Then, you can run the following command to interract with the project:

```bash
# to add the tags to azure
python python_scripts/create_tags.py

# to publish the images to azure
python python_scripts/publish_images.py
```

## Website

To run the website locally, you can run the following commands in the root of the project. Make sure you have installed NodeJS and NPM.

```bash
npm install
npm run dev
```
