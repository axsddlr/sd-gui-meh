# Simple GUI for MEH - Merging Execution Helper

This project is a graphical user interface (GUI) application that simplifies the process of merging multiple machine learning models. The application allows users to merge models with various merge modes and customizable weight configurations.

## Features

- Graphical interface for easy model selection and merging
- Support for merging up to 3 models
- Customizable weights for each model
- Selection of various merge modes
- Precision selection (fp16 and fp32)

## Dependencies

- Python 3.8 or later
- [sd_meh](https://github.com/s1dlx/meh) library
- [Tkinter](https://docs.python.org/3/library/tkinter.html) library

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/axsddlr/sd-gui-meh.git
   cd meh
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or ".venv\Scripts\activate" on Windows
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
    python app.py
   ```

## Usage

1. Select Model A and Model B using the "Select Model A" and "Select Model B" buttons. Optionally, you can select Model C as well.
2. Choose a merge mode from the dropdown menu.
3. Select the desired precision (fp16 or fp32) from the dropdown menu.
4. Input the weight alpha, weight beta, base alpha, and base beta values in their respective fields.
5. Click the "Merge Models" button to merge the models.
6. Save the merged model by choosing a filename and location in the save dialog that appears.

<mark>if you have experience with supermerger extension in automatic1111, the first leading number in weights alpha will be the base alpha integer.</mark>

## Contributing

Please feel free to open an issue or submit a pull request with any improvements or bug fixes. We appreciate your contributions!

## License

This project is licensed under the MIT License.
