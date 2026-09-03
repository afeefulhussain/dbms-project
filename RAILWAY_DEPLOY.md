# Railway.app 1-Click Deployment Guide

Follow these quick steps to deploy the **MedCare Clinic System** and its **MySQL Database** on Railway for free:

---

### Step 1: Push Code to GitHub
1. Go to [GitHub.com](https://github.com/) and click **New Repository** (e.g., `clinic-management-system`).
2. Upload all files from `d:\UET study\DBMS\project web` and click **Commit changes**.

---

### Step 2: Create Railway Project
1. Go to [Railway.app](https://railway.app/) and **Sign in with GitHub**.
2. Click **+ New Project** $\rightarrow$ select **Deploy from GitHub repo**.
3. Select your `clinic-management-system` repository.

---

### Step 3: Add 1-Click MySQL Cloud Database
1. In your Railway project screen, click **+ Create** / **+ New**.
2. Choose **Database** $\rightarrow$ click **Add MySQL**.
3. Railway will provision a dedicated MySQL cloud database server.

---

### Step 4: Generate Public Live URL
1. Click on your Python Flask service tile in Railway.
2. Go to **Settings** $\rightarrow$ **Networking**.
3. Click **Generate Domain** (e.g., `https://medcare-production.up.railway.app`).
4. Click the link to open your live web application!

*Note: The app will automatically create the tables and seed initial data in the Railway MySQL database upon first startup.*
