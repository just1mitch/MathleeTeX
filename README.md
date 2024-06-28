# ![MathleeTeX](https://latex.codecogs.com/svg.image?%5Chuge%20%7B%5Ccolor%7BWhite%7D%5Csqrt%7BMathleeTeX%7D%7D%5Cmathbf%7B%7D)
- [Startup Steps](#cits3403---agile-web-development---group-project-2024)
- [What is MathleeTeX?](#what-is-)
- [Website Preview](#website-preview)
- [Technologies Used](#technologies-used)
## CITS3403 - Agile Web Development - Group Project, 2024.

**Developed by:**
- [Jack Blackwood](https://github.com/QuamCode)
- [Mitchell Otley](https://github.com/just1mitch)
- [Nate Trew](https://github.com/Nate202003)
- [James Wigfield](https://github.com/JamesW293)

**Startup Steps:**
1. Clone the repository

   `git clone https://github.com/just1mitch/mathleetex.git`
2. Create a virtual environment
   
   `python -m venv .venv`
3. Start the virtual environment

   Windows: `.venv\Scripts\activate.bat`
   POSIX: `source .venv/bin/activate`
4. Install dependencies from _requirements.txt_

   `pip install -r requirements.txt`
5. Run the flask app

   `flask --app run.py run`

## What is ![MathleeTeX](https://latex.codecogs.com/svg.image?%5Clarge%20%7B%5Ccolor%7BWhite%7D%5Csqrt%7BMathleeTeX%7D%7D%5Cmathbf%7B%7D)?

![MathleeTeX](https://latex.codecogs.com/svg.image?%7B%5Ccolor%7BWhite%7D%5Csqrt%7BMathleeTeX%7D%7D) is a unique community-driven platform designed to empower individuals to enhance their LaTeX skills through a collaborative question-and-answer format. We believe in the power of community engagement, acting as a key tool in accelerating learning and mastering complex LaTeX concepts. On ![MathleeTeX](https://latex.codecogs.com/svg.image?%7B%5Ccolor%7BWhite%7D%5Csqrt%7BMathleeTeX%7D%7D), you can:
- Ask and Answer Questions: Dive into a vast array of type-set challenges ranging from beginner to advanced levels. Whether you're starting out or are looking to polish your expertise, there's something here for everyone.
- Leaderboard: Track your progress and compare your performance with other users. Earn points and climb the ranks to become a MathleeTex champion.
- Comment and Collaborate: Engage with the community by sharing your thoughts, feedback, and insights. Collaborate with other users to solve complex problems and learn from one another.

## Website Preview
| ![login](https://github.com/just1mitch/mathleetex/assets/57031880/e31fe384-4885-456c-b3f0-5be4c047ba6b) | 
|:--:| 
| *Login Screen* |

| ![create](https://github.com/just1mitch/mathleetex/assets/57031880/c7e5ccf6-c470-4330-a178-05b110bf0199) | 
|:--:|
| *Create questions* |

| ![play](https://github.com/just1mitch/mathleetex/assets/57031880/f2560fc1-269e-4195-973d-7132b8cde85d) | 
|:--:|
| *View other players questions* |

| ![image](https://github.com/just1mitch/mathleetex/assets/57031880/949a3cad-011d-4457-b531-f747e4005e44) | 
|:--:|
| *Answer questions, and add your own comments* |

| ![leaderboard](https://github.com/just1mitch/mathleetex/assets/57031880/f501c023-3e16-44cb-bf60-bf8fedf5acdb)| 
|:--:|
| *View your statistics and the leaderboard* |

## Technologies Used
- Flask (Web application backend) - including:
    - Flask-Bcrypt
    - Flask-Login
    - Flask-Migrate
    - Flask-Paginate
    - Flask-SQLAlchemy
    - Flask-WTF
- [Bootstrap 5.3](https://getbootstrap.com/docs/5.3/getting-started/introduction/) (Website layout and styling)
- [KaTeX](https://katex.org/) (LaTeX rendering)
- jQuery and AJAX (powered by JavaScript)
- Jinja (HTML page templates)
- SQLite (Lightweight Database) with SQLAlchemy to interact with Flask
