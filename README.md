<div align="center">

<img src="assets/logo.png" alt="FileFlow logo" width="96" />

# FileFlow

**Turn a cluttered folder into descriptive filenames and useful categories.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)

[Quick start](#quick-start) · [Preview](#preview) · [How it works](#how-it-works)

</div>

---

FileFlow is a local Streamlit app that uses Google Gemini to suggest filenames from file content and category folders from existing filenames. It renames and moves files on the computer running the app.

<a id="how-it-works"></a>

## ✨ How it works

| Action | What Gemini receives | What changes locally |
|---|---|---|
| Smart Rename | The file uploaded through Gemini's Files API | A sanitized descriptive name, preserving the extension; numeric suffixes avoid existing names |
| Smart Organize | The filename | The file moves into a sanitized category folder |

The app processes visible files directly inside the selected folder; it does not recursively traverse subfolders. There is no preview/approval queue or undo history, so start with a copy of a small test folder.

<a id="quick-start"></a>

## 🚀 Quick start

Requirements: Python, the packages in [requirements.txt](requirements.txt), a Gemini API key, and a text model available to that key. No Python minimum is pinned in this repository.

```bash
git clone https://github.com/Vignesh-S-GitHub/FileFlow-Intelligent-Organizer.git
cd FileFlow-Intelligent-Organizer
python -m venv .venv
# macOS / Linux; Windows: .venv\Scripts\activate
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local address Streamlit prints, usually **http://localhost:8501**.

1. Enter your API key and available model ID in **Configuration**.
2. Enter the absolute path to your test folder.
3. Choose **Smart Rename** or **Smart Organize**, then start processing.
4. Review the per-file results and the resulting folder contents.

Get a key through [Google AI Studio](https://aistudio.google.com/). Model availability, accepted file formats, limits, and charges depend on your provider account; the interface's example ID is editable.

<a id="preview"></a>

## 🖼️ Preview

<p align="center">
  <img src="assets/Demo-1_Screenshot.png" alt="FileFlow configuration and rename workflow" width="46%" />
  <img src="assets/Demo-2_Screenshot.png" alt="FileFlow organization workflow" width="46%" />
</p>

## 🔐 Files and provider access

Renaming sends file content to Gemini; organizing sends filenames. The code attempts to delete the uploaded provider file after a successful rename-generation call, but cleanup is not guaranteed if that call fails. The API key is entered in a password field and configured in the running process. Use files appropriate for that provider and retain your own backup.

## 🛠️ Repository guide

| Path | Purpose |
|---|---|
| [app.py](app.py) | Streamlit configuration, tabs, progress, and file loops |
| [utils.py](utils.py) | Gemini calls, sanitization, renaming, and moving |
| [assets/](assets/) | Existing logo and application screenshots |

If processing fails, check the model ID, file permissions, supported formats, and provider quota. A configuration success message only confirms SDK configuration; an actual generation call verifies model access. No automated test suite is included.

## 🤝 Contributing

Open an issue with a reproducible example or submit a focused pull request. Keep setup instructions and documentation aligned with any behavior changes.

## 📄 License

No repository-level `LICENSE` file is currently included.
