# Woman Safety App

Welcome to the **Woman Safety App** – a solution designed to enhance the safety of women using cutting-edge **machine learning** and **web technology**. This app offers real-time safety features like danger detection, location sharing, and emergency contact addt alerts, ensuring rapid response in critical situations.

Our aim is to provide a reliable tool that empowers women by leveraging the latest advancements in technology.

## 🌟 Features
- **Real-time Danger Detection**: Uses a trained ML model to detect unsafe environments or situations.
- **Emergency Alerts**: Quickly send SOS alerts to pre-configured emergency contacts with real-time location.
- **Location Sharing**: Share live location with trusted contacts for enhanced safety.
- **ML Model Integration**: Analyze risk levels in various environments based on real-time data.
- **User-Friendly Interface**: Designed for ease of use with minimal interaction during emergencies.

## 🔧 Tech Stack
- **Frontend**: HTML, CSS, JavaScript, React.js
- **Backend**: Node.js, Express.js
- **ML Model**: TensorFlow / PyTorch
- **Database**: MongoDB (for user data and logs)
- **Deployment**: AWS / Heroku
- **Version Control**: Git & GitHub

## 🚀 Getting Started
### Prerequisites
- Node.js installed (v14.x or higher)
- MongoDB running locally or cloud (MongoDB Atlas)
- TensorFlow / PyTorch for ML model

### Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/woman-safety-app.git
    cd woman-safety-app
    ```

2. **Install dependencies**:
    ```bash
    npm install
    ```

3. **Run the server**:
    ```bash
    npm start
    ```

4. **Run the frontend**:
    ```bash
    cd client
    npm install
    npm start
    ```

### Environment Variables
Create a `.env` file in the root directory and add the following:
```
MONGODB_URI=<your-mongodb-connection-string>
PORT=5000
ML_MODEL_PATH=<path-to-ml-model>
```

## 🧠 Machine Learning Model
We have integrated an ML model that uses environmental data (such as sound levels, location, etc.) to assess risk. The model can be trained further using real-world data to improve its accuracy.

The pre-trained model is stored in the `models/` directory, and during runtime, it analyzes inputs and flags dangerous situations in real-time.

## 📱 Screenshots

| Home Page  | Emergency Mode |
| ---------- | -------------- |
| ![Home Page](screenshots/home.png) | ![Emergency Mode](screenshots/emergency.png) |

## 📂 Project Structure
```
.
├── client                 # Frontend React app
│   ├── public
│   └── src
├── models                 # ML models
├── routes                 # Backend API routes
├── utils                  # Helper functions and utilities
├── server.js              # Main server file
├── README.md
└── package.json
```

## 💡 Contributing
We welcome contributions from the community! Here's how you can help:
1. **Fork the repository**.
2. **Create a feature branch** (`git checkout -b feature-name`).
3. **Commit your changes** (`git commit -m 'Add some feature'`).
4. **Push to the branch** (`git push origin feature-name`).
5. **Create a new Pull Request**.

## 📄 License
This project is licensed under the **MIT License**.

## 🙏 Acknowledgements
- TensorFlow and PyTorch for providing robust ML frameworks.
- Open-source libraries and the developer community for continuous support.

---

This README provides a clean, professional overview of your project with an emphasis on:
- Project description and purpose.
- Features and functionalities.
- Tech stack and installation steps.
- Contribution guidelines.

**Next Steps:**
- Add links to screenshots.
- Update the ML model and database paths. 
