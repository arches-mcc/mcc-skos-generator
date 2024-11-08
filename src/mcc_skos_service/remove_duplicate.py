from uuid import UUID

def remove_duplicate_uuids(uuid_list, filename="unique_uuids.txt"):
    seen = set()
    unique_uuids = []
    
    for uuid_str in uuid_list:
        try:
            uuid_obj = UUID(uuid_str)  # Valida o UUID
            if uuid_obj not in seen:
                seen.add(uuid_obj)
                unique_uuids.append(uuid_str)
        except ValueError:
            print(f"'{uuid_str}' não é um UUID válido e será ignorado.")
    
    # Salvar em arquivo .txt com IDs separados por vírgula
    with open(filename, "w") as file:
        file.write(",".join(unique_uuids))
    
    return "finished"
