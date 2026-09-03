from db import init_db

if __name__ == "__main__":
    print("Connecting to MySQL and initializing clinic_db database...")
    try:
        init_db()
        print("Setup completed successfully!")
    except Exception as e:
        print(f"Error during database setup: {e}")
