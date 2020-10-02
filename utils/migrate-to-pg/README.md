# NbGrader migration from sqlite to postgres

This script should be used in case we need to migrate accounts that are using sqlite with nbgrader

## Instructions

1. SSH into remote host

2. Install system dependencies:

    - Install **pgloader** with: `sudo apt-get install -y pgloader`

3. Clone and change directories into the script's root:

    ```shell
    git clone https://github.com/IllumiDesk/infra
    cd infra/utils/migrate-to-pg
    ```

4. Install pip dependencies:

    ```shell
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

5. Copy and set env file:

   ```shell
   cp env.example .env
   ```

    - Set env vars with organization values
  
6. Run the script

    ```shell
    python pgloader_batch.py
    ```
