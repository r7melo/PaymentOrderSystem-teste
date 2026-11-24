from app.consumer import AuthConsumer


def main():
    consumer = AuthConsumer()
    consumer.start()


if __name__ == "__main__":
    main()