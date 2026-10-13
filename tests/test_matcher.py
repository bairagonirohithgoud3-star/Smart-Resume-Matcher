from services.matcher import extract_skills, analyze_resume

def test_extract_skills():
    skills = extract_skills("Built a Python app using Flask, SQL, and machine learning.")
    assert "python" in skills
    assert "flask" in skills
    assert "sql" in skills
    assert "machine learning" in skills

def test_matcher_returns_scores():
    result = analyze_resume("Python Flask SQL Git REST API OOP", "Any")
    assert result["results"]
    assert all(0 <= row["score"] <= 100 for row in result["results"])
    assert result["predicted_domain"]
