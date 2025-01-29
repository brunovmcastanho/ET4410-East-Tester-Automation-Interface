

## 📌 **Repository**: **ET4410 East Tester Automation Interface**  
🔹 **description**: A Python-based GUI for automating impedance measurements with the **ET4410 East Tester LCR Meter**. Allows remote operation via a serial connection, enabling parameter configuration, automated measurements, and real-time data visualization.

---


## 📌 Overview
This Python application provides a **graphical user interface (GUI)** for automating impedance measurements using the **ET4410 East Tester LCR Meter**. The software enables remote operation via a serial connection, allowing users to configure parameters, execute measurements, and visualize results in real-time.

## ✨ Features
✅ **Serial Communication** – Connect to the ET4410 via a serial (USB) interface.  
✅ **Measurement Automation** – Automate impedance measurements with predefined frequency sweeps.  
✅ **Configurable Parameters** – Adjust DC bias, AC level, and baud rate.  
✅ **Data Visualization** – Plot impedance (Re{Z}) and phase angle (Theta) on logarithmic scales.  
✅ **User-Friendly Interface** – Simple and intuitive GUI built with Tkinter.  

## 🛠 Requirements
Ensure you have the following dependencies installed before running the program:

```sh
pip install pyserial numpy matplotlib
```
- **Python 3.x**  
- **Tkinter** (built-in with Python)  
- **PySerial** (`pip install pyserial`)  
- **NumPy** (`pip install numpy`)  
- **Matplotlib** (`pip install matplotlib`)  

## 🚀 Installation
1️⃣ Clone this repository:
   ```sh
   git clone https://github.com/brunovmcastanho/ET4410-East-Tester-Automation.git
   cd ET4410-East-Tester-Automation
   ```
2️⃣ Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3️⃣ Run the application:
   ```sh
   python ET4410_East_Tester.py
   ```

## 📝 Usage
1️⃣ **Connect** the **ET4410 East Tester** to your computer via USB.  
2️⃣ **Open** the application and set the **serial port** (e.g., `COM14` or `/dev/ttyUSB0`).  
3️⃣ **Configure** measurement parameters:  
   - **DC Bias** (mV)  
   - **AC Level** (mV)  
   - **Baudrate**
     
4️⃣ **Select** the **Graph Type** (Points or Line).  
5️⃣ **Click "Start"** to begin measurements.  
6️⃣ **View results** in real-time with live graphs.  

## 🛠 Troubleshooting
🔹 **Device not detected?** Ensure the correct serial port is selected.  
🔹 **ET4410 not responding?** Check if it’s powered on and properly connected.  
🔹 **Communication errors?** Try a different baud rate (default: `9600`).  

## 📜 License
This project is licensed under the **MIT License**.  


---
🔗 **Developed by:** *Bruno Castanho*  
📌 **GitHub Repository:** *[brunovmcastanho/ET4410-East-Tester-Automation](https://github.com/brunovmcastanho/ET4410-East-Tester-Automation)*
```

