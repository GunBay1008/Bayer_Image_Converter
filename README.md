# Bayer_Image_Converter
a tool specified for converting bayer images on BigX4 machine to original images

pending bug: error page when user converts without selecting any files.

# Setting up the Project

To get started with the project, follow these steps:

## Steo 1: Clone this Repo
```
git clone
```

## Step 2: Set Up a Virtual Environment

It's recommended to work within a virtual environment to manage dependencies and isolate your project's environment. We'll use Conda for this purpose. If you don't have Conda installed, you can download and install it from the [official website](https://docs.conda.io/en/latest/miniconda.html).

```bash
conda create --name myenv
conda activate myenv
```
replace myenv with desired environment name

## Step 3: Install Dependencies
make sure you are in the project directory
```
pip install -r requirements.txt
```

## Step 4: Run the program
```
python main.py
```
