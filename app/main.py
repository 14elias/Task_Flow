from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def main():
    return ("Hello from taskflow!")


if __name__ == "__main__":
    main()
