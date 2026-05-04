"""
templates.py
Role-specific paragraph 2 templates for both internship and full-time roles.
{role}     → replaced with the actual role/position
{manager}  → replaced with the reporting manager's first name
{duration} → replaced with the duration (internship only)
"""

# ── Internship templates ──────────────────────────────────────────────────────
INTERNSHIP_TEMPLATES = {
    "AI": (
        "As such, your internship will include training and focus primarily on learning and developing "
        "new skills and gaining a deeper understanding of artificial intelligence and machine learning, "
        "working alongside {manager}, assisting {manager} in building and evaluating AI/ML models, "
        "experimenting with data pipelines, and contributing to research-driven projects that create a "
        "meaningful impact in the team. Based on your performance after {duration}, your employment will "
        "be rediscussed."
    ),
    "HR": (
        "As such, your internship will include training and focus primarily on learning and developing "
        "new skills in human resources operations, working alongside {manager}, assisting {manager} in "
        "recruitment coordination, onboarding processes, maintaining employee records, and supporting "
        "day-to-day HR activities that help build a positive and productive workplace. Based on your "
        "performance after {duration}, your employment will be rediscussed."
    ),
    "Mobile Dev": (
        "As such, your internship will include training and focus primarily on learning and developing "
        "new skills in mobile application development, working alongside {manager}, assisting {manager} "
        "in designing, building, and testing features across iOS and/or Android platforms, contributing "
        "to code reviews, and helping deliver smooth and responsive user experiences. Based on your "
        "performance after {duration}, your employment will be rediscussed."
    ),
    "Frontend": (
        "As such, your internship will include training and focus primarily on learning and developing "
        "new skills in frontend web development, working alongside {manager}, assisting {manager} in "
        "crafting responsive UI components, improving user experience, collaborating on design-to-code "
        "implementations, and ensuring cross-browser compatibility across our web products. Based on your "
        "performance after {duration}, your employment will be rediscussed."
    ),
    "Backend": (
        "As such, your internship will include training and focus primarily on learning and developing "
        "new skills in backend systems and API development, working alongside {manager}, assisting "
        "{manager} in designing robust server-side logic, managing databases, building scalable REST APIs, "
        "and contributing to the reliability and performance of our core platform infrastructure. Based on "
        "your performance after {duration}, your employment will be rediscussed."
    ),
    "Marketing": (
        "As such, your internship will include training and focus primarily on learning and developing "
        "new skills in digital marketing and brand communication, working alongside {manager}, assisting "
        "{manager} in crafting content strategies, managing social media channels, analysing campaign "
        "performance, and supporting initiatives that strengthen Tericsoft's presence and reach in the "
        "market. Based on your performance after {duration}, your employment will be rediscussed."
    ),
    "DevOps": (
        "As such, your internship will include training and focus primarily on learning and developing "
        "new skills in DevOps practices and cloud infrastructure, working alongside {manager}, assisting "
        "{manager} in managing CI/CD pipelines, containerisation, cloud deployments, system monitoring, "
        "and helping maintain a reliable and scalable infrastructure that supports our engineering teams. "
        "Based on your performance after {duration}, your employment will be rediscussed."
    ),
}

# ── Full-time templates ───────────────────────────────────────────────────────
FULLTIME_TEMPLATES = {
    "AI": (
        "In this role, you will be responsible for researching, designing, and deploying AI/ML solutions "
        "that drive real business impact. Working closely with {manager}, you will own end-to-end model "
        "development — from data exploration and feature engineering through to training, evaluation, and "
        "production deployment — while collaborating cross-functionally to integrate intelligent systems "
        "into our products and workflows."
    ),
    "HR": (
        "In this role, you will be responsible for driving core human resources functions across the "
        "organisation. Working closely with {manager}, you will lead recruitment pipelines, manage "
        "employee lifecycle processes, support performance management cycles, and champion initiatives "
        "that foster a strong, inclusive, and high-performing culture at Tericsoft."
    ),
    "Mobile Dev": (
        "In this role, you will be responsible for building and maintaining high-quality mobile "
        "applications for iOS and/or Android platforms. Working closely with {manager}, you will "
        "architect and implement new features, conduct thorough code reviews, optimise app performance, "
        "and collaborate with design and backend teams to deliver polished, reliable user experiences."
    ),
    "Frontend": (
        "In this role, you will be responsible for crafting and maintaining exceptional frontend "
        "experiences across our web products. Working closely with {manager}, you will translate "
        "designs into pixel-perfect, accessible, and performant interfaces, establish frontend "
        "standards and best practices, and collaborate with product and backend teams to ship "
        "features that delight our users."
    ),
    "Backend": (
        "In this role, you will be responsible for designing and maintaining robust, scalable backend "
        "systems that power our products. Working closely with {manager}, you will architect APIs and "
        "microservices, optimise database performance, ensure system reliability and security, and "
        "contribute to architectural decisions that support the long-term growth of our platform."
    ),
    "Marketing": (
        "In this role, you will be responsible for planning and executing marketing strategies that "
        "grow Tericsoft's brand and customer base. Working closely with {manager}, you will develop "
        "multi-channel campaigns, produce compelling content, analyse performance metrics, and "
        "identify new opportunities to strengthen our market presence and drive business growth."
    ),
    "DevOps": (
        "In this role, you will be responsible for building and maintaining the infrastructure and "
        "tooling that enables our engineering teams to ship with speed and confidence. Working closely "
        "with {manager}, you will own CI/CD pipelines, cloud infrastructure provisioning, system "
        "monitoring and alerting, and drive a culture of reliability, automation, and continuous "
        "improvement across the organisation."
    ),
}

TEAM_LIST = list(INTERNSHIP_TEMPLATES.keys())


def get_paragraph_2(team: str, manager: str, employment_type: str, duration: str = "", role: str = "") -> str:
    """Return the filled-in paragraph 2 for the given team and employment type."""
    manager_first = manager.strip().split()[0]
    if employment_type == "Full-Time":
        template = FULLTIME_TEMPLATES.get(team, FULLTIME_TEMPLATES["AI"])
    else:
        template = INTERNSHIP_TEMPLATES.get(team, INTERNSHIP_TEMPLATES["AI"])
    return template.format(role=role, manager=manager_first, duration=duration)