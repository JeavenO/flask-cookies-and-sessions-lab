from flask import Flask, jsonify, session
from models import db, Article

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super-secret-key"

db.init_app(app)

# Only import flask_migrate if running directly
if __name__ == "__main__":
    try:
        from flask_migrate import Migrate
        migrate = Migrate(app, db)
    except ImportError:
        print("flask_migrate not installed, skipping migrations")

    app.run(debug=True)

@app.route("/articles/<int:id>", methods=["GET"])
def get_article(id):
    if "page_views" not in session:
        session["page_views"] = 0
    session["page_views"] += 1

    if session["page_views"] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    article = Article.query.get_or_404(id)
    return jsonify({
        "id": article.id,
        "title": article.title,
        "content": article.content
    })

@app.route("/clear", methods=["GET"])
def clear_session():
    session.clear()
    return jsonify({"message": "Session cleared"})
