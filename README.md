
# 🎮 BuckShot Roulette - AI Gameplay Automation

Welcome to **Test #3** of our experimental gameplay automation series for **BuckShot Roulette**, a psychological horror game. This project showcases the use of AI and automation to interact with and control gameplay in real-time based on live YouTube chat commands.

![ChatGPT Image Jul 2, 2025, 09_02_41 PM (1)](https://github.com/user-attachments/assets/2e1f52ba-c69c-4599-8d70-15374cb0ca6c)


---

## 🔍 What is this?

This project demonstrates how artificial intelligence, computer vision, and automation tools can control gameplay dynamically based on live audience input. Viewers send commands via YouTube Live Chat, which are read and executed by an AI bot in real time.

---

## 🧠 Tech Stack

| Tool        | Purpose                                   |
|-------------|-------------------------------------------|
| `YOLOv8`    | Object detection for in-game elements     |
| `OpenCV`    | Image preprocessing and region tracking   |
| `PyAutoGUI` | Keyboard and mouse automation             |
| `pytchat`   | YouTube Live Chat parsing and handling    |
| `Win32 API` | Window detection and screen grabbing      |
| `Python`    | Main controller logic                     |

---

## ⚙️ Features

- ✅ **YOLO-Powered Object Detection**  
  Detects interactive elements in the BuckShot Roulette UI (weapons, buttons, faces).

- ✅ **Real-Time Chat Command Execution**  
  Commands like `take aim`, `pull trigger`, `spin chamber` are parsed and acted upon.

- ✅ **Floating Chat Overlays**  
  Twitch-style overlays are displayed in-game using command data.

- ✅ **Bot-Controlled Decision-Making**  
  AI autonomously decides actions based on command votes and game state.

---

## 🖥️ Setup Instructions

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/buckshot-ai-automation.git
   cd buckshot-ai-automation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure YouTube Chat**
   - Set up `pytchat` to pull from your YouTube livestream using the video ID.

4. **Run the bot**
   ```bash
   python main.py
   ```

---

## 🧪 Test Scenario #3

This test specifically includes:

- 🔄 Multiple round automation
- 📡 Chat command synchronization
- 🎯 Weapon interaction automation (pulling the trigger, aiming, spinning chamber)
- 🧩 Advanced object confidence filtering

---

## 🖼️ Screenshots

| Gameplay Automation | Chat Command Parsing |
|---------------------|----------------------|
| ![game](./screenshots/gameplay.png) | ![chat](./screenshots/chat.png) |

---

## 📜 License

MIT License – feel free to fork, adapt, and contribute!

---

## 🤝 Contributions

Pull requests are welcome! If you have cool ideas like better chat parsing, Twitch integration, or support for other horror games, feel free to contribute.

---

## 📺 Watch it Live

> 🔴 **YouTube:** [Test #3 – BuckShot Roulette Live AI Bot]([https://youtube.com/your-video-link](https://www.youtube.com/watch?v=GfU5hpaR2vI)

---

## 👨‍💻 Author

**Tarun** – Full Stack Developer & AI Automation Enthusiast  
📧 [tarun.email@example.com](mailto:tarunchelumalla@gmail.com)
