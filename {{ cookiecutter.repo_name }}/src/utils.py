from dotenv import find_dotenv, load_dotenv

def dotenv_loader() -> None:
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
