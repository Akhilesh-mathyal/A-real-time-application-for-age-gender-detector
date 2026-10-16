# Dataset and model documentation

## Inference assets

This application downloads six public inference artifacts through `scripts/download_models.py`:

| Artifact | Purpose | Source |
| --- | --- | --- |
| OpenCV TensorFlow face detector | Face localization | OpenCV DNN public model files |
| Levi & Hassner age Caffe model | Eight apparent-age ranges | [LearnOpenCV AgeGender repository](https://github.com/spmallick/learnopencv/tree/master/AgeGender) |
| Levi & Hassner gender Caffe model | Binary gender-presentation classifier | [LearnOpenCV AgeGender repository](https://github.com/spmallick/learnopencv/tree/master/AgeGender) |

The model files are not versioned in Git because they are large binary artifacts. The download script is reproducible and records exact filenames.

## Google Drive submission folder

Create a Drive folder named `gender-age-detector-datasets`, upload only datasets/materials you have rights to distribute, and replace the placeholder in the README/submission form with its share URL. If you use no local training dataset, state that clearly: this project performs inference using public pretrained models and does not train on user-provided images.

Never upload webcam captures or personally identifying images without informed consent.
