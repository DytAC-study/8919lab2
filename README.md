# CST8919 Lab 2 – Flask App with Threat Detection

## ✅ Overview

This lab demonstrates how to build a simple Flask-based login application, deploy it to Azure App Service, enable diagnostic logging, detect brute-force login behavior using KQL, and configure an alert that notifies upon suspicious activity.

---

## 🏗️ Application Features

- Python Flask app with `/login` route
- Structured logging of login attempts (IP, username, user-agent, failure count)
- Deployed to Azure App Service with `gunicorn` via VS Code
- Logs collected using Azure Monitor (Log Analytics)
- KQL used to extract and analyze failed login behavior
- Azure Alert Rule created to notify on brute-force detection

---

## 📂 Project Structure

```
.
├── app.py                # Main Flask app
├── requirements.txt      # Python dependencies
├── test-app.http         # REST Client test file to simulate login requests
├── README.md             # This file
```

---

## 🔍 KQL Query for Brute-Force Login Detection

Simplified version：

```
AppServiceConsoleLogs
| where TimeGenerated > ago(15m)
| where ResultDescription has "Login FAILED"
```

Full version：

```kql
AppServiceConsoleLogs
| where TimeGenerated > ago(15m)
| where Level == "Error" or Level == "Informational"
| where ResultDescription has "Login FAILED"
| extend 
    Username = extract("user=([^|]+)", 1, ResultDescription),
    IP = extract("ip=([^|]+)", 1, ResultDescription),
    UserAgent = extract("ua=\"([^\"]+)\"", 1, ResultDescription),
    FailCount = toint(extract("fail_count=(\\d+)", 1, ResultDescription))
| summarize FailedAttempts = count(), MaxFailCount = max(FailCount) 
    by IP, Username, bin(TimeGenerated, 5m)
| where FailedAttempts > 5 or MaxFailCount > 5
| order by FailedAttempts desc
```

### 🧠 Explanation

- Extracts failed login attempts from logs
- Parses `username`, `ip`, `user-agent`, and failure count
- Aggregates by IP and username in 5-minute intervals
- Filters rows where attempts > 5 → triggers alert

---

## 📢 Azure Alert Rule Configuration

| Setting                     | Value                              |
| --------------------------- | ---------------------------------- |
| **Scope**                   | `lab2-law` Log Analytics Workspace |
| **Condition**               | Custom log search (KQL above)      |
| **Evaluation frequency**    | Every 1 minute                     |
| **Aggregation granularity** | 5 minutes                          |
| **Threshold**               | Greater than 0                     |
| **Action Group**            | `lab2-email` (email notification)  |
| **Severity**                | 2 – Warning                        |

---

## 🧪 How to Test

Use `test-app.http` and run the following request multiple times:

```http
POST https://<your-app>.azurewebsites.net/login
Content-Type: application/json

{
  "username": "admin",
  "password": "wrongpass"
}
```

> Run this request at least 6 times to simulate a brute-force attempt.

---

## 🧠 Reflection

- **What I learned:**  
  I learned how to integrate structured application logging with Azure Monitor, and use KQL to perform advanced pattern detection. This lab deepened my understanding of logging pipelines, regex extraction, and alert automation in cloud environments.

- **Challenges faced:**  
  Troubleshooting Azure App startup issues (gunicorn config), and properly extracting structured fields from log strings using `extract()` in KQL.

- **Improvement suggestions:**  
  In a real-world scenario, I would enhance the app with rate-limiting, account lockout, and storage-backed credential verification. I’d also enrich logs with request headers and geolocation information.

---

## 📹 YouTube Demo

https://youtu.be/y_vpTymfCh8