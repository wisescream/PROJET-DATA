import os
import mysql.connector

def create_table(table_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  
        port=3306,        
        database="projet"
    )
    cursor = conn.cursor()

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            creation_date VARCHAR(255),
            first_page VARCHAR(255),
            second_page VARCHAR(255),
            product_id VARCHAR(255),
            product_price VARCHAR(255),
            checkout VARCHAR(255)
        )
    """
    cursor.execute(create_table_query)
    
    conn.commit()
    cursor.close()
    conn.close()

def insert_into_database(table_name, data):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # Ensure the password matches the create_table function
            port=3306,        # Use the correct port
            database="projet" # Ensure the database name is consistent
        )
        cursor = conn.cursor()
        insert_query = f"""
            INSERT INTO `{table_name}` (user_id, creation_date, first_page, second_page, product_id, product_price, checkout)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion des données {data} dans la table {table_name}: {err}")

def process_file(file_path, table_name):
    inserted_count = 0
    print(f"Fichier trouvé : {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line_data = line.strip().split('|')

            line_data = line_data[:7]

            if len(line_data) == 7:
                print(f"Contenu de {file_path} :\n{line}")
                print(f"Données extraites : {line_data}")

                insert_into_database(table_name, line_data)
                inserted_count += 1
                print(f"Ligne insérée dans la table {table_name}.")
            else:
                print(f"Ligne mal formée (nombre incorrect d'éléments) : {line}")
    return inserted_count

def process_folder(folder_path):
    total_lines = 0
    total_inserted_lines = 0
    for root, dirs, _ in os.walk(folder_path):
        for dir_name in sorted(dirs):
            dir_path = os.path.join(root, dir_name)
            print(f"Sous-dossier trouvé : {dir_path}")
            for subroot, subdirs, subfiles in os.walk(dir_path):
                for subdir_name in sorted(subdirs):
                    subdir_path = os.path.join(subroot, subdir_name)
                    table_name = subdir_name.replace("-", "_") 
                    create_table(table_name)
                    print(f"Sous-sous-dossier trouvé : {subdir_path}")
                    dir_lines = 0
                    for subsubroot, _, subsubfiles in os.walk(subdir_path):
                        for filename in sorted(subsubfiles):
                            file_path = os.path.join(subsubroot, filename)
                            inserted_lines = process_file(file_path, table_name)
                            dir_lines += inserted_lines
                            total_inserted_lines += inserted_lines
                            total_lines += 1
                    print(f"Total des lignes insérées dans le sous-sous-dossier {subdir_path} (table {table_name}) : {dir_lines}")

    print(f"Total des lignes dans tous les fichiers : {total_lines}")
    print(f"Total des lignes insérées dans la base de données : {total_inserted_lines}")

folder_path = r'C:\Users\Rayane\Downloads\zbi\zbi\nifi-2.0.0-M2\test'

process_folder(folder_path)
