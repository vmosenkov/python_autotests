import requests
from config import URL, API, TRAINER_TOKEN, TRAINER_ID  # Импортируем данные из config.py

URL_pokemonbattle = URL
API_version = API
my_trainer_token = TRAINER_TOKEN
my_trainer_id = TRAINER_ID

path_pokemons = '/pokemons'

header = {
    'Content-Type' : 'application/json',
    'trainer_token' : my_trainer_token
}

# --- Создание нового покемона---
body_create_pokemons = {
    "name": "generate",
    "photo_id": -1
}

response_create_pokemon = requests.post(
    url = f'{URL_pokemonbattle}{API_version}{path_pokemons}',
    headers = header, 
    json = body_create_pokemons
)

# Проверка статуса ответа и получение id покемона
if response_create_pokemon.status_code == 201:
    pokemon_create_data = response_create_pokemon.json()
    pokemon_id = pokemon_create_data['id']
    
    # Запрос на получение данных о покемоне
    response_my_pokemon_list = requests.get(
        url=f'{URL_pokemonbattle}{API_version}{path_pokemons}?trainer_id={my_trainer_id}&pokemon_id={pokemon_id}&status=1',
        headers=header
    )
    
    if response_my_pokemon_list.status_code == 200:
        my_pokemon_data = response_my_pokemon_list.json()
        if my_pokemon_data.get("status") == "success" and my_pokemon_data.get("data"):
            pokemon_info = my_pokemon_data["data"][0]  # Берём первый элемент из списка
            pokemon_name = pokemon_info.get("name")
            pokemon_photo_id = pokemon_info.get("photo_id")
            
            print(f"Создан покемон с ID {pokemon_id}. Его имя - {pokemon_name}, и у него есть фото под номером {pokemon_photo_id}")
        else:
            print("Ошибка: данные о покемоне не найдены или имеют некорректный формат.")
            exit()
    else:
        print(f"Ошибка при получении данных о покемоне: {response_my_pokemon_list.status_code}")
        exit()

# Обработка ошибки 422        
elif response_create_pokemon.status_code == 422:
    error_data = response_create_pokemon.json()
    error_message = error_data.get("message")
    print(f"Ошибка 422: {error_message}")
    exit()

else:
    print(f"Ошибка при создании покемона: {response_create_pokemon.status_code}")
    exit()

# --- Смена имени и фото покемона ---
new_pokemon_name = "generate"
new_pokemon_photo_id = -1  # Укажите новый photo_id
body_change_name = {
    "pokemon_id": pokemon_id,
    "name": new_pokemon_name,
    "photo_id": new_pokemon_photo_id
}

response_change_name = requests.put(
    url=f'{URL_pokemonbattle}{API_version}{path_pokemons}',
    headers=header,
    json=body_change_name
)

# Проверка статуса ответа
if response_change_name.status_code == 200:
    updated_data = response_change_name.json()
    updated_pokemon_id = updated_data.get("id")

    # Запрос на получение обновлённых данных о покемоне
    response_updated_pokemon = requests.get(
        url=f'{URL_pokemonbattle}{API_version}{path_pokemons}?trainer_id={my_trainer_id}&pokemon_id={updated_pokemon_id}&status=1',
        headers=header
    )

    if response_updated_pokemon.status_code == 200:
        updated_pokemon_data = response_updated_pokemon.json()
        if updated_pokemon_data.get("status") == "success" and updated_pokemon_data.get("data"):
            updated_pokemon_info = updated_pokemon_data["data"][0]  # Берём первый элемент из списка
            updated_name = updated_pokemon_info.get("name")
            updated_photo_id = updated_pokemon_info.get("photo_id")
            
            print(f"Информация о покемоне с ID {updated_pokemon_id} успешно обновлена! Его новое имя изменилось с {pokemon_name} на {updated_name}, и его новое фото cменилось с № {pokemon_photo_id} на № {updated_photo_id}")
        else:
            print("Ошибка: обновлённые данные о покемоне не найдены или имеют некорректный формат.")
            exit()
    else:
        print(f"Ошибка при получении обновлённых данных о покемоне: {response_updated_pokemon.status_code}")
        exit()

else:
    print(f"Ошибка при обновлении покемона с ID: {pokemon_id}: {response_change_name.status_code}")
    exit()



# --- Поймать покемона в покебол ---
path_add_pokeball = "/trainers/add_pokeball"

body_add_pokeball = {
    "pokemon_id": pokemon_id 
}

response_add_pokeball = requests.post(
    url=f'{URL_pokemonbattle}{API_version}{path_add_pokeball}',
    headers=header,
    json=body_add_pokeball
)

if response_add_pokeball.status_code == 200:
    add_pokeball_data = response_add_pokeball.json()
    print(f"Успех! {add_pokeball_data.get('message')} с ID {add_pokeball_data.get('id')}")
elif response_add_pokeball.status_code == 400:
    error_data = response_add_pokeball.json()
    print(f"Ошибка 400: {error_data.get('message')}")
else:
    print(f"Ошибка при поимке покемона в покебол: {response_add_pokeball.status_code}")
