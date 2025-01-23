from flask import Flask, render_template, request, redirect, url_for, session
import smtplib

app = Flask(__name__)
app.secret_key = "super_secret_key"  # For session handling

@app.route("/")
def landing_page():
    return render_template("landing.html")

@app.route("/start", methods=["POST"])
def start_survey():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()

    # Validate form inputs
    if not first_name or not last_name or not email:
        error_message = "All fields are required. Please fill out the form completely."
        return render_template("landing.html", error_message=error_message)

    # Save validated data in the session
    session['first_name'] = first_name
    session['last_name'] = last_name
    session['email'] = email
    session['answers'] = {}

    return redirect(url_for("section1"))

@app.route("/section1", methods=["GET", "POST"])
def section1():
    if request.method == "POST":
        section1_answers = request.form.to_dict()
        required_fields = ["q1", "q2", "q3", "q4", "q5"]

        # Validate all required fields
        for field in required_fields:
            if field not in section1_answers or section1_answers[field].strip() == "":
                error_message = "Please answer all questions before proceeding."
                return render_template(
                    "audit_section1.html",
                    error_message=error_message,
                    progress=33,
                    saved_answers=session.get("answers", {})
                )

        # Save answers for Section 1 in the session
        session['answers'].update(section1_answers)
        print("Session after Section 1:", session)  # Debugging
        return redirect(url_for("section2"))

    return render_template(
        "audit_section1.html",
        progress=33,
        saved_answers=session.get("answers", {})
    )

@app.route("/section2", methods=["GET", "POST"])
def section2():
    if request.method == "POST":
        action = request.form.get("action")

        # Navigate to previous section
        if action == "previous":
            return redirect(url_for("section1"))

        # Validate answers for Section 2
        section2_answers = request.form.to_dict()
        required_fields = ["q6", "q7", "q8"]

        for field in required_fields:
            if field not in section2_answers or section2_answers[field].strip() == "":
                error_message = "Please answer all questions before proceeding."
                return render_template(
                    "audit_section2.html",
                    error_message=error_message,
                    progress=66,
                    saved_answers=session.get("answers", {})
                )

        # Save answers for Section 2 in the session
        session['answers'].update(section2_answers)
        print("Session after Section 2:", session)  # Debugging
        return redirect(url_for("section3"))

    return render_template(
        "audit_section2.html",
        progress=66,
        saved_answers=session.get("answers", {})
    )

@app.route("/section3", methods=["GET", "POST"])
def section3():
    if request.method == "POST":
        action = request.form.get("action")

        # Navigate to previous section
        if action == "previous":
            return redirect(url_for("section2"))

        # Validate answers for Section 3
        section3_answers = request.form.to_dict()
        required_fields = ["q9", "q10", "q11", "q12", "q13"]

        for field in required_fields:
            if field not in section3_answers or section3_answers[field].strip() == "":
                error_message = "Please answer all questions before proceeding."
                return render_template(
                    "audit_section3.html",
                    error_message=error_message,
                    progress=100,
                    saved_answers=session.get("answers", {})
                )

        # Save answers for Section 3 in the session
        session['answers'].update(section3_answers)
        print("Session after Section 3:", session)  # Debugging
        return redirect(url_for("results_page"))

    return render_template(
        "audit_section3.html",
        progress=100,
        saved_answers=session.get("answers", {})
    )

@app.route("/results", methods=["GET", "POST"])
def results_page():
    answers = session.get('answers', {})
    score = sum(int(value) for value in answers.values() if value.isdigit())
    session['score'] = score

    if request.method == "POST":
        recipient_email = request.form.get("email", session['email'])
        send_email(
            recipient_email,
            session['first_name'],
            score,
            answers
        )
        return render_template("results.html", score=score, email_sent=True)

    return render_template("results.html", score=score, email_sent=False)

def send_email(to_email, first_name, score, answers):
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password
    subject = "Your Audit Results"
    body = (
        f"Hi {first_name},\n\n"
        f"Thank you for completing the Client Engagement Audit.\n\n"
        f"Your Total Score: {score}/65\n\n"
        f"Here are your detailed answers:\n"
        + "\n".join(f"{key}: {value}" for key, value in answers.items())
        + "\n\n"
        f"Based on your results, here are some next steps:\n"
        f"- Identify areas for improvement.\n"
        f"- Create an action plan.\n"
        f"- Contact Loan Flow Analytics for tailored solutions.\n\n"
        f"Best Regards,\n"
        f"Loan Flow Analytics Team"
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, to_email, message)
    except Exception as e:
        print("Failed to send email:", e)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)  # Ensure this is placed at the root
