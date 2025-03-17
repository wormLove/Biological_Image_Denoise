# 📊 Biological_Image_Denoise 🚀
> **A pipeline for tif image denoising and statistical analysis**

[![GitHub stars](https://img.shields.io/github/stars/wormLove/Biological_Image_Denoise.svg)](https://github.com/wormLove/Biological_Image_Denoise)
[![GitHub issues](https://img.shields.io/github/issues/wormLove/Biological_Image_Denoise.svg)](https://github.com/wormLove/Biological_Image_Denoise/issues)
[![License](https://img.shields.io/github/license/wormLove/Biological_Image_Denoise.svg)](LICENSE)

## 📖 Introduction
This pipeline is designed for denoising biological images that contain R, G, and B channels.
It includes multiple filtering methods and supports batch processing.

🚀 Designed for researchers working on **biomedical imaging, neuroscience.**

---

## 🔧 Installation
### **1️⃣ Clone this repository**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### **2️⃣ Create a virtual environment**
```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### **3️⃣ Install dependencies**
```bash
# Upgrade pip to the latest version
pip install --upgrade pip

# Install all required packages from requirements.txt
pip install -r requirements.txt
```

---

## 🚀 Usage
### **1️⃣ Run Denoising and Analysis
```bash
python main.py --FilePath /path/to/image.tif --Action ds --Config config.cfg --OutputDir /path/to/output
```

### **📌 --Action 参数：
- **s** → Only perform statistical analysis
- **d** → Only perform image denoising
- **"ds" or "sd"** → Perform both analysis and denoising

### **2️⃣ Batch Processing
```bash
python batch_run.py --InputDir /path/to/folder --Action d --OutputDir /path/to/output
```

---

## 🛠 Configuration
All parameters are stored in config.cfg, allowing you to fine-tune:

- **Denoising filters** (e.g., extrema filter, adaptive threshold)
- **Morphological operations**
- **Circularity filtering**
- **Channel mappings**
- **Batch processing options**

---

## 📊 Example Output























