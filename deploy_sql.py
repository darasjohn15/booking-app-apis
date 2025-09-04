import subprocess
import glob
import sys
import os
from dotenv import load_dotenv

load_dotenv()

SQL_DIR = "./sql"  # Path to your SQL files

def run_sql_file(filepath):
    print(f"Running {filepath} ...")
    
    # Read connection info from environment variables
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT", "5432")
    
    # Check that none of the variables are missing
    if not all([host, dbname, user, password, port]):
        print("Error: One or more DB environment variables are missing.")
        sys.exit(1)
    
    # Set environment variable for password
    env = os.environ.copy()
    env["PGPASSWORD"] = password

    # Run the SQL file with SSL required
    result = subprocess.run(
        [
            "psql",
            f"-h{host}",
            f"-p{port}",
            f"-d{dbname}",
            f"-U{user}",
            "-v", "ON_ERROR_STOP=1",  # Stop on first error
            "--set", "sslmode=require",
            "-f", filepath
        ],
        capture_output=True,
        text=True,
        env=env
    )

    if result.returncode != 0:
        print(f"Error running {filepath}:\n{result.stderr}")
        sys.exit(1)
    else:
        print(f"Success:\n{result.stdout}")

def main():
    sql_files = sorted(glob.glob(f"{SQL_DIR}/*.sql"))
    if not sql_files:
        print(f"No .sql files found in {SQL_DIR}")
        sys.exit(0)

    print(f"Starting deployment of {len(sql_files)} files...")
    for sql_file in sql_files:
        run_sql_file(sql_file)

    print("Deployment complete!")

if __name__ == "__main__":
    main()
