# 🏥 Hospital Data Analytics Dashboard – Power BI

### 📊 **Project Overview**

The **Hospital Data Analytics Dashboard** is an interactive Power BI report designed to analyze patient demographics, membership activity, and regional distribution.  
This dashboard was created during my internship to gain real-world experience in **data analytics, visualization, and storytelling using Power BI**.

---

## 🚀 **Project Objectives**

- Analyze patient data to uncover trends in demographics, regions, and memberships.  
- Visualize insights such as:
  - Total patient count
  - Gender distribution
  - Age group segmentation
  - Membership activity (Active vs Inactive)
  - Regional performance
  - Registration trends over time  
- Build a clean, professional dashboard layout for healthcare insights.

---

## 🧰 **Tools & Technologies Used**

| Tool / Tech | Purpose |
|--------------|----------|
| **Power BI Desktop** | Dashboard creation & data visualization |
| **Microsoft Excel** | Data source (cleaned and preprocessed file) |
| **DAX (Data Analysis Expressions)** | Custom measures & KPIs |
| **Python (optional preprocessing)** | Data cleaning and formatting |
| **GitHub** | Project version control & portfolio showcase |

---

## 🧮 **Key DAX Measures**

```DAX
Total Patients = COUNTROWS(cleaned_data)

Average Age = AVERAGE(cleaned_data[age])

Male % =
DIVIDE(
    CALCULATE(COUNTROWS(cleaned_data), cleaned_data[sex] = "M"),
    [Total Patients]
)

Female % =
DIVIDE(
    CALCULATE(COUNTROWS(cleaned_data), cleaned_data[sex] = "F"),
    [Total Patients]
)

Membership Rate % =
DIVIDE(
    CALCULATE(COUNTROWS(cleaned_data), cleaned_data[membership_status] = "Active"),
    [Total Patients]
)

New Patients =
COUNTROWS(
    FILTER(cleaned_data, NOT(ISBLANK(cleaned_data[registrationdate])))
)
```

---

## 📈 **Dashboard Features**

| Feature | Description |
|----------|--------------|
| **KPI Cards** | Display Average Age, Gender %, Membership %, and Total Patients |
| **Gender Distribution** | Pie chart showing male, female, and unknown ratios |
| **Patients by Place** | Horizontal bar chart showing top-performing regions |
| **Patients by Age Group** | Column chart visualizing age-wise segmentation |
| **Membership Status** | Donut chart for Active vs Inactive members |
| **Patient Trend Analysis** | Line/bar chart tracking registrations over time |
| **Filters / Slicers** | Interactive filters by Age Group, Gender, Membership |

---

## 🧱 **Dashboard Layout**

- **Top Row:** KPI Cards (Avg Age, Male %, Female %, Membership %, Total Patients)  
- **Middle Row:** Major Insights (Gender, Region, Age, Membership)  
- **Right Panel:** Registration trend & filters  
- **Header:** Project title and author details  
- **Footer:** Data source, tool, and credits  

---

## 📊 **Insights Derived**

- Total of **47.7K patients** analyzed  
- **53% female** patient ratio  
- **40% active membership rate**  
- **Prayagraj region** recorded the highest patient count  
- Clear pattern in **age demographics** (majority between 31–45 years)  
- Steady growth in new registrations during the analyzed period  

---

## 🧠 **Learning Outcomes**

- Understanding Power BI data modeling (Star Schema with fact & dimension tables)  
- Writing effective **DAX measures** for KPIs  
- Designing visually consistent dashboards with dark themes  
- Performing **data cleaning and transformation** in Excel/Python before visualization  
- Presenting analytical findings in a business-oriented layout  

---

## 📁 **Project Structure**

```
📂 Hospital-Data-Analytics-Dashboard/
 ┣ 📜 README.md
 ┣ 📊 Hospital_Data_Analytics_Dashboard.pbix
 ┣ 📗 Hospital_Data_Revised.xlsx
 ┗ 📸 Dashboard_Screenshot.png

---

## 💼 **Author**

👤 **Piyush Singh**  
📌 *Data Analyst Intern | Aspiring Business Intelligence Developer*  
📧 Email: ps1521155@gmail.com  
🔗 [LinkedIn Profile](www.linkedin.com/in/piyush-singh-90b5bb2b0)  
🔗 [Portfolio / GitHub](https://github.com/Piyush9928)  


---

## 🏁 **Conclusion**
The **Hospital Data Analytics Dashboard** effectively summarizes healthcare insights using Power BI.  
It showcases the potential of business intelligence tools in turning raw hospital data into actionable insights for better patient management and decision-making.  

---

### ⭐ Don’t forget to star the repo if you found it useful!
