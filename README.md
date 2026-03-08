# Jan Sahayak AI: Bridging the Information Gap for Rural India

**Jan Sahayak AI** is an intelligent, multilingual portal designed to help Indian citizens—especially those in rural areas—navigate and understand complex government schemes in their native language.

## 🚀 Live Demo
**[Live MVP Portal](https://soha17-jan-sahayak-v2.hf.space/)** *(Hosted on Hugging Face Spaces)*

---

## 📖 Problem Statement
Millions of citizens in India are eligible for transformative government schemes like **PM-KISAN**, but they often face a "Paper Wall"—complex eligibility criteria and language barriers that make it difficult to access benefits. **Jan Sahayak AI** removes this friction by providing instant, accurate, and empathetic guidance in Hindi.

## 🛠️ Technical Architecture
The system is built using a modern AI stack optimized for performance and regional language accuracy:

* **Frontend**: Built with **Gradio** for a clean, responsive, and mobile-friendly user interface.
* **LLM Engine**: Powered by **Google Gemini 3.1 Flash-Lite** (via Google AI Studio) for high-speed, cost-effective natural language processing.
* **Hosting**: Deployed on **Hugging Face Spaces** using Docker containers for high availability.
* **Security**: API keys are managed through **Hugging Face Secrets** to ensure no credentials are leaked in the source code.



## ✨ Key Features
* **Native Language Support**: Specifically tuned to provide high-quality responses in Hindi.
* **Context-Aware**: Understands the nuances of Indian government schemes like PM-KISAN.
* **Real-time Interaction**: Near-instant response times thanks to the Gemini 3.1 architecture.
* **Accessibility**: Designed with a simple interface suitable for users with varying levels of digital literacy.

---

## 📁 Repository Structure
* `app.py`: The main application logic and API integration.
* `requirements.txt`: List of Python dependencies (Gradio & Requests).
* `docs/`: Detailed design and requirement documentation.
* `README.md`: Project overview and setup instructions.

---

## 🔧 Installation & Setup
To run this project locally:

1.  **Clone the repo**:
    ```bash
    git clone [https://github.com/Soha1711/AI-for-Bharat.git](https://github.com/Soha1711/AI-for-Bharat.git)
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set your API Key**:
    Export your Gemini API key as an environment variable:
    ```bash
    export GEMINI_API_KEY='your_api_key_here'
    ```
4.  **Launch the app**:
    ```bash
    python app.py
    ```

## 🛡️ License
Distributed under the **MIT License**. See `LICENSE` for more information.
