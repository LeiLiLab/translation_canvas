import duckdb
import os

path_to_file = os.path.dirname(__file__)
if not os.path.exists(os.path.join(path_to_file, "tmp")):
    os.makedirs(os.path.join(path_to_file, "tmp"))

lock_file_path = os.path.join(path_to_file, "tmp", "duckdb.lock")
if not os.path.exists(lock_file_path):
    open(lock_file_path, 'w').close()

shared_mem_path = os.path.join(path_to_file, "tmp", "shared_mem_duckdb")
if not os.path.exists(shared_mem_path):
    open(shared_mem_path, 'w').close()

con = duckdb.connect(database='temporary.db')

results = con.execute("CREATE SEQUENCE runs_id_sequence START 1;")
results = con.execute("CREATE SEQUENCE refs_id_sequence START 1;")
results = con.execute("CREATE SEQUENCE preds_id_sequence START 1;")
results = con.execute("CREATE SEQUENCE preds_text_id_sequence START 1;")

results = con.execute("""
                      CREATE TABLE IF NOT EXISTS runs (
                          id INT PRIMARY KEY DEFAULT nextval('runs_id_sequence'), 
                          filename VARCHAR(255) NOT NULL, 
                          source_lang VARCHAR(2) NOT NULL,   
                          target_lang VARCHAR(2) NOT NULL,
                          in_progress FLOAT,
                          exit_status INT,
                          path_to_err VARCHAR(255),
                          se_score FLOAT,
                          num_predictions INT,
                          run_type VARCHAR(10));""")

results = con.execute("""CREATE TABLE IF NOT EXISTS refs (
                            id INT DEFAULT nextval('refs_id_sequence') PRIMARY KEY, 
                            source_text TEXT NOT NULL, 
                            lang VARCHAR(2));""")

results = con.execute("""
                      CREATE TABLE IF NOT EXISTS preds (
                          id INT DEFAULT nextval('preds_id_sequence') PRIMARY KEY,
                          se_score FLOAT,
                          num_errors INT,
                          ref_id INT,
                          run_id INT,
                          FOREIGN KEY (ref_id) REFERENCES refs(id),
                          FOREIGN KEY (run_id) REFERENCES runs(id));""")

results = con.execute("""
                   CREATE TABLE IF NOT EXISTS preds_text (
                      id INT DEFAULT nextval('preds_text_id_sequence') PRIMARY KEY,
                        source_text TEXT NOT NULL,
                        error_type VARCHAR(255),
                        error_scale VARCHAR (8),
                        error_location TEXT,
                        error_explanation TEXT,
                        pred_id INT,
                        FOREIGN KEY (pred_id) REFERENCES preds(id));""")   

 