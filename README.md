# CN331-AS2 (Quota App)

This repository contains the Quota app, which has two use cases, one for admins and one for students.

## Member
1. กษิดิศ กรสังข์ 6510685016
2. ชยุตม์พงศ์ พลเยี่ยม 6510525022

## Link คลิปตัวอย่างการใช้งาน
[คลิปตัวอย่างการใช้งาน คลิก]( https://tuipied-my.sharepoint.com/:v:/g/personal/chayutpong_pon_dome_tu_ac_th/EUT9HUn32FxEplT4fA4bGZABiuhWJ9g0o4lB6eisXpkV4Q?e=XguzEE )

## Features

### Admin Side
Admins have the ability to manage subjects and handle quota requests submitted by students. Specifically, admins can:
- **Add Subject and Subject Details**:
  - This includes adding the subject code, subject name, academic year, semester, capacity, Quota request's status (open or closed).
- **Manage Student Quota Requests**:
  - Approve or deny quota requests submitted by students.

### Student Side
Students can submit and manage their quota requests, as well as view the status of the subjects they’ve requested.
- **Submit a Quota Request**: Request to enroll in a subject with a limited quota.
- **Search Subject, View Subject Details**:
  - See the status of their request (waiting, approved, denied).
- **Cancel a Quota Request**: Withdraw a request.

## How to Start the Quota App

To get the Quota app running locally, follow these steps:

1. **Clone the Repository**:
     ```bash
     git clone https://github.com/6510525022/cn331-as2.git
     ```

2. **Set Up the Virtual Environment**:
     ```bash
     python -m venv venv
     ```

3. **Activate the Virtual Environment**:
     - Windows:
       ```bash
       .\venv\Scripts\activate
       ```

4. **Install the requirements packages**:
     ```bash
     pip install -r requiments.txt
     ```

5. **Run Server**:
     ```bash
     cd myProject
     python manage.py runserver
     ```

6. **Access Web Application**:
   - `http://localhost:8000`

