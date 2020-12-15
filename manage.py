from app import create_app


if __name__ == "__main__":
    scrap_app = create_app()
    scrap_app.run("127.0.0.1", "5000", debug=False)
