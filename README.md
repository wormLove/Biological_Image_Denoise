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

## ⚙️ Configuration
This pipeline is configurable via a `config.cfg` file, allowing you to fine-tune denoising parameters, morphological operations, and circularity filtering.

### **🔹 Basic Settings**
```ini
[basic_setting]
FilePath = /path/to/your/file.tif  # Path to input TIFF image
channel_name_list = BGR            # Input channel order
OutDir = /path/to/output/folder    # Output directory
```

### **🔹 Denoising Settings**
```ini
[denoise_setting]
extrema_filter = True                # Enable extrema filter
adaptive_threshold_filter = True     # Enable adaptive threshold filter
morphology_operations = True         # Enable morphological operations
circularity_filter = True            # Enable circularity filter
channel_plan = [1, 2]                # Channels to process (indexing starts from 0)
gen_overlap = True                   # Generate overlap analysis
```

### **🔹 Extrema Filter**
Removes extreme pixel values based on predefined thresholds.
```ini
[extrema_filter]
max_thre = 10000        # Remove pixels with values greater than this threshold
base_value = median     # Baseline value ('mean' | 'median' | '0')
std_multi = 1           # Pixels below (base_value + std_multi * STD) are removed
```

### **🔹 Adaptive Threshold Filter**
Removes pixels based on local mean intensity.
```ini
[adaptive_threshold_filter]
filter_size = 50      # Sliding window size for local mean calculation
mean_multi = 5        # Remove values below mean_multi * local_mean
```

### **🔹 Morphological Operations**
Used for refining segmentation results.
```ini
[morphology_operations]
kernal_rank = 2       # Kernel rank determines the structuring element size
connectivity = 2      # Defines neighborhood connectivity (e.g., 4-connectivity, 8-connectivity)
opening_operation = True   # Apply morphological opening
closing_operation = True   # Apply morphological closing
```

### **🔹 Circularity Filter**
Filters out non-circular signals and small signals.
```ini
[circularity_filter]
circularity_thre = 0.75  # Remove objects with circularity below this threshold
area_thre = 10           # Remove objects smaller than this area (in pixels)
```

---

## 📊 Example Output























