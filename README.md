# MundaAI 🌾

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kuda2026/-mundaai-/blob/main/model/02_mundaai_interactive_demo.ipynb)

**MundaAI** is an AI-driven agricultural risk prediction platform built for smallholder farmers in Zimbabwe. By integrating predictive machine learning with high-accessibility communication channels (WhatsApp, USSD, Web), MundaAI delivers real-time crop risk assessments to help farmers mitigate the impacts of climate change and shifting market signals.

Developed under the **POTRAZ AI4I Challenge 2026 (Development Track)**.

---

## 🛠️ Interactive Demo
To view and test our live prediction pipeline, click the **"Open in Colab"** badge above or use the direct link below. 

The notebook features a **no-code interactive form** where reviewers can adjust parameters (rainfall, soil moisture, agro-ecological region) to watch the Random Forest classifier predict crop risk in real-time.

🔗 **Direct Colab Link:** [MundaAI Interactive Demo](https://colab.research.google.com/github/kuda2026/-mundaai-/blob/main/model/02_mundaai_interactive_demo.ipynb)

---

## 📂 Repository Architecture
The project has been refactored into modular directories to support robust pipeline deployment:

*   **`api/`**: Contains the FastAPI backend code (`main.py`) serving prediction endpoints.
*   **`data/`**: Holds our agricultural, climate, and market data, including the baseline 360-record dataset.
*   **`docs/`**: Includes architectural diagrams, dataset overviews, and our formal proposal.
*   **`model/`**: Houses the model training history and the interactive demo:
    *   `01_mundaai_training.ipynb`: Original training pipeline (Random Forest + CTGAN).
    *   `02_mundaai_interactive_demo.ipynb`: Live demo notebook with interactive prediction sliders.
*   **`frontend/` / `whatsapp/` / `ussd/`**: Contain the respective codebase directories for user interfaces.

---

## 🚀 How to Run the API Locally
1. Clone this repository:
   ```bash
   git clone [https://github.com/kuda2026/-mundaai-.git](https://github.com/kuda2026/-mundaai-.git)