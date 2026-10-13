# Smart Resume Matcher & Internship Predictor

A student project built with Flask, HTML/CSS/JavaScript and Python resume parsing. Upload a PDF, DOCX or TXT resume to detect skills, compare them with sample internship profiles, view skill-overlap scores and get an exploratory domain suggestion.

## Features
- Responsive landing page and results dashboard
- PDF, DOCX and TXT resume text extraction
- Skill detection across programming, web, data/AI, cloud, design and core CS
- Role matching with a transparent skill-overlap percentage
- Missing-skill hints and domain recommendation
- Upload size/type validation; uploaded file processed in memory, not stored
- Health endpoint at `/health`
- Render deployment configuration

## Run locally
Python 3.10+ recommended.

```bash
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows PowerShell:
# .\\venv\\Scripts\\Activate.ps1

python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Deploy on Render
1. Push this folder to a GitHub repository.
2. Sign in to https://render.com and choose **New → Blueprint**.
3. Connect your repository; Render reads `render.yaml`.
4. Deploy, wait for the build to finish, and open the generated URL.

## Publish to GitHub
Create an empty repository on https://github.com/new, then from this folder run:

```bash
git init
git add .
git commit -m "Build Smart Resume Matcher MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Smart-Resume-Matcher.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not commit `.env`, credentials, private resumes, or personal student data.

## How scoring works
Each sample internship profile has a small set of required skills. The match score is the percentage of those listed skills detected in the resume text. The suggested domain is a lightweight heuristic based on skill overlap, not a trained predictive model and not a probability of getting hired.

## Important limitations
- Sample roles are illustrative only, not live vacancies or real employer listings.
- Resume parsing may not work well for scanned/image-only PDFs.
- Skill matching looks for known terms and can miss synonyms or skills not explicitly written.
- The domain recommendation is a baseline heuristic. It should not be presented as a validated ML prediction.
- This MVP does not persist resumes or require student accounts. MongoDB/authentication can be added later if needed.
