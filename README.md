
# 🌱 **Mycelium: Data Contract Editor**

Mycelium is a powerful platform designed to simplify the creation and management of Data Contracts, facilitating seamless data ingestion by acting as a bridge between different systems. It is built to serve business teams, IT services, and data services such as data factories, making it a central platform for managing data contracts efficiently.

## 🧠 **Key Features**

- **AI-Powered Data Contracts**: Mycelium leverages a Large Language Model (LLM) to auto-generate data contracts when provided with database details such as the host, secret, and user.
- **Accelerated Data Ingestion**: Simplify and automate the process of generating ingestion configurations based on provided Data Contracts.
- **Visualization**: Easily track which data sources have Data Contracts.
- **Collaboration**: Align data engineers, business teams, and IT services around centralized data contract management.
  
## 📦 **Installation**

### **1. Clone the Repository**

```bash
git clone https://github.com/ThomasGraff/mycelium.git
cd mycelium
```

### **2. Run the Application**

```bash
docker-compose up -d
```

### **3. Access the Application**

Open your browser and go to:

```
http://localhost:8080
```

This will start the Mycelium application on your local machine.

---

## 🚀 **Usage**

Once the application is running, you can:

1. **Search or Create Data Contracts**:  
   - Type keywords in the search bar to browse existing Data Contracts.
   - Type `new` to initiate the creation of a new Data Contract.

2. **Auto-generate Data Contracts**:  
   - Upload your list of company databases including information like `host`, `secret`, and `user`.  
   - The system will use a Large Language Model (LLM) to auto-generate relevant Data Contracts.

3. **Ingestion Configuration Generation**:  
   - Provide an example configuration for ingestion tools.  
   - Mycelium will automatically generate the appropriate ingestion configuration for any Data Contract.

4. **Visualization**:  
   - Easily visualize which data sources already have Data Contracts in place.

---

## 🔄 **License**

This project is licensed under the [AGPL 3.0 License](https://www.gnu.org/licenses/agpl-3.0.en.html).

---

## 🤝 **Contributing**

Feel free to contribute by submitting a pull request or opening an issue. Contributions are always welcome!

- Fork the repo
- Create your feature branch (`git checkout -b feature/YourFeature`)
- Commit your changes (`git commit -m 'Add feature'`)
- Push to the branch (`git push origin feature/YourFeature`)
- Open a pull request
