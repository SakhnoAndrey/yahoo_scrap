from app import scrap_app
from scrap_app.extensions import db
from scrap_app.models import Company


@scrap_app.shell_context_processor
def make_shell_context():
    return {"db": db, "Company": Company}


if __name__ == "__main__":
    scrap_app.run("127.0.0.1", "5000", debug=False)
