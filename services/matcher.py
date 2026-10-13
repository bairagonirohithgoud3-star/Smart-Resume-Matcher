import re
from collections import Counter

SKILL_GROUPS = {
    "Programming": ["python", "java", "c++", "c", "javascript", "typescript"],
    "Web Development": ["html", "css", "javascript", "react", "node.js", "flask", "django", "rest api"],
    "Data & AI": ["machine learning", "deep learning", "artificial intelligence", "data analysis", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "nlp", "sql", "excel", "power bi"],
    "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "linux", "git", "github", "ci/cd"],
    "Design & Product": ["figma", "ui/ux", "wireframing", "user research", "product management"],
    "Core CS": ["data structures", "algorithms", "oop", "dbms", "operating systems", "computer networks"],
}

INTERNSHIPS = [
    {"title":"Python Developer Intern","company":"Sample Opportunity","domain":"Software Development","skills":["python","git","sql","rest api","oop"],"description":"Build and test Python applications, APIs and database features."},
    {"title":"Machine Learning Intern","company":"Sample Opportunity","domain":"AI & Machine Learning","skills":["python","machine learning","pandas","numpy","scikit-learn","data analysis"],"description":"Prepare datasets, train baseline models and evaluate model performance."},
    {"title":"Frontend Developer Intern","company":"Sample Opportunity","domain":"Web Development","skills":["html","css","javascript","react","git"],"description":"Build responsive web pages and interactive user interfaces."},
    {"title":"Full Stack Developer Intern","company":"Sample Opportunity","domain":"Full Stack Development","skills":["html","css","javascript","python","flask","sql","git","rest api"],"description":"Create end-to-end web features across the frontend and backend."},
    {"title":"Data Analyst Intern","company":"Sample Opportunity","domain":"Data Analytics","skills":["sql","excel","python","pandas","data analysis","power bi"],"description":"Clean data, build reports and communicate data-driven insights."},
    {"title":"Cloud / DevOps Intern","company":"Sample Opportunity","domain":"Cloud & DevOps","skills":["linux","git","docker","aws","ci/cd"],"description":"Assist with deployment workflows, cloud resources and automation."},
    {"title":"UI/UX Design Intern","company":"Sample Opportunity","domain":"UI/UX Design","skills":["figma","ui/ux","wireframing","user research"],"description":"Research user needs and design accessible product experiences."},
]

def extract_skills(text):
    lowered = text.lower()
    found = []
    for group, skills in SKILL_GROUPS.items():
        for skill in skills:
            # Flexible whitespace and punctuation-safe whole phrase matching.
            pattern = r"(?<![a-z0-9+#])" + re.escape(skill).replace(r"\ ", r"\s+") + r"(?![a-z0-9+#])"
            if re.search(pattern, lowered):
                found.append(skill)
    return sorted(set(found))

def analyze_resume(text, target_role="Any"):
    found = extract_skills(text)
    role_options = {"Any", "Software Development", "AI & Machine Learning", "Web Development", "Full Stack Development", "Data Analytics", "Cloud & DevOps", "UI/UX Design"}
    if target_role not in role_options:
        target_role = "Any"
    rows = []
    for item in INTERNSHIPS:
        if target_role != "Any" and item["domain"] != target_role:
            # Keep related software/full-stack roles discoverable.
            if not (target_role == "Full Stack Development" and item["domain"] in {"Web Development", "Software Development"}):
                continue
        required = item["skills"]
        matched = [s for s in required if s in found]
        missing = [s for s in required if s not in found]
        score = round(100 * len(matched) / max(1, len(required)))
        rows.append({**item, "score": score, "matched": matched, "missing": missing})
    rows.sort(key=lambda x: (-x["score"], x["title"]))
    domain_counts = Counter()
    for item in INTERNSHIPS:
        hits = len(set(item["skills"]) & set(found))
        domain_counts[item["domain"]] += hits
    predicted = domain_counts.most_common(1)[0][0] if found and domain_counts and domain_counts.most_common(1)[0][1] else "Software Development"
    # If a role was requested, prioritize it as the recommendation context.
    if target_role != "Any" and any(r["domain"] == target_role for r in rows):
        predicted = target_role
    categories = {}
    for group, skills in SKILL_GROUPS.items():
        categories[group] = [s for s in found if s in skills]
    return {
        "skills": found,
        "categories": {k:v for k,v in categories.items() if v},
        "results": rows,
        "predicted_domain": predicted,
        "total_skills": len(found),
        "target_role": target_role,
        "summary": "Your strongest domain estimate is based on the skills detected in your resume and overlap with sample internship requirements. It is a guidance signal, not a hiring guarantee."
    }
