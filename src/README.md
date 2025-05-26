# Automated Lie Detection

This project provides an interface for assessing the credibility of autobiographical statements using a pretrained DistilBERT model.

## Technical Overview

The application is built using Streamlit, allowing users to submit statements of any length and receive real-time feedback. A pretrained DistilBERT model powers the predictions, determining whether a statement is likely true or false, along with how confident the model is in its prediction.

## Intended Use

The model is specifically trained on autobiographical statements. As such, this tool is designed to evaluate the credibility of personal narratives, such as stories shared in casual conversations. The tool can also be used for:

1. Automated interview analysis 
2. Security screening
3. Academic statement analysis 

## Installation

You can install the package via pip (from the project root):

```bash
pip3 install -e src
# or
pip install -e src
```

You can also install the package directly from GitHub:

```bash
pip3 install git+https://github.com/Programming-The-Next-Step-2025/automated-lie-detection.git@week-4#egg=automated_lie_detection_package

# or 

pip install git+https://github.com/Programming-The-Next-Step-2025/automated-lie-detection.git@week-4#egg=automated_lie_detection_package
```

**Note:**
Depending on your environment, you may need to use pip instead of pip3, and python instead of python3.

## Model Folder Setup

Before making any predictions, you need to download a pretrained model into a local models/ directory.

Run the following Python code:

```python
from automated_lie_detection_package import download_model_folder_from_gdrive

download_model_folder_from_gdrive()
```

The folder structure should look like:

your_project/
├── models/
│   └── [model files go here]
├── src/
│   └── automated_lie_detection_package/
│       └── ...
├── run.sh
└── ...

The default option downloads a DistilBert that has been pretrained to classify autobiographical lies and truths from: 

"https://drive.google.com/drive/folders/1BByWnxuJ8gXWDPEWjPjAnU4iVaeQp1dZ?usp=sharing"

However, you can also download another model as long as: 

1. The download includes all necessary files (e.g., config.json, pytorch_model.bin, tokenizer.json, vocab.txt, etc.)

2. The model is a sequence classification model (such as DistilBERT, BERT, RoBERTa, etc.)

## Usage

### Run modelprediction
Run the following code in Python to get get a model prediction:

```python
from automated_lie_detection_package import modelprediction

modelprediction("I swear I am innocent")
```

**Example output:**

"The statement was classified as deceptive with 87.5% confidence."

### Run the Streamlit Application

If you have the run.sh script, run the app with:

```bash
./run.sh
```

If your file structure does not include the run.sh file, run the following in your terminal:

```bash
python3 -m streamlit run src/automated_lie_detection_package/app.py --server.port=8501

# or 

python -m streamlit run src/automated_lie_detection_package/app.py --server.port=8501
```

#### Creating `run.sh` yourself 

If you want to create the `run.sh` script for convenience, create a new file named run.sh in your project root with the following content:

```bash
#!/bin/bash
python3 -m streamlit run src/automated_lie_detection_package/app.py --server.port=8501

or 

python -m streamlit run src/automated_lie_detection_package/app.py --server.port=8501
```

Then make it executable in your terminal: 

```bash
chmod +x run.sh
```

### Clear Models Folder  

If you want to remove all files and subdirectories from the models folder (for example, before downloading a new model):

```python
from automated_lie_detection_package import clear_models_folder 

clear_model_folder()
```

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Contact

Maintained by [Lucca Pfruender](mailto:luccip.upn@googlemail.com).

## FAQ

**Q:** I get a "models folder not found" error.  
**A:** Make sure you have created the `models/` folder and downloaded the model files as described above.

**Q:** Can I use a different model?  
**A:** Yes, as long as it is a Hugging Face sequence classification model and all required files are present.
