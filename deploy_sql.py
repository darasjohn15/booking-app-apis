import subprocess
import glob
import sys

SERVICE_NAME = "booking_app"  # Your pg_service.conf service name
SQL_DIR = "./sql"             # Directory where your .sql files live

def run_sql_file(filepath):
    print(f"Running {filepath} ...")
    result = subprocess.run(
        ["psql", f"service={SERVICE_NAME}", "-f", filepath],
        capture_output=True,
        text=True
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
